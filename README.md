# Thesis-Toolkit — 博士论文自动化工具链

> 适用项目：海南大学·生物医学工程·医疗数据安全合规方向
> 最后更新：2026-06-29
> 跨设备兼容：所有脚本使用相对路径/命令行参数，拷贝到任意目录即可运行

---

## 快速开始（给AI Agent / 新用户的入口指令）

以下指令假设你（AI Agent 或用户）在当前目录下，章节.md文件在 `chapters/` 子目录中：

```bash
# 1. 查看目录结构
ls -la

# 2. Markdown → LaTeX 转换（输入: chapters/ 输出: chapters_tex/）
python toolchain/md2tex.py chapters chapters_tex

# 3. 修复残留Markdown粗体
python toolchain/fix_md_bold.py chapters_tex

# 4. 检测写作质量（所有章节）
python toolchain/validate_thesis.py style all

# 5. 编译PDF
xelatex --enable-installer thesis_main.tex

# 6. 检测编译后的Overfull问题
python toolchain/validate_thesis.py fix
```

> 所有脚本均可在目录内通过相对路径调用。拷贝文件夹到新设备后无需修改任何路径。

---

## 目录结构

```
Thesis-Toolkit/
├── README.md              ← 本文件（使用说明）
├── toolchain/             ← 核心工具链脚本
│   ├── md2tex.py          #  Markdown → LaTeX 转换
│   ├── md_to_word_v2.py   #  Markdown → Word 转换
│   ├── validate_thesis.py #  论文质量三合一检测（format + style + fix）
│   ├── fix_md_bold.py     #  修复残留Markdown粗体 **xxx** → \textbf{xxx}
│   ├── fix_tex_bold.py    #  TeX粗体修复辅助
│   ├── format_thesis.py   #  论文格式化辅助
│   ├── generate_figures.py#  论文图表（matplotlib）生成
│   └── emr_crif_v2_model.py # 行为合规性评估模型 v2.0
└── skills/
    └── thesis-formatter/  #  WorkBuddy Skill：论文格式编排规范
        └── SKILL.md
```

---

## 一、工作流程（建议执行顺序）

```
[1] 写稿阶段               →  章节文件（.md）
[2] md2tex.py              →  .tex 文件
[3] fix_md_bold.py         →  清除残留Markdown
[4] validate_thesis.py     →  检测报告
[5] 手动修复（根据报告）    →  调表格、补引用
[6] xelatex 编译            →  PDF
```

---

## 二、工具说明

### 1. md2tex.py — Markdown → LaTeX 转换 ⭐核心工具

```
用途: 将博士论文章节Markdown文件转为LaTeX格式
用法: python toolchain/md2tex.py [输入目录] [输出目录]
示例: python toolchain/md2tex.py chapters chapters_tex
输入: chapters/01-第一章_绪论.md 等6章
输出: chapters_tex/chapter_01.tex 等

转换规则:
  # 第一章 绪论        → \chapter{绪论}          （一级标题）
  ## 1.1 研究背景      → \section{研究背景}      （二级标题）
  ### 1.1.1 内容       → \subsection{内容}       （三级标题）
  **粗体**             → \textbf{粗体}            （加粗）
  *斜体*               → \textit{斜体}            （斜体）
  > 引用              → \begin{quote}...\end{quote}
  |表格|              → \begin{table}...\end{table}（tabular）

已验证: 175个标题全部正确映射（6章）
依赖: Python 3，无第三方包
```

### 2. fix_md_bold.py — 残留Markdown修复 ⭐零人工

```
用途: 将转换后残留的 **xxx** 全部替换为 \textbf{xxx}
用法: python toolchain/fix_md_bold.py [tex目录]
示例: python toolchain/fix_md_bold.py chapters_tex
效果: 修复18处，成功率100%
依赖: Python 3
```

### 3. validate_thesis.py — 论文质量三合一检测

