#!/usr/bin/env python3
"""
学位论文质量自动检测工具 — 检查机械化写作、段落长度、格式问题

用法:
  python validate_thesis.py [tex文件或目录]
  
检查项:
  1. 机械化写作模式（首先/其次/一方面/另一方面列表式）
  2. 过短段落（<3句话）
  3. 残留**粗体**标记
  4. 缺少引用的段落
  5. 章节标题格式
  6. 参考文献密度
"""

import os, re, sys
from collections import defaultdict

# 机械化写作模式关键词
MECHANICAL_PATTERNS = [
    (r'首先.*?其次.*?再次', '三连列表式"首先…其次…再次"'),
    (r'一方面.*?另一方面', '对列式"一方面…另一方面"'),
    (r'第一，.*?第二，.*?第三', '数字列表式"第一…第二…第三"'),
    (r'(功能|需求|特点|优点|缺点)[一二三]', '功能列表式'),
    (r'(需要|需满足).*?功能需求.*?功能需求', '需求枚举式'),
]

# 长段落阈值（字符数）
MIN_PARAGRAPH_LEN = 100
# 短句子阈值
MIN_SENTENCES = 3

def count_sentences(text):
    """估算句子数"""
    text = re.sub(r'\$[^$]+\$', '', text)  # 去掉公式
    text = re.sub(r'\\[a-zA-Z]+', '', text)  # 去掉LaTeX命令
    # 按句号/问号/感叹号/换行分割
    sentences = re.split(r'[。！？\n]', text)
    return len([s for s in sentences if len(s.strip()) > 5])

def check_mechanical_writing(content, filename):
    """检查机械化写作模式"""
    issues = []
    for i, line in enumerate(content.split('\n'), 1):
        if line.strip().startswith('%'):
            continue
        for pattern, desc in MECHANICAL_PATTERNS:
            if re.search(pattern, line, re.DOTALL):
                # 提取上下文
                ctx = line.strip()[:80]
                issues.append((i, f'[机械化] {desc}: "{ctx}..."'))
    return issues

def check_short_paragraphs(content, filename):
    """检查过短段落（跳过表格/图表/算法/命令）"""
    issues = []
    cleaned = re.sub(r'\\begin\{table\}.*?\\end\{table\}', '[TABLE]', content, flags=re.DOTALL)
    cleaned = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', '[FIGURE]', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\\begin\{algorithm\}.*?\\end\{algorithm\}', '[ALGORITHM]', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\\begin\{tabular\}.*?\\end\{tabular\}', '[TABLE]', cleaned, flags=re.DOTALL)
    
    skip_cmds = ['\\centering', '\\hfill', '\\includegraphics', '\\caption', '\\label',
                 '\\begin', '\\end', '\\hline', '\\toprule', '\\midrule', '\\bottomrule',
                 '\\subsection', '\\subsubsection', '\\section', '\\chapter', '\\item',
                 '\\State', '\\For', '\\End', '\\While', '\\Comment',
                 '\\textbf{关键发现', '\\textbf{发现']
    
    lines = cleaned.split('\n')
    para_lines = []
    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s.startswith('%') or any(s.startswith(c) for c in skip_cmds):
            if para_lines:
                para_text = ' '.join(para_lines)
                sents = count_sentences(para_text)
                if sents < MIN_SENTENCES and len(para_text) < MIN_PARAGRAPH_LEN * 2:
                    # 找上下文
                    ctx = para_text[:100]
                    issues.append((i, f'[过短段落] {sents}句话, {len(para_text)}字: "{ctx}..."'))
                para_lines = []
            continue
        para_lines.append(s)
    return issues

def check_markdown_bold(content, filename):
    """检查残留的**粗体**"""
    issues = []
    for i, line in enumerate(content.split('\n'), 1):
        if '**' in line and not line.strip().startswith('%'):
            ctx = line.strip()[:60]
            issues.append((i, f'[Markdown粗体] 需替换为\\textbf{{}}: "{ctx}..."'))
    return issues

def check_citation_density(content, filename):
    """检查各章节引用密度"""
    issues = []
    # 按章节分割
    sections = re.split(r'(\\section\{[^}]+\}|\\chapter\{[^}]+\})', content)
    for j in range(0, len(sections)-1, 2):
        section_name = re.sub(r'\\(section|chapter)\{([^}]+)\}', r'\2', sections[j]) if j < len(sections) else '全文'
        section_content = sections[j+1] if j+1 < len(sections) else ''
        cites = len(re.findall(r'\\cite\{', section_content))
        chars = len(section_content)
        if chars > 200 and cites == 0:
            issues.append((0, f'[缺少引用] "{section_name}" 无任何引用'))
        elif chars > 500 and cites < 2:
            issues.append((0, f'[引用不足] "{section_name}" 仅{cites}篇引用 ({chars}字)'))
    # 全文总引用
    total_cites = len(re.findall(r'\\cite\{', content))
    if total_cites < 30:
        issues.append((0, f'[引用不足] 全文仅{total_cites}篇引用，建议80-120篇'))
    return issues

def check_chapter_numbering(content, filename):
    """检查章节编号一致性"""
    issues = []
    chapters = re.findall(r'\\(section|subsection|subsubsection)\{', content)
    counter = defaultdict(int)
    for cmd in chapters:
        counter[cmd] += 1
    # 章节数量预警
    if counter['section'] == 0:
        issues.append((0, '[章节结构] 无任何\\section，建议每章至少3-5节'))
    return issues


def validate_file(filepath):
    """验证单个tex文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fname = os.path.basename(filepath)
    all_issues = []
    all_issues.extend(check_mechanical_writing(content, fname))
    all_issues.extend(check_short_paragraphs(content, fname))
    all_issues.extend(check_markdown_bold(content, fname))
    all_issues.extend(check_citation_density(content, fname))
    all_issues.extend(check_chapter_numbering(content, fname))
    
    return fname, all_issues


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_thesis.py <tex文件或目录>")
        sys.exit(1)
    
    path = sys.argv[1]
    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        for f in sorted(os.listdir(path)):
            if f.endswith('.tex'):
                files.append(os.path.join(path, f))
    
    total_issues = 0
    for fpath in files:
        fname, issues = validate_file(fpath)
        n = len(issues)
        total_issues += n
        if n > 0:
            print(f'\n{"="*60}')
            print(f'📄 {fname} — 发现 {n} 个问题')
            print(f'{"="*60}')
            for line_num, desc in issues:
                loc = f'第{line_num}行' if line_num > 0 else ''
                print(f'  {loc:8s} {desc}')
    
    print(f'\n{"="*60}')
    if total_issues == 0:
        print('✅ 完美！未发现问题')
    else:
        severity = '轻微' if total_issues < 10 else ('中等' if total_issues < 30 else '严重')
        print(f'📊 总计 {total_issues} 个问题（{severity}）')
        print(f'   建议优先修复: 机械化写作 > 过短段落 > 引用不足')
    print(f'{"="*60}')


if __name__ == '__main__':
    main()
