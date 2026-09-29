with open("D:/DemoCN2026/dblearning/frontend/src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()
    
with open("D:/DemoCN2026/dblearning/frontend/dashboard_streak.txt", "w", encoding="utf-8") as out:
    for i, line in enumerate(lines):
        if "ng" in line and "y" in line and "1" in line: # guessing "1 ngày" or something
            pass
        # let's just dump lines 50 to 90 which likely contain the stats
        if 50 <= i <= 90:
            out.write(f"{i}: {line}")
