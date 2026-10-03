file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "getSurveyResults:" not in content:
    content = content.replace(
        "getSurveyStats: () => axiosClient.get('/admin/surveys/stats/overview'),",
        "getSurveyStats: () => axiosClient.get('/admin/surveys/stats/overview'),\n  getSurveyResults: () => axiosClient.get('/admin/surveys/active/results'),"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Updated adminApi.js for survey results")
