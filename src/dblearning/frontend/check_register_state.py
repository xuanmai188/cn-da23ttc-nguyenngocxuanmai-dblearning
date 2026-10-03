import sys
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Register.jsx"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        if "confirmPasswordError" in content:
            print("confirmPasswordError is defined in Register.jsx")
        else:
            print("confirmPasswordError is MISSING in Register.jsx")
except Exception as e:
    print(e)
