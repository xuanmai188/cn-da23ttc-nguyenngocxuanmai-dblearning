file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix get_users
idx1 = content.find("def get_users")
idx1_end = content.find("return {", idx1)
if idx1 != -1 and idx1_end != -1:
    section1 = content[idx1:idx1_end]
    section1 = section1.replace(".limit(5).all()", ".limit(limit).all()")
    content = content[:idx1] + section1 + content[idx1_end:]

# Fix get_items
idx2 = content.find("def get_items")
idx2_end = content.find("@router.post(\"/items\"", idx2)
if idx2 != -1 and idx2_end != -1:
    section2 = content[idx2:idx2_end]
    section2 = section2.replace(".limit(5).all()", ".limit(limit).all()")
    content = content[:idx2] + section2 + content[idx2_end:]

# Fix get_quizzes
idx3 = content.find("def get_quizzes")
idx3_end = content.find("@router.post(\"/quizzes\"", idx3)
if idx3 != -1 and idx3_end != -1:
    section3 = content[idx3:idx3_end]
    section3 = section3.replace(".limit(5).all()", ".limit(limit).all()")
    content = content[:idx3] + section3 + content[idx3_end:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Restored correct limit variable in get_users, get_items, and get_quizzes")
