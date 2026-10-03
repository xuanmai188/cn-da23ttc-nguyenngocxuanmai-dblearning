file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# We need to find this block and replace it:
old_block = """  if (currentTab === 'quiz') {
    return <QuizManagement />;
  }"""

new_block = """  if (currentTab === 'quiz') {
    return <QuizManagement />;
  }

  if (currentTab === 'flashcards') {
    return <FlashcardManagement />;
  }"""

if "return <FlashcardManagement />;" not in content:
    content = content.replace(old_block, new_block)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed ContentManagement.jsx")
else:
    print("Already fixed.")
