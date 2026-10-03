file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Replace user_growth_rate calculation
content = re.sub(
    r"user_growth_rate = \(\(users_last_30 - users_prev_30\).*?\n",
    "user_growth_rate = users_last_30\n",
    content
)

# Replace item_growth_rate calculation
content = re.sub(
    r"item_growth_rate = \(\(items_last_30 - items_prev_30\).*?\n",
    "item_growth_rate = items_last_30\n",
    content
)

# Replace quiz_growth_rate calculation
content = re.sub(
    r"quiz_growth_rate = \(\(quizzes_last_30 - quizzes_prev_30\).*?\n",
    "quiz_growth_rate = quizzes_last_30\n",
    content
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated admin.py stats calculation")
