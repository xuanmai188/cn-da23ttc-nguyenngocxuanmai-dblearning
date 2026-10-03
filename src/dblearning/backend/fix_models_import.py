import re

file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "from datetime import datetime" not in content:
    content = "from datetime import datetime\n" + content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Added datetime import to models.py")
else:
    print("datetime already imported")
