file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
if "getStatistics" in content or "stats" in content.lower():
    print("Found stats references in adminApi.js:")
    for line in content.split("\n"):
        if "stats" in line.lower() or "statistics" in line.lower():
            print(line)
else:
    print("No stats references in adminApi.js")
