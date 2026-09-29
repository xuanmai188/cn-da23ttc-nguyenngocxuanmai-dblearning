with open("D:/DemoCN2026/dblearning/frontend/src/pages/Dashboard.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if "Chuỗi" in line or "ngày" in line:
            print(f"{i-2}: {lines[i-2].strip()}")
            print(f"{i-1}: {lines[i-1].strip()}")
            print(f"{i}: {line.strip()}")
            print(f"{i+1}: {lines[i+1].strip()}")
            print(f"{i+2}: {lines[i+2].strip()}")
            print("-" * 20)
