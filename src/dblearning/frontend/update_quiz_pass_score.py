file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/content/QuizManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Update Modal label
content = content.replace("Điểm đạt (/100)", "Tỷ lệ đỗ tối thiểu (%)")

# Update Table Header
content = content.replace("<th className=\"px-6 py-4\">Điểm đạt</th>", "<th className=\"px-6 py-4\">Tỷ lệ đỗ</th>")

# Update Table cell
content = content.replace("{quiz.pass_score}/100", "{quiz.pass_score}%")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated QuizManagement.jsx UI for pass_score")
