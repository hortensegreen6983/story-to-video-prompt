# 提示词模板与范例（Prompt Templates）

模板是骨架，范例是标尺。写不出来时，先照着范例的密度写，再把内容换成自己的故事。

## 目录

1. 单镜模板（通用 / Veo / Sora / Kling / Seedance / Hailuo / Runway）
2. 单条总提示词模板
3. 多镜头单提示词（Seedance 类）
4. 三个成片级范例
5. 弱 → 强改写对照
6. 分镜 JSON 格式（给脚本用）

---

## 1. 单镜模板

### 1.1 通用（任何模型都能吃，信息最全）

```text
{SIZE}. {SUBJECT} {ACTION_1}{, then ACTION_2}. {SETTING}. {LIGHTING}.
Camera: {CAMERA_MOVE}, {LENS}, {DEPTH}. {LOOK}. {GRAIN_ASPECT}.
Audio: {AMBIENCE}; {FOLEY}; {MUSIC}. {DIALOGUE}. No {NEG_1}, no {NEG_2}.
```

### 1.2 Veo 3 / 3.1

散文式，一句一句推进；音频写在结尾；对白直接引号。

```text
{SIZE}, {SUBJECT} {ACTION_1}, then {ACTION_2}. {SETTING}, {ATMOSPHERE}.
{LIGHTING}. The camera {CAMERA_MOVE}, {LENS}.
{LOOK}, {GRAIN}, {ASPECT}.
Audio: {AMBIENCE}, {FOLEY}. {MUSIC}. {SPEAKER} says in {LANG}, {ADVERB}: "{LINE}"
No subtitles, no on-screen text, no watermark.
```

要点：Veo 3 会真的生成对白与音效，所以**必须写 `no subtitles`**，否则它会在画面上烧字幕。

### 1.3 Sora 2

叙事段落，强调物理因果与重量感，时长写在开头。

```text
A {DURATION}-second {SIZE} shot. {SUBJECT} {ACTION_1}. {PHYSICS_DETAIL}.
{SETTING}. {LIGHTING}. The camera {CAMERA_MOVE}, {LENS}. {LOOK}, {ASPECT}.
{SPEAKER} says: "{LINE}"
```

要点：Sora 2 对「物理」最敏感——写清重量、摩擦、惯性、衣服怎么动，出片质量差一档。

### 1.4 Kling 2.x

关键词堆叠，逗号分隔，短句优先；负面词单独给。

```text
{SIZE}, {SUBJECT}, {ACTION_1}, {SETTING}, {LIGHTING}, {CAMERA_MOVE}, {LENS}, {LOOK}
Negative prompt: {NEG_LIST}
```

要点：Kling 吃「主语 + 动作 + 场景 + 运镜 + 风格」的平铺结构，写长句反而降质。支持首帧/尾帧图，连续性靠图不靠词。

### 1.5 Seedance

支持一条提示词多镜头，用编号分段：

```text
镜头1：{SIZE}, {SUBJECT} {ACTION_1}, {SETTING}, {LIGHTING}, {CAMERA_MOVE}
镜头2：{SIZE}, {SUBJECT} {ACTION_2}, {SETTING}, {LIGHTING}, {CAMERA_MOVE}
整体风格：{LOOK}, {ASPECT}
```

### 1.6 Hailuo / MiniMax

极简，一句话说完。

```text
[{CAMERA_MOVE}] {SUBJECT} {ACTION_1}, {SETTING}, {LIGHTING}, {LOOK}
```

### 1.7 Runway Gen-4

先有首帧图，提示词只描述**运动**。

```text
{SUBJECT} {ACTION_1}. Camera: {CAMERA_MOVE}. {LIGHTING_CHANGE}
```

---

## 2. 单条总提示词模板

给「一段话只能出一个视频」的模型，或做 8s 概念片。

