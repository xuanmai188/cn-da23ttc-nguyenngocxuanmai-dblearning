file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace all .limit(limit) with .limit(5)
content = content.replace(".limit(limit).all()", ".limit(5).all()")

# Then only inside get_recent_activities, replace it back to limit(limit)
idx = content.find("def get_recent_activities")
idx_end = content.find("@router.", idx)
if idx_end == -1:
    idx_end = len(content)

if idx != -1:
    section = content[idx:idx_end]
    section = section.replace(".limit(5).all()", ".limit(limit).all()")
    content = content[:idx] + section + content[idx_end:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed ALL limit errors in admin.py")
