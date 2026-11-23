# 本地 MiniMax H3 适配卡

面向在自己机器上跑 MiniMax 系视频模型（Hailuo / H3 构建）的场景：没有 API 的长度税，所以提示词可以长；但也因为没有平台侧兜底，**结构**成为唯一的稳定性来源。

参数名各构建不同（ComfyUI 节点、CLI、gradio 前端字段名都不一样），下表给的是**语义 + 起点值**，按你的构建对应过去。

---

## 一、它吃什么

- **长提示词**：本地推理没有 200 词上限，600–900 词的分区块提示词是正常量级，不是浪费。
- **中英混排**：英文写画面与光学，中文写对白与语气，通常比全英文更准。
- **顺序敏感**：先主体后环境、先光后镜头。把最重要的信息放在前 1/3。
- **标签化程度低**：给完整句子好过给 `masterpiece, best quality` 这类标签堆。
- **对时间码敏感**：`0.0–1.8s — ...` 这种写法能显著减少"动作糊在一起"。

## 二、提示词骨架（脚本 `--model h3` 已自动生成）

```
S01 | 7s | MEDIUM SHOT | 2.39:1 | 24 fps

IDENTITY LOCK — copy verbatim
<角色锚点，逐字复制，绝不改写>

WARDROBE / PROPS
<本镜穿着与随身物件，含磨损状态>

PERFORMANCE — real time, beat by beat
0.0–1.8s — <动作 + 一个生理反应>
...

ENVIRONMENT
<空间几何 + 空气介质>

PHYSICS — weight, contact, secondary motion
<重量、接触、次级动作>

LIGHT — one physical source logic
<主光 + 比值 + 衰减 + 实用光源>

CAMERA / OPTICS
<运镜; 焦段光圈; 1/48s shutter>

TEXTURE — micro detail that must be visible
- <5–8 条材质使用史>

IMAGE QUALITY
<look / palette / grade / texture>
<光学与捕捉描述>

AUDIO
<底噪; 事件; 人体; 对白>

CONTINUITY
<与哪一镜同源>

NEGATIVE
<负面词>
```

**为什么分区**：崩的时候能立刻定位是哪一段错了。段落是一句话的时候，你只能整条重写。

## 三、时长

| 时长 | 结果 |
|---|---|
| 3–4s | 只能容纳一个动作，叙事不够 |
| **5–8s** | 最优区间，四拍表演能完整落地 |
| 9–10s | 上限，需要更严格的 timecode，否则后半段开始漂 |
| >10s | 拼接两镜，不要硬拉 |

一个 5–8s 镜头 = 四个 timecode 拍子。少一拍就空，多一拍就糊。

## 四、参数起点

| 语义 | 起点 | 说明 |
|---|---|---|
| 分辨率 | 720p 先跑通，再上 1080p | 先验证提示词，再烧算力 |
| 帧率 | 24 fps | 与 1/48s 快门配对，运动才自然 |
| 步数 | 构建默认到默认 ×1.5 | 过高会"过度锐化"，塑料感变强 |
| CFG / 提示词强度 | 中低 | 太高会让模型死抠字面，动作变僵 |
| 运动强度 | 低–中 | 运镜靠文字，不靠这个参数 |
| 种子 | **固定** | 调提示词时必须固定，否则分不清变量 |

## 五、一致性：靠图，不靠字

单靠文字描述锁脸，跨镜一定漂。四步流程：

1. **定妆帧**：先用 poster frame 那一镜生成一张角色首帧，挑最好的一张存档。
2. **首帧回灌**：每一镜都用这张图走 image-to-video，而不是纯文生视频。
3. **整段复制 IDENTITY LOCK**：不要"缩写一下"，一个字都别改。
4. **场景同理**：同一空间先用一张环境定妆帧，再逐镜回灌。

跨镜变化只允许发生在：动作、机位、光比、时间。**脸、衣服、房间几何**不动。

## 六、负面词（本地常用）

```
on-screen text, subtitles, watermark, logo, extra fingers, deformed hands,
morphing faces, duplicate limbs, warped shelving, rubber-looking skin,
floating objects, cartoon shading, oversaturated, sharpening halos,
plastic texture, jitter, flickering, frame tearing
```

按题材加：`no blood`、`no weapons`、`no crowd`、`no lens flare`（当你不想要眩光时）。

## 七、崩坏定位表

| 现象 | 真正的原因 | 改法 |
|---|---|---|
| 脸每镜都不同 | 没走 I2V / 锚点被改写 | 首帧回灌 + 整段复制 IDENTITY LOCK |
| 手指糊成一团 | 手在画面里占太大 / 动作太快 | 手部降到画面 1/5，改成"停住"而非"抓取" |
| 纹理像塑料 | 只写了 `realistic` | 加 TEXTURE 段 5–8 条材质使用史 |
| 后半段动作漂 | 缺 timecode | 拆成四拍，每拍给起止时间 |
| 镜头自己乱动 | 运镜描述含糊 + 运动强度高 | 明确 `locked off` 或给具体百分比，强度调低 |
| 光很平 | 没给比值 | 补 `four stops of falloff behind him` |
| 画面"太干净" | 没有使用史 | 加灰尘、指纹、水痕、磨损 |
| 人物瞬移/多出一个人 | 提示词里塞了两个主体 | 一镜一主体，配角放进 ENVIRONMENT |
| 对白口型对不上 | 对白太长 | 压到 12 词以内，或改成画外 |
| 闪烁/撕裂 | 步数或分辨率超了构建能力 | 降一档先跑通 |

## 八、拼接

- 同场景连续镜 → 用同一张环境首帧，转场直接 `cut`。
- 跨场景 → 允许一次 `cut to black`，比硬切安全。
- 需要运动衔接 → 前一镜末尾和后一镜开头写同一个动作（`hand still raised` / `hand already raised`）。
- 不要靠模型自己生成转场（溶解、推拉过渡），渲染出来通常是糊的。

## 九、跑批约定

- 输出命名：`S03_take2_seed1234.mp4`，种子进文件名。
- 一次只改一个变量（提示词 / 种子 / 步数），三次对比再下结论。
- 每镜留 3 个 take，剪辑时按表演挑，不按"哪条最清晰"挑。
- 失败镜头别删，留着做"这条提示词到底错在哪"的证据。