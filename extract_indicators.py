# -*- coding: utf-8 -*-
"""
从Choice API指标手册CHM提取的HTML文件中提取API字段名
"""
import os
import re
from html.parser import HTMLParser

class IndicatorExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_text = ""
        self.indicators = []

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.current_text += text + " "

def extract_english_from_html(file_path):
    """从HTML中提取英文字段名"""
    try:
        with open(file_path, 'r', encoding='gb2312', errors='ignore') as f:
            content = f.read()
    except:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

    # 提取英文字段名（全大写或驼峰命名的字段）
    # 匹配模式：<td class=...>FIELDNAME</td>
    pattern = r'<td[^>]*class=xl\d+[^>]*>([A-Z][A-Za-z0-9_]*)</td>'
    matches = re.findall(pattern, content)

    return list(set(matches))

def process_directory(base_dir):
    """处理目录下所有HTML文件"""
    results = {}

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f == 'sheet001.html':
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, base_dir)
                indicators = extract_english_from_html(full_path)
                if indicators:
                    # 获取父目录名作为分类
                    parent = os.path.basename(os.path.dirname(os.path.dirname(full_path)))
                    category = os.path.basename(os.path.dirname(full_path))

                    key = f"{parent}/{category}"
                    if key not in results:
                        results[key] = []
                    results[key].extend(indicators)

    # 去重
    for key in results:
        results[key] = sorted(list(set(results[key])))

    return results

def main():
    base_dir = r"D:\聪明的小C2.0\资产配置框架搭建\chm_extracted"

    print("=" * 60)
    print("Choice API 指标字段提取")
    print("=" * 60)

    results = process_directory(base_dir)

    # 按类别输出
    output_lines = []
    for key in sorted(results.keys()):
        indicators = results[key]
        if indicators:
            output_lines.append(f"\n## {key}")
            output_lines.append(", ".join(indicators))

    # 保存到文件
    output_file = r"D:\聪明的小C2.0\资产配置框架搭建\choice_api_indicators.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))

    print(f"\n提取完成！保存到: {output_file}")
    print(f"共提取 {len(results)} 个类别的指标")

if __name__ == "__main__":
    main()