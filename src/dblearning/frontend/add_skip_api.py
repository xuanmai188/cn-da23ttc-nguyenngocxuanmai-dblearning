file_path = "D:/DemoCN2026/dblearning/frontend/src/api/recommendationApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "skipOnboarding:" not in content:
    content = content.replace("getActiveSurvey: () => axiosClient.get('/survey/active'),", "getActiveSurvey: () => axiosClient.get('/survey/active'),\n  skipOnboarding: () => axiosClient.post('/survey/skip'),")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Updated recommendationApi.js")
