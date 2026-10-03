import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/content/LessonManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# 1. Remove quiz and flashcard from select options
old_select = """                    <option value="document">Tài liệu (Document)</option>
                    <option value="video">Video</option>
                    <option value="flashcard_set">Bộ Flashcard</option>
                    <option value="quiz">Bài Quiz</option>"""

new_select = """                    <option value="document">Tài liệu (Document)</option>
                    <option value="video">Video</option>"""

content = content.replace(old_select, new_select)

# 2. Filter items in the table
old_map = """              {items.length === 0 ? ("""
new_map = """              {items.filter(i => i.content_type === 'document' || i.content_type === 'video').length === 0 ? ("""
content = content.replace(old_map, new_map)

old_items_map = """                items.map(item => ("""
new_items_map = """                items.filter(i => i.content_type === 'document' || i.content_type === 'video').map(item => ("""
content = content.replace(old_items_map, new_items_map)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated LessonManagement.jsx")
