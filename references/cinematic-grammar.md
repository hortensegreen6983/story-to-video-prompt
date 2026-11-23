# 镜头语言词库（Cinematic Grammar）

写提示词时的取词表。全部给出可直接粘进英文提示词的表达，括号内为中文对应。按需查，不要通读。

## 目录

1. 景别与角度
2. 运镜（含量化句式）
3. 焦段、光圈与景深
4. 光位与光源
5. 色彩、胶片与质感
6. 空气介质与物理细节
7. 声音设计
8. 节奏、转场与时间感
9. 高频描述中英对照
10. 低效词黑名单

---

## 1. 景别与角度

| 英文 | 中文 | 什么时候用 | 什么时候会翻车 |
|---|---|---|---|
| extreme wide shot / establishing shot | 大远景、定场 | 交代空间尺度、孤独感、史诗感 | 人物表情全废，别在这里放情绪 |
| wide shot / full shot | 全景 | 人物与环境关系、动作完整性 | 动作细节看不清 |
| medium full shot / cowboy shot | 七分身 | 腰以上，兼顾手部与表情，西部片常用 | 手部动作复杂时仍会崩 |
| medium shot | 中景 | 对话、日常动作，最稳的通用景别 | 平淡，需要靠光和构图救 |
| medium close-up | 中近景 | 情绪 + 一点环境，性价比最高 | — |
| close-up | 特写 | 情绪爆发、决定性瞬间 | 频繁用会疲劳；脸部细节要求高 |
| extreme close-up / macro | 大特写、微距 | 眼睛、指尖、水滴、刀刃 | 最容易崩结构，慎重 |
| insert shot | 插入镜 | 物件传信息（信、照片、药瓶） | 物件文字会糊，别指望读出字 |
| over-the-shoulder | 过肩 | 对话、窥视、压迫 | 双人调度容易糊在一起 |
| two-shot | 双人镜 | 关系、对峙 | 两人动作都要简单 |
| POV shot | 主观 | 代入、恐惧 | 需要明确「手持轻微晃动」 |
| low angle | 仰拍 | 权力、威胁、崇高 | 过度使用变廉价 |
| high angle | 俯拍 | 弱势、被审判、地图感 | 人物会显得小丑化 |
| dutch angle / canted | 斜角 | 失衡、精神异常 | 全片用一次就够 |
| top-down / overhead | 正俯 | 几何构图、命运感 | 空间关系容易读不清 |
| worm's eye | 虫视 | 极端压迫 | 畸变严重 |
| aerial / drone | 航拍 | 地理、尺度、结尾拉远 | 需要写清高度与速度 |

组合写法：`low-angle medium close-up`、`top-down wide shot`、`over-the-shoulder two-shot`。景别放提示词最前。

---

## 2. 运镜

运镜 = 类型 + 幅度 + 速度 + 落点。四样缺一样模型就开始乱飘。

| 英文 | 中文 | 量化写法示例 |
|---|---|---|
| locked-off / static tripod | 固定机位 | `locked-off on a tripod, no camera movement` |
| slow push-in | 缓推 | `a very slow 10% push-in over the full 6 seconds` |
| dolly in / out | 移动车推拉 | `dolly out two steps, revealing the empty chair` |
| truck left / right | 横移 | `a half-step lateral truck right, ending with her centered` |
| pan left / right | 摇 | `a slow 30-degree pan right, settling on the doorway` |
| tilt up / down | 俯仰摇 | `tilt up from her shoes to her face in one continuous move` |
| whip pan | 甩镜 | `a quick whip pan right, motion blur, landing on the clock` |
| handheld follow | 手持跟随 | `handheld follow half a step behind, breathing micro-shake` |
| Steadicam | 稳定器跟拍 | `smooth Steadicam tracking backward as he walks forward` |
| orbit / arc | 环绕 | `a slow 90-degree orbit around her, clockwise, chest height` |
| crane up / down | 升降 | `crane up three meters, revealing the flooded street` |
| drone pull-back | 航拍拉远 | `drone pull-back to 80 meters, subject shrinking to a dot` |
| vertigo / dolly zoom | 希区柯克变焦 | `dolly zoom: camera pushes in while zooming out, background warping` |
| rack focus | 移焦 | `rack focus from the glass in the foreground to her eye` |
| snap zoom | 急推 | `a snap zoom onto the door handle` |
| tilt-reveal | 竖摇揭示 | `tilt down from the ceiling stain to the body on the floor` |
| parallax slide | 视差滑移 | `lateral slide past a foreground pillar, parallax, subject revealed` |
| overhead descend | 垂直下降 | `camera descends straight down onto the table` |
| push through | 穿门推进 | `push forward through the doorway into the next room` |

规则：

- 一镜一运动。想同时推和摇，就写 `a slow push-in that drifts slightly left`，仍是一个复合但连贯的运动。
- 结尾要有落点：`ending on her hands`、`settling on the empty doorway`。没有落点，模型容易中途乱转。
- 要「稳」就明写 `locked-off tripod, no handheld shake`；要「呼吸感」写 `subtle handheld breathing, 2–3 mm of drift`。

---

## 3. 焦段、光圈与景深

| 写法 | 效果 |
|---|---|
| `14mm ultra-wide, strong perspective distortion` | 空间被撑开，适合狭窄走廊、车内、主观压迫 |
| `24mm wide, deep focus` | 环境叙事，人物与背景都清楚 |
| `35mm, natural reportage look` |  documentary 感，最像「真实发生」 |
| `50mm, neutral perspective` | 最接近人眼，通用 |
| `85mm, creamy bokeh, compressed background` | 人像、情绪、隔离感 |
| `135mm, heavy compression, background melting` | 窥视、疏离、街头远摄 |
| `100mm macro, razor-thin depth of field` | 细节、纹理、昆虫/水滴 |
| `anamorphic, oval bokeh, horizontal flares` | 电影感、宽银幕 |
| `T1.4 wide open, only the eyes in focus` | 极浅景深，注意别整张糊 |
| `T5.6 deep focus, everything sharp` | 群像、环境喜剧、韦斯·安德森式构图 |

---

## 4. 光位与光源

**结构**：光源是什么 + 方向 + 软硬 + 色温。

| 英文 | 中文 |
|---|---|
| single hard key from screen-left | 左前方单硬光 |
| soft window light from camera-right | 右侧窗光柔光 |
| backlit, rim-lit silhouette | 逆光、轮廓光剪影 |
| three-quarter backlight, hair glowing | 侧逆光，发丝发亮 |
| top light, eye sockets in shadow | 顶光，眼窝陷黑 |
| underlight from a phone screen | 手机屏底光 |
| practical neon from the street sign | 街牌霓虹实景光 |
| sodium street lamp, 2200K amber pools | 钠灯暖黄光斑 |
| tungsten interior, 2800K warm | 钨丝灯室内暖调 |
| overcast daylight, 6500K flat and soft | 阴天冷白平光 |
| hard midday sun, short shadows | 正午硬光短影 |
| firelight flicker, warm and unstable | 火光跳动 |
| headlights sweeping across a wall | 车灯扫墙 |
| single bare bulb, harsh falloff | 单灯泡硬光快速衰减 |
| bounce fill off a white wall | 白墙反射补光 |
| mixed color: warm interior vs cold exterior | 冷暖对撞 |
| chiaroscuro, 90% shadow | 明暗对照，大面积暗部 |

规则：**一个镜头一个主光**。写两个以上光源，模型会平均化，结果又平又脏。需要层次就写「主光 + 一处反射/轮廓」。

---

## 5. 色彩、胶片与质感

| 写法 | 气质 |
|---|---|
| `35mm Kodak Vision3 500T, fine grain, halation on highlights` | 夜戏、钨丝灯、电影常规 |
| `Kodak Portra 400, warm pastel, soft contrast` | 温柔、怀旧、日常 |
| `Fuji Eterna, muted green shadows, low saturation` | 冷、克制、日式 |
| `bleach bypass, crushed blacks, silver highlights` | 战争、粗粝、硬 |
| `teal-and-orange grade` | 商业大片，用滥了，慎用 |
| `monochrome, high contrast, deep blacks` | 黑白、宿命 |
| `desaturated blue-grey, milky fog` | 阴郁、雨城 |
| `warm amber and dust, sun-bleached` | 回忆、夏日、旧时光 |
| `neon magenta and cyan, wet asphalt reflections` | 赛博、夜街 |
| `16mm grain, gate weave, slight vignette` | 独立、纪实、粗 |
| `Super 8, heavy grain, light leaks, soft focus` | 家庭录像、记忆 |
| `VHS artifacts, scan lines, chroma bleed` | 90 年代录像带 |
| `digital clean, log-flat then graded, no grain` | 现代剧、广告 |
| `high-key, white background, soft shadow` | 广告、棚拍 |
| `low-key, single source, 80% falloff` | 惊悚、黑色电影 |

全片只用一套。逐镜复制，不换词。

---

## 6. 空气介质与物理细节

介质让画面「有空气」，是廉价提升质感的最大杠杆。

