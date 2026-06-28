#!/usr/bin/env python3
"""精确替换表格中残留的单字姓名"""
import os

chapters_dir = "C:/Users/Administrator/WorkBuddy/Claw/chapters"
files = ['04-第四章_DS-CRIF 风险识别框架.md', '05-第五章_系统实证验证与案例分析.md']

# 只替换表格行（以|开头和结尾的行）中的残留姓名
name_map = {
    '程': '受访者P',
    '吴': '受访者Q', 
    '魏': '受访者R',
    '亚妮': '受访者S',
    '冯': '受访者T',
}

total = 0
for fname in files:
    path = os.path.join(chapters_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        # 只在表格行中替换（以|开头）
        if stripped.startswith('|') and stripped.endswith('|'):
            for old, new in name_map.items():
                if old in stripped:
                    stripped = stripped.replace(old, new)
                    # 重新组合行（保留原始缩进）
                    line = line[:len(line)-len(line.lstrip())] + stripped
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        # 统计替换了多少
        count = sum(1 for old, new in name_map.items() if orig.count(old) != content.count(old))
        print(f'✅ {fname}: 替换表格中残留姓名')
        total += count

print(f'\n替换完成')