file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

old_session_growth = """    session_growth_rate = 0.0
    if yesterday_sessions > 0:
        session_growth_rate = ((today_sessions - yesterday_sessions) / yesterday_sessions) * 100
    elif today_sessions > 0:
        session_growth_rate = 100.0"""

new_session_growth = """    session_growth_rate = today_sessions - yesterday_sessions"""

content = content.replace(old_session_growth, new_session_growth)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated session growth logic")
