#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_thesis.py — 学位论文格式与写作质量机器验证
根据 thesis-formatter skill 第8节设计实现

用法:
  python validate_thesis.py format thesis_main.tex    # 格式合规检测
  python validate_thesis.py style chapter_04.tex      # 写作质量检测
  python validate_thesis.py style all                 # 检测所有章节写作质量
  python validate_thesis.py fix                       # 修复Overfull hbox
"""

import re
import os
import sys

# ============================================================
# FORMAT 模式：格式合规检测
# ============================================================

def check_format(tex_path):
    """检测TeX主文件的格式合规性"""
    if not os.path.exists(tex_path):
        print(f"❌ 文件不存在: {tex_path}")
        return
    
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = []
    
    # 1. 页面边距
    checks = {
        "页面边距": [
            ("geometry宏包", r'\\usepackage\[.*?geometry\]' in content),
            ("上边距2.5cm", r'top\s*=\s*2\.5cm' in content),
            ("下边距2.5cm", r'bottom\s*=\s*2\.5cm' in content),
            ("左边距3cm", r'left\s*=\s*3cm' in content),
            ("右边距2.5cm", r'right\s*=\s*2\.5cm' in content),
        ],
        "字体配置": [
            ("正文字体 SimSun", r'\\setCJKmainfont\{SimSun\}' in content),
            ("标题字体 SimHei", r'\\setCJKsansfont\{SimHei\}' in content),
            ("英文字体 Times New Roman", r'\\setmainfont\{Times New Roman\}' in content),
        ],
        "宏包完整性": [
            ("fontspec", r'\\usepackage\{fontspec\}' in content),
            ("xeCJK (通过ctex)", r'\\usepackage\[.*\]\{ctexbook\}' in content or r'\\documentclass\[.*\]\{ctexbook\}' in content),
            ("geometry", r'\\usepackage\{geometry\}' in content),
            ("fancyhdr", r'\\usepackage\{fancyhdr\}' in content),
            ("hyperref", r'\\usepackage\{hyperref\}' in content),
            ("graphicx", r'\\usepackage\{graphicx\}' in content),
            ("amsmath", r'\\usepackage\{amsmath' in content),
            ("booktabs", r'\\usepackage\{booktabs\}' in content),
            ("caption", r'\\usepackage\[.*\]\{caption\}' in content),
            ("setspace", r'\\usepackage\{setspace\}' in content),
        ],
        "文档结构": [
            ("\\frontmatter", r'\\frontmatter' in content),
            ("\\mainmatter", r'\\mainmatter' in content),
            ("\\backmatter", r'\\backmatter' in content),
            ("目录 \\tableofcontents", r'\\tableofcontents' in content),
        ],
        "页眉页脚": [
            ("fancyhead", r'\\fancyhead' in content),
            ("fancyfoot", r'\\fancyfoot' in content),
            ("页码 \\thepage", r'\\thepage' in content),
            ("页眉线", r'\\headrulewidth' in content),
        ],
        "行距": [
            ("1.5倍行距", r'\\onehalfspacing' in content),
        ],
    }
    
    print(f"\n{'='*60}")
    print(f"📋 FORMAT检测: {tex_path}")
    print(f"{'='*60}\n")
    
    total = 0
    passed = 0
    for category, items in checks.items():
        print(f"  【{category}】")
        for name, ok in items:
            total += 1
            status = "✅" if ok else "❌"
            if ok: passed += 1
            print(f"    {status} {name}")
        print()
    
    print(f"  结果: {passed}/{total} 通过 ({passed/total*100:.0f}%)\n")


# ============================================================
# STYLE 模式：写作质量检测
# ============================================================

def check_style(chapter_path):
    """检测单章写作质量"""
    if chapter_path == "all":
        base = sys.argv[3] if len(sys.argv) > 3 else "chapters_tex"
        for f in sorted(os.listdir(base)):
            if f.endswith('.tex'):
                check_style_one(os.path.join(base, f))
        return
    
    check_style_one(chapter_path)


def check_style_one(tex_path):
    """检测单章文件"""
    if not os.path.exists(tex_path):
        print(f"❌ 文件不存在: {tex_path}")
        return
    
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    ch_name = os.path.basename(tex_path)
    print(f"\n{'='*60}")
    print(f"📝 STYLE检测: {ch_name}")
    print(f"{'='*60}")
    
    # 1. 机械化写作检测（首先/其次/列表式）
    first_count = len(re.findall(r'首先', content))
    second_count = len(re.findall(r'其次', content))
    third_count = len(re.findall(r'再次|最后', content))
    
    print(f"\n  1️⃣  机械化写作检测")
    print(f"    '首先' 出现: {first_count}次")
    print(f"    '其次' 出现: {second_count}次")
    print(f"    '再次/最后' 出现: {third_count}次")
    if first_count > 5 and second_count > 3:
        print(f"    ⚠️  可能存在列表式写作残留")
    else:
        print(f"    ✅ 正常")
    
    # 2. 过短段落检测（<3句话）
    para_count = 0
    short_para_count = 0
    short_paras = []
    
    current_para = ""
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if current_para:
                para_count += 1
                # 统计句数（以。！？结尾）
                sentences = len(re.findall(r'[。！？]', current_para))
                if sentences < 3 and len(current_para) > 20:
                    short_para_count += 1
                    short_paras.append(current_para[:60])
                current_para = ""
        else:
            if not stripped.startswith('\\') or stripped.startswith('\\textbf'):
                current_para += stripped
    
    if current_para:
        para_count += 1
        sentences = len(re.findall(r'[。！？]', current_para))
        if sentences < 3 and len(current_para) > 20:
            short_para_count += 1
            short_paras.append(current_para[:60])
    
    print(f"\n  2️⃣  段落长度检测")
    print(f"    总段落数: {para_count}")
    print(f"    过短段落 (<3句): {short_para_count}个")
    if short_paras:
        for sp in short_paras[:5]:
            print(f"    ⚠️  {sp}...")
    
    # 3. 引用密度
    cite_count = len(re.findall(r'\\cite\{', content))
    print(f"\n  3️⃣  引用密度检测")
    print(f"    引用数: {cite_count}次")
    if cite_count < 3:
        print(f"    ❌ 引用过少")
    elif cite_count < 8:
        print(f"    ⚠️  引用偏少")
    else:
        print(f"    ✅ 正常")
    
    # 4. 残留Markdown检测
    bold_md = len(re.findall(r'\*\*[^*]+\*\*', content))
    print(f"\n  4️⃣  残留Markdown检测")
    if bold_md > 0:
        print(f"    ❌ 残留 {bold_md}处 Markdown粗体 (**text**)")
    else:
        print(f"    ✅ 无残留Markdown粗体")
    
    # 5. 小标题统计
    bold_tex = len(re.findall(r'\\textbf\{[^}]+\}', content))
    print(f"\n  5️⃣  小标题统计")
    print(f"    \\textbf小标题: {bold_tex}处")
    
    print(f"\n  📊 综合评分:", end=" ")
    issues = 0
    if first_count > 5: issues += 1
    if short_para_count > 3: issues += 1
    if cite_count < 8: issues += 1
    if bold_md > 0: issues += 1
    
    score_map = {0: "A (优秀)", 1: "B (良好)", 2: "C (需改进)", 3: "D (不通过)", 4: "E (严重问题)"}
    print(score_map.get(issues, "未知"))


# ============================================================
# FIX 模式：修复Overfull hbox
# ============================================================

def fix_overfull():
    """修复Overfull hbox问题"""
    log_path = sys.argv[2] if len(sys.argv) > 2 else "thesis_main.log"
    tex_dir = sys.argv[3] if len(sys.argv) > 3 else "chapters_tex"
    
    # 从log中提取Overfull位置
    if not os.path.exists(log_path):
        print("❌ 找不到编译日志")
        return
    
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        log = f.read()
    
    # 提取Overfull的具体位置和行号
    overfulls = []
    lines_list = log.split('\n')
    for i, line in enumerate(lines_list):
        if 'Overfull \\hbox' in line:
            # 提取下一行中的章节信息
            page_info = ""
            for j in range(i, min(i+5, len(lines_list))):
                if 'chapter_' in lines_list[j] or ']' in lines_list[j]:
                    page_info = lines_list[j].strip()
                    break
            overfulls.append((line.strip(), page_info))
    
    print(f"\n{'='*60}")
    print(f"🔧 FIX: Overfull hbox 修复")
    print(f"{'='*60}")
    print(f"\n找到 {len(overfulls)} 处Overfull hbox警告\n")
    
    # 处理各章节.tex文件中的长行
    fixes = 0
    for tex_file in sorted(os.listdir(tex_dir)):
        if not tex_file.endswith('.tex'):
            continue
        tex_path = os.path.join(tex_dir, tex_file)
        
        with open(tex_path, 'r', encoding='utf-8') as f:
            content = f.read()
            orig = content
        
        # 修复1: 表格列数过多 → 添加small环境缩小
        content = re.sub(
            r'(\\begin\{tabular\}\{[lcr]+\}\n)',
            r'{\\small\n\1',
            content
        )
        content = re.sub(
            r'(\\end\{tabular\}\n)(?!}|\\par)',
            r'\1}\n',
            content
        )
        
        # 修复2: 超长段落添加断行点
        # 在长段落中插入 \\ 强制换行
        # （这个比较复杂，暂时跳过）
        
        if content != orig:
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(content)
            fixes += 1
            print(f"  ✅ 修复 {tex_file}: 表格添加缩小环境")
    
    print(f"\n已修复 {fixes} 个文件")
    print("提示：某些Overfull需要手动调整表格列宽")


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python validate_thesis.py format thesis_main.tex")
        print("  python validate_thesis.py style chapter_04.tex")
        print("  python validate_thesis.py style all")
        print("  python validate_thesis.py fix")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "format":
        target = sys.argv[2] if len(sys.argv) > 2 else "thesis_main.tex"
        check_format(target)
    
    elif mode == "style":
        target = sys.argv[2] if len(sys.argv) > 2 else "all"
        check_style(target)
    
    elif mode == "fix":
        fix_overfull()
    
    else:
        print(f"未知模式: {mode}")