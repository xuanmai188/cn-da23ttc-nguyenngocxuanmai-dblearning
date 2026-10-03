import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the notification button
# Original: <button className="relative p-2 text-slate-500 hover:text-slate-700 transition-colors rounded-full hover:bg-slate-100">
# New: <button onClick={() => alert('Tính năng quản lý Thông báo đang được phát triển!')} className="relative p-2 text-slate-500 hover:text-slate-700 transition-colors rounded-full hover:bg-slate-100">

content = content.replace(
    '<button className="relative p-2 text-slate-500 hover:text-slate-700 transition-colors rounded-full hover:bg-slate-100">',
    '<button onClick={() => alert(\'Tính năng quản lý Thông báo đang được phát triển!\')} className="relative p-2 text-slate-500 hover:text-slate-700 transition-colors rounded-full hover:bg-slate-100">'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added onClick to notification bell")
