import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "getFullStatistics" in content:
            print("Found getFullStatistics!")
        else:
            print("MISSING getFullStatistics!")
except Exception as e:
    print(e)
