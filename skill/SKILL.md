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
