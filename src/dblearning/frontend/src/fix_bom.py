import os

files = [
    'D:/DemoCN2026/dblearning/frontend/src/api/quizApi.js',
    'D:/DemoCN2026/dblearning/frontend/src/api/learningApi.js',
    'D:/DemoCN2026/dblearning/frontend/src/pages/LearningPath.jsx',
    'D:/DemoCN2026/dblearning/frontend/src/components/Layout.jsx'
]

for file in files:
    with open(file, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print("Removed BOM from all files.")
