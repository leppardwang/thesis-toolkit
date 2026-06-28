---
title: "thesis-formatter"
summary: "学位论文完整格式编排工具 — 多学校/多学科/详细标题序号/参考文献/插入方法"
---

# Thesis Formatter — 学位论文格式编排工具

## 适用场景
当用户需要对其学位论文（TeX或Word格式）进行格式编排时使用，包括标题层级、参考文献、字体对齐、插入方法。

---

## 一、标题序号体系（最易出错部分）

### 海南大学博士论文标准层级

| 层级 | LaTeX命令 | 编号样式 | 字体字号 | 对齐 | 说明 |
|------|-----------|---------|---------|------|------|
| 一级 | `\chapter{第X章}` | **第1章** | 黑体小三(15pt) | 居中 | 自动"第X章"格式 |
| 二级 | `\section{}` | **1.1** | 黑体四号(14pt) | 左对齐 | 章内序号 |
| 三级 | `\subsection{}` | **1.1.1** | 黑体小四(12pt) | 左对齐 | 节内序号 |
| 四级 | `\subsubsection{}` | **(1)** | 黑体小四(12pt) | 左对齐 | 左缩进2字符 |
| 五级 | 手动 | **①** | 宋体小四 | 左对齐 | 极少使用, 手动输入 |

### ctexbook关键配置（解决序号自动生成的痛点）

```latex
\ctexset{
    chapter = {
        name = {第,章},
        number = {\arabic{chapter}},
        format = {\zihao{-2}\heiti\centering},
        beforeskip = {20pt},
        afterskip = {30pt},
    },
    section = {
        format = {\zihao{4}\heiti},
        beforeskip = {12pt},
        afterskip = {6pt},
    },
    subsection = {
        format = {\zihao{-4}\heiti},
        beforeskip = {6pt},
        afterskip = {3pt},
    },
    subsubsection = {
        format = {\zihao{-4}\heiti},
        numbering = {\arabic{subsubsection}},
        beforeskip = {6pt},
        afterskip = {3pt},
    },
}
```

### 四级标题(1)的解决方法
ctexbook默认不支持中文括号的四级编号。需要手动：

```latex
% 方案A：ctexset手动设置
\ctexset{
    subsubsection = {
        name = {(,)},
        number = {\arabic{subsubsection}},
    }
}

% 方案B：手动编号（更可控）
\subsubsection*{(1) 具体内容}
```

### 章标题自动编号与手动调整
```latex
% 正常使用
\chapter{绪论}      % 输出"第1章 绪论"

% 如果不需要编号（如摘要、致谢）
\chapter*{摘  要}
\addcontentsline{toc}{chapter}{摘  要}
```

---

## 二、参考文献格式（GB/T 7714-2015）

### 期刊文章
```
[序号] 作者. 题名[J]. 刊名, 出版年, 卷号(期号): 起止页码.
```
示例：
```
[1] McMahan B, Moore E, Ramage D, et al. Communication-efficient learning of deep networks from decentralized data[C]. AISTATS, 2017.
[2] 李宁, 欧嵬. 面向智慧医疗的联邦学习数据共享方法[J]. 计算机学报, 2024, 47(3): 556-572.
```

### 学位论文
```
[序号] 作者. 题名[D]. 城市: 学校, 出版年.
```
示例：
```
[3] 李宁. 面向智慧医疗的数据共享关键技术研究[D]. 海口: 海南大学, 2024.
[4] 王伟嵩. 医院信息化外包风险评价研究[D]. 北京: 北京大学, 2021.
```

### 著作
```
[序号] 作者. 书名[M]. 版次. 出版地: 出版社, 出版年.
```

### 在线资源
```
[序号] 作者. 题名[EB/OL]. (发布日期)[引用日期]. URL.
```

### LaTeX实现（biblatex + biber方案）
```latex
\usepackage[backend=biber, style=gb7714-2015, sortcites]{biblatex}
\addbibresource{references.bib}
% 输出
\printbibliography[heading=bibintoc]
```

