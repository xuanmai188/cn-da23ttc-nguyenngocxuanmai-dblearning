file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Add import for QuizManagement
if "QuizManagement" not in content:
    content = content.replace("import LessonManagement from '../../components/admin/content/LessonManagement';", "import LessonManagement from '../../components/admin/content/LessonManagement';\nimport QuizManagement from '../../components/admin/content/QuizManagement';")

target = """  if (currentTab === 'items') {
    return <LessonManagement />;
  }"""

new_block = """  if (currentTab === 'items') {
    return <LessonManagement />;
  }
  if (currentTab === 'quiz') {
    return <QuizManagement />;
  }"""

content = content.replace(target, new_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated ContentManagement to route to QuizManagement.")
