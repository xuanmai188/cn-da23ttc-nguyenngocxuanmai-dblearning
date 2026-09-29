file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Dashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "{profile && profile.is_onboarded === false && (",
    "{profile && profile.is_onboarded === false && profile.total_items_completed === 0 && ("
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Dashboard.jsx updated")