### biblatex-gb7714-2015.bib 条目示例
```bibtex
@article{McMahan2017fedavg,
  author  = {McMahan, Brendan and Moore, Eider and Ramage, Daniel and others},
  title   = {Communication-efficient learning of deep networks from decentralized data},
  journal = {AISTATS},
  year    = {2017},
  pages   = {1273--1282}
}

@phdthesis{Li2024smarthealth,
  author = {李宁},
  title  = {面向智慧医疗的数据共享关键技术研究},
  school = {海南大学},
  year   = {2024},
  address = {海口}
}
```

---

## 三、字体字号对齐规范

### 中文字号对照表

| 名称 | 磅值(pt) | LaTeX命令 | 用途 |
|------|---------|-----------|------|
| 小初 | 24 | `\zihao{1}` | 封面论文标题 |
| 一号 | 26 | `\zihao{0}` | 极少使用 |
| 小一 | 24 | `\zihao{1}` | 封面 |
| 二号 | 22 | `\zihao{2}` | 极少使用 |
| 小二 | 18 | `\zihao{-2}` | 章标题（黑体） |
| 三号 | 16 | `\zihao{3}` |   |
| 小三 | 15 | `\zihao{-3}` | 一级节标题 |
| 四号 | 14 | `\zihao{4}` | 二级节标题（黑体） |
| 小四 | 12 | `\zihao{-4}` | 正文（宋体） |
| 五号 | 10.5 | `\zihao{5}` | 参考文献、页眉 |

### 字体对齐要点
- **宋体(SimSun)**: 正文、参考文献。Windows系统自带，xelatex直接调用
- **黑体(SimHei)**: 各级标题。Windows系统自带
- **楷体(KaiTi)**: 引文、证明等。可选
- **Times New Roman**: 英文正文
- **Arial/Courier New**: 英文标题/代码

关键配置：
```latex
\setCJKmainfont{SimSun}    % 宋体（正文字体）
\setCJKsansfont{SimHei}    % 黑体（标题字体）
\setmainfont{Times New Roman}  % 英文字体
```

### Word中的行距控制
```python
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING

# 1.5倍行距
paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

# 固定值行距（如20磅）
paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
paragraph.paragraph_format.line_spacing = Pt(20)
```

---

## 四、内容风格规范

### 标题层级展开方法
```
第1章 → 1.1 → 1.1.1 → (1) → ①
         ↓
    每个层级用小标题展开论述
         ↓
    每个小标题下至少写3-5个自然段
         ↓
    每段至少3-5句话（100-200字）
```

### 段落写作检查清单
- ❌ **列表式**: "首先...其次...再次..." / "功能一...功能二..."
- ✅ **长段落**: 每段一个主题，3-8句话，连贯叙事
- ❌ **短段落**: 单段少于3句话
- ❌ **Markdown粗体**: `**内容**` → 应使用 `\textbf{内容}`

### 参考文献插入密度
- 每节至少5-8篇引用
- 每章总引用不少于15篇
- 全文总引用80-120篇

---

### 小标题规范（论文中实际使用的8种模式 — 2026-06-28补充）

海南大学博士论文（生物医学工程方向）在正文中大量使用独立成段的`\textbf{}`粗体作为小标题，替代四级/五级正式标题。以下是检测到的8种模式及LaTeX实现：

| 模式 | 示例 | 出现频次 | LaTeX实现 | 说明 |
|------|------|---------|-----------|------|
| **目标/贡献+X** | **目标一**、**贡献三** | 12次 | `\subsubsection*{(X) 标题}` | X用中文数字 |
| **发现+X** | **发现一**~**发现五** | 10次 | `\subsubsection*{发现X}` | 第3/5章结论 |
| **建议+X** | **建议一**~**建议三** | 6次 | `\subsubsection*{建议X}` | 第6章政策建议 |
| **步骤/阶段+X** | **步骤一**、**阶段二** | 16次 | `\subsubsection*{步骤X}` | 方法流程描述 |
| **验证点+X** | **验证点一**~**验证点四** | 4次 | `\subsubsection*{验证点X}` | 第5章实证 |
| **XX层面/方面** | **顶层立法层面** | 3次 | `\subsubsection*{XX层面}` | 分类论述 |
| **XX认知/特征** | **效率与统一管理的正面认知** | 10次 | `\subsubsection*{XX认知}` | 受访者观点 |
| **X.X.X.X四级编号** | **2.2.1.1 CIA Triad** | 14次 | `\paragraph{标题}` 或 `\textbf{标题}` | 第2章文献分类 |

