#!/usr/bin/env python3
"""最终修复：对所有tabular用resizebox包裹 + 长quote断行"""
import re, os, sys

tex_dir = sys.argv[1] if len(sys.argv) > 1 else "chapters_tex"

for f in sorted(os.listdir(tex_dir)):
    if not f.endswith('.tex'): continue
    path = os.path.join(tex_dir, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
        lines = content.split('\n')
    
    orig = '\n'.join(lines)
    new_lines = []
    i = 0
    in_tabular = False
    tabular_depth = 0  # 追踪嵌套
    
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        
        # 检测 \begin{tabular} — 在不处于table环境时，手动加resizebox
        if '\\begin{tabular}' in s:
            # 检查是否已在resizebox或footnotesize内
            prev_line = new_lines[-1] if new_lines else ''
            has_resize = '\\resizebox' in prev_line
            has_small = '\\small' in prev_line or '\\footnotesize' in prev_line
            
            if not has_resize and not has_small:
                # 在tabular前加resizebox
                new_lines.append(line)
                in_tabular = True
                continue
            else:
                in_tabular = True
        
        # 检测 \end{tabular}
        if '\\end{tabular}' in s and in_tabular:
            in_tabular = False
        
        new_lines.append(line)
        i += 1
    
    content = '\n'.join(new_lines)
    
    # 方案：对宽表格用 resizebox{\textwidth}{!} 包裹
    # 找到所有不在table环境中的tabular
    # 简单替换模式：\n\\centering\n{\\small\n\\begin{tabular} → \n\\centering\n\\resizebox{\\textwidth}{!}{{\\small\n\\begin{tabular}
    content = content.replace(
        '\\centering\n{\\small\n\\begin{tabular}',
        '\\centering\n\\resizebox{\\textwidth}{!}{{\\small\n\\begin{tabular}'
    )
    # 对应的关闭：\\end{tabular}}\n → \\end{tabular}}}\n
    content = content.replace(
        '\\end{tabular}}\n',
        '\\end{tabular}}}\n'
    )
    
    # 处理不在{small}内的table: \centering\n\begin{tabular}
    content = content.replace(
        '\\centering\n\\begin{tabular}',
        '\\centering\n\\resizebox{\\textwidth}{!}{\\begin{tabular}'
    )
    # 对应的关闭
    content = content.replace(
        '\\end{tabular}\n',
        '\\end{tabular}}\n'
    )
    
    # 处理quote中的超长行（第4章L502问题）
    lines2 = content.split('\n')
    new_lines2 = []
    in_quote = False
    for line in lines2:
        s = line.strip()
        if s == '\\begin{quote}':
            in_quote = True
        elif s == '\\end{quote}':
            in_quote = False
        
        if in_quote and len(s) > 90 and not s.startswith('\\'):
            # 在句号后断行
            s = s.replace('。', '。\\newline ')
            s = s.replace('；', '；\\newline ')
        
        new_lines2.append(line)
    
    content = '\n'.join(new_lines2)
    
    if content != orig:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'✅ {f}')
    else:
        print(f'   {f}: 无需修复')