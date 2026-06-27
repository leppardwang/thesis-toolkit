#!/usr/bin/env python3
"""
学位论文格式自动检测工具 — 双模式：格式合规 + 写作质量

用法:
  # 格式合规检查（检查TeX模板配置）
  python validate_thesis.py format thesis_main.tex

  # 写作质量检查（检查内容风格）
  python validate_thesis.py style chapter4_experiments.tex

  # 全量检查
  python validate_thesis.py all chapters/

检查项:
  [格式]
  1. 页面设置 (geometry: 上下2.5cm, 左3cm右2.5cm)
  2. 字体配置 (SimSun/SimHei/Times New Roman)
  3. 页眉页脚 (fancyhdr配置)
  4. 章节编号 (chapter/section/subsection结构)
  5. 参考文献格式 (biblatex + gb7714-2015)
  6. 图表浮动参数 (htbp)
  7. 前文结构 (摘要/目录/符号表)
  8. 后文结构 (参考文献/附录/致谢)

  [写作]
  1. 机械化模式（首先/其次/列表式）
  2. 过短段落（<3句话）
  3. 残留Markdown粗体
  4. 引用密度不足
"""

import os, re, sys
from collections import defaultdict

# ===== 格式检查规则 =====
REQUIRED_GEOMETRY = {
    'top': '2.5cm', 'bottom': '2.5cm',
    'left': '3cm', 'right': '2.5cm'
}
REQUIRED_FONTS = ['SimSun', 'SimHei', 'Times New Roman']
REQUIRED_PACKAGES = [
    ('geometry', '页面设置'),
    ('fontspec', '英文字体'),
    ('xeCJK', '中文字体'),
    ('fancyhdr', '页眉页脚'),
    ('biblatex', '参考文献'),
    ('graphicx', '插图'),
    ('hyperref', '超链接'),
    ('setspace', '行距'),
]

def check_format(tex_path):
    """检查TeX模板格式合规性"""
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fname = os.path.basename(tex_path)
    issues = []
    
    # 1. 检查必要宏包（支持多行选项）
    content_flat = re.sub(r'\n\s*', ' ', content)  # 多行合并为一行
    for pkg, purpose in REQUIRED_PACKAGES:
        if pkg == 'xeCJK' and ('ctexbook' in content or 'ctexart' in content or 'ctexrep' in content):
            continue  # ctex文档类已内置xeCJK
        if not re.search(r'\\usepackage(\[.*?\])?\{' + pkg + r'\}', content_flat):
            issues.append(f'[格式] 缺少宏包 {pkg}（{purpose}）')
    
    # 2. 检查页面设置
    for key, val in REQUIRED_GEOMETRY.items():
        pattern = rf'{key}\s*=\s*{re.escape(val)}'
        if not re.search(pattern, content):
            found = re.search(rf'{key}\s*=\s*([^\s,}}]+)', content)
            found_val = found.group(1) if found else '未设置'
            issues.append(f'[格式] 页面 {key} 应为{val}，当前为 {found_val}')
    
    # 3. 检查字体
    for font in REQUIRED_FONTS:
        if font not in content:
            issues.append(f'[字体] 未配置 {font}')
    
    # 4. 检查页眉页脚
    if '\\pagestyle{fancy}' not in content:
        issues.append('[格式] 未启用 fancyhdr 页眉页脚')
    if '\\fancyhead' not in content:
        issues.append('[格式] 缺少页眉设置 (\\fancyhead)')
    if '\\fancyfoot' not in content and '\\thepage' not in content:
        issues.append('[格式] 缺少页码设置')
    
    # 5. 检查文档结构
    if '\\frontmatter' not in content:
        issues.append('[结构] 缺少 \\frontmatter')
    if '\\mainmatter' not in content:
        issues.append('[结构] 缺少 \\mainmatter')
    if '\\backmatter' not in content:
        issues.append('[结构] 缺少 \\backmatter')
    if '\\tableofcontents' not in content:
        issues.append('[结构] 缺少目录 \\tableofcontents')
    
    # 6. 检查参考文献
    if 'biblatex' in content and 'gb7714' not in content:
        issues.append('[引用] 建议使用gb7714-2015国标参考文献格式')
    if '\\printbibliography' not in content:
        issues.append('[引用] 缺少 \\printbibliography')
    
    # 7. 检查图表浮动参数
    bad_floats = re.findall(r'\\begin\{figure\}\[.*?[^htbp].*?\]', content)
    if bad_floats:
        issues.append(f'[图表] {len(bad_floats)}处浮动参数不含htbp')
    
    # 8. 检查附录和致谢
    if '\\begin{appendix}' not in content and '\\appendix' not in content:
        issues.append('[结构] 缺少附录')
    if 'acknowledgements' not in content and '致谢' not in content:
        issues.append('[结构] 缺少致谢')
    
    return fname, issues


