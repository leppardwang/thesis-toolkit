#!/usr/bin/env python3
"""修复tex文件中\\t extbf为\\textbf"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "chapter_file.tex"

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 **bold** -> \textbf{content}
content = re.sub(r'\*\*(.+?)\*\*', lambda m: '\\textbf{' + m.group(1) + '}', content)

# 修复 \t extbf -> \textbf
content = content.replace('\\t extbf', '\\textbf')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

count = content.count('\\textbf')
print(f'Fixed {path}! Total \\textbf instances: {count}')
