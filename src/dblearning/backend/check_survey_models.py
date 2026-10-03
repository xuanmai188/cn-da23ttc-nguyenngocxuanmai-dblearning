file_path = "D:/DemoCN2026/dblearning/backend/app/models/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read().lower()
    
if "survey" in content or "onboarding" in content:
    print("Found survey/onboarding in models.py")
else:
    print("No survey/onboarding found in models.py")
