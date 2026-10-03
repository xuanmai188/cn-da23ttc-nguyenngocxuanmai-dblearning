file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

funcs = """
  // Content Management - Quizzes
  getQuizzes: async (params) => {
    const response = await axiosClient.get('/admin/quizzes', { params });
    return response.data;
  },
  createQuiz: async (data) => {
    const response = await axiosClient.post('/admin/quizzes', data);
    return response.data;
  },
  updateQuiz: async (id, data) => {
    const response = await axiosClient.put(`/admin/quizzes/${id}`, data);
    return response.data;
  },
  deleteQuiz: async (id) => {
    const response = await axiosClient.delete(`/admin/quizzes/${id}`);
    return response.data;
  },
"""

content = content.replace("  // Content Management", funcs + "  // Content Management")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js for quizzes")
