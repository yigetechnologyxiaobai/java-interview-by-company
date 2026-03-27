#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重构 Java 面试题目录结构
按公司 + 知识点组织
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# 公司中文名映射
COMPANY_NAMES = {
    '01-alibaba': '阿里巴巴',
    '02-tencent': '腾讯',
    '03-bytedance': '字节跳动',
    '04-meituan': '美团',
    '05-jd': '京东',
    '06-huawei': '华为',
    '07-baidu': '百度',
    '08-kuaishou': '快手',
    '09-xiaohongshu': '小红书',
    '10-didi': '滴滴',
    '11-netease': '网易',
    '12-pinduoduo': '拼多多',
}

# 章节到知识点的映射规则
SECTION_MAPPING = {
    'Java基础': ['Java 基础', 'Java基础', '集合', 'String', 'Object', '反射', '泛型', 'IO'],
    '并发编程': ['并发', '线程', '锁', 'JUC', 'CAS', 'AQS', 'ThreadLocal', 'synchronized'],
    'JVM': ['JVM', 'GC', '类加载', '内存模型', 'JVM调优'],
    '数据库': ['MySQL', 'Redis', '数据库', 'SQL', '事务', '索引'],
    '分布式': ['分布式', '微服务', 'MQ', '消息队列', 'RPC', 'CAP', '分布式锁'],
    '场景设计': ['系统设计', '架构', '秒杀', '限流', '场景', '高并发'],
    '真题收录': ['真题', '面经', '面试题', '最新面经'],
}

# 特殊章节（不分类）
SPECIAL_SECTIONS = ['面试风格', '面试技巧', '自动更新', '项目深挖']

def classify_section(section_title):
    """
    根据章节标题判断属于哪个知识点
    """
    # 特殊章节
    for special in SPECIAL_SECTIONS:
        if special in section_title:
            return None  # 不分类，放到 README
    
    # 匹配知识点
    for category, keywords in SECTION_MAPPING.items():
        for keyword in keywords:
            if keyword in section_title:
                return category
    
    # 算法单独处理
    if '算法' in section_title:
        return '算法'
    
    # 网络和操作系统归入Java基础
    if '网络' in section_title or '操作系统' in section_title:
        return 'Java基础'
    
    # Spring 归入分布式
    if 'Spring' in section_title:
        return '分布式'
    
    return None  # 未匹配，放到 README

def parse_company_file(filepath):
    """
    解析公司文件，提取面试风格和各章节内容
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # 提取公司名称
    filename = os.path.basename(filepath)
    company_key = filename.replace('.md', '')
    company_name = COMPANY_NAMES.get(company_key, company_key)
    
    # 提取面试风格
    style_lines = []
    sections = []
    current_section = {'title': '', 'content': []}
    in_style = False
    in_section = False
    
    for i, line in enumerate(lines):
        # 第一行是标题
        if i == 0 and line.startswith('# '):
            continue
        
        # 面试风格部分
        if '## 面试风格' in line:
            in_style = True
            in_section = False
            continue
        
        # 其他二级标题
        if line.startswith('## '):
            if in_style:
                # 面试风格结束，开始新章节
                in_style = False
                in_section = True
                current_section = {'title': line[3:].strip(), 'content': []}
            elif in_section:
                # 保存上一个章节
                if current_section['title']:
                    sections.append(current_section.copy())
                current_section = {'title': line[3:].strip(), 'content': []}
            continue
        
        # 收集内容
        if in_style:
            style_lines.append(line)
        elif in_section:
            current_section['content'].append(line)
    
    # 保存最后一个章节
    if current_section['title']:
        sections.append(current_section)
    
    return {
        'name': company_name,
        'style': '\n'.join(style_lines).strip(),
        'sections': sections
    }

def create_company_folder(base_path, company_name, data):
    """
    创建公司文件夹和文件
    """
    folder_path = os.path.join(base_path, company_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # 创建 README.md（公司简介、面试风格）
    readme_content = f"""# {company_name} 面试题

## 面试风格

{data['style']}

## 知识点索引

