import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add useNavigate import if not exists
if "useNavigate" not in content:
    content = content.replace(
        "import { useState, useEffect } from 'react';",
        "import { useState, useEffect } from 'react';\nimport { useNavigate } from 'react-router-dom';"
    )

# Add navigate instance inside component
if "const navigate = useNavigate();" not in content:
    content = content.replace(
        "export default function AdminDashboard() {",
        "export default function AdminDashboard() {\n  const navigate = useNavigate();"
    )

# Replace the 3 buttons
# 1. Sinh viên
content = re.sub(
    r'<div className="flex items-center gap-2">\s*<TrophyIcon className="w-5 h-5 text-amber-500" />\s*<h2 className="text-lg font-bold text-slate-800">Sinh viAn hot `Tng nhi?u nht</h2>\s*</div>\s*<button onClick=\{\(\) => alert\("TA-nh nAng xem chi tit `ang `?c phAt trin"\)\} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">Xem tt c &rarr;</button>',
    r'<div className="flex items-center gap-2">\n              <TrophyIcon className="w-5 h-5 text-amber-500" />\n              <h2 className="text-lg font-bold text-slate-800">Sinh viên hoạt động nhiều nhất</h2>\n            </div>\n            <button onClick={() => navigate("/admin/users")} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">Xem tất cả &rarr;</button>',
    content, flags=re.DOTALL
)

# 2. Bài học
content = re.sub(
    r'<div className="flex items-center gap-2">\s*<FireIcon className="w-5 h-5 text-red-500" />\s*<h2 className="text-lg font-bold text-slate-800">BAi h?c truy c-p nhi?u nht</h2>\s*</div>\s*<button onClick=\{\(\) => alert\("TA-nh nAng xem chi tit `ang `?c phAt trin"\)\} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">Xem tt c &rarr;</button>',
    r'<div className="flex items-center gap-2">\n              <FireIcon className="w-5 h-5 text-red-500" />\n              <h2 className="text-lg font-bold text-slate-800">Bài học truy cập nhiều nhất</h2>\n            </div>\n            <button onClick={() => navigate("/admin/content")} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">Xem tất cả &rarr;</button>',
    content, flags=re.DOTALL
)

# 3. Hoạt động gần đây
content = re.sub(
    r'<div className="flex items-center gap-2">\s*<ClockIcon className="w-5 h-5 text-blue-600" />\s*<h2 className="text-lg font-bold text-slate-800">Hot `Tng g n `Ay</h2>\s*</div>\s*<button onClick=\{\(\) => alert\("TA-nh nAng xem chi tit `ang `?c phAt trin"\)\} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">Xem tt c &rarr;</button>',
    r'<div className="flex items-center gap-2">\n              <ClockIcon className="w-5 h-5 text-blue-600" />\n              <h2 className="text-lg font-bold text-slate-800">Hoạt động gần đây</h2>\n            </div>\n            <button onClick={() => navigate("/admin/reports")} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">Xem tất cả &rarr;</button>',
    content, flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated AdminDashboard.jsx with proper navigation links")
