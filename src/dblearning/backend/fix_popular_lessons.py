file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# get_popular_lessons has no 'limit' parameter, so we find its body and replace .limit(limit) back to .limit(5)
idx = content.find("def get_popular_lessons")
idx_end = content.find("def get_recent_activities", idx)

if idx != -1 and idx_end != -1:
    section = content[idx:idx_end]
    section = section.replace(".limit(limit).all()", ".limit(5).all()")
    content = content[:idx] + section + content[idx_end:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed limit error in get_popular_lessons")
