#!/usr/bin/env python3
"""
学位论文模板生成器 — 多学校/多学位/多专业自由切换
用法:
  python format_thesis.py --school hainanu --degree phd --major 生物医学工程
  python format_thesis.py --school pku --degree master --major 社会医学与卫生事业管理
"""

import os, re, sys, argparse
from datetime import datetime

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# ===== 模板库 =====
TEMPLATES = {
    "hainanu": {
        "name": "海南大学",
        "code": "10589",
        "city": "海口",
        "degrees": {
            "phd": {
                "name": "博士学位论文",
                "title_page": "海南大学博士学位论文",
                "header": "海南大学博士学位论文",
                "font_cn": "SimSun",
                "font_heading": "SimHei",
                "font_en": "Times New Roman",
                "body_size": "12pt",
                "heading1_size": "15pt",
                "heading2_size": "14pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm",
                "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "生物医学工程": {"eng": "Biomedical Engineering", "code": "0831"},
                    "计算机科学与技术": {"eng": "Computer Science", "code": "0812"},
                    "软件工程": {"eng": "Software Engineering", "code": "0835"},
                }
            },
            "master": {
                "name": "硕士学位论文",
                "title_page": "海南大学硕士学位论文",
                "header": "海南大学硕士学位论文",
                "font_cn": "SimSun",
                "font_heading": "SimHei",
                "font_en": "Times New Roman",
                "body_size": "12pt",
                "heading1_size": "14pt",
                "heading2_size": "12pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm",
                "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "软件工程": {"eng": "Software Engineering", "code": "0835"},
                    "计算机技术": {"eng": "Computer Technology", "code": "0854"},
                    "工商管理硕士（MBA）": {"eng": "MBA", "code": "125101"},
                }
            }
        }
    },
    "pku": {
        "name": "北京大学",
        "code": "10001",
        "degrees": {
            "master": {
                "name": "硕士研究生学位论文",
                "title_page": "北京大学硕士研究生学位论文",
                "header": "北京大学硕士学位论文",
                "font_cn": "SimSun",
                "font_heading": "SimHei",
                "font_en": "Times New Roman",
                "body_size": "12pt",
                "heading1_size": "14pt",
                "heading2_size": "12pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm",
                "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "社会医学与卫生事业管理": {"eng": "Social Medicine and Health Management", "code": "120402"},
                    "公共卫生": {"eng": "Public Health", "code": "100400"},
                }
            }
        }
    },
    "tsinghua": {
        "name": "清华大学",
        "code": "10003",
        "city": "北京",
        "degrees": {
            "phd": {
                "name": "博士学位论文", "title_page": "清华大学博士学位论文",
                "header": "清华大学博士学位论文",
                "font_cn": "SimSun", "font_heading": "SimHei", "font_en": "Times New Roman",
                "body_size": "12pt", "heading1_size": "15pt", "heading2_size": "14pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm", "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "计算机科学与技术": {"eng": "Computer Science", "code": "0812"},
                    "软件工程": {"eng": "Software Engineering", "code": "0835"},
                }
            },
            "master": {
                "name": "硕士学位论文", "title_page": "清华大学硕士学位论文",
                "header": "清华大学硕士学位论文",
                "font_cn": "SimSun", "font_heading": "SimHei", "font_en": "Times New Roman",
                "body_size": "12pt", "heading1_size": "14pt", "heading2_size": "12pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm", "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "计算机技术": {"eng": "Computer Technology", "code": "0854"},
                }
            }
        }
    },
    "zju": {
        "name": "浙江大学",
        "code": "10335",
        "city": "杭州",
        "degrees": {
            "phd": {
                "name": "博士学位论文", "title_page": "浙江大学博士学位论文",
                "header": "浙江大学博士学位论文",
                "font_cn": "SimSun", "font_heading": "SimHei", "font_en": "Times New Roman",
                "body_size": "12pt", "heading1_size": "15pt", "heading2_size": "14pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm", "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "计算机科学与技术": {"eng": "Computer Science", "code": "0812"},
                }
            }
        }
    },
    "sjtu": {
        "name": "上海交通大学",
        "code": "10248",
        "city": "上海",
        "degrees": {
            "phd": {
                "name": "博士学位论文", "title_page": "上海交通大学博士学位论文",
                "header": "上海交通大学博士学位论文",
                "font_cn": "SimSun", "font_heading": "SimHei", "font_en": "Times New Roman",
                "body_size": "12pt", "heading1_size": "15pt", "heading2_size": "14pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm", "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "计算机科学与技术": {"eng": "Computer Science", "code": "0812"},
                    "生物医学工程": {"eng": "Biomedical Engineering", "code": "0831"},
                }
            }
        }
    },
    "whu": {
        "name": "武汉大学",
        "code": "10486",
        "city": "武汉",
        "degrees": {
            "phd": {
                "name": "博士学位论文", "title_page": "武汉大学博士学位论文",
                "header": "武汉大学博士学位论文",
                "font_cn": "SimSun", "font_heading": "SimHei", "font_en": "Times New Roman",
                "body_size": "12pt", "heading1_size": "15pt", "heading2_size": "14pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm", "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "计算机科学与技术": {"eng": "Computer Science", "code": "0812"},
                }
            }
        }
    },
    "hust": {
        "name": "华中科技大学",
        "code": "10487",
        "city": "武汉",
        "degrees": {
            "phd": {
                "name": "博士学位论文", "title_page": "华中科技大学博士学位论文",
                "header": "华中科技大学博士学位论文",
                "font_cn": "SimSun", "font_heading": "SimHei", "font_en": "Times New Roman",
                "body_size": "12pt", "heading1_size": "15pt", "heading2_size": "14pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm", "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "计算机科学与技术": {"eng": "Computer Science", "code": "0812"},
                }
            }
        }
    },
    "sysu": {
        "name": "中山大学",
        "code": "10558",
        "city": "广州",
        "degrees": {
            "phd": {
                "name": "博士学位论文", "title_page": "中山大学博士学位论文",
                "header": "中山大学博士学位论文",
                "font_cn": "SimSun", "font_heading": "SimHei", "font_en": "Times New Roman",
                "body_size": "12pt", "heading1_size": "15pt", "heading2_size": "14pt",
                "line_spacing": "onehalfspacing",
                "margin_top": "2.5cm", "margin_bottom": "2.5cm", "margin_left": "3cm", "margin_right": "2.5cm",
                "ref_style": "gb7714-2015",
                "majors": {
                    "计算机科学与技术": {"eng": "Computer Science", "code": "0812"},
                    "生物医学工程": {"eng": "Biomedical Engineering", "code": "0831"},
                }
            }
        }
    },
}


