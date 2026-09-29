import json
import urllib.request

# Check how a naive datetime is serialized by running a quick test against the backend directly
# But wait, we can just fix the frontend to add Z if it doesn't end with Z
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Quiz.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("new Date(h.taken_at).toLocaleDateString", "new Date(h.taken_at + (!h.taken_at.endsWith('Z') ? 'Z' : '')).toLocaleDateString")
content = content.replace("new Date(h.taken_at).toLocaleTimeString", "new Date(h.taken_at + (!h.taken_at.endsWith('Z') ? 'Z' : '')).toLocaleTimeString")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Quiz.jsx time timezone fixed")
