import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    if "useSearchParams" in content or "location.search" in content:
        print("Tab logic found!")
    else:
        print("No tab logic found.")