**注意事项：**
- 上述小标题在Markdown源文件中使用`**粗体**`，转换为LaTeX后变为`\textbf{粗体}`，但在学术规范中应使用正式的标题命令
- 建议使用`\subsubsection*{}`（无编号子小节）替代`\textbf{}`粗体段落，以保持标题层级语义
- 编号格式：一级**第X章** → 二级**X.X** → 三级**X.X.X** → 四级**(X)** → 五级**①**（手工）
- 当前论文实际只用到三级（h3）标题，更深层级用`\textbf{}`小标题代替

---

## 五、插入方法

### 插图插入
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{figures/filename.png}
\caption{图标题}
\label{fig:label_name}
\end{figure}
```
在Word中对应：使用`tex2docx.py`脚本自动插入。

### 表格插入
```latex
\begin{table}[htbp]
\caption{表标题}
\label{tab:label_name}
\centering
\begin{tabular}{lccc}
\toprule
列1 & 列2 & 列3 & 列4 \\
\midrule
数据1 & 数据2 & 数据3 & 数据4 \\
\bottomrule
\end{tabular}
\end{table}
```

### 公式插入
```latex
\begin{equation}
\label{eq:label_name}
E = mc^2
\end{equation}
```
Word中需手动使用公式编辑器转换。

### 文献引用
```latex
\cite{McMahan2017fedavg}          % 单个文献
\cite{Li2020fedprox,Karimireddy2020scaffold}  % 多个文献并列
\textcite{McMahan2017fedavg}       % 自然语言引用: "McMahan等人(2017)提出..."
```

---

## 六、多学科分类适配

### 数据安全/计算机方向
- 英文术语使用频率高 → 正文需中英对照
- 算法伪代码用algorithm环境
- 实验数据用三线表

### 管理/文博方向
- 术语以中文为主
- 图表标题以中文优先
- 引用格式以中文文献为主

### 混编策略
```latex
% 首次出现英文术语时括号标注中文
联邦学习（Federated Learning, FL）
差分隐私（Differential Privacy, DP）

% 后续可直接使用英文缩写
FL、DP
```

---

## 七、参考论文库

| 学校 | 分类 | 作者 | 论文题目 | 页码 |
|------|------|------|---------|------|
| 海南大学 | 计算机/数据安全 | 李宁 | 面向智慧医疗的数据共享关键技术研究 | 69页 |
| 海南大学 | 计算机/监管 | 申朋旭 | 基于智能合约的医师电子执业证照监管模型研究 | 81页 |
| 北京大学 | 公共卫生/管理 | 王伟嵩 | 医院信息化外包风险评价研究 | 132页 |

## 八、机器验证体系（三格式统一校验）

目标：无论最终输出 TeX / Word / PDF，格式保持一致，减少人工核对。

### 8.1 格式合规验证（format 模式）
```bash
python validate_thesis.py format thesis_main.tex
```
自动检测：
- ✅ 页面边距：上下2.5cm, 左3cm右2.5cm
- ✅ 字体配置：SimSun(正文) / SimHei(标题) / Times New Roman(英文)
- ✅ 宏包完整性：geometry / fontspec / xeCJK / fancyhdr 等8项
- ✅ 文档结构：\frontmatter → \mainmatter → \backmatter
- ✅ 页眉页脚：\fancyhead / \fancyfoot / \thepage
- ✅ 参考文献：biblatex + gb7714-2015
- ✅ 附录与致谢

### 8.2 写作质量验证（style 模式）
```bash
python validate_thesis.py style chapter4.tex
```
自动检测：
- ✅ 机械化写作：首先/其次/列表式模式
- ✅ 过短段落：<3句话标记
- ✅ 引用密度：每节<3篇标记，全文<30篇警告
- ✅ 残留Markdown：`**粗体**` 未转为 `\textbf{}`

### 8.3 格式稳定性保障机制
```python
# 每次修改后自动运行：
# 1. format检测 → 模板配置不变
# 2. style检测 → 写作质量不退化
# 3. git diff → 确认改动范围
```

### 8.4 跨格式一致性保障
| 格式 | 源文件 | 校验方法 | 自动修复 |
|------|--------|---------|---------|
| TeX | .tex | validate_thesis.py format/style | fix_tex_bold.py |
| Word | .docx | tex2docx.py 生成 | 重新生成 |
| PDF | .pdf | xelatex 编译（需MiKTeX） | 重新编译 |

**核心原则**：所有修改在 TeX 源文件上进行，Word 和 PDF 均由 TeX 生成，避免三格式各自维护的不一致。

---

## 九、图文混排规范（TeX核心优势）

### 9.1 浮动体位置参数（`[htbp]`）

LaTeX 通过浮动体环境（`figure`/`table`）自动排版图表，位置参数控制排版优先级：

| 参数 | 含义 | 说明 |
|------|------|------|
| `h` | here（此处） | 尽量放在代码所在位置 |
| `t` | top（页顶） | 放在页面顶部 |
| `b` | bottom（页底） | 放在页面底部 |
| `p` | page（独立页） | 放在专门用于浮动体的页面 |
| `H` | 强制此处 | 需`\usepackage{float}`宏包，强制固定位置（慎用，易导致空白页） |

**推荐配置**：
```latex
% 全局设置：允许浮动体放在页面底部（默认不允许）
\setcounter{bottomnumber}{2}  % 页底最多2个浮动体
\renewcommand{\topfraction}{0.85}  % 页顶最多占用85%版面
\renewcommand{\bottomfraction}{0.70}  % 页底最多占用70%版面
\renewcommand{\textfraction}{0.15}  % 页面至少保留15%正文

