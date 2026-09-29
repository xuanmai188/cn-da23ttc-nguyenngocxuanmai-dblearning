# Trigger a change to verify polling works
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/LearningItem.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("// v2-fixed", "// v4-polling-test")
content = content.replace("// v3-fixed", "// v4-polling-test")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("File changed to test polling")
