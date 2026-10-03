file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if i == 14:
        new_lines.append("from app.schemas.user import UserCreate, UserUpdate\n")
    
    if "class UserCreate(BaseModel):" in line and i > 500:
        skip = True
    
    if skip and "@router.post" in line:
        skip = False
        
    if not skip:
        new_lines.append(line)

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Removed inline schemas and added proper import in admin.py")
