file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Dashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "<p className=\"text-2xl font-bold\">1 ngAy</p>",
    "<p className=\"text-2xl font-bold\">{profile?.learning_streak || 1} ngày</p>"
)

# just in case it wasn't the weird utf8 string
content = content.replace(
    "<p className=\"text-2xl font-bold\">1 ngày</p>",
    "<p className=\"text-2xl font-bold\">{profile?.learning_streak || 1} ngày</p>"
)

# Handle the utf-8 corrupted one we saw in python print:
content = content.replace(
    "<p className=\"text-2xl font-bold\">1 ng\u00e0y</p>",
    "<p className=\"text-2xl font-bold\">{profile?.learning_streak || 1} ngày</p>"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Dashboard.jsx updated")