def generate_preamble(school, degree, major):
    """生成LaTeX导言区"""
    cfg = TEMPLATES[school]["degrees"][degree]
    major_info = cfg["majors"].get(major, {"eng": major, "code": "0000"})

    return rf"""% {TEMPLATES[school]['name']}{cfg['name']} — {major}
% 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
% 使用 xelatex 编译

\documentclass[12pt, a4paper, oneside, openany]{{ctexbook}}

% 页面设置
\usepackage[a4paper,
    top={cfg['margin_top']}, bottom={cfg['margin_bottom']},
    left={cfg['margin_left']}, right={cfg['margin_right']},
    headheight=1.5cm, footskip=1.5cm,
    includehead, includefoot]{{geometry}}

% 英文字体
\usepackage{{fontspec}}
\setmainfont{{{cfg['font_en']}}}
\setsansfont{{Arial}}
\setmonofont{{Courier New}}

% 中文字体
\setCJKmainfont{{{cfg['font_cn']}}}      % 正文
\setCJKsansfont{{{cfg['font_heading']}}}  % 标题
\setCJKmonofont{{FangSong}}

% 中文版式
\ctexset{{
    chapter = {{
        format = {{\zihao{{-2}}\heiti\centering}},
        name = {{第,章}},
        number = {{\arabic{{chapter}}}},
        beforeskip = {{20pt}},
        afterskip = {{30pt}},
    }},
    section = {{
        format = {{\zihao{{4}}\heiti}},
        beforeskip = {{12pt}},
        afterskip = {{6pt}},
    }},
    subsection = {{
        format = {{\zihao{{-4}}\heiti}},
        beforeskip = {{6pt}},
        afterskip = {{3pt}},
    }},
    subsubsection = {{
        format = {{\zihao{{-4}}\heiti}},
        numbering = {{\arabic{{subsubsection}}}},
        beforeskip = {{6pt}},
        afterskip = {{3pt}},
    }},
}}

% 行距
\usepackage{{setspace}}
\onehalfspacing

% 数学
\usepackage{{amsmath, amssymb, amsthm}}

% 图表
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage[font=small, labelfont=bf]{{caption}}
\graphicspath{{{{figures/}}}}

% 参考文献
\usepackage[backend=biber, style={cfg['ref_style']}, sortcites]{{biblatex}}
\addbibresource{{references/references.bib}}

% 超链接
\usepackage[hidelinks]{{hyperref}}

% 页眉页脚
\usepackage{{fancyhdr}}
\pagestyle{{fancy}}
\fancyhf{{}}
\fancyhead[C]{{\heiti\zihao{{5}}{cfg['header']}}}
\fancyfoot[C]{{\thepage}}
\renewcommand{{\headrulewidth}}{{0.4pt}}

% 字号命令
\newcommand{{\zihao}}[1]{{
    \ifcase#1\or\fontsize{{26pt}}{{32pt}}\selectfont
    \or\fontsize{{24pt}}{{30pt}}\selectfont
    \or\fontsize{{16pt}}{{24pt}}\selectfont
    \or\fontsize{{14pt}}{{22pt}}\selectfont
    \or\fontsize{{12pt}}{{18pt}}\selectfont
    \or\fontsize{{10pt}}{{15pt}}\selectfont\fi}}
\newcommand{{\heiti}}{{\CJKfamily{{{cfg['font_heading']}}}}}
\newcommand{{\songti}}{{\CJKfamily{{{cfg['font_cn']}}}}}

\begin{{document}}

\frontmatter
% 封面（需补充学校模板）
\include{{chapters/abstract}}

% 目录
\tableofcontents

\mainmatter
"""


def generate_title_page(school, degree, major, title, author, advisor):
    """生成封面页"""
    cfg = TEMPLATES[school]["degrees"][degree]
    school_name = TEMPLATES[school]["name"]
    return rf"""
\begin{{titlepage}}
\centering
\vspace*{{2cm}}
{{\zihao{{0}}\heiti {cfg['title_page']}}}\\[2cm]
{{\zihao{{2}}\songti {school_name}}}\\[0.5cm]
{{\zihao{{3}}\textbf{{{title}}}}}\\[3cm]
\begin{{flushleft}}
\zihao{{4}}
\setlength{{\tabcolsep}}{{8pt}}
\begin{{tabular}}{{ll}}
  作者姓名： & {author} \\
  学    号： & {TEMPLATES[school]['code']}00001 \\
  学    院： &  \\
  专    业： & {major} \\
  指导教师： & {advisor} \\
  完成日期： & {datetime.now().strftime('%Y年%m月')} \\
\end{{tabular}}
\end{{flushleft}}
\end{{titlepage}}
"""


def generate_end():
    return r"""
\backmatter
\printbibliography[heading=bibintoc]
\begin{appendix}
\include{appendices/appendix_a}
\end{appendix}
\include{acknowledgements}
\end{document}
"""


def main():
    parser = argparse.ArgumentParser(description='学位论文模板生成器')
    parser.add_argument('--school', default='hainanu', choices=list(TEMPLATES.keys()))
    parser.add_argument('--degree', default='phd', help='phd/master')
    parser.add_argument('--major', default='生物医学工程')
    parser.add_argument('--title', default='论文标题')
    parser.add_argument('--author', default='作者姓名')
    parser.add_argument('--advisor', default='导师姓名')
    parser.add_argument('--output', default='thesis_generated.tex')
    args = parser.parse_args()

    # 验证参数
    if args.school not in TEMPLATES:
        print(f"❌ 未知学校: {args.school}，可选: {list(TEMPLATES.keys())}")
        return
    if args.degree not in TEMPLATES[args.school]["degrees"]:
        print(f"❌ {TEMPLATES[args.school]['name']}不支持{args.degree}学位")
        return
    depts = TEMPLATES[args.school]["degrees"][args.degree]["majors"]
    if args.major not in depts:
        print(f"⚠️ 专业'{args.major}'不在预设列表中，将使用默认配置")
        print(f"   预设专业: {list(depts.keys())}")

    # 生成
    content = generate_preamble(args.school, args.degree, args.major)
    content += "\n% === 正文请插入各章节 ===\n"
    content += generate_end()

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(content)

    degree_name = TEMPLATES[args.school]["degrees"][args.degree]["name"]
    print(f'\n✅ 模板生成完成!')
    print(f'   学校: {TEMPLATES[args.school]["name"]}')
    print(f'   学位: {degree_name}')
    print(f'   专业: {args.major}')
    print(f'   文件: {os.path.abspath(args.output)}')
    print(f'\n   编译命令:')
    print(f'   xelatex {args.output} && biber {args.output.replace(".tex","")} && xelatex {args.output} && xelatex {args.output}')


if __name__ == '__main__':
    main()
