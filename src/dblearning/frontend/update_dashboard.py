import os

file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Dashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace total_score with avg_quiz_score
content = content.replace("<p className=\"text-primary-100 text-sm\">Tng im</p>", "<p className=\"text-primary-100 text-sm\">Điểm TB Quiz</p>")
content = content.replace("profile?.total_score || 0", "profile?.avg_quiz_score ? Math.round(profile.avg_quiz_score) : 0")

# Replace completed_items?.length with total_items_completed
content = content.replace("profile?.completed_items?.length || 0", "profile?.total_items_completed || 0")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Dashboard.jsx updated")
