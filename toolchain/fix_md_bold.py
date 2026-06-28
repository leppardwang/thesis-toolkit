#!/usr/bin/env python3
"""修复残留Markdown粗体：**xxx** → \\textbf{xxx}"""
import re, os, sys

tex_dir = sys.argv[1] if len(sys.argv) > 1 else "chapters_tex"

total_fixes = 0
for f in sorted(os.listdir(tex_dir)):
    if not f.endswith('.tex'): continue
    path = os.path.join(tex_dir, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # **xxx** → \textbf{xxx}（不跨行）
    new_content = re.sub(r'\*\*([^*\n]+?)\*\*', r'\\textbf{\1}', content)
    
    if new_content != content:
        fixes = len(re.findall(r'\\textbf\{', new_content)) - len(re.findall(r'\\textbf\{', content))
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        print(f"✅ {f}: 修复 {fixes} 处")
        total_fixes += fixes
    else:
        print(f"✅ {f}: 无需修复")

print(f"\n总计修复 {total_fixes} 处Markdown粗体残留")