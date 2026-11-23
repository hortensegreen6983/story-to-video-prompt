# story-to-video-prompt

> 一段剧情进，一套能直接开跑的镜头提示词出。

把小说片段、故事梗概、剧本节选，或者一句「深夜便利店，一个穿雨衣的人在货架前站了很久」，变成一份**可以直接投喂 AI 视频模型**的完整提示词包：故事脊柱、角色与场景一致性圣经、分镜表、逐镜提示词、单条总提示词、负面词与生成参数。

默认输出**中文**。支持两种密度：云端模型的散文版，和本地长上下文模型（MiniMax H3 一类）的高密度分区块版。

---

## 它解决三个具体问题

| 问题 | 普通提示词的写法 | 这个技能的写法 |
|---|---|---|
| 提示词太笼统，出来是「AI 感画面」 | `cinematic, beautiful, 8K, ultra detailed` | 材质使用史：「抹布擦过留下一道水弧，还没擦完，弧的两端已经开始收干」 |
| 同一个角色第二镜换脸 | 每镜重新描述一遍，措辞各不相同 | 一致性圣经：一条固定串，**逐字复制**进每一镜 |
| 动作做一半、后半段漂 | 一段话描述一个长动作 | 逐拍时间码：`0.0–1.8s / 1.8–4.2s / 4.2–5.6s / 5.6–7.0s`，每拍一个动作 + 一个生理反应 |

---

## 长什么样

`examples/sample-output.md` 是真实产出（《雨衣 · 便利店夜班》，4 镜 28 秒）。节选：

```text
S01 | 7s | 中景 | 2.39:1 | 24 fps

身份锁 — 以下整段逐字复制，不要改写
22岁男性夜班店员，身高178，眼睛窄而疲惫、眼下有青黑，黑发被蓝色工作帽压平，
下颌有淡青的胡茬，右手关节上有一道小裂口；蓝色便利店短袖制服大了两号，
袖子卷起一道，胸牌挂歪15度，黑长裤，灰球鞋，站在收银台后

表演 — 实拍时间轴，一拍一行
0.0–1.8s — 抹布在台面上打圈，肩跟着圈轻轻晃，呼吸用嘴，眼睛已经不在手上
1.8–4.2s — 圈变小、变慢，重心前压到手腕，下颌肌肉绷了一下
4.2–5.6s — 手停在半圈上，抹布还压在湿印里，指节微微发白
5.6–7.0s — 下巴抬起转向监控屏，眨一次眼，胸口停住不起伏

材质 — 必须看得见的微观细节
- 层压板台面在他肘部常搭的位置磨成一块哑光月牙，边缘被前臂抛光
- 抹布擦过留下一道水弧，还没擦完，弧的两端已经开始收干
- 大拇指甲盖上有打价枪的墨印，洗掉了一半
```

单镜 800–1400 字，十二个区块，每个区块只回答一个问题。

---

## 安装

技能本质是一个带 `SKILL.md` 的目录。放进你的 skills 目录即可，主流 agent 客户端都认这个格式（Claude Code、Cursor、DSH 等）。

### 方式一：直接 clone 到 skills 目录

```bash
# macOS / Linux
git clone https://github.com/hortensegreen6983/story-to-video-prompt.git \
  ~/.agents/skills/story-to-video-prompt
```

```powershell
# Windows
git clone https://github.com/hortensegreen6983/story-to-video-prompt.git `
  "$env:USERPROFILE\.agents\skills\story-to-video-prompt"
```

> 单个 `SKILL.md` 也能用：拷到 skills 目录即生效，`references/` 是可选的深度资料，`scripts/` 是可选的生成器。

### 方式二：手动拷

把仓库里的 `SKILL.md`、`references/`、`scripts/`、`examples/` 一起放进 `~/.agents/skills/story-to-video-prompt/`。

### 方式三：装打包版

`dist/story-to-video-prompt.skill` 是 zip 包，解压到 skills 目录同样可用（需要本仓库 Release 里取，或本地 `python scripts/build_prompt_pack.py` 生成后自打）。

---

## 用起来

装好后不用记命令，说人话就行：

> 帮我写视频提示词：深夜便利店，店员从监控里看见一个穿雨衣的人站了很久，走过去只剩一件还在滴水的雨衣。要超细，本地 H3 跑，5–8 秒一镜。

会说这几种话，它就知道该走哪条路：

- 「要电影级 / 更细 / 超真实 / 角色别换脸」→ 高密度版
- 「本地跑 / 5–10 秒一镜 / H3」→ 高密度版 + 本地参数
- 「Veo / Sora / 可灵 / 海螺」→ 对应模型的散文版
- 「给我文件」→ 落一个 `prompt-pack.md`
- 「S03 改成手持跟拍」→ 只改那一镜

---

## 两种密度

| 密度 | 用于 | 单镜长度 | 结构 |
|---|---|---|---|
| 散文版 | Veo 3 / Sora 2 / Kling / Seedance / Hailuo / Runway / Wan | 200–450 字 | 一段话，槽位顺序固定 |
| 高密度版 | 本地 MiniMax H3、自部署长上下文模型 | 800–1400 字 | 十二区块 + 逐拍时间码 |

高密度版的区块顺序：

```text
身份锁 → 服装与随身物 → 表演（时间码）→ 环境 → 物理
→ 光线 → 机位与焦段 → 材质微观 → 画质与风格 → 成像规格
→ 声音 → 连续性 → 负面词
```

---

## 脚本：分镜 JSON → 整套提示词

`scripts/build_prompt_pack.py`，纯标准库，Python 3.8+。

```bash
# 高密度版（本地 H3）
python scripts/build_prompt_pack.py examples/h3-storyboard-zh.json --model h3 --out pack.md

