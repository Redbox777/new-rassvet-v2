#!/usr/bin/env python3
"""
Сборка всех Markdown документов проекта "Новый Рассвет" в один HTML/PDF файл.
"""

import os
import markdown
from pathlib import Path

# Порядок модулей для сборки
MODULES_ORDER = [
    "SUMMARY.md",
    "00_Ядро_и_Идеология",
    "01_Общество_и_Социум",
    "02_Инфраструктура_и_Логистика",
    "03_Энергетика_и_Технологии",
    "04_Безопасность_и_Оборона",
    "05_Строительство_и_Купол",
    "06_Еда_и_Водоснабжение",
    "07_Материалы_и_Производство",
    "08_Медицина_и_Генетика",
    "09_Образование_и_Культура",
    "10_Космос_и_Транспорт",
]

def get_markdown_files(module_path):
    """Получить все .md файлы в папке модуля, отсортированные по имени."""
    path = Path(module_path)
    if not path.exists():
        return []
    
    files = []
    for f in sorted(path.glob("*.md")):
        if f.name == "README.md":
            files.insert(0, f)  # README первым
        else:
            files.append(f)
    return files

def convert_md_to_html(md_content):
    """Конвертировать Markdown в HTML."""
    md = markdown.Markdown(extensions=['tables', 'toc', 'fenced_code'])
    return md.convert(md_content)

def build_html():
    """Собрать все документы в один HTML."""
    html_parts = []
    
    # Шапка HTML
    html_parts.append("""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Новый Рассвет v2.0 - Полная база знаний</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            color: #333;
        }
        h1 { color: #d2691e; border-bottom: 3px solid #d2691e; padding-bottom: 10px; }
        h2 { color: #2e8b57; border-bottom: 2px solid #2e8b57; padding-bottom: 8px; margin-top: 40px; }
        h3 { color: #4169e1; margin-top: 30px; }
        .module { margin-bottom: 50px; page-break-before: always; }
        .module:first-child { page-break-before: avoid; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f5f5f5; }
        code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .warning { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .toc { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 30px 0; }
        .toc ul { list-style-type: none; padding-left: 20px; }
        @media print {
            body { padding: 20px; }
            .module { page-break-before: always; }
            a { color: #333; text-decoration: none; }
        }
    </style>
</head>
<body>
""")
    
    # Обрабатываем каждый модуль
    for module in MODULES_ORDER:
        if module == "SUMMARY.md":
            # Главный файл
            summary_path = Path("SUMMARY.md")
            if summary_path.exists():
                content = summary_path.read_text(encoding='utf-8')
                html_parts.append(f"<div class='module'>\n{convert_md_to_html(content)}\n</div>\n")
        else:
            # Папка модуля
            files = get_markdown_files(module)
            if files:
                html_parts.append(f"<div class='module'>\n")
                for md_file in files:
                    content = md_file.read_text(encoding='utf-8')
                    html_parts.append(convert_md_to_html(content))
                    html_parts.append("\n<hr>\n")
                html_parts.append(f"</div>\n")
    
    # Закрываем HTML
    html_parts.append("""
</body>
</html>""")
    
    return "\n".join(html_parts)

if __name__ == "__main__":
    print("🔨 Собираем базу знаний 'Новый Рассвет v2.0' в HTML...")
    html_content = build_html()
    
    output_file = "New_Dawn_Complete.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Готово! Файл сохранён: {output_file}")
    print(f"📄 Размер: {os.path.getsize(output_file) / 1024:.1f} KB")
    print(f"\n📖 Откройте файл в браузере и используйте Ctrl+P → 'Сохранить как PDF'")
