import base64
import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add useNavigate
if "useNavigate" not in content:
    content = content.replace(
        "import { useState, useEffect } from 'react';",
        "import { useState, useEffect } from 'react';\nimport { useNavigate } from 'react-router-dom';"
    )
if "const navigate = useNavigate();" not in content:
    content = content.replace(
        "export default function AdminDashboard() {",
        "export default function AdminDashboard() {\n  const navigate = useNavigate();"
    )

search_str = b'onClick={() => alert("T\xc3\xadnh n\xc4\x83ng xem t\xc3\xa2\xcc\x81t ca\xcc\x89 \xc4\x91ang \xc4\x91\xc6\xb0\xc6\xa1\xcc\xa3c pha\xcc\x81t tri\xc3\xaa\xcc\x89n")}'
try:
    search_str = search_str.decode('utf-8')
except:
    pass

# Replace by occurrences
parts = content.split('onClick={() => alert("Tính năng xem tất cả đang được phát triển")}')
if len(parts) == 4:
    content = parts[0] + 'onClick={() => navigate("/admin/users")}' + parts[1] + 'onClick={() => navigate("/admin/content")}' + parts[2] + 'onClick={() => navigate("/admin/reports")}' + parts[3]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated via exact string match!")
else:
    # Try regex with wildcards for Vietnamese chars
    content = re.sub(
        r'onClick=\{\(\) => alert\("T.nh n.ng xem t.t c. \x11ang \x11.c ph.t tri.n"\)\}',
        'onClick={() => navigate("/admin/users")}',
        content, count=1
    )
    content = re.sub(
        r'onClick=\{\(\) => alert\("T.nh n.ng xem t.t c. \x11ang \x11.c ph.t tri.n"\)\}',
        'onClick={() => navigate("/admin/content")}',
        content, count=1
    )
    content = re.sub(
        r'onClick=\{\(\) => alert\("T.nh n.ng xem t.t c. \x11ang \x11.c ph.t tri.n"\)\}',
        'onClick={() => navigate("/admin/reports")}',
        content, count=1
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated via regex fallback!")