"""
    
    # 按知识点分类
    categorized = defaultdict(list)
    uncategorized = []
    
    for section in data['sections']:
        category = classify_section(section['title'])
        if category:
            categorized[category].append(section)
        else:
            uncategorized.append(section)
    
    # 生成索引
    for category in ['Java基础', '并发编程', 'JVM', '数据库', '分布式', '场景设计', '算法', '真题收录']:
        if category in categorized:
            readme_content += f"- [{category}]({category}.md)\n"
    
    with open(os.path.join(folder_path, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # 创建知识点文件
    for category, sections in categorized.items():
        create_category_file(folder_path, company_name, category, sections)
    
    # 未分类的内容（面试技巧、项目深挖等）追加到 README
    if uncategorized:
        with open(os.path.join(folder_path, 'README.md'), 'a', encoding='utf-8') as f:
            for section in uncategorized:
                f.write(f"\n\n## {section['title']}\n\n")
                f.write('\n'.join(section['content']))

def create_category_file(folder_path, company_name, category, sections):
    """
    创建知识点文件
    """
    filepath = os.path.join(folder_path, f"{category}.md")
    
    content = f"""# {company_name} - {category}

> 本文档整理自 {company_name} 面经真题，按知识点归类

"""
    
    # 添加目录
    content += "## 目录\n\n"
    for section in sections:
        # 生成锚点
        anchor = section['title'].replace(' ', '-').replace('/', '-')
        content += f"- [{section['title']}](#{anchor})\n"
    content += "\n---\n\n"
    
    # 添加内容
    for section in sections:
        content += f"## {section['title']}\n\n"
        content += '\n'.join(section['content'])
        content += "\n\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def create_internship_folder(base_path, source_file):
    """
    创建实习专题文件夹
    """
    folder_path = os.path.join(base_path, '实习专题')
    os.makedirs(folder_path, exist_ok=True)
    
    # 复制实习文件
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 调整标题
    content = content.replace('# 2025-2026 Java 实习面试高频题汇总', '# 实习专题 - 2025-2026高频题')
    
    with open(os.path.join(folder_path, '2025-2026高频题.md'), 'w', encoding='utf-8') as f:
        f.write(content)

def create_root_readme(base_path):
    """
    创建根目录 README.md
    """
    content = """# Java 面试题汇总

> 本项目整理了国内主流互联网公司的 Java 面经真题，按公司 + 知识点组织，方便系统化学习。

## 📂 目录结构

```
docs/
├── 实习专题/
│   └── 2025-2026高频题.md
├── 阿里巴巴/
│   ├── README.md (公司简介、面试风格、题目索引)
│   ├── Java基础.md
│   ├── 并发编程.md
│   ├── JVM.md
│   ├── 数据库.md
│   ├── 分布式.md
│   ├── 场景设计.md
│   └── 真题收录.md
├── 腾讯/
├── 字节跳动/
├── 美团/
├── 京东/
├── 华为/
├── 百度/
├── 快手/
├── 小红书/
├── 滴滴/
├── 网易/
└── 拼多多/
```

## 🏢 公司列表

| 公司 | 面试特点 | 重点考察 |
|------|---------|---------|
| [阿里巴巴](阿里巴巴/) | 深挖底层原理，连环追问 | JVM、并发、分布式、MySQL |
| [腾讯](腾讯/) | 注重基础扎实，算法能力 | 算法、网络、操作系统、Java基础 |
| [字节跳动](字节跳动/) | 算法驱动，系统设计占比大 | 算法、系统设计、基础 |
| [美团](美团/) | 注重实战能力，偏爱场景题 | MySQL、Redis、分布式、高并发 |
| [京东](京东/) | 注重基础扎实，偏爱八股文 | Java基础、MySQL、Redis、Spring |
| [华为](华为/) | 注重综合素质，深度广度并重 | 并发、JVM、分布式、系统设计 |
| [百度](百度/) | 注重基础扎实，引导式提问 | Java基础、多线程、JVM、MySQL |
| [快手](快手/) | 一面基础八股，二面深挖项目 | JUC多线程、并发、网络编程 |
| [小红书](小红书/) | 注重实战能力，关注高并发 | Redis、MySQL、分布式、高并发 |
| [滴滴](滴滴/) | 注重业务场景，关注分布式 | 分布式、MySQL、Redis、消息队列 |
| [网易](网易/) | 注重分布式理解，关注项目经验 | 分布式系统、多线程、Spring |
| [拼多多](拼多多/) | 高压测试，高强度技术拷问 | Java基础、多线程、JVM、操作系统 |

## 🎯 快速导航

### 按知识点

