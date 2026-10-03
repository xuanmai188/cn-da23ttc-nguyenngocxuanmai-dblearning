file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_methods = """
  getSurveyStats: () => axiosClient.get('/admin/surveys/stats/overview'),
"""

if "getSurveyStats:" not in content:
    content = content.replace(
        "getSurveys: () => axiosClient.get('/admin/surveys'),",
        "getSurveys: () => axiosClient.get('/admin/surveys'),\n" + new_methods
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Updated adminApi.js")
