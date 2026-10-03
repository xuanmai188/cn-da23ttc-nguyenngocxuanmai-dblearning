file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_methods = """
  // Surveys
  getSurveys: () => axiosClient.get('/admin/surveys'),
  createSurvey: (data) => axiosClient.post('/admin/surveys', data),
  updateSurvey: (id, data) => axiosClient.put(`/admin/surveys/${id}`, data),
  deleteSurvey: (id) => axiosClient.delete(`/admin/surveys/${id}`),
  activateSurvey: (id) => axiosClient.post(`/admin/surveys/${id}/activate`),
  
  // Survey Questions
  getSurveyQuestions: (surveyId) => axiosClient.get(`/admin/surveys/${surveyId}/questions`),
  createSurveyQuestion: (surveyId, data) => axiosClient.post(`/admin/surveys/${surveyId}/questions`, data),
  deleteSurveyQuestion: (questionId) => axiosClient.delete(`/admin/questions/${questionId}`),
"""

if "getSurveys:" not in content:
    content = content.replace(
        "export const adminApi = {",
        "export const adminApi = {\n" + new_methods
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Updated adminApi.js")
