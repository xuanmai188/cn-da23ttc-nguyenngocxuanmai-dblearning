file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add import
if "import FlashcardManagement" not in content:
    content = content.replace(
        "import QuizManagement from '../../components/admin/content/QuizManagement';",
        "import QuizManagement from '../../components/admin/content/QuizManagement';\nimport FlashcardManagement from '../../components/admin/content/FlashcardManagement';"
    )

# Add early return
old_return = """  if (currentTab === 'quiz') {
    return <QuizManagement />;
  }"""

new_return = """  if (currentTab === 'quiz') {
    return <QuizManagement />;
  }

  if (currentTab === 'flashcards') {
    return <FlashcardManagement />;
  }"""

if "currentTab === 'flashcards'" not in content:
    content = content.replace(old_return, new_return)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added FlashcardManagement return to ContentManagement.jsx")
