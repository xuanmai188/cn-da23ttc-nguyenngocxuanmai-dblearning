file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

new_endpoints = """  deleteQuiz: (id) => axiosClient.delete(`/admin/quizzes/${id}`),
  
  // Questions
  getQuestionsByQuiz: (quizId) => axiosClient.get(`/admin/quizzes/${quizId}/questions`),
  createQuestion: (quizId, data) => axiosClient.post(`/admin/quizzes/${quizId}/questions`, data),
  updateQuestion: (id, data) => axiosClient.put(`/admin/questions/${id}`, data),
  deleteQuestion: (id) => axiosClient.delete(`/admin/questions/${id}`),"""

content = content.replace("  deleteQuiz: (id) => axiosClient.delete(`/admin/quizzes/${id}`),", new_endpoints)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js with Question endpoints")