```
用途: 自动化论文质量检测，三种模式：

python validate_thesis.py format thesis_main.tex
  → 格式合规检测（27项）
    - 页面边距（上下2.5cm/左3cm/右2.5cm）
    - 字体配置（SimSun/SimHei/Times New Roman）
    - 宏包完整性（geometry/fontspec/xeCJK/fancyhdr等10项）
    - 文档结构（\frontmatter → \mainmatter → \backmatter）
    - 页眉页脚（fancyhead/fancyfoot/页码/页眉线）
    - 行距（1.5倍）

python validate_thesis.py style chapter_XX.tex
  → 写作质量检测
    - 机械化写作（首先/其次/列表式）
    - 过短段落（<3句话）
    - 引用密度（每节<3篇标记）
    - 残留Markdown（**粗体**）
    - 小标题统计

python validate_thesis.py fix
  → 自动修复Overfull hbox（表格加{\small}缩小）

依赖: Python 3
效果: 初始33处Overfull → 修复后15处
```

### 4. md_to_word_v2.py — Markdown → Word

```
用途: 将章节Markdown合并导出为Word文档
输入: 6章.md文件
输出: 博士论文_完整版.docx
功能: 标题映射/表格/引用块/加粗斜体
依赖: python-docx（pip install python-docx）
```

### 5. generate_figures.py — 论文图表生成

```
用途: 生成论文用5张核心图表
输出: figures/fig1~fig5（PNG，300dpi）
图表: 收敛曲线/算法对比/集中式vs联邦/隐私-效用权衡/Non-IID影响
依赖: matplotlib, numpy
```

### 6. emr_crif_v2_model.py — 行为合规性评估模型

```
用途: 电子病历数据使用行为合规性评估
评估对象: 人使用数据的行为（主体/权限/场景/操作）
法律依据: PIPL/DSL/CSL/伦理审查办法/GB/T 35273
风险等级: 合规→基本合规→不合规→严重违法
依赖: Python 3，无第三方包
```

---

## 三、环境依赖

### TeX编译环境（MiKTeX）
```
安装: winget install MiKTeX.MiKTeX
编译命令: xelatex --enable-installer thesis_main.tex
必要宏包:
  - ctexbook（中文文档类）
  - fontspec（字体）
  - geometry（页面设置）
  - fancyhdr（页眉页脚）
  - hyperref（超链接）
  - graphicx / booktabs / caption（图表）
  - amsmath / amssymb / amsthm（数学）
  - setspace（行距）
```

### Python依赖
```
Python ≥ 3.8
可选: python-docx（Word导出用）
可选: matplotlib + numpy（图表生成用）
```

---

## 四、Skill：thesis-formatter

```
位置: skills/thesis-formatter/SKILL.md
用途: 学位论文格式编排规范参考（WorkBuddy Skill）
覆盖内容:
  - 标题序号体系（h1-h5 + ctexbook配置）
  - 参考文献格式（GB/T 7714-2015 + biblatex）
  - 字体字号对齐规范
  - 内容风格规范（段落/引用/小标题）
  - 图文混排规范（浮动体/图题表题/交叉引用/图表目录）
  - 小标题规范（8种模式：目标/贡献/发现/建议/步骤/验证点/层面/四级编号）
  - 机器验证体系（format + style + fix）
```

---

## 五、效果数据

| 指标 | 初始 | 处理后 | 改善 |
|------|------|--------|------|
| Overfull hbox | 33处 | 15处 | ↓55% |
| Markdown残留 | 18处 | 0处 | ↓100% |
| PDF页数 | 91页 | 83页 | ↓9% |
| 格式检测覆盖 | — | 27项全通过 | — |
| 自动修复成功率 | — | 100% | — |

**综合评价：** 自动工具覆盖约80%格式问题，节省约90%验证时间。剩余20%（宽表格排版）需人工微调。

---

## 六、博士论文产出体系

```
论文6章结构:
  第1章 绪论（h2:9 + h3:10）
  第2章 理论基础与文献综述（h2:7 + h3:17）
  第3章 部署模式安全特性分析（h2:7 + h3:17）←深改版
  第4章 DS-CRIF风险识别框架（h2:9 + h3:26）
  第5章 系统实证验证与案例分析（h2:10 + h3:21）
  第6章 结论与展望（h2:11 + h3:25）
总标题数: 175个（h1:6 + h2:53 + h3:116）
总页数: 83页PDF

配套产出:
  - 联邦学习实验（19轮自动验证，准确率99.96%-99.98%）
  - EIAF审计体系（LSTM，延迟↓70%，带宽↓82.2%）
  - CVSS评估模型（ES-CRIF + DS-CRIF，ESDR 96.3%）
  - 文献计量学分析（投稿Annals of Medicine）
```