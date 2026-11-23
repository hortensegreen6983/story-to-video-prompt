#!/usr/bin/env python3
"""Build a video-prompt pack from a storyboard JSON file.

Turns a structured shot list into copy-paste-ready prompts for one or more
AI video models, plus a shot table, consistency bible, negative list and
generation plan.

Usage
-----
    python build_prompt_pack.py storyboard.json --model veo3 --out pack.md
    python build_prompt_pack.py storyboard.json --model veo3,kling,generic
    python build_prompt_pack.py storyboard.json --model veo3 --lang both
    python build_prompt_pack.py storyboard.json --check

Schema (only "shots" is required)
---------------------------------
{
  "title": str,
  "logline": str,
  "poster_frame": str,
  "aspect_ratio": "2.39:1",
  "fps": 24,
  "style": {"look": str, "palette": str, "grade": str, "texture": str},
  "audio": {"music": "none", "ambience": "ventilation hum"},
  "characters": [{"id": "CHAR_A", "name": "学徒", "anchor": "a 34-year-old woman, ..."}],
  "locations":  [{"id": "LOC_KITCHEN", "name": "厨房", "anchor": "a narrow 1990s kitchen, ..."}],
  "negatives": ["on-screen text", "watermark"],
  "shots": [{
      "id": "S01",
      "duration": 6,
      "beat": "他把最后一卷胶片举到红光下",   # Chinese gloss / intent
      "size": "MEDIUM CLOSE-UP",
      "subject": "{{CHAR_A}}",
      "action": ["holds a brass canister up to the light", "blinks once"],
      "setting": "{{LOC_DARKROOM}}",
      "lighting": "hard red key from screen-left, everything else in shadow",
      "camera": "performs a very slow 8% push-in over the full 6 seconds",
      "lens": "50mm at T2, shallow depth",
      "atmosphere": "dust suspended in the light",     # optional
      "physics": "the canister's weight pulling his wrist down",  # optional
      "sound": ["ventilation fan hum", "a single drip"],
      "dialogue": "师父，这卷……还没拍完。",   # or "dialogue_en"
      "dialogue_lang": "Mandarin",
      "speaker": "CHAR_A",
      "adverb": "barely audible",
      "style_override": null,        # optional per-shot look
      "timeline": ["0.0–1.5s | lifts the canister", "1.5–4.0s | turns it to the light"],
      "micro": ["dust on the brass lid", "a hairline scratch across the thread"],
      "wardrobe": "union overalls with a bleached patch on the knee",   # optional
      "continuity": "same hand as S01; same darkroom geography",        # optional
      "negative_extra": ["no blood"],
      "transition": "cut"
  }]
}

{{TOKEN}} placeholders are replaced with the matching characters/locations
anchor, so the same wording appears verbatim in every prompt.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MODEL_LIMITS = {
    "veo3": 200,
    "sora2": 220,
    "kling": 150,
    "seedance": 150,
    "hailuo": 120,
    "runway": 120,
    "generic": 220,
    "minimax": 900,
}

# local deployments take long structured prompts; the soft ceiling above only
# stops a runaway 900-word shot, it is not a platform limit.
MODEL_ALIASES = {
    "h3": "minimax",
    "minimax-h3": "minimax",
    "minimaxh3": "minimax",
    "hailuo-local": "minimax",
    "local": "minimax",
}

# the "beyond cinema" layer: physical capture description instead of taste
# adjectives, shared by every shot so the look does not breathe.
DEFAULT_OPTICS = (
    "shot on a full-frame sensor through anamorphic glass, 1/48s shutter, "
    "real motion blur on moving hands, lens breathing on the push, "
    "elliptical bokeh, mild chromatic fringing at the frame edges, "
    "halation blooming off speculars, highlight rolloff instead of clipped white, "
    "no sharpening halos, no CGI sheen"
)
DEFAULT_TEXTURE = (
    "skin keeps pores, fine vellus hair and subsurface warmth, "
    "fabric shows weave and pilling, metal keeps fingerprints and micro-scratches, "
    "glass keeps smudges and dust, every surface carries a readable wear history"
)

# Chinese twin set: the deliverable language is Chinese by default, so the
# fallback text has to be usable as-is rather than translated on the fly.
DEFAULT_OPTICS_ZH = (
    "全画幅传感器配变形宽银幕镜头，1/48 秒快门，手部运动带真实动态模糊，"
    "推镜时有轻微呼吸效应，椭圆散景，画面边缘有轻度色散，"
    "高光处有光晕溢出，高光滚降而不是死白，没有锐化光边，没有 CG 反光"
)
DEFAULT_TEXTURE_ZH = (
    "皮肤保留毛孔、细小绒毛与皮下暖色，织物看得出织纹和起球，"
    "金属留着手印和细划痕，玻璃带着污渍和灰，每一处表面都带着能读出来的磨损史"
)

DEFAULT_NEGATIVES_ZH = [
    "画面文字",
    "字幕",
    "水印",
    "角标",
    "多余手指",
    "畸形的手",
    "五官漂移",
    "重复肢体",
]

DEFAULT_NEGATIVES = [
    "on-screen text",
    "subtitles",
    "watermark",
    "logo",
    "extra fingers",
    "deformed hands",
    "morphing faces",
    "duplicate limbs",
]

ABSTRACT_WORDS = [
    "cinematic",
    "epic",
    "beautiful",
    "stunning",
    "masterpiece",
    "best quality",
    "8k",
    "4k",
    "ultra-detailed",
    "hyperrealistic",
    "award-winning",
    "highly detailed",
    "trending on artstation",
    "dramatic lighting",
]

MOVE_VERBS = {
    "push", "pushes", "pull", "pulls", "truck", "trucks", "pan", "pans",
    "tilt", "tilts", "orbit", "orbits", "crane", "cranes", "dolly", "dollies",
    "track", "tracks", "follow", "follows", "descend", "descends", "ascend",
    "ascends", "rise", "rises", "settle", "settles", "hold", "holds", "drift",
    "drifts", "perform", "performs", "zoom", "zooms", "slide", "slides",
    "float", "floats", "circle", "circles", "arc", "arcs", "whip", "whips",
}

STILL_WORDS = ("static", "locked-off", "locked off", "tripod", "no camera movement")

TOKEN_RE = re.compile(r"\{\{\s*([A-Za-z0-9_\-]+)\s*\}\}")


# ---------------------------------------------------------------- utilities

def norm_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        value = [value]
    out = []
    for item in value:
        if item is None:
            continue
        text = str(item).strip()
        if text:
            out.append(text)
    return out


CJK_RE = re.compile(r"[\u3400-\u9fff]")

#: prompt-side vocabulary, keyed so every builder speaks the same language as
#: the storyboard it was handed.
LABELS = {
    "audio": ("声音", "Audio"),
    "avoid": ("避免", "Avoid"),
    "negative": ("负面提示词", "Negative prompt"),
    "no_negatives": ("负面词", "NEGATIVE"),
}

ZH_BLOCKS = {
    "identity": "身份锁 — 以下整段逐字复制，不要改写",
    "wardrobe": "服装与随身物",
    "performance": "表演 — 实拍时间轴，一拍一行",
    "environment": "环境",
    "physics": "物理 — 重量、接触、次级动态",
    "light": "光线 — 一个物理光源逻辑",
    "camera": "机位与焦段",
    "texture": "材质 — 必须看得见的微观细节",
    "quality": "画质与风格",
    "optics": "成像规格",
    "audio": "声音",
    "continuity": "连续性",
    "no_negatives": "负面词 — 这些都不要出现",
}


def has_cjk(text: str) -> bool:
    return bool(CJK_RE.search(str(text or "")))


def glue(parts, lang: str = "en") -> str:
    """Join fragments with the separator the language actually uses."""
    items = [str(p).strip() for p in parts if p and str(p).strip()]
    if lang == "zh" or has_cjk("".join(items)):
        return "，".join(items)
    return ", ".join(items)


def label(key: str, lang: str) -> str:
    zh, en = LABELS[key]
    return zh if lang == "zh" else en


def tag(key: str, ctx: "Ctx") -> str:
    """'声音：' / 'Audio: ' — the label and its punctuation follow the language."""
    name = label(key, ctx.lang)
    return name + ("：" if has_cjk(name) else ": ")


def sent(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    if text[-1] in ".?!…。！？；;":
        return text
    return text + ("。" if has_cjk(text) else ".")


def cap(text: str) -> str:
    text = (text or "").strip()
    return text[0].upper() + text[1:] if text else text


def word_count(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def is_verb_move(camera: str) -> bool:
    first = re.split(r"[\s,;]", (camera or "").strip(), maxsplit=1)[0].lower()
    return first in MOVE_VERBS


def camera_command(camera: str) -> str:
    """Bracket / stack friendly camera phrase: no 'performs', no duration tail."""
    cam = (camera or "").strip().rstrip(".")
    cam = re.sub(r"^(performs|does|executes|uses)\s+", "", cam, flags=re.I)
    cam = re.sub(
        r"\s+over the (full|entire)\s+\d+(?:\.\d+)?\s*(?:s|sec|secs|second|seconds)\b",
        "",
        cam,
        flags=re.I,
    )
    if re.search(r"\b(static|locked)\b", cam, re.I):
        cam = re.sub(r",?\s*no camera movement\b", "", cam, flags=re.I)
    return cam.strip().strip(",").strip()


def camera_clause(camera: str, lens: str) -> str:
    """Verb-led move: 'The camera pushes in, 50mm.'
    Static or noun-led: 'Camera: locked-off on a tripod. Lens: 50mm.'
    Chinese: '镜头：定机位三脚架。焦段：50mm。'"""
    camera = (camera or "").strip().rstrip(".")
    lens = (lens or "").strip().rstrip(".")
    if has_cjk(camera) or has_cjk(lens):
        bits = []
        if camera:
            bits.append(f"镜头：{camera}")
        if lens:
            bits.append(f"焦段：{lens}")
        return "。".join(bits) + "。"
    if not camera:
        return f"Lens: {lens}." if lens else ""
    if is_verb_move(camera):
        tail = f", {lens}" if lens else ""
        return f"The camera {camera}{tail}."
    out = f"Camera: {camera}."
    if lens:
        out += f" Lens: {lens}."
    return out


def join_subject_action(subject: str, action: str) -> str:
    """A one-word subject welds to its verb; a long comma-laden anchor needs a
    comma before the action or the sentence turns into word salad.
    Chinese needs no space and uses a full-width comma."""
    subject = (subject or "").strip().rstrip(",，")
    action = (action or "").strip()
    if not subject:
        return action
    if not action:
        return subject
    if has_cjk(subject):
        sep = "，" if ("," in subject or "，" in subject or len(subject) > 40) else ""
        return f"{subject}{sep}{action}"
    sep = ", " if ("," in subject or word_count(subject) > 8) else " "
    return f"{subject}{sep}{action}"


def action_phrase(shot: dict, ctx: "Ctx") -> str:
    actions = norm_list(shot.get("action"))
    if not actions:
        return ""
    actions = [
        re.sub(r"^then\s+", "", ctx.resolve(a).strip().rstrip("."), flags=re.I)
        for a in actions
    ]
    actions = [a for a in actions if a]
    if not actions:
        return ""
    if len(actions) == 1:
        return actions[0]
    return join_beats(actions)


# ---------------------------------------------------------------- context

class Ctx:
    def __init__(self, data: dict, lang: str = "zh"):
        self.data = data
        self.lang = "en" if str(lang).lower().startswith("en") else "zh"
        self.style = data.get("style") or {}
        self.audio = data.get("audio") or {}
        self.aspect = str(data.get("aspect_ratio") or "")
        self.entities: dict[str, str] = {}
        for group in ("characters", "locations"):
            for item in data.get(group) or []:
                if not isinstance(item, dict):
                    continue
                key = str(item.get("id") or "").strip()
                if not key:
                    continue
                self.entities[key] = str(item.get("anchor") or "").strip()
        self.names = {
            str(item.get("id")): str(item.get("name") or item.get("id") or "")
            for group in ("characters", "locations")
            for item in (data.get(group) or [])
            if isinstance(item, dict) and item.get("id")
        }
        self.unresolved: set[str] = set()

    def resolve(self, text: str) -> str:
        if not text:
            return ""

        def sub(match: re.Match) -> str:
            key = match.group(1)
            anchor = self.entities.get(key)
            if anchor is None:
                self.unresolved.add(key)
                return match.group(0)
            if not anchor:
                self.unresolved.add(key)
                return ""
            return anchor

        return TOKEN_RE.sub(sub, str(text))

    def style_text(self, shot: dict) -> str:
        override = shot.get("style_override")
        if override:
            return str(override).strip().rstrip(".")
        joined = glue(
            [
                self.style.get("look"),
                self.style.get("palette"),
                self.style.get("grade"),
                self.style.get("texture"),
                self.aspect,
            ],
            self.lang,
        )
        return joined

    def compact_style(self, shot: dict) -> str:
        """Short-budget models get the look and the ratio only."""
        override = shot.get("style_override")
        if override:
            return str(override).strip().rstrip(".")
        return glue([self.style.get("look"), self.aspect], self.lang)

    def speaker_name(self, shot: dict) -> str:
        raw = str(shot.get("speaker") or "").strip()
        if not raw:
            return "he"
        return self.names.get(raw, raw.replace("_", " "))


# ---------------------------------------------------------------- prompt builders

def dialogue_block(shot: dict, ctx: Ctx) -> str:
    line = str(shot.get("dialogue_en") or shot.get("dialogue") or "").strip()
    if not line:
        return ""
    lang = str(shot.get("dialogue_lang") or "").strip()
    if ctx.lang == "zh":
        # a Chinese question mark carries the performance; only drop periods
        line = line.strip().rstrip("。．.")
        adverb = str(shot.get("adverb") or "轻声").strip()
        speaker = ctx.speaker_name(shot)
        lang_part = f"用{lang}" if lang and not has_cjk(lang) else (lang or "")
        verb = f"{lang_part}说" if lang_part else "说"
        return f"{speaker}{verb}，{adverb}：「{line}」"
    adverb = str(shot.get("adverb") or "quietly").strip()
    speaker = ctx.speaker_name(shot)
    lang_part = f" in {lang}" if lang else ""
    quoted = line if line[:1] in "\"“'" else f"\"{line}\""
    return f"{speaker} says{lang_part}, {adverb}: {quoted}"


def join_beats(beats: list[str]) -> str:
    """Multiple action beats in one sentence: English needs ', then', Chinese
    needs the same connective in its own script or the sentence reads bilingual."""
    head = beats[0]
    sep = "，然后" if has_cjk(head) else ", then "
    for extra in beats[1:]:
        head += f"{sep}{extra}"
    return head


def sound_block(shot: dict, ctx: Ctx) -> str:
    layers = norm_list(shot.get("sound"))
    music = str(ctx.audio.get("music") or "").strip()
    if music and music.lower() not in ("none", "no music", "无", "无音乐", "-"):
        layers.append(music)
    return ("；" if ctx.lang == "zh" else "; ").join(layers)


def negative_block(shot: dict, ctx: Ctx) -> str:
    fallback = DEFAULT_NEGATIVES_ZH if ctx.lang == "zh" else DEFAULT_NEGATIVES
    items = norm_list(ctx.data.get("negatives")) or fallback
    items += norm_list(shot.get("negative_extra"))
    seen, uniq = set(), []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            uniq.append(item)
    if ctx.lang == "zh":
        return "，".join(uniq)
    return ", ".join(f"no {i}" if not i.lower().startswith("no ") else i for i in uniq)


def core_parts(shot: dict, ctx: Ctx) -> dict:
    subject = ctx.resolve(str(shot.get("subject") or "")).strip()
    action = action_phrase(shot, ctx)
    setting = ctx.resolve(str(shot.get("setting") or "")).strip().rstrip(".")
    atmosphere = ctx.resolve(str(shot.get("atmosphere") or "")).strip().rstrip(".")
    physics = str(shot.get("physics") or "").strip().rstrip(".")
    setting_full = glue([setting, atmosphere], ctx.lang)
    return {
        "size": str(shot.get("size") or "").strip(),
        "subject": subject,
        "action": action,
        "setting": setting_full,
        "setting_base": setting,
        "physics": physics,
        "lighting": str(shot.get("lighting") or "").strip().rstrip("."),
        "camera": str(shot.get("camera") or "").strip(),
        "lens": str(shot.get("lens") or "").strip(),
        "style": ctx.style_text(shot).rstrip("."),
        "style_short": ctx.compact_style(shot).rstrip("."),
        "sound": sound_block(shot, ctx),
        "dialogue": dialogue_block(shot, ctx),
        "negative": negative_block(shot, ctx),
    }


def build_generic(shot: dict, ctx: Ctx) -> str:
    p = core_parts(shot, ctx)
    parts = [sent(cap(p["size"]) if p["size"] else "")]
    body = join_subject_action(p["subject"], p["action"])
    if body:
        parts.append(sent(cap(body)))
    if p["physics"]:
        parts.append(sent(cap(p["physics"])))
    if p["setting"]:
        parts.append(sent(cap(p["setting"])))
    if p["lighting"]:
        parts.append(sent(cap(p["lighting"])))
    if p["camera"] or p["lens"]:
        parts.append(camera_clause(p["camera"], p["lens"]))
    if p["style"]:
        parts.append(sent(cap(p["style"])))
    if p["sound"]:
        parts.append(sent(tag("audio", ctx) + p["sound"]))
    if p["dialogue"]:
        parts.append(sent(p["dialogue"]))
    if p["negative"]:
        parts.append(sent(tag("avoid", ctx) + p["negative"]))
    return " ".join(x for x in parts if x)


def build_veo(shot: dict, ctx: Ctx) -> str:
    p = core_parts(shot, ctx)
    parts = []
    head = join_subject_action(p["subject"], p["action"])
    if p["size"]:
        head = f"{p['size']}, {head}"
    parts.append(sent(cap(head)))
    if p["physics"]:
        parts.append(sent(cap(p["physics"])))
    if p["setting"]:
        parts.append(sent(cap(p["setting"])))
    if p["lighting"]:
        parts.append(sent(cap(p["lighting"])))
    if p["camera"] or p["lens"]:
        parts.append(camera_clause(p["camera"], p["lens"]))
    if p["style"]:
        parts.append(sent(cap(p["style"])))
    if p["sound"]:
        parts.append(sent(tag("audio", ctx) + p["sound"]))
    if p["dialogue"]:
        parts.append(sent(p["dialogue"]))
    parts.append(sent(cap(p["negative"])))
    return " ".join(x for x in parts if x)


def build_sora(shot: dict, ctx: Ctx) -> str:
    p = core_parts(shot, ctx)
    dur = shot.get("duration") or 8
    parts = [sent(f"A {dur}-second {p['size'] or 'shot'} shot")]
    body = join_subject_action(p["subject"], p["action"])
    if body:
        parts.append(sent(cap(body)))
    if p["physics"]:
        parts.append(sent(cap(p["physics"])))
    if p["setting"]:
        parts.append(sent(cap(p["setting"])))
    if p["lighting"]:
        parts.append(sent(cap(p["lighting"])))
    if p["camera"] or p["lens"]:
        parts.append(camera_clause(p["camera"], p["lens"]))
    if p["style"]:
        parts.append(sent(cap(p["style"])))
    if p["sound"]:
        parts.append(sent(tag("audio", ctx) + p["sound"]))
    if p["dialogue"]:
        parts.append(sent(p["dialogue"]))
    if p["negative"]:
        parts.append(sent(tag("avoid", ctx) + p["negative"]))
    return " ".join(x for x in parts if x)


def build_kling(shot: dict, ctx: Ctx) -> str:
    """Kling reads comma stacks well but its box punishes bloat: keep the
    setting, drop the lens and the long grade chain."""
    p = core_parts(shot, ctx)
    cam = p["camera"].strip()
    if cam:
        if has_cjk(cam):
            cam = f"镜头：{camera_command(cam)}"
        else:
            cam = f"the camera {cam}" if is_verb_move(cam) else f"camera: {camera_command(cam)}"
    stack = [
        p["size"],
        join_subject_action(p["subject"], p["action"]),
        p["setting"],
        p["lighting"],
        cam,
        p["style_short"],
    ]
    stack = [re.sub(r"[,;]+$", "", s).strip() for s in stack if s]
    line = ("，" if has_cjk("".join(stack)) else ", ").join(stack)
    neg_tag = tag("negative", ctx)
    return f"{line}\n{neg_tag}{p['negative']}" if p["negative"] else line


def build_seedance(shot: dict, ctx: Ctx) -> str:
    p = core_parts(shot, ctx)
    cam = p["camera"].strip()
    if cam:
        cam = f"the camera {cam}" if is_verb_move(cam) else camera_command(cam)
    body = ", ".join(
        x
        for x in (
            p["size"],
            join_subject_action(p["subject"], p["action"]),
            p["setting"],
            p["lighting"],
            cam,
        )
        if x
    )
    head = f"镜头1：{body}" if body else "镜头1："
    tail = f"整体风格：{p['style_short']}" if p["style_short"] else ""
    return "\n".join(x for x in (head, tail) if x)


def build_hailuo(shot: dict, ctx: Ctx) -> str:
    p = core_parts(shot, ctx)
    body = join_subject_action(p["subject"], p["action"])
    cam = f"[{camera_command(p['camera'])}] " if p["camera"] else ""
    rest = ", ".join(x for x in (p["setting"], p["lighting"], p["style_short"]) if x)
    return f"{cam}{body}, {rest}".rstrip(", ")


def build_runway(shot: dict, ctx: Ctx) -> str:
    p = core_parts(shot, ctx)
    body = join_subject_action(p["subject"], p["action"])
    parts = [sent(cap(body))]
    if p["setting"]:
        parts.append(sent(cap(p["setting"])))
    if p["camera"]:
        parts.append(camera_clause(p["camera"], ""))
    if p["lighting"]:
        parts.append(sent(cap(p["lighting"])))
    return " ".join(x for x in parts if x)


def normalize_timeline(shot: dict, ctx: Ctx) -> list[str]:
    """Time-coded beats. Accepts explicit timeline entries or derives them from
    the action list, so a shot never ships without an internal clock."""
    dur = float(shot.get("duration") or 0) or 8.0
    raw = shot.get("timeline")
    beats: list[list[str]] = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                t = str(item.get("t") or item.get("time") or "").strip()
                act = str(item.get("act") or item.get("action") or "").strip()
            else:
                s = str(item).strip()
                t, act = "", s
                m = re.match(
                    r"^([0-9.]+\s*[-–~]\s*[0-9.]+\s*s?|[0-9.]+s)\s*[|:：]\s*(.+)$", s
                )
                if m:
                    t, act = m.group(1), m.group(2)
            if act:
                beats.append([t, ctx.resolve(act).rstrip(".")])
    if not beats:
        acts = [ctx.resolve(a).rstrip(".") for a in norm_list(shot.get("action"))]
        zh = ctx.lang == "zh"
        if not acts:
            gloss = ctx.resolve(str(shot.get("beat") or "")).strip()
            acts = [gloss or ("定住画面，只剩微动" if zh else "holds the frame, only micro-motion")]
        beats = [["", a] for a in acts]
        if len(beats) < 3:
            beats.append(
                ["", "收势；只剩呼吸、脉搏与布料的微动" if zh
                 else "settles; breath, pulse and cloth micro-motion only"]
            )
    n = len(beats)
    out: list[str] = []
    for i, (t, act) in enumerate(beats):
        if not t:
            t = f"{dur * i / n:.1f}–{dur * (i + 1) / n:.1f}s"
        out.append(f"{t} — {act}")
    return out


def build_minimax(shot: dict, ctx: Ctx) -> str:
    """Structured, sectioned, time-coded prompt for a local MiniMax H3 box.

    Local inference has no prompt-length tax, so this trades the paragraph for
    labelled blocks: identity lock, per-beat performance, physical light,
    optics, micro texture, continuity. Blocks survive long generations and make
    a bad shot diagnosable line by line instead of all-or-nothing."""
    p = core_parts(shot, ctx)
    dur = float(shot.get("duration") or 0)
    fps = ctx.data.get("fps") or 24
    zh = ctx.lang == "zh"

    def H(key: str, en: str) -> str:
        return ZH_BLOCKS[key] if zh else en

    head = " | ".join(
        x
        for x in (
            str(shot.get("id") or ""),
            f"{dur:g}s" if dur else "",
            p["size"],
            ctx.aspect,
            f"{fps} fps",
        )
        if x
    )

    lines: list[str] = [head, ""]

    lines += [H("identity", "IDENTITY LOCK — copy verbatim"), p["subject"], ""]

    wardrobe = ctx.resolve(str(shot.get("wardrobe") or "")).strip().rstrip(".")
    if wardrobe:
        lines += [H("wardrobe", "WARDROBE / PROPS"), wardrobe, ""]

    lines += [H("performance", "PERFORMANCE — real time, beat by beat")]
    lines += normalize_timeline(shot, ctx)
    lines.append("")

    if p["setting"]:
        lines += [H("environment", "ENVIRONMENT"), sent(cap(p["setting"])), ""]

    if p["physics"]:
        lines += [H("physics", "PHYSICS — weight, contact, secondary motion"), sent(cap(p["physics"])), ""]

    if p["lighting"]:
        lines += [H("light", "LIGHT — one physical source logic"), sent(cap(p["lighting"])), ""]

    cam_bits = [x for x in (camera_command(p["camera"]) if p["camera"] else "", p["lens"]) if x]
    cam_bits.append("1/48s 快门" if zh else "1/48s shutter")
    lines += [
        H("camera", "CAMERA / OPTICS"),
        ("；".join(cam_bits) + "。") if zh else ("; ".join(cam_bits).rstrip(".") + "."),
        "",
    ]

    micro = [ctx.resolve(str(m)).strip().rstrip(".") for m in norm_list(shot.get("micro"))]
    lines += [H("texture", "TEXTURE — micro detail that must be visible")]
    lines += [f"- {m}" for m in (micro or [DEFAULT_TEXTURE_ZH if zh else DEFAULT_TEXTURE])]
    lines += ["", H("quality", "IMAGE QUALITY"), sent(cap(ctx.style_text(shot).rstrip("."))), ""]
    lines += [
        H("optics", "OPTICS"),
        sent(
            cap(
                str(ctx.style.get("optics") or (DEFAULT_OPTICS_ZH if zh else DEFAULT_OPTICS)).strip().rstrip(".")
            )
        ),
        "",
    ]

    audio = [p["sound"], p["dialogue"]]
    audio = [a for a in audio if a]
    if audio:
        joined = ("；".join(a.rstrip("。.") for a in audio) + "。") if zh else ("; ".join(audio).rstrip(".") + ".")
        if zh and joined.endswith("」。") and "「" in joined:
            joined = joined[:-1]
        lines += [H("audio", "AUDIO"), joined, ""]

    continuity = ctx.resolve(str(shot.get("continuity") or "")).strip().rstrip(".")
    if not continuity:
        continuity = (
            "与参考帧同一张脸、同一套服装、同一空间结构；不重新打光，不挪动陈设"
            if zh
            else "same face, same wardrobe, same room geometry as the reference frame; no relighting, no set dressing drift"
        )
    lines += [H("continuity", "CONTINUITY"), sent(cap(continuity)), ""]

    if p["negative"]:
        lines += [H("no_negatives", "NEGATIVE"), p["negative"]]

    text = "\n".join(lines).strip()
    return re.sub(r"\n{3,}", "\n\n", text)


BUILDERS = {
    "generic": build_generic,
    "veo3": build_veo,
    "sora2": build_sora,
    "kling": build_kling,
    "seedance": build_seedance,
    "hailuo": build_hailuo,
    "runway": build_runway,
    "minimax": build_minimax,
}


def build_prompt(shot: dict, ctx: Ctx, model: str) -> str:
    return BUILDERS[model](shot, ctx)


def build_single_prompt(ctx: Ctx, shots: list[dict], model: str = "veo3") -> str:
    """One-paragraph version for models that only take a single prompt.
    Labelled shots beat 'opens on / then / ends on' prose because the model
    can see the seams between beats."""
    if not shots:
        return ""
    total = sum(float(s.get("duration") or 0) for s in shots)
    zh = ctx.lang == "zh"
    if zh:
        parts = [sent(f"一条 {int(total)} 秒短片，共 {len(shots)} 个镜头")]
    else:
        parts = [
            sent(
                f"A {int(total)}-second short film in {len(shots)} "
                f"{'shot' if len(shots) == 1 else 'shots'}"
            )
        ]
    anchor_seen: set[str] = set()
    for i, shot in enumerate(shots, 1):
        p = core_parts(shot, ctx)
        # A single prompt cannot repeat a ten-line anchor four times; spell it
        # out once, then keep the character by name.
        subject_text = p["subject"]
        for key, anchor in ctx.entities.items():
            if not anchor or not subject_text.startswith(anchor):
                continue
            if anchor in anchor_seen:
                subject_text = subject_text.replace(anchor, ctx.names.get(key, key), 1)
            else:
                anchor_seen.add(anchor)
            break
        if zh:
            head = f"镜头 {i} — {p['size']}：" if p["size"] else f"镜头 {i}："
        else:
            head = f"Shot {i} — {p['size']}:" if p["size"] else f"Shot {i}:"
        seg = [head, sent(cap(join_subject_action(subject_text, p["action"])))]
        if p["lighting"]:
            seg.append(sent(cap(p["lighting"])))
        if p["camera"] or p["lens"]:
            seg.append(camera_clause(p["camera"], p["lens"]))
        parts.append(("" if zh else " ").join(x for x in seg if x))
    style = ctx.style_text({})
    if style:
        parts.append(sent(("全片统一风格：" if zh else "Throughout: ") + style))
    amb = str(ctx.audio.get("ambience") or "").strip()
    music = str(ctx.audio.get("music") or "").strip()
    if music.lower() in ("none", "no music", "无", "无音乐", "-"):
        music = ""
    audio = ("；" if zh else "; ").join(x for x in (amb, music) if x)
    if audio:
        parts.append(sent(tag("audio", ctx) + audio))
    negatives = norm_list(ctx.data.get("negatives")) or (
        DEFAULT_NEGATIVES_ZH if zh else DEFAULT_NEGATIVES
    )
    parts.append(sent(tag("avoid", ctx) + ("，".join(negatives) if zh else ", ".join(negatives))))
    return " ".join(x for x in parts if x)


# ---------------------------------------------------------------- checks

def shot_placeholders(shot: dict) -> str:
    """Every string field of a shot, so a token used only inside an action
    still counts as used."""
    flat = []
    for key, value in shot.items():
        if isinstance(value, str):
            flat.append(value)
        elif isinstance(value, list):
            flat.extend(str(v) for v in value if isinstance(v, str))
    return "\n".join(flat)


def run_checks(data: dict, ctx: Ctx, models: list[str]) -> list[tuple[str, str, str]]:
    issues: list[tuple[str, str, str]] = []  # (level, where, message)
    shots = data.get("shots") or []
    if not shots:
        issues.append(("ERROR", "-", "no shots defined"))
        return issues
    if not ctx.aspect:
        issues.append(("WARN", "-", "aspect_ratio missing; prompts omit the frame shape"))
    if not ctx.style.get("look"):
        issues.append(("WARN", "-", "style.look missing; every shot will drift in look"))
    if not norm_list(data.get("negatives")):
        issues.append(("WARN", "-", "no global negatives; text/watermark artifacts likely"))

    seen_ids = set()
    referenced = set()
    total = 0.0
    for shot in shots:
        sid = str(shot.get("id") or "?")
        if sid in seen_ids:
            issues.append(("ERROR", sid, "duplicate shot id"))
        seen_ids.add(sid)

        dur = float(shot.get("duration") or 0)
        total += dur
        if dur <= 0:
            issues.append(("ERROR", sid, "duration missing"))
        elif "minimax" in models:
            if dur < 5 or dur > 10:
                issues.append(
                    ("WARN", sid, f"{dur:g}s outside the 5–10s band a local H3 box holds cleanly")
                )
        elif dur > 8:
            issues.append(("WARN", sid, f"{dur:g}s exceeds 8s; the model drifts after ~8s"))
        elif dur < 3:
            issues.append(("WARN", sid, f"{dur:g}s is short; viewers cannot read the frame"))

        if "minimax" in models:
            if not norm_list(shot.get("timeline")):
                issues.append(
                    ("WARN", sid, "no timeline; a 5–10s shot drifts without time-coded beats")
                )
            micro = norm_list(shot.get("micro"))
            if len(micro) < 4:
                issues.append(
                    ("WARN", sid, f"{len(micro)} micro details; this is what reads as detail — aim for 5–8")
                )
            if not str(shot.get("continuity") or "").strip():
                issues.append(("INFO", sid, "continuity blank; the default line will be used"))

        if not str(shot.get("subject") or "").strip():
            issues.append(("ERROR", sid, "subject missing"))
        if not str(shot.get("size") or "").strip():
            issues.append(("WARN", sid, "size missing; model picks a random framing"))
        if not str(shot.get("lighting") or "").strip():
            issues.append(("ERROR", sid, "lighting missing; the shot will be flat"))
        if not str(shot.get("camera") or "").strip():
            issues.append(("WARN", sid, "camera missing; motion will be arbitrary"))

        actions = norm_list(shot.get("action"))
        if not actions:
            issues.append(("ERROR", sid, "action missing"))
        elif len(actions) > 2 and not norm_list(shot.get("timeline")):
            issues.append(("WARN", sid, f"{len(actions)} action beats; keep 1–2"))
        for beat in actions:
            if TOKEN_RE.search(str(beat)):
                issues.append(
                    ("WARN", sid, "placeholder inside action; move the fixed anchor into subject")
                )
        for field, value in shot.items():
            if isinstance(value, str) and re.search(r"\{\{[^}]+\}\}['’]s\b", value):
                issues.append(
                    (
                        "WARN",
                        sid,
                        f"possessive after a placeholder in {field}: "
                        "the anchor is a noun phrase, so write 'the hand of {{CHAR_A}}'",
                    )
                )

        cam = str(shot.get("camera") or "").lower()
        sequenced = " then " in cam or "then a " in cam or "then the " in cam
        if (
            not sequenced
            and any(w in cam for w in STILL_WORDS)
            and re.search(
                r"\b(push|pull|truck|pan|tilt|orbit|crane|dolly|track|zoom|whip)\b", cam
            )
        ):
            issues.append(("ERROR", sid, "camera contradicts itself: static + movement"))

        for token in TOKEN_RE.findall(shot_placeholders(shot)):
            referenced.add(token)

        text = str(shot.get("dialogue_en") or shot.get("dialogue") or "")
        if text and word_count(text) > 12:
            issues.append(("WARN", sid, f"dialogue is {word_count(text)} words; keep ≤ 12"))

        for model in models:
            prompt = build_prompt(shot, ctx, model)
            limit = MODEL_LIMITS[model]
            if has_cjk(prompt):
                # words are the wrong metric for Chinese; count characters and
                # only flag a prompt that is too thin to hold a shot together.
                floor = 240 if model == "minimax" else 90
                chars = len(re.sub(r"\s+", "", prompt))
                if chars < floor:
                    issues.append(
                        ("WARN", sid, f"{model} prompt is only {chars} 字; too thin for this model")
                    )
            else:
                n = word_count(prompt)
                if n > limit:
                    issues.append(("WARN", sid, f"{model} prompt is {n} words (limit ~{limit}); trim style or setting"))
            lowered = prompt.lower()
            hits = [w for w in ABSTRACT_WORDS if w in lowered]
            if hits:
                issues.append(("WARN", sid, f"{model} prompt contains low-value words: {', '.join(sorted(set(hits)))}"))

    for key in sorted(set(ctx.entities) - referenced):
        issues.append(("INFO", key, "defined but never used by any shot"))
    for key in sorted(ctx.unresolved):
        issues.append(("ERROR", "-", f"unresolved placeholder {{{{{key}}}}}"))

    if total > 90:
        issues.append(("WARN", "-", f"total runtime {total:g}s; split into sequences"))
    issues.append(("INFO", "-", f"total runtime {total:g}s across {len(shots)} shots"))
    return issues


# ---------------------------------------------------------------- render

def render_markdown(data: dict, ctx: Ctx, models: list[str], lang: str) -> str:
    shots = data.get("shots") or []
    title = str(data.get("title") or "Video prompt pack")
    out: list[str] = [f"# {title}", ""]

    if data.get("logline"):
        out += [f"> {data['logline']}", ""]
    if data.get("poster_frame"):
        out += [f"**封面帧**：{data['poster_frame']}", ""]

    total = sum(float(s.get("duration") or 0) for s in shots)
    meta = [f"{len(shots)} 镜", f"{total:g}s"]
    if ctx.aspect:
        meta.append(ctx.aspect)
    if data.get("fps"):
        meta.append(f"{data['fps']}fps")
    out += ["**规格**：" + " · ".join(meta), ""]

    style_bits = [
        ctx.style.get("look"),
        ctx.style.get("palette"),
        ctx.style.get("grade"),
        ctx.style.get("texture"),
    ]
    style_line = " · ".join(str(b) for b in style_bits if b)
    if style_line:
        out += ["## 风格锚点", style_line, ""]
    optics = str(ctx.style.get("optics") or "").strip()
    if optics:
        out += [f"**光学**：{optics}", ""]
    music_raw = str(ctx.audio.get("music") or "").strip()
    music_ok = music_raw.lower() not in ("none", "no music", "无", "无音乐", "-")
    audio = " · ".join(
        str(x)
        for x in (ctx.audio.get("ambience"), music_raw if music_ok else "")
        if x
    )
    if audio:
        out += [f"**声音基调**：{audio}", ""]

    chars = [c for c in (data.get("characters") or []) if isinstance(c, dict)]
    locs = [loc for loc in (data.get("locations") or []) if isinstance(loc, dict)]
    if chars or locs:
        out += ["## 一致性圣经", "", "逐字复制到每一镜，不要改写。", ""]
        for item in chars + locs:
            key = str(item.get("id") or "")
            name = str(item.get("name") or "")
            anchor = str(item.get("anchor") or "")
            label = f"（{name}）" if name else ""
            out.append(f"- `{{{{{key}}}}}`{label} — {anchor}")
        out += [""]

    out += [
        "## 分镜表",
        "",
        "| # | 时长 | 景别 | 画面 | 运镜 | 声音 |",
        "|---|---|---|---|---|---|",
    ]
    for shot in shots:
        sid = str(shot.get("id") or "?")
        dur = shot.get("duration") or ""
        size = str(shot.get("size") or "")
        beat = str(shot.get("beat") or "").replace("|", "/")
        cam = str(shot.get("camera") or "").replace("|", "/")
        snd = " / ".join(norm_list(shot.get("sound")))
        out.append(f"| {sid} | {dur}s | {size} | {beat} | {cam} | {snd} |")
    out.append("")

    out += ["## 逐镜提示词", ""]
    for model in models:
        if len(models) > 1:
            out += [f"### 模型：{model}", ""]
        for shot in shots:
            sid = str(shot.get("id") or "?")
            dur = shot.get("duration") or ""
            size = str(shot.get("size") or "")
            out.append(f"#### {sid} · {dur}s · {size}")
            if lang in ("zh", "both") and shot.get("beat"):
                out.append(f"*{shot['beat']}*")
            out.append("")
            prompt = build_prompt(shot, ctx, model)
            out.append("```text")
            out.append(prompt)
            out.append("```")
            if has_cjk(prompt):
                chars = len(re.sub(r"\s+", "", prompt))
                out.append(f"`{chars} 字`")
            else:
                out.append(f"`{word_count(prompt)} words`")
            if shot.get("transition"):
                out.append(f"`转场: {shot['transition']}`")
            out.append("")

    single = build_single_prompt(ctx, shots)
    if single:
        out += ["## 单条总提示词", "", "给「一段话只能出一个视频」的模型用。", "", "```text", single, "```", ""]

    negatives = norm_list(data.get("negatives")) or (
        DEFAULT_NEGATIVES_ZH if ctx.lang == "zh" else DEFAULT_NEGATIVES
    )
    joiner = "，" if ctx.lang == "zh" else ", "
    out += ["## 负面词", "", joiner.join(negatives), ""]

    per_shot = ""
    if shots:
        durs = [float(s.get("duration") or 0) for s in shots]
        if "minimax" in models:
            per_shot = "本地 H3 单镜 5–8s 最稳，10s 上限；"
        elif durs and max(durs) <= 6:
            per_shot = "单镜 4–6s 最稳；"
    param_lines = [
        f"- 画幅：{ctx.aspect or '16:9（未指定，按横屏处理）'}",
        f"- 时长：共 {total:g}s；{per_shot}超过 8s 拆镜",
        "- 运镜强度：有该参数时用低档（0.3–0.5），运镜靠文字描述，不靠强度",
        "- 首帧：先做「封面帧」那一镜，把它当角色定妆参考",
        "- 生成顺序：封面帧 → 出场镜 → 其余按叙事顺序 → 结尾镜",
        "- 重试：同一提示词跑 3 次取最好；连续 3 次都崩说明提示词有问题",
        "- 一致性：同一角色跨镜用沿用同一张首帧图做图生视频，比纯文字稳一个档",
    ]
    if "minimax" in models:
        param_lines += [
            "- 本地 H3：种子固定后再调提示词，否则分不清是提示词还是采样在变",
            "- 本地 H3：分辨率与时长按显卡实录，先 720p 短跑通再上高分辨率",
            "- 本地 H3：逐镜生成后用同一张角色首帧回灌，跨镜一致性靠图不靠字",
            "- 本地 H3：把「身份锁」段整段复制，不要改写、不要缩写",
        ]
    out += ["## 参数与生成顺序", ""] + param_lines + [""]
    return "\n".join(out)


# ---------------------------------------------------------------- cli

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a video prompt pack from storyboard JSON.")
    parser.add_argument("storyboard", help="path to storyboard .json")
    parser.add_argument(
        "--model",
        default="veo3",
        help="comma separated: " + ", ".join(BUILDERS),
    )
    parser.add_argument("--out", help="write markdown to this path")
    parser.add_argument(
        "--lang",
        default="zh",
        choices=["en", "zh", "both"],
        help="prompt language; zh is the default and only affects labels/glue",
    )
    parser.add_argument("--check", action="store_true", help="only run quality checks")
    args = parser.parse_args(argv)

    path = Path(args.storyboard)
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        print(f"storyboard not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"invalid JSON in {path}: {exc}", file=sys.stderr)
        return 2

    models = [m.strip().lower() for m in args.model.split(",") if m.strip()]
    models = [MODEL_ALIASES.get(m, m) for m in models]
    unknown = [m for m in models if m not in BUILDERS]
    if unknown:
        print(f"unknown model(s): {', '.join(unknown)}; choose from {', '.join(BUILDERS)}", file=sys.stderr)
        return 2

    ctx = Ctx(data, args.lang)

    if args.check:
        issues = run_checks(data, ctx, models)
        for level, where, message in issues:
            print(f"[{level}] {where}: {message}")
        errors = sum(1 for level, _, _ in issues if level == "ERROR")
        return 1 if errors else 0

    issues = run_checks(data, ctx, models)
    pack = render_markdown(data, ctx, models, args.lang)
    errors = [i for i in issues if i[0] == "ERROR"]
    if errors:
        pack += "\n## 质量闸门\n\n"
        for level, where, message in errors:
            pack += f"- **{level}** {where}: {message}\n"

    if args.out:
        out_path = Path(args.out)
        with out_path.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(pack)
        print(f"wrote {args.out} ({len(pack)} chars)")
    else:
        print(pack)

    for level, where, message in issues:
        if level in ("ERROR", "WARN"):
            print(f"[{level}] {where}: {message}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    raise SystemExit(main())