file_path = "C:/Users/pc/.gemini/antigravity-ide/brain/ececc0bd-480a-4632-b797-c6cb0840346f/task.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("- [ ] Elevate current user to `admin` in DB.", "- [x] Elevate current user to `admin` in DB.")
content = content.replace("- [ ] Create `backend/app/schemas/admin.py`", "- [x] Create `backend/app/schemas/admin.py`")
content = content.replace("- [ ] Create `backend/app/api/endpoints/admin.py`", "- [x] Create `backend/app/api/endpoints/admin.py`")
content = content.replace("- [ ] Register `/api/admin` router", "- [x] Register `/api/admin` router")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Task list updated")
