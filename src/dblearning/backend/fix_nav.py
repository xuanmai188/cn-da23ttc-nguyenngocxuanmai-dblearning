import os

# Fix Flashcard.jsx
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Flashcard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("navigate(-1); // Quay lại trang trước", "navigate('/topics');")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

# Fix Quiz.jsx
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Quiz.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("onClick={() => navigate(-1)}", "onClick={() => navigate('/topics')}")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Navigation fixed in Flashcard and Quiz")
