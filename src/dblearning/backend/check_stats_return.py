import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        in_stats = False
        count = 0
        for i, line in enumerate(lines):
            if "def get_user_stats" in line or "def get_performance_stats" in line:
                in_stats = True
                count = 0
            if in_stats:
                try:
                    sys.stdout.buffer.write(line.encode("utf-8"))
                except:
                    pass
                count += 1
                if count > 20 and "return" in line:
                    in_stats = False
                    print("---")
except Exception as e:
    print(e)