% 单图设置：优先此处→页顶→页底→独立页
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{figures/ch3_comparison.png}
\caption{集中式与分布式部署模式安全特性对比}
\label{fig:ch3_deployment_comparison}
\end{figure}
```

### 9.2 图题/表题格式规范

**图题**（Figure Caption）：
- 位置：**图下方**
- 格式：`图3-1 集中式与分布式部署模式安全特性对比`（章号-序号）
- 字体：宋体10.5pt（五号），居中
- 实现：
```latex
\captionsetup[figure]{
    name={图},
    labelsep=space,  % "图3-1 标题"（空格分隔）
    font={small},  % 10.5pt
    justification=centering
}
```

**表题**（Table Caption）：
- 位置：**表上方**
- 格式：`表4-2 ES-CRIF框架风险评估维度`（章号-序号）
- 字体：黑体10.5pt（五号），居中
- 实现：
```latex
\captionsetup[table]{
    name={表},
    labelsep=space,
    font={small, bf},  % 黑体加粗
    justification=centering,
    position=above  % 表题在表上方
}
```

### 9.3 交叉引用自动化

**问题**：手动编号（如"见图3-1"）会导致图表增删时编号错乱。

**解决**：`cleveref`宏包自动处理交叉引用格式：
```latex
\usepackage[capitalise]{cleveref}  % 自动大写"图"/"表"

% 文中引用
如图\cref{fig:ch3_deployment_comparison}所示，集中式部署...
% 输出："如图3-1所示，集中式部署..."

如表\cref{tab:ch4_risk_dimensions}所示，ES-CRIF框架...
% 输出："如表4-2所示，ES-CRIF框架..."

% 多个引用
\cref{fig:ch3_a,fig:ch3_b,fig:ch3_c}
% 输出："图3-1, 3-2和3-3"
```

**注意**：
- `\label`必须放在`\caption`**之后**（否则引用编号错误）
- 正确：`\caption{...} \label{...}`
- 错误：`\label{...} \caption{...}`

### 9.4 图表目录自动生成

博士论文要求图表目录独立成页：

```latex
% 在正文开始前（\mainmatter之后）
\listoffigures  % 生成图目录
\addcontentsline{toc}{chapter}{图目录}  % 加入总目录

\listoftables   % 生成表目录
\addcontentsline{toc}{chapter}{表目录}  % 加入总目录

