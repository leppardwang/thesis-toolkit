"""将博士论文章节 .md 转为 .tex"""
import re, os, sys

CHAPTERS = [
    ("01", "第一章_绪论"),
    ("02", "第二章_理论基础与文献综述"),
    ("03", "第三章_部署模式安全特性分析"),
    ("04", "第四章_DS-CRIF_风险识别框架"),
    ("05", "第五章_系统实证验证与案例分析"),
    ("06", "第六章_结论与展望"),
]

def md_to_tex(md_path, tex_path):
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    tex_lines = []
    in_code_block = False
    in_quote = False
    in_table = False
    table_buf = []

    for i, line in enumerate(lines):
        raw = line.rstrip("\n")

        # 代码块
        if raw.startswith("```"):
            if in_code_block:
                tex_lines.append("\\end{verbatim}\n")
                in_code_block = False
            else:
                tex_lines.append("\\begin{verbatim}\n")
                in_code_block = True
            continue
        if in_code_block:
            tex_lines.append(raw + "\n")
            continue

        # 空行
        if not raw.strip():
            if in_quote:
                tex_lines.append("\\end{quote}\n")
                in_quote = False
            tex_lines.append("\n")
            continue

        # 引用块
        if raw.startswith("> "):
            if not in_quote:
                tex_lines.append("\\begin{quote}\n")
                in_quote = True
            content = raw[2:]
            tex_lines.append(content + "\n")
            continue

        if in_quote:
            tex_lines.append("\\end{quote}\n")
            in_quote = False

        # 标题
        h_match = re.match(r'^(#{1,4})\s+(.+)$', raw)
        if h_match:
            level = len(h_match.group(1))
            title = h_match.group(2).strip()

            # 去掉章节编号前缀： "第一章 " → 去掉；"1.1 " → 去掉；"1.1.1 " → 去掉
            # 但保留标题文本
            clean_title = re.sub(r'^第[一二三四五六七八九十]+章\s+', '', title)
            clean_title = re.sub(r'^\d+(?:\.\d+)+\s+', '', clean_title)

            # 转义特殊字符
            clean_title = clean_title.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')

            if level == 1:
                tex_lines.append(f"\\chapter{{{clean_title}}}\n")
            elif level == 2:
                tex_lines.append(f"\\section{{{clean_title}}}\n")
            elif level == 3:
                tex_lines.append(f"\\subsection{{{clean_title}}}\n")
            elif level == 4:
                tex_lines.append(f"\\subsubsection{{{clean_title}}}\n")
            continue

        # 表格
        if raw.startswith("|"):
            table_buf.append(raw)
            in_table = True
            continue
        else:
            if in_table and table_buf:
                tex_lines.append(convert_table(table_buf))
                table_buf = []
                in_table = False

        # 分隔线
        if raw.strip() == "---":
            tex_lines.append("\n\\medskip\n\n")
            continue

        # 普通段落 — 内联格式转换
        para = raw
        # **加粗**
        para = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', para)
        # *斜体*
        para = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\textit{\1}', para)
        # `代码`
        para = re.sub(r'`([^`]+)`', r'\\texttt{\1}', para)
        # 转义
        para = para.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')
        # 恢复已转义
        para = para.replace('\\textit', '\\textit').replace('\\textbf', '\\textbf')
        para = para.replace('\\texttt', '\\texttt')
        # 修复过度转义
        # LaTeX命令中的下划线不应转义
        para = re.sub(r'\\textbackslash(\w+)', lambda m: '\\' + m.group(1), para)

        tex_lines.append(para + "\n\n")

    # 清理未关闭的引用
    if in_quote:
        tex_lines.append("\\end{quote}\n")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.writelines(tex_lines)

    print(f"  ✅ {tex_path}")

def convert_table(rows):
    """将Markdown表格转为LaTeX tabular"""
    if len(rows) < 2:
        return ""

    # 解析列数
    headers = [c.strip() for c in rows[0].strip("|").split("|")]
    n_cols = len(headers)
    col_spec = "l" * n_cols

    tex = "\\begin{table}[htbp]\n\\centering\n"
    tex += "\\begin{tabular}{" + col_spec + "}\n\\toprule\n"

    # 表头
    tex += " & ".join(escape_tex(h) for h in headers) + " \\\\\n\\midrule\n"

    # 数据行（跳过分隔行）
    for row in rows[2:]:
        if row.strip().startswith("|---"):
            continue
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) != n_cols:
            continue
        tex += " & ".join(escape_tex(c) for c in cells) + " \\\\\n"

    tex += "\\bottomrule\n\\end{tabular}\n\\end{table}\n\n"
    return tex

def escape_tex(s):
    s = s.replace('&', '\\&').replace('%', '\\%').replace('_', '\\_')
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s)
    return s

if __name__ == "__main__":
    base = "C:/Users/Administrator/WorkBuddy/Claw/chapters"
    out_base = "C:/Users/Administrator/WorkBuddy/Claw/chapters_tex"
    os.makedirs(out_base, exist_ok=True)

    for num, name in CHAPTERS:
        md_file = os.path.join(base, f"{num}-{name}.md".replace("_DS-CRIF_", "_DS-CRIF_"))
        # 修正文件名（第四章文件名含空格）
        if num == "04":
            md_file = os.path.join(base, "04-第四章_DS-CRIF 风险识别框架.md")
        if not os.path.exists(md_file):
            # 尝试其他变体
            for f in os.listdir(base):
                if f.startswith(num):
                    md_file = os.path.join(base, f)
                    break

        tex_file = os.path.join(out_base, f"chapter_{num}.tex")
        print(f"转换: {md_file}")
        md_to_tex(md_file, tex_file)

    print("全部转换完成！")
