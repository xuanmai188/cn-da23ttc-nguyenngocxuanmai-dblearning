file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(file_path, "w", encoding="utf-8") as f:
    for line in lines:
        if "Quản lý gợi ý AI" not in line:
            f.write(line)
print("Removed AI menu item")
