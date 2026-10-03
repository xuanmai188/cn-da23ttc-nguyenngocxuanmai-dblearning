file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix time_ago in get_recent_activities
old_time_str = 'time_str = f"{mins_ago} phút trước" if mins_ago < 60 else f"{mins_ago // 60} giờ trước"'
new_time_str = 'time_str = f"{mins_ago} phút trước" if mins_ago < 60 else (f"{mins_ago // 60} giờ trước" if mins_ago < 1440 else f"{mins_ago // 1440} ngày trước")'

content = content.replace(old_time_str, new_time_str)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py time_ago logic")