- 尘：`dust motes drifting in a shaft of light`
- 雾：`thin ground fog`, `dense mist reducing contrast at 20 meters`
- 烟：`cigarette smoke curling through the key light`
- 雨：`thin rain visible only against the light`, `heavy rain sheets, backlit`
- 雪：`large wet snowflakes falling slowly`
- 蒸汽：`steam rising from the kettle, catching the light`
- 火星：`embers drifting upward`
- 花粉：`pollen floating in warm afternoon light`
- 海雾：`salt spray hanging in the air`
- 呼吸：`breath vapor in the cold air`
- 湿：`wet hair stuck to the forehead`, `damp fabric clinging`
- 汗：`a bead of sweat catching the light at the temple`
- 布：`coat hem lifting in the wind`, `fabric creasing at the elbow`
- 重力：`weight shifting onto the front foot`, `knees bending as he lands`

物理细节写 1–2 个就够。写多了模型抓不住重点。

---

## 7. 声音设计

Veo 3 / Sora 2 能吃音频提示，写法：`Audio: ambience; foley; music.`

| 层 | 示例 |
|---|---|
| 环境床 | `distant traffic hum`, `cicadas`, `rain on tile`, `fluorescent buzz`, `wind through a gap` |
| 拟音 | `a single drip into a tray`, `keys dropping on wood`, `chair leg scraping concrete` |
| 音乐 | `a low bowed-string drone, no melody`, `solo piano, sparse, one note at a time`, `no music` |
| 静 | `silence except for her breathing` — 比任何配乐都狠 |

规则：音乐写「乐器 + 密度 + 情绪」，不要写曲名。`no music` 是有效指令，别忘。

---

## 8. 节奏、转场与时间感

| 英文 | 用法 |
|---|---|
| `cut on action` | 在动作中切，最顺 |
| `match cut: same shape, different object` | 形状/动作匹配切 |
| `hard cut` | 默认 |
| `dissolve` | 时间流逝，慎用，容易廉价 |
| `fade to black` | 段落结束 |
| `whip-pan transition` | 快节奏段 |
| `J-cut` / `L-cut` | 声音先入/后出，专业感来源 |
| `slow motion, 120fps` | 强调瞬间，全片最多一次 |
| `time-lapse` | 时间压缩 |
| `stop-motion / frame-skip` | 抽帧，怪异感 |
| `speed ramp` | 变速，动作片 |

节奏换算：3s＝一个眼神；5s＝一个完整动作；8s＝一个小场景。观众对 4s 以下的镜头会感到「赶」。

---

## 9. 高频描述中英对照

| 中文 | 英文（可直接用） |
|---|---|
| 斑驳 | mottled, peeling paint |
| 潮湿 | damp, slick with condensation |
| 逼仄 | cramped, low ceiling |
| 空旷 | cavernous, echoing |
| 逆光剪影 | backlit silhouette |
| 光线被切碎 | light broken into slats by the blinds |
| 冷暖对撞 | warm interior against cold blue exterior |
| 一镜到底 | one continuous take, no cuts |
| 手持呼吸感 | subtle handheld breathing |
| 颗粒感 | visible film grain |
| 高光溢出 | halation blooming on highlights |
| 慢门拖影 | long-exposure motion trails |
| 焦点游移 | focus drifting, then locking |
| 面无表情 | expression flat, eyes not moving |
| 僵住 | frozen mid-gesture |
| 强撑 | jaw tight, holding it together |
| 迟了一拍 | a beat too late |
| 泄气 | shoulders dropping, breath leaving |
| 视线躲开 | eyes sliding away |
| 手指蜷起 | fingers curling into the palm |
| 喉结动了一下 | throat moving once |
| 强光刺眼 | squinting against hard light |
| 灰尘在光柱里飘 | dust suspended in a shaft of light |
| 雨点砸在水面 | rain striking the water surface |
| 远处的车灯 | distant headlights sweeping |
| 呼吸在冷空气里成雾 | breath steaming in the cold |

---

## 10. 低效词黑名单

这些词对视频模型几乎不产生画面信息，只会稀释 token：

`cinematic` `epic` `beautiful` `stunning` `masterpiece` `best quality` `8K` `4K` `ultra-detailed` `hyperrealistic` `award-winning` `trending on artstation` `highly detailed` `professional photography` `dramatic lighting`（除非你写清是什么光）

替换法则：把形容词换成**可拍摄的事实**。

- ✗ `beautiful dramatic lighting` → ✓ `a single hard key from screen-left, 80% of the frame in shadow`
- ✗ `epic landscape` → ✓ `a 300-meter cliff face, a single figure at the base, drone pulling back`
- ✗ `sad atmosphere` → ✓ `rain on the window, no music, her reflection doubled in the glass`