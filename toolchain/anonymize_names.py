#!/usr/bin/env python3
"""替换.md中所有真实人名为代号（隐私保护）"""
import os

chapters_dir = "C:/Users/Administrator/WorkBuddy/Claw/chapters"

# 替换映射：真实姓名 → 代号
replacements = {
    '韩扬畴': '受访者A',
    '何雨能': '受访者B',
    '陈德群': '受访者C',
    '迟工': '受访者D',
    '蒋欢': '受访者E',
    '唐先好': '受访者F',
    '林焕强': '受访者G',
    '张工': '受访者H',
    '王倩': '受访者L',
    '王丹': '受访者M',
}

# 单字名需要特殊处理（只替换独立出现的情况，用"、"分隔确认）
single_names = {}  # 跳过单字名替换，避免误伤

total = 0
for f in sorted(os.listdir(chapters_dir)):
    if not f.endswith('.md'): continue
    path = os.path.join(chapters_dir, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    orig = content
    
    # 替换三字名
    for old, new in replacements.items():
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            if count > 0:
                print(f'  {f}: {old} → {new} ({count}处)')
                total += count
    
    # 替换单字名（需谨慎：只在姓名列表上下文中替换）
    for old, new in single_names.items():
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            if count > 0:
                print(f'  {f}: {old} → {new} ({count}处)')
                total += count
    
    if content != orig:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)

print(f'\n总计替换 {total} 处人名')