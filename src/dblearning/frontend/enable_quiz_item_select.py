file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/content/QuizManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Remove disabled={!!editingQuiz}
content = content.replace("                  disabled={!!editingQuiz}\n", "")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Removed disabled from item_id select in QuizManagement.jsx")
