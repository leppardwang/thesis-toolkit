# Thesis Toolkit — 学位论文格式编排工具链

一套面向中文学位论文的自动化工具链，支持多学校/多学位/多专业模板切换、TeX→Word转换、写作质量自动检测、论文级图表生成。

## 工具一览

| 工具 | 功能 | 用法 |
|------|------|------|
| `format_thesis.py` | 多模板LaTeX生成 | `--school hainanu --degree phd --major 生物医学工程` |
| `tex2docx.py` | TeX→Word（含图） | `python tex2docx.py <tex文件>` |
| `validate_thesis.py` | 写作质量检测 | `python validate_thesis.py <tex文件或目录>` |
| `generate_figures.py` | 论文级PNG图 | `python generate_figures.py` |
| `fix_tex_bold.py` | Markdown粗体修复 | `python fix_tex_bold.py <tex文件>` |

## 支持的模板

| 学校(代码) | 学位 | 专业 |
|-----------|------|------|
| 海南大学(10589) | 博士 | 生物医学工程、计算机科学与技术 |
| 海南大学(10589) | 硕士 | 软件工程、工商管理(MBA) |
| 北京大学(10001) | 硕士 | 社会医学与卫生事业管理、公共卫生 |
| 清华大学(10003) | 博士/硕士 | 计算机科学与技术 |
| 浙江大学(10335) | 博士 | 计算机科学与技术 |
| 上海交通大学(10248) | 博士 | 计算机科学与技术、生物医学工程 |
| 武汉大学(10486) | 博士 | 计算机科学与技术 |
| 华中科技大学(10487) | 博士 | 计算机科学与技术 |
| 中山大学(10558) | 博士 | 计算机科学与技术、生物医学工程 |

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 生成海南大学博士论文模板
python format_thesis.py \
  --school hainanu \
  --degree phd \
  --major "生物医学工程" \
  --title "论文标题" \
  --author "姓名" \
  --advisor "导师"

# 检测写作质量
python validate_thesis.py chapter4_experiments.tex

# TeX转Word
python tex2docx.py
```

## 检测项目

运行 `validate_thesis.py` 可自动检测：
- 机械化写作模式（首先/其次/列表式）
- 过短段落（<3句话）
- 残留Markdown粗体标记
- 章节引用密度不足
- 结构完整性问题

## 配套Skill（WorkBuddy用户）

`skill/SKILL.md` 可直接在WorkBuddy中加载使用。

## 参考论文

本工具格式标准来源于以下公开学位论文：
1. 李宁. 面向智慧医疗的数据共享关键技术研究[D]. 海南大学, 2024.
2. 申朋旭. 基于智能合约的医师电子执业证照监管模型研究[D]. 海南大学, 2024.
3. 王珑. DX公司政务云项目的管理优化研究[D]. 海南大学, 2024.
4. 王伟嵩. 医院信息化外包风险评价研究[D]. 北京大学, 2021.
