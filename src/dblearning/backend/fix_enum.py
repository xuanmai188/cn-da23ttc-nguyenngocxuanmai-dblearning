import os

file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('rec_type = Column(Enum("content", "path", "review"), default="content")', 'rec_type = Column(Enum("content", "path", "review", "cold_start"), default="content")')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("models.py updated with cold_start")
