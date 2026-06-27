#!/usr/bin/env python3
"""修复tex文件中\\t extbf为\\textbf"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Administrator\Documents\短暂同步\01-博士论文主干材料\准备2025.6\4 日志行为模型\【前置的联邦学习】medical-federated-learning0418博论设计备胎\thesis博论\chapters\chapter5_system.tex'

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
