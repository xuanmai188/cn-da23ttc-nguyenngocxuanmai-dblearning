import os

backend_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(backend_path, "r", encoding="utf-8") as f:
    content = f.read()
    
endpoints = ["/topics", "/items", "/quizzes", "/flashcards", "/documents"]
for ep in endpoints:
    if ep in content:
        print(f"Found endpoint: {ep}")
    else:
        print(f"NOT found: {ep}")
