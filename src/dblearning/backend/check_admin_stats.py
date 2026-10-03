import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "def get_user_stats" in content:
            print("Found get_user_stats")
        if "def get_performance_stats" in content:
            print("Found get_performance_stats")
except Exception as e:
    print(e)
