file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'button className="text-sm font-medium text-blue-600 hover:text-blue-700">Xem tất cả &rarr;</button>',
    'button onClick={() => alert("Tính năng xem tất cả đang được phát triển")} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">Xem tất cả &rarr;</button>'
)

# Wait, Vietnamese encoding might be tricky with "tất cả" in the code. Let's use regex with wildcards for "Xem t"
import re
content = re.sub(
    r'<button\s+className="text-sm font-medium text-blue-600 hover:text-blue-700">([^<]+)&rarr;<\/button>',
    r'<button onClick={() => alert("Tính năng xem chi tiết đang được phát triển")} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">\1&rarr;</button>',
    content
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated AdminDashboard.jsx onClick handlers")