# ===== 写作质量检查（原validate功能）=====
MECHANICAL_PATTERNS = [
    (r'首先.*?其次.*?再次', '三连列表式"首先…其次…再次"'),
    (r'一方面.*?另一方面', '对列式"一方面…另一方面"'),
    (r'第一，.*?第二，.*?第三，', '数字列表式"第一…第二…第三"'),
    (r'(需要|需满足).*?功能需求', '需求枚举式'),
]

def count_sentences(text):
    text = re.sub(r'\$[^$]+\$', '', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    sents = re.split(r'[。！？\n]', text)
    return len([s for s in sents if len(s.strip()) > 5])

def check_style(tex_path):
    """检查写作质量"""
    with open(tex_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    fname = os.path.basename(tex_path)
    issues = []
    
    # 跳过preamble（\\begin{document}之前的内容），只检查正文
    preamble_end = 0
    doc_match = re.search(r'\\begin\{document\}', raw)
    if doc_match:
        preamble_end = doc_match.end()
        content = raw[preamble_end:]  # 只检查正文
    else:
        content = raw  # 没有document环境，检查全文
    
    line_offset = raw[:preamble_end].count('\n') + 1 if preamble_end else 0
    raw_lines = raw.split('\n')
    
    # 机械化写作
    for i, line in enumerate(raw_lines, 1):
        if i <= line_offset:
            continue
        if line.strip().startswith('%'):
            continue
        for pattern, desc in MECHANICAL_PATTERNS:
            if re.search(pattern, line, re.DOTALL):
                ctx = line.strip()[:60]
                issues.append((i, f'[机械化] {desc}: "{ctx}..."'))
    
    # 过短段落（跳过表格/图表/算法）
    cleaned = re.sub(r'\\begin\{(table|figure|algorithm)\}.*?\\end\{\1\}', '', content, flags=re.DOTALL)
    cleaned = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '', cleaned, flags=re.DOTALL)
    
    skip_cmds = ['\\centering', '\\hfill', '\\includegraphics', '\\caption', '\\label',
                 '\\begin', '\\end', '\\hline', '\\toprule', '\\midrule', '\\bottomrule',
                 '\\subsection', '\\subsubsection', '\\section', '\\chapter', '\\item',
                 '\\State', '\\For', '\\End', '\\While',
                 '\\backmatter', '\\printbibliography', '\\include', '\\input', '\\addbibresource']
    
    para_lines = []
    for i, line in enumerate(cleaned.split('\n')):
        s = line.strip()
        if not s or s.startswith('%') or any(s.startswith(c) for c in skip_cmds):
            if para_lines:
                para_text = ' '.join(para_lines)
                sents = count_sentences(para_text)
                if sents < 3 and len(para_text) > 30:
                    ctx = para_text[:80]
                    issues.append((i, f'[过短] {sents}句, {len(para_text)}字: "{ctx}..."'))
                para_lines = []
            continue
        para_lines.append(s)
    
    # 引用密度
    total_cites = len(re.findall(r'\\cite\{', content))
    sections = re.split(r'\\section\{', content)
    for j, sec in enumerate(sections):
        if len(sec) > 500:
            sec_name = sec.split('}')[0] if '}' in sec else f'第{j}节'
            cites = len(re.findall(r'\\cite\{', sec))
            if cites < 3:
                issues.append((0, f'[引用] "{sec_name}" 仅{cites}篇引用 ({len(sec)}字)'))
    
    if total_cites < 30:
        issues.append((0, f'[引用] 全文仅{total_cites}篇，建议80-120篇'))
    
    # 残留Markdown粗体
    for i, line in enumerate(raw_lines, 1):
        if i <= line_offset:
            continue
        if '**' in line and not line.strip().startswith('%'):
            ctx = line.strip()[:50]
            issues.append((i, f'[Markdown] "**"需替换\\textbf: "{ctx}..."'))
    
    return fname, issues


def main():
    # 修复Windows GBK终端emoji编码问题
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    mode = sys.argv[1]
    target = sys.argv[2]
    
    files = []
    if os.path.isfile(target):
        files.append(target)
    elif os.path.isdir(target):
        for f in sorted(os.listdir(target)):
            if f.endswith('.tex'):
                files.append(os.path.join(target, f))
    
    total = 0
    for fpath in files:
        if mode == 'format' or mode == 'all':
            fname, issues = check_format(fpath)
            if issues:
                print(f'\n{"="*50}')
                print(f'[FORMAT] {fname} - {len(issues)} issue(s)')
                print(f'{"="*50}')
                for desc in issues:
                    print(f'  {desc}')
                total += len(issues)
        
        if mode == 'style' or mode == 'all':
            fname, issues = check_style(fpath)
            if issues:
                print(f'\n{"="*50}')
                print(f'[STYLE] {fname} - {len(issues)} issue(s)')
                print(f'{"="*50}')
                for line_num, desc in issues:
                    loc = f'第{line_num}行' if line_num > 0 else ''
                    print(f'  {loc:12s} {desc}')
                total += len(issues)
    
    if total == 0:
        print('\n[OK] No issues found.')
    else:
        print(f'\n[SUMMARY] Total: {total} issue(s)')

if __name__ == '__main__':
    main()
