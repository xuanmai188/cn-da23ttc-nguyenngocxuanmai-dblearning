file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserFormModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    if "EyeIcon" in f.read():
        print("EyeIcon found!")
    else:
        print("No EyeIcon.")
