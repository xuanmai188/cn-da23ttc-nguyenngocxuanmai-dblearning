file_path = "C:/Users/pc/.gemini/antigravity-ide/brain/ececc0bd-480a-4632-b797-c6cb0840346f/task.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("- [ ] Install `recharts`.", "- [x] Install `recharts`.")
content = content.replace("- [ ] Add new schemas", "- [x] Add new schemas")
content = content.replace("- [ ] Add new endpoints", "- [x] Add new endpoints")
content = content.replace("- [ ] Update `frontend/src/api/adminApi.js`.", "- [x] Update `frontend/src/api/adminApi.js`.")
content = content.replace("- [ ] Update `frontend/src/pages/admin/AdminDashboard.jsx`", "- [x] Update `frontend/src/pages/admin/AdminDashboard.jsx`")
content = content.replace("- [ ] Create `frontend/src/pages/admin/ContentManagement.jsx`", "- [x] Create `frontend/src/pages/admin/ContentManagement.jsx`")
content = content.replace("- [ ] Update `frontend/src/components/AdminLayout.jsx`", "- [x] Update `frontend/src/components/AdminLayout.jsx`")
content = content.replace("- [ ] Update `frontend/src/App.jsx`", "- [x] Update `frontend/src/App.jsx`")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Task list updated")