```text
A {DURATION}-second {GENRE} short. {LOGLINE_AS_VISUAL}.
Opens on {SHOT_1}. {SUBJECT} {ACTION}. {LIGHT_1}.
Then {SHOT_2_BEAT}, {CAMERA_MOVE}. {LIGHT_2}.
Ends on {SHOT_3_BEAT}, {CAMERA_MOVE_TO_REST}.
Throughout: {LOOK}, {GRAIN}, {ASPECT}. Audio: {AMBIENCE}, {MUSIC}. No on-screen text.
```

三条纪律：

1. 只写三个 beat，多了模型抓不住
2. 每个 beat 只给一个动作 + 一个光
3. 结尾一定要「停住」（`the camera settles, she does not move`），否则模型会在最后 2 秒乱加动作

---

## 3. 多镜头单提示词（Seedance 类）

```text
镜头1：大远景，{SETTING}，{SUBJECT} 从画面右侧走入，{LIGHTING}，固定机位
镜头2：中近景，{SUBJECT} 停下，{ACTION}，{LIGHTING}，缓推
镜头3：特写，{DETAIL_PROP}，{LIGHTING}，固定
风格：{LOOK}, {ASPECT}, {GRAIN}
```

要点：每镜仍要「一动作一机位」；镜头之间要有**视觉钩子**（同一形状、同一颜色、同一动作方向）才不散。

---

## 4. 三个成片级范例

### 范例 A · 暗房（文艺 / 克制）

**剧情**：师父死后，学徒在暗房里冲洗他留下的最后一卷胶片。

**风格锚点**：2.39:1 · 24fps · 35mm Kodak Vision3 500T 细颗粒 · 红光高光溢出 · 青灰阴影 · 无配乐

**圣经**

```text
{{CHAR_A}} = an 18-year-old apprentice, buzz-cut hair, faded navy canvas apron over a grey tee, dark freckles across the nose, dust on his knuckles
{{LOC_DARKROOM}} = a cramped 1980s photo studio darkroom, stained enamel developing trays, strings of drying prints overhead, one red safelight above the door
```

**S01 · 6s · 中近景 · 缓推**

```text
MEDIUM CLOSE-UP, an 18-year-old apprentice, buzz-cut hair, faded navy canvas apron over a grey tee, dark freckles across the nose, dust on his knuckles, holds a small brass film canister up to the red safelight with both hands, as if it might break, then blinks once, too slowly. The darkroom behind him: stained enamel trays, strings of drying prints, one red safelight above the door. Hard red key from screen-left rims his cheekbone and one eye, everything else in soft shadow, a bead of sweat catching the light at his temple. The camera performs a very slow 8% push-in over the full 6 seconds, 50mm at T2, shallow depth so the doorway melts into red bokeh. 35mm Kodak Vision3 500T, fine grain, halation blooming on the safelight, muted cyan in the shadows, 2.39:1. Audio: ventilation fan hum, a single drip into a tray, no music. He whispers in Mandarin, barely audible: "师父，这卷……还没拍完。" No subtitles, no on-screen text, no watermark, no extra fingers, no morphing faces.
```

**S02 · 4s · 特写 · 固定**

```text
EXTREME CLOSE-UP, two thumbs prying the brass lid off a film canister, the metal edge nicked and green with age, dust falling from the seam. Red safelight from screen-left, hard shadows in the knuckle creases; the rest of the frame is near black. Locked-off on a tripod, 100mm macro at T4, razor-thin depth of field — only the rim of the lid is sharp. 35mm Kodak Vision3 500T, fine grain, halation on the metal edge, 2.39:1. Audio: metal creaking, one dry click as the lid gives, no music. No on-screen text, no watermark, no extra fingers.
```

**S03 · 5s · 中景 · 横移**

```text
MEDIUM SHOT, the same 18-year-old apprentice, buzz-cut hair, faded navy canvas apron over a grey tee, stands at a line of drying prints clipped to a wire, lifting one print by its corner. On the paper: the blurred face of a stranger he has never met. He holds it still; the print trembles slightly. Red safelight above and behind him, so his face is a half-lit silhouette and the print catches the light. The camera trucks right one slow step, ending with the print centered and the boy at the edge of frame. 50mm at T2.8. 35mm Kodak Vision3 500T, fine grain, halation, muted cyan shadows, 2.39:1. Audio: paper fibers creaking as it bends, ventilation hum, no music. No on-screen text, no watermark, no morphing faces.
```

**S04 · 6s · 全景 · 后拉**

```text
WIDE SHOT, the cramped 1980s darkroom in full: stained enamel trays, strings of drying prints, one red safelight above the door. The apprentice sits on an upturned crate in the middle of the floor, apron bunched at his waist, a dozen prints of strangers spread around his feet, his head down. Red light from screen-left, the corners of the room falling to black. The camera dollies back slowly through the doorway, ending with the red rectangle of the door framing him. 35mm at T2.8, deep enough that the trays read. 35mm Kodak Vision3 500T, fine grain, halation, 2.39:1. Audio: ventilation fan, the hum of a refrigerator starting up, no music. No on-screen text, no watermark.
```

→ 四镜的论证：S01 他不敢打开；S02 打开了；S03 里面不是师父；S04 他坐在陌生人的脸中间。**没有一句解释。**

---

### 范例 B · 雨夜（武侠 / 静止）

**风格锚点**：2.39:1 · 变形宽银幕 · 去饱和蓝绿 · 重雨雾 · 低音弦乐 drone

**S01 · 6s · 全景 · 横移**

```text
WIDE SHOT, a lone swordsman in a rain-soaked grey hemp robe stands at the far end of a flooded stone courtyard, sword still sheathed, shoulders rising once with breath. Rain falls in visible sheets, backlit by a single blue-white paper lantern hanging from the eaves, so every drop reads as a bright thread. He steps forward once; the water at his feet breaks into a ring. The camera trucks right laterally at chest height, very slowly, ending with him dead center and the lantern at frame edge. 35mm anamorphic, T2.8, oval bokeh, gentle horizontal flare from the lantern. Desaturated blue-green grade, heavy rain haze, 2.39:1. Audio: dense rain on tile, distant thunder, a low bowed-string drone. No slow motion, no wire work, no text.
```

**S02 · 4s · 大特写 · 固定**

```text
EXTREME CLOSE-UP on the sword's scabbard, black lacquer beaded with rain, one drop gathering at the mouth of the scabbard and falling. Blue-white lantern light from screen-right, everything else in deep shadow, the lacquer holding a single long highlight. Locked-off tripod, 100mm macro at T4, only the water bead in focus. Anamorphic, desaturated blue-green, fine mist on the lens, 2.39:1. Audio: rain on lacquer, the drop landing, drone continuing. No text, no watermark.
```

**S03 · 5s · 中近景 · 缓推**

```text
MEDIUM CLOSE-UP, the swordsman's face under the dripping eaves, water running off his jaw, eyes lifting to look down the street. A single lantern flame reflected in each pupil, warm against the cold blue of his skin. Rain streaks the foreground out of focus. The camera pushes in very slowly, 4% over five seconds, 85mm at T2, background dissolving into blue haze. Anamorphic, desaturated blue-green, 2.39:1. Audio: rain, a wooden shutter creaking somewhere, drone rising a semitone. He says nothing. No text, no watermark, no morphing.
```

**S04 · 6s · 大全景 · 固定**

```text
EXTREME WIDE SHOT down a narrow flooded street at night, rain sheeting, blue-white lanterns receding into mist. At the far end, a figure under a black oil-paper umbrella stands perfectly still, face unreadable. The swordsman steps forward into the foreground, back to camera, hand on the hilt, and stops. Neither moves. Locked-off tripod, 24mm, deep focus so both figures read. Anamorphic, desaturated blue-green, heavy atmosphere, 2.39:1. Audio: rain, one distant temple bell, drone cutting to silence on the cut. No text, no watermark, no blood.
```

→ 四镜没有一次交手。**静止本身就是动作。**

---

### 范例 C · 天文台（科幻 / 尺度）

**风格锚点**：2.39:1 · 数码干净 + 轻微颗粒 · 冷青 + 一点钨丝暖 · 极简合成器音

**S01 · 6s · 大远景 · 航拍拉远**

```text
EXTREME WIDE SHOT, a rusted radio telescope dish on a snowy ridge at blue hour, its frame skeletal against a deep indigo sky. A single figure in a red parka stands on the catwalk beneath it, small enough to be a speck, one hand on the railing. Wind lifts loose snow off the ridge in thin streaks. The camera pulls back slowly on a drone to 120 meters, the dish shrinking, the figure becoming a red dot. 24mm, deep focus, cold cyan grade with a single warm work-light glowing inside the control hut. Light digital grain, 2.39:1. Audio: high wind, cable humming, a low synth pad. No text, no watermark.
```

**S02 · 4s · 特写 · 固定**

```text
CLOSE-UP of an old reel-to-reel tape machine inside a dim control hut, one reels turning, a needle trembling in the red on a VU meter. Dust on the glass. A single tungsten desk lamp from screen-right, warm against the cold blue leaking through a porthole window. Locked-off, 50mm at T2, shallow. Fine grain, halation on the lamp, 2.39:1. Audio: tape hiss, a crackle, then a voice too degraded to understand, low synth. No on-screen text, no readable labels.
```

**S03 · 5s · 中近景 · 极缓推**

```text
MEDIUM CLOSE-UP, a woman in her thirties in a red parka, breath steaming, headphones pressed to one ear with one hand, the other flat on the tape machine. Her eyes move as she listens; her mouth opens slightly, then closes. Static in her hair from the dry air. Cold blue from the porthole on her left, warm tungsten on her right, the two colors meeting on her cheek. The camera pushes in 5% over five seconds, 85mm at T2. Fine grain, 2.39:1. Audio: tape hiss, a man's voice saying one short sentence, unintelligible, then silence except her breathing. No subtitles, no text.
```

**S04 · 6s · 全景 · 固定**

```text
WIDE SHOT, the control hut interior from the doorway: banks of dead equipment, the woman sitting on the floor with her back against the tape machine, headphones around her neck, face tilted up toward the ceiling. Through the porthole behind her, the telescope dish begins to turn, snow swirling through its frame. Warm lamp low screen-right, cold blue from the window, most of the room in shadow. Locked-off tripod, 35mm, T2.8. Fine grain, 2.39:1. Audio: the deep mechanical groan of the dish turning, wind, no music. No text, no watermark.
```

→ 尺度对比：S01 人是一个红点；S04 机器在她背后开始转动。**她听懂了，但没说。**

---

## 5. 弱 → 强改写对照

### ① 哭戏

✗ `A beautiful woman crying in the rain, cinematic, emotional, 8K`

问题：没有动作、没有光位、没有景别；`cinematic/8K` 是无效词；「哭」是一个状态，不是一个动作。

✓
```text
CLOSE-UP, a woman in her late twenties, wet hair stuck to her cheek, standing under a broken awning. She is not crying yet; her jaw tightens, she blinks twice, and then her face simply gives way, no sound. Thin rain falls between her and the camera, backlit by a single sodium street lamp so each drop flashes amber. Locked-off on a tripod, 85mm at T1.8, only her eyes sharp. 35mm film, fine grain, halation on the street lamp, cold blue shadows against amber, 2.39:1. Audio: rain on canvas, a car passing in the distance, no music. No subtitles, no text.
```

### ② 争吵

✗ `Two people arguing in a kitchen, intense, dramatic lighting`

问题：两人同框且都在动，模型必崩；`dramatic lighting` 等于没写。

✓
```text
MEDIUM SHOT, a man in his forties in a sweat-stained shirt stands at a kitchen counter, both hands flat on the formica, shoulders up, not speaking. Behind him, out of focus in the doorway, a woman's silhouette does not move. One bare bulb overhead, hard top light, his eye sockets in shadow. Locked-off, 35mm at T2.8, the woman soft. 35mm film, fine grain, 2.39:1. Audio: a refrigerator humming, a clock, no music. He says quietly, without turning: "你先把刀放下。" No text, no watermark, no extra limbs.
```

### ③ 战斗

✗ `Epic battle scene, hundreds of soldiers charging, swords, horses, cinematic masterpiece`