\cleardoublepage  % 确保下一项从奇数页开始
```

**图表目录格式调整**（如需要）：
```latex
\usepackage{tocloft}
\renewcommand{\listfigurename}{图目录}
\renewcommand{\listtablename}{表目录}
\setlength{\cftfignumwidth}{2.5em}  % 图编号栏宽度
\setlength{\cfttabnumwidth}{2.5em}  % 表编号栏宽度
```

### 9.5 通栏图/双栏图处理

如果论文模板是**双栏排版**（`\documentclass[twocolumn]{article}`），跨栏图需特殊处理：

```latex
% 双栏模板中的通栏图（跨两栏）
\begin{figure*}[htbp]
\centering
\includegraphics[width=\textwidth]{figures/ch5_results.png}
\caption{联邦学习实验完整结果（通栏）}
\label{fig:ch5_full_results}
\end{figure*}

% 注意：
% 1. figure*环境只能放在页面顶部（t）或独立页（p），不能用[h]或[b]
% 2. 通栏图不会出现在当前页，会在下一页顶部出现
```

### 9.6 图片格式与分辨率要求

**海南大学博士论文提交规范**（参考同类高校）：

| 项目 | 要求 |
|------|------|
| 格式 | PNG（矢量图用PDF/EPS） |
| 分辨率 | ≥300dpi（打印清晰） |
| 色彩模式 | RGB（屏幕阅读）/ CMYK（印刷） |
| 文件大小 | 单图≤2MB（PDF总大小限制） |
| 推荐使用 | `matplotlib`保存为`dpi=300`的PNG |

**Python生成论文用图**：
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, linewidth=2)
ax.set_xlabel('Epoch', fontsize=12)
ax.set_ylabel('Accuracy', fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('figures/ch5_fl_accuracy.png', dpi=300, bbox_inches='tight')
plt.close()
```

### 9.7 Word导出的图文混排对应方法

使用`python-docx`转换时，需手动处理图片（Markdown的`![](path)`无法直接转Word图片）：

**方案A：转换后手动插入**（适合图片少的情况）

**方案B：改进转换脚本**，自动识别Markdown图片语法并插入：
```python
# 在md_to_word_v2.py中添加图片处理
import re
from docx.shared import Inches

# 识别Markdown图片语法：![alt](path)
img_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'

for para in doc.paragraphs:
    matches = re.findall(img_pattern, para.text)
    for alt_text, img_path in matches:
        if os.path.exists(img_path):
            # 在段落前插入图片
            run = para.insert_paragraph_before().add_run()
            run.add_picture(img_path, width=Inches(5.0))
            
            # 添加题注（需要手动指定图号）
            caption = para.insert_paragraph_before()
            caption.add_run(f'图X-Y {alt_text}').bold = True
            caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

**方案C：直接使用LaTeX→Word转换工具**（推荐）
- `pandoc`：支持LaTeX→Word转换，保留图片和基本格式
- `tex4ht`：LaTeX→HTML→Word，转换质量更高
- 优点：直接在TeX源文件上操作，图片位置由TeX控制，转换后格式更接近原版

### 9.8 常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 图片跑到章节末尾 | 浮动体位置参数太严格 | 改用`[htbp]`，或调整`\textfraction` |
| 图表编号错误（如"图3-2"变成"图4-1"） | `\label`放在`\caption`之前 | 确保`\label`在`\caption`之后 |
| 双栏模板中通栏图不显示 | `figure*`只能放在页顶 | 调整代码位置，或改用`\usepackage{stfloats}`允许页底 |
| 图片分辨率低（打印模糊） | 保存时dpi不足 | `plt.savefig(dpi=300)` |
| Word中图片丢失 | 转换脚本未处理图片 | 用pandoc转换，或手动插入 |

---

**核心优势总结**：
- ✅ **TeX**：浮动体自动排版 + 交叉引用自动更新 + 图表目录自动生成
- ❌ **纯文本/Markdown**：图片位置固定 + 手动编号 + 无法自动生成图表目录
- ⚠️ **Word**：可以图文混排，但需手动调整图片位置 + 手动编号（或用题注功能）
