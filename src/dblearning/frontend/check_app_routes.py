file_path = "D:/DemoCN2026/dblearning/frontend/src/App.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    for line in f.readlines():
        if "/admin/onboarding" in line or "Onboarding" in line:
            print(line.strip())