# 一次出多种模型格式
python scripts/build_prompt_pack.py examples/storyboard.json --model veo3,kling --out pack.md

# 只体检，不生成
python scripts/build_prompt_pack.py examples/h3-storyboard-zh.json --check
```

| 参数 | 说明 |
|---|---|
| `--model` | `veo3` `sora2` `kling` `seedance` `hailuo` `runway` `generic` `minimax`（`h3` 是 `minimax` 的别名），可逗号多选 |
| `--out` | 输出文件；省略则打到 stdout |
| `--lang` | `zh`（默认）/ `en` / `both` |
| `--check` | 只跑质量扫描：有 ERROR 退出码 1，WARN 不影响退出码 |

`--check` 会查：时长是否越界、缺字段、一个动作塞太多拍、静态机位与运动描述冲突、对白过长、抽象词、占位符未解析、把固定串塞进动作导致病句、高密度版的微观细节数量与字数是否够。

分镜 JSON 只有 `shots` 必填，字段定义见脚本头部注释。

---

## 目录

```text
.
├── SKILL.md                         技能本体（0 语言 → 11 脚本用法）
├── references/
│   ├── cinematic-grammar.md         景别/运镜/焦段/光位/色彩/声音的词库
│   ├── story-to-beats.md            剧情拆成拍子的方法、类型套路
│   ├── prompt-templates.md          七家模型的提示词模板与成片级范例
│   ├── model-playbooks.md           逐家模型的脾气与参数
│   ├── hyperreal-detail.md          材质细节通道、光学替换表、反 AI 味词表
│   └── minimax-h3.md                本地 H3 适配卡：参数、一致性、崩坏定位
├── scripts/build_prompt_pack.py     分镜 JSON → 提示词包
└── examples/
    ├── h3-storyboard-zh.json        中文高密度样例（雨衣，4 镜 28s）
    ├── storyboard.json              散文版样例（暗房，4 镜 21s）
    └── sample-output.md             上面那个样例跑出来的完整产出
```

---

## 几条设计原则

1. **固定串只放主体和环境**。塞进动作里会立刻出病句（「……落在瓷砖上，站着面朝货架」）。
2. **一镜一个主动词**。「她推门进来，看见尸体，后退半步」是三个镜头。
3. **光只有一个来源**。写方向、写比值（`身后四档衰减`），不写「氛围感」。
4. **材质要有使用史**。不是「金属质感」，是「指纹和划痕把高光切碎了」。
5. **抽象词一律删**。电影感、史诗、绝美、8K、超精细，模型读不懂，只会让画面更平庸。
6. **密度看字数，不看形容词数量**。高密度版单镜不到 600 字，就是还没写完。

---

## 常见崩坏

| 症状 | 改法 |
|---|---|
| 每镜换脸 | 固定串逐字复制 + 首帧图走图生视频 |
| 手指畸变 | 改中景或过肩，手出画或握物 |
| 后半段动作漂 | 拆成 3–5 拍，每拍给起止时间 |
| 画面太干净 | 加材质使用史：灰、指纹、水痕、磨损 |
| 光很平 | 单一动机光 + 方向 + 四档衰减 |
| 一镜多出一个人 | 一镜一主体，配角写进「环境」段 |

完整诊断表见 `references/minimax-h3.md`。

---

## English

Turns a plot or a one-line scene into a production-ready video prompt pack: story spine, entity lock bible, shot list, per-shot prompts, single-pass prompt, negatives and parameters. Chinese output by default; two densities — prose for hosted models (Veo / Sora / Kling / Seedance / Hailuo / Runway) and a 12-block, timecoded, hyper-detailed format for local long-context models such as MiniMax H3.

```bash
git clone https://github.com/hortensegreen6983/story-to-video-prompt.git ~/.agents/skills/story-to-video-prompt
python scripts/build_prompt_pack.py examples/h3-storyboard-zh.json --model h3 --out pack.md
```

---

## License

MIT. 用、改、商用都行，保留版权声明即可。