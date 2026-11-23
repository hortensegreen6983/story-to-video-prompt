# 超越电影感：物理细节库

"远超电影效果"不是形容词堆叠，而是**把画面写成可被拍摄的物理现场**。
模型对 `cinematic` / `epic` / `8k` 无感，对 `the rag leaves a wet arc that dries from its edges inward` 有反应。

三条铁律：

1. **让摄影机有物理属性** —— 焦段、光圈、快门、呼吸、眩光、色散。没有这些，画面是"渲染"不是"拍摄"。
2. **让材质有使用史** —— 磨损、油污、水痕、指纹、起球。崭新材料 = CG 感。
3. **让光只有一个来源** —— 一个主光逻辑 + 衰减 + 比值。多光源无逻辑 = 打光感。

---

## 一、细节通道（每镜挑 1–3 个通道，取 5–8 条）

### 皮肤 / 人体
- `skin keeps visible pores across the nose and cheekbone, matte except one shine on the brow`
- `a shaving nick under the jaw, already closed, slightly darker than the skin`
- `subsurface warmth in the ear and nostril edges where the light passes through`
- `fine vellus hair on the forearm catching the rim light in a soft halo`
- `the lower lip dry and faintly cracked, one flake lifting`
- `sweat at the temple not running yet, just a sheen breaking the matte`
- `knuckles red and tight from cold water, the skin over them shiny`
- `a bruise two days old, yellow at the edge, not yet faded`
- `stubble uneven on the neck, sharper on the jaw, a patch missed under the chin`
- `the eye wet at the lower lid, one vessel visible at the corner`

### 毛发
- `hair flattened by a cap, a hard band where the brim sat`
- `three strands stuck to the forehead with sweat, the rest dry`
- `stubble length inconsistent, longer at the chin than the cheek`
- `grey hairs mixed in at the temple, maybe a dozen, catching light differently`

### 织物
- `the polo collar frayed, one thread standing up and trembling with breath`
- `fabric pilling at the cuff where the wrist rubs the counter`
- `a bleach spot on the knee, edges soft from washing`
- `the seam puckered where the thread pulled, a small diagonal ridge`
- `shirt untucked at the back, the hem shadowed and creased from sitting`
- `the rag gray and thinning at the fold, its weave opened into holes`
- `wet cotton gone translucent at the shoulder, sticking to the collarbone`

### 硬表面 / 金属
- `the counter worn matte in a crescent where elbows rest, polished at the edge`
- `chrome tap holding fingerprints and one long dried water streak`
- `the hook's paint chipped to bare metal at the contact point, bright where it rubs`
- `screws on the hinge rusted at the slot, not the head`
- `the door handle darker in the middle from hands, lighter at both ends`

### 玻璃 / 透明
- `condensation across the fridge door, one clean drip track cut through it`
- `the monitor glass dusty, dust brighter than the image behind it`
- `a chip in the window corner, radiating a short crack that stops`
- `fingerprints low on the glass, from a child's height`

### 水
- `water beaded on the PVC, running down the folds in thin branching threads`
- `one drop gathering at the hem, swelling, then falling with a visible stretch`
- `a drip line on the tile leading back three meters, drops spaced unevenly`
- `wet footprints drying from the heel inward, the toe still dark`
- `a puddle holding the reflection of one tube, rippled by a step`

### 尘 / 颗粒
- `dust suspended in the light shaft, drifting with the air handler`
- `dust on every horizontal surface, thicker where nothing has been moved`
- `grit on the floor, one grain catching a highlight as it is crushed`

### 烟 / 雾 / 汽
- `cold air from the open fridge pushing a faint fog along the floor`
- `steam off the hot-snack case rising, breaking against the vent current`
- `breath visible in the cold, dense at the mouth, thinning two feet out`

### 火 / 热
- `the lighter flame bending toward the gap under the door`
- `heat shimmer above the fryer making the price tags wobble`

### 纸 / 旧物
- `the price label peeling at one corner, the adhesive gone gray with dust`
- `receipt paper curled and faded, the print gray instead of black`
- `cardboard furred with moisture at the torn corner`

### 食物 / 液体
- `dried broth on the case rim, browned and cracked, one edge lifted`
- `coffee surface with a thin skin, a ring of old residue at the mug's lip`

---

## 二、让画面像"拍的"：光学与捕捉

每镜都该带一句光学描述。可直接抄：

```
shot on a full-frame sensor through anamorphic glass at T2, 1/48s shutter,
elliptical bokeh, mild chromatic fringing at the frame edges,
halation blooming off speculars, highlight rolloff instead of clipped white,
no sharpening halos, no CGI sheen
```

按需替换的部件：

| 想要 | 写 |
|---|---|
| 浅景深人像 | `85mm at T1.8, focus on the near eyelash, the ear already soft` |
| 广角压迫 | `24mm at T2.8, edges stretching, the room bending toward the corners` |
| 长焦压缩 | `135mm at T2.5, background stacked flat behind him` |
| 微距质感 | `100mm macro at T4, texture resolving at the pixel level` |
| 手持呼吸 | `shoulder-mounted, micro-drift on every step, no stabilization` |
| 稳定器滑行 | `gimbal at chest height, the horizon locked, no roll` |
| 变形宽银幕 | `anamorphic 2x squeeze, oval bokeh, horizontal flares only` |
| 手机/监控 | `phone sensor, heavy compression in the shadows, rolling scanlines` |

快门是常被忽略的开关：`1/48s`（24fps 的 180°）给真实运动模糊；`1/1000s` 让动作变"锐利假"；`1/24s` 给拖影和眩晕。

---

## 三、光：一个来源，一条衰减

写法固定为四段：**主光 → 比值 → 衰减 → 实用光源**。

- 主光：`hard cold key from the ceiling grid, straight down`（硬/软、色温、方向）
- 比值：`the aisles behind him falling to black, four stops under the key`
- 衰减：`light dying off the shoulder into the aisle, no bounce back`
- 实用光源：`the monitor is the only source in frame, spilling cold blue onto the bezel`

补充可用的物理现象：
- `a second weak reflection of the tube on the wet counter`
- `hard shadow under the cap brim, the eyes lost in it until he lifts his chin`
- `rim light along the shoulder from the fridge glass, one finger wide`
- `practical flicker: one tube stuttering for two frames`

---

## 四、微表演：让 5–10 秒有内容

一个镜头里，人至少要经历 **四拍**：起始状态 → 变化 → 停顿/犹豫 → 收束。
写法带时间码，每拍一个动作 + 一个生理反应：

```
0.0–1.8s — wipes the counter in slow circles, breathing through his mouth
1.8–4.2s — the circles shorten; he leans weight onto the rag hand, jaw tightening
4.2–5.6s — the hand stops mid-circle, rag still pressed flat
5.6–7.0s — lifts his chin, one blink, breath held
```

可用的生理细节：`一次吞咽`、`眨眼频率变慢`、`鼻翼扩张`、`手指在裤缝上蹭`、`重心从一只脚换到另一只`、`肩膀先动再转身`、`呼吸停在半口`。

**反例**（会被模型演成木偶）：`he is sad and looks at the monitor`。
**正例**：`he stops wiping, thumb still on the rag, and does not blink for two seconds`。

---

## 五、反 AI 味词表

| 别写 | 改写 |
|---|---|
| cinematic lighting | hard cold key from the ceiling grid, four stops of falloff behind him |
| hyperrealistic | skin keeps pores and subsurface warmth; fabric shows weave and pilling |
| 8k, ultra detailed | 100mm macro at T4, texture resolving at the pixel level |
| epic, stunning | 24mm at T2.8, the room bending toward the corners |
| dramatic shadow | one hard shadow from the brim cutting across the eyes |
| beautiful woman | (直接写特征：骨相、发型、皮肤状态、穿着磨损) |
| masterpiece, best quality | 删除，换成光学参数 |
| smooth skin | skin matte except one shine on the brow, pores visible at the nose |
| realistic | shot on a full-frame sensor, 1/48s shutter, halation off speculars |
| volumetric light | dust suspended in the shaft, drifting with the air handler |

---

## 六、一镜的细节预算（5–10 秒）

| 段落 | 条数 | 说明 |
|---|---|---|
| 身份锁 | 1 段 | 逐字复制，绝不改写 |
| 表演 | 3–5 拍 | 每拍一个动作 + 一个生理反应 |
| 环境 | 1 段 | 空间几何 + 空气介质 |
| 物理 | 1–2 条 | 重量、接触、次级动作 |
| 光 | 1 段 | 主光 + 比值 + 衰减 |
| 光学 | 1 行 | 焦段/光圈/快门/散景 |
| 微观 | 5–8 条 | 材质使用史，这是"细节"的真正来源 |
| 声音 | 3–6 层 | 底噪 / 事件 / 人体 / 空间 |
| 连续 | 1 行 | 与哪一镜同源 |

低于这个密度，出来就是"AI 味"；高于这个密度（>8 条微观），模型会开始随机挑着实现，反而丢重点。