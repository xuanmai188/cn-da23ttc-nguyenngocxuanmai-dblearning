import sys
file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/admin.py"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        has_stats = False
        for i, line in enumerate(lines):
            if "dashboard_stats" in line or "statistics" in line:
                start = max(0, i-2)
                for j in range(start, min(len(lines), start+15)):
                    try:
                        sys.stdout.buffer.write(f"{j+1}: {lines[j]}".encode("utf-8"))
                    except:
                        pass
                print("---")
                has_stats = True
        if not has_stats:
            print("No stats endpoints found in admin.py")
except Exception as e:
    print(e)