- [Java基础](阿里巴巴/Java基础.md)：集合、String、反射、泛型、IO
- [并发编程](阿里巴巴/并发编程.md)：线程、锁、线程池、JUC
- [JVM](阿里巴巴/JVM.md)：内存模型、GC、类加载、调优
- [数据库](阿里巴巴/数据库.md)：MySQL、Redis、SQL优化、事务
- [分布式](阿里巴巴/分布式.md)：微服务、MQ、分布式锁、CAP
- [场景设计](阿里巴巴/场景设计.md)：系统设计、架构、秒杀、限流

### 按公司

- [实习专题](实习专题/2025-2026高频题.md)：2025-2026 实习高频题汇总
- [阿里巴巴](阿里巴巴/)：JVM、并发、分布式、MySQL、Spring
- [腾讯](腾讯/)：算法、网络、操作系统、Java基础
- [字节跳动](字节跳动/)：算法、系统设计
- [美团](美团/)：MySQL、Redis、分布式、高并发
- [京东](京东/)：Java基础、MySQL、Redis、Spring
- [华为](华为/)：并发、JVM、分布式、系统设计
- [百度](百度/)：Java基础、多线程、JVM、MySQL
- [快手](快手/)：JUC多线程、并发、网络编程
- [小红书](小红书/)：Redis、MySQL、分布式、高并发
- [滴滴](滴滴/)：分布式、MySQL、Redis、消息队列
- [网易](网易/)：分布式系统、多线程、Spring
- [拼多多](拼多多/)：Java基础、多线程、JVM、操作系统

## 📚 使用建议

1. **实习/校招准备**：先看[实习专题](实习专题/2025-2026高频题.md)，了解整体趋势
2. **公司针对性准备**：进入对应公司目录，阅读 README 了解面试风格
3. **知识点系统学习**：按知识点（Java基础、并发、JVM等）纵向对比学习
4. **真题实战**：查看各公司的真题收录，了解最新面试动态

## 📝 数据来源

- 牛客网
- GitHub
- CSDN
- 知乎
- 面经分享

## 🔄 更新记录

- 2026-03-25：初始版本，整理 12 家公司面经
- 2026-03-27：重构目录结构，按公司 + 知识点组织

---

**Star ⭐ 本项目，助力求职成功！**
"""
    
    with open(os.path.join(base_path, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """
    主函数：执行重构
    """
    docs_path = '/root/.openclaw/workspace/java-interview-by-company/docs'
    backup_path = '/root/.openclaw/workspace/java-interview-by-company/docs_backup'
    
    # 备份原始文件
    if os.path.exists(backup_path):
        import shutil
        shutil.rmtree(backup_path)
    os.makedirs(backup_path)
    
    for filename in os.listdir(docs_path):
        if filename.endswith('.md'):
            src = os.path.join(docs_path, filename)
            dst = os.path.join(backup_path, filename)
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print("✅ 备份完成")
    
    # 处理实习专题
    internship_file = os.path.join(docs_path, '00-internship-2026.md')
    if os.path.exists(internship_file):
        create_internship_folder(docs_path, internship_file)
        print("✅ 实习专题处理完成")
    
    # 处理每个公司文件
    for i in range(1, 13):
        filename = f'{i:02d}-{list(COMPANY_NAMES.keys())[i-1].split("-")[1]}.md'
        filepath = os.path.join(docs_path, filename)
        
        # 查找实际文件
        actual_file = None
        for f in os.listdir(docs_path):
            if f.startswith(f'{i:02d}-'):
                actual_file = os.path.join(docs_path, f)
                break
        
        if actual_file and os.path.exists(actual_file):
            data = parse_company_file(actual_file)
            create_company_folder(docs_path, data['name'], data)
            print(f"✅ {data['name']} 处理完成")
    
    # 创建根目录 README
    create_root_readme(docs_path)
    print("✅ README.md 创建完成")
    
    # 删除旧文件
    for filename in os.listdir(docs_path):
        if filename.endswith('.md') and filename != 'README.md':
            filepath = os.path.join(docs_path, filename)
            os.remove(filepath)
            print(f"🗑️  删除旧文件: {filename}")
    
    print("\n🎉 重构完成！")
    print(f"📁 新结构已生成在: {docs_path}")
    print(f"💾 备份位置: {backup_path}")

if __name__ == '__main__':
    main()