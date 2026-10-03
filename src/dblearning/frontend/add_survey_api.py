file_path = "D:/DemoCN2026/dblearning/frontend/src/api/recommendationApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_methods = """
  // Dynamic Survey
  getActiveSurvey: () => axiosClient.get('/survey/active'),
  submitSurvey: (surveyId, data) => axiosClient.post(`/survey/${surveyId}/submit`, data),
"""

if "getActiveSurvey" not in content:
    content = content.replace(
        "export const recommendationApi = {",
        "export const recommendationApi = {\n" + new_methods
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Updated recommendationApi.js")
