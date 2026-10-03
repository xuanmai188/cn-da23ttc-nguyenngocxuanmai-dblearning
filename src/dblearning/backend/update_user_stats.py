file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

old_growth = """    users_last_30 = db.query(User).filter(User.created_at >= thirty_days_ago).count()
    users_prev_30 = db.query(User).filter(User.created_at >= sixty_days_ago, User.created_at < thirty_days_ago).count()
    growth_rate = ((users_last_30 - users_prev_30) / users_prev_30 * 100) if users_prev_30 > 0 else (100.0 if users_last_30 > 0 else 0.0)"""

new_growth = """    users_last_30 = db.query(User).filter(User.created_at >= thirty_days_ago).count()
    users_prev_30 = db.query(User).filter(User.created_at >= sixty_days_ago, User.created_at < thirty_days_ago).count()
    growth_rate = users_last_30"""

content = content.replace(old_growth, new_growth)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py /users/stats growth_rate calculation")