问题：几百人 + 复杂动作 = 必然糊；模型没有能力处理群体调度。

✓
```text
WIDE SHOT, a muddy field at dawn, low fog. One soldier in dented plate armor stands alone in the foreground, back to camera, sword hanging at his side, breathing hard. Far behind him, on the ridge, a line of torches is lighting one by one. He does not turn around. Locked-off, 35mm at T4, deep focus so the torches read. Overcast grey light, no sun, desaturated, 2.39:1. Audio: wind, distant metal, a single horse nickering, no music. No text, no blood, no crowd in the foreground.
```

### ④ 美食 / 广告

✗ `Delicious noodles, steam, appetizing, high quality food photography`

问题：没有动作、没有光、没有镜头。食物片全靠「一瞬间的物理」。

✓
```text
EXTREME CLOSE-UP, a pair of chopsticks lifting a bundle of hand-pulled noodles from a bowl of clear broth, the strands stretching and snapping back, one drop of broth falling. Steam rises through a hard side light from screen-right, so the steam reads as visible white threads. The bowl is chipped enamel, blue rim, worn. Locked-off, 100mm macro at T2.8, only the noodle bundle sharp. Warm tungsten, subtle steam haze, fine grain, 16:9. Audio: broth dripping, ceramic clink, no music. No text, no watermark.
```

**改写公式**：删掉所有形容词 → 补景别 → 补一个动作 → 补单一光源与方向 → 补运镜与焦段 → 补质感与画幅 → 补声音 → 补负面词。

---

## 6. 分镜 JSON 格式（给脚本用）

`scripts/build_prompt_pack.py` 的输入。字段缺省时脚本会用空值并给出警告。

```json
{
  "title": "最后一卷",
  "logline": "师父死后，学徒在暗房里冲洗他留下的最后一卷胶片。",
  "poster_frame": "他坐在一地的陌生人照片中间，红光只照亮半张脸。",
  "aspect_ratio": "2.39:1",
  "fps": 24,
  "style": {
    "look": "35mm Kodak Vision3 500T, fine grain, halation on highlights",
    "palette": "muted cyan shadows, red safelight highlights",
    "grade": "low contrast, milky blacks",
    "texture": "subtle gate weave"
  },
  "audio": { "music": "none", "ambience": "ventilation hum" },
  "characters": [
    {
      "id": "CHAR_A",
      "name": "学徒",
      "anchor": "an 18-year-old apprentice, buzz-cut hair, faded navy canvas apron over a grey tee, dark freckles across the nose, dust on his knuckles"
    }
  ],
  "locations": [
    {
      "id": "LOC_DARKROOM",
      "name": "暗房",
      "anchor": "a cramped 1980s photo studio darkroom, stained enamel developing trays, strings of drying prints overhead, one red safelight above the door"
    }
  ],
  "negatives": ["on-screen text", "watermark", "extra fingers", "morphing faces"],
  "shots": [
    {
      "id": "S01",
      "duration": 6,
      "beat": "他把最后一卷胶片举到红光下",
      "size": "MEDIUM CLOSE-UP",
      "subject": "{{CHAR_A}}",
      "action": [
        "holds a small brass film canister up to the red safelight with both hands, as if it might break",
        "blinks once, too slowly"
      ],
      "setting": "{{LOC_DARKROOM}}",
      "lighting": "hard red key from screen-left rims his cheekbone and one eye, everything else in soft shadow",
      "camera": "a very slow 8% push-in over the full 6 seconds",
      "lens": "50mm at T2, shallow depth",
      "sound": ["ventilation fan hum", "a single drip into a tray"],
      "dialogue": "师父，这卷……还没拍完。",
      "dialogue_lang": "Mandarin",
      "speaker": "CHAR_A",
      "adverb": "barely audible",
      "transition": "cut"
    }
  ]
}
```

常用可选字段：`dialogue_en`（英文台词，优先于 `dialogue`）、`style_override`（单镜覆盖风格）、`negative_extra`（单镜追加负面词）、`physics`（Sora 用的重量/惯性描述）、`atmosphere`（空气介质）。