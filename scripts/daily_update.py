#!/usr/bin/env python3
"""
Java 面试题每日检索更新脚本
每天自动检索最新面经，更新到对应公司文档
"""

import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path

# 添加项目路径
PROJECT_DIR = Path(__file__).parent.parent
DOCS_DIR = PROJECT_DIR / "docs"
MAINTAIN_FILE = PROJECT_DIR / "MAINTAIN.md"

# 公司列表（与 docs 目录文件对应）
COMPANIES = {
    "阿里巴巴": "01-alibaba.md",
    "腾讯": "02-tencent.md",
    "字节跳动": "03-bytedance.md",
    "美团": "04-meituan.md",
    "京东": "05-jd.md",
    "华为": "06-huawei.md",
    "百度": "07-baidu.md",
    "快手": "08-kuaishou.md",
    "小红书": "09-xiaohongshu.md",
    "滴滴": "10-didi.md",
    "网易": "11-netease.md",
    "拼多多": "12-pinduoduo.md",
    "实习": "00-internship-2026.md",
}

def get_existing_questions(file_path: Path) -> set:
    """从现有文档中提取已有问题"""
    if not file_path.exists():
        return set()
    
    content = file_path.read_text(encoding="utf-8")
    # 匹配问题格式：### 数字. 问题内容
    questions = re.findall(r'###\s*\d+\.\s*(.+?)(?:\n|$)', content)
    # 也匹配追问格式
    followups = re.findall(r'\*\*追问[：:]\*\*\s*(.+?)(?:\n|$)', content)
    
    all_questions = set()
    for q in questions + followups:
        # 标准化问题文本
        normalized = re.sub(r'\s+', ' ', q.strip()).lower()
        all_questions.add(normalized)
    
    return all_questions

def update_maintain_log(date: str, company: str, new_count: int):
    """更新 MAINTAIN.md 日志"""
    content = MAINTAIN_FILE.read_text(encoding="utf-8")
    
    # 更新检查清单表格
    table_pattern = rf'\| {company} \| (\d{{4}}-\d{{2}}-\d{{2}}) \| ([\d+]+) \|'
    match = re.search(table_pattern, content)
    
    if match:
        old_date, old_count = match.groups()
        new_content = re.sub(
            table_pattern,
            f'| {company} | {date} | {new_count} |',
            content
        )
        MAINTAIN_FILE.write_text(new_content, encoding="utf-8")

def append_to_doc(file_path: Path, company: str, new_questions: list):
    """将新问题追加到文档"""
    if not new_questions:
        return 0
    
    content = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
    
    # 找到最后一个问题编号
    last_num = 0
    matches = re.findall(r'###\s*(\d+)\.', content)
    if matches:
        last_num = max(int(m) for m in matches)
    
    # 构建新内容
    new_content = "\n\n---\n\n## 📥 自动更新 ({})\n\n".format(
        datetime.now().strftime("%Y-%m-%d")
    )
    
    for i, q in enumerate(new_questions, 1):
        new_content += f"### {last_num + i}. {q['question']}\n\n"
        if q.get('answer'):
            new_content += f"{q['answer']}\n\n"
        if q.get('followups'):
            for fq in q['followups']:
                new_content += f"**追问：** {fq}\n\n"
    
    # 追加到文件
    with open(file_path, 'a', encoding="utf-8") as f:
        f.write(new_content)
    
    return len(new_questions)

def main():
    """主函数：检索并更新面经"""
    print(f"[{datetime.now()}] 开始检索面经更新...")
    
    results = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "updates": [],
        "total_new": 0
    }
    
    # 这里需要调用搜索工具获取最新面经
    # 由于脚本独立运行，实际搜索逻辑通过 openclaw agent 执行
    # 此脚本主要用于文件操作
    
    # 输出 JSON 结果供外部调用
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results

if __name__ == "__main__":
    main()