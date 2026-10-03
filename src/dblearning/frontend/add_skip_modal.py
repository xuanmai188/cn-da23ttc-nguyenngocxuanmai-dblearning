file_path = "D:/DemoCN2026/dblearning/frontend/src/components/OnboardingModal.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("if (err.response?.status === 404) {\n        onComplete();\n      }", "if (err.response?.status === 404) {\n        await recommendationApi.skipOnboarding();\n        onComplete();\n      }")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated OnboardingModal.jsx")
