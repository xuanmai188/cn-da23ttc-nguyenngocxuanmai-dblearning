file_path = "D:/DemoCN2026/dblearning/frontend/src/api/recommendationApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_func = "  getProfile: () => axiosClient.get('/recommendations/profile'),\n  submitOnboarding: (data) => axiosClient.post('/recommendations/onboarding', data)"
content = content.replace("  getProfile: () => axiosClient.get('/recommendations/profile')", new_func)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("recommendationApi.js updated")
