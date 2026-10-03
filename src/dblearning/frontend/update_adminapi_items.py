file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Add item and quiz endpoints
if "getItems:" not in content:
    new_endpoints = """  deleteTopic: (id) => axiosClient.delete(`/admin/topics/${id}`),
  
  // Learning Items
  getItems: (params) => axiosClient.get('/admin/items', { params }),
  createItem: (data) => axiosClient.post('/admin/items', data),
  updateItem: (id, data) => axiosClient.put(`/admin/items/${id}`, data),
  deleteItem: (id) => axiosClient.delete(`/admin/items/${id}`),
  
  // Quizzes
  getQuizzes: (params) => axiosClient.get('/admin/quizzes', { params }),
  createQuiz: (data) => axiosClient.post('/admin/quizzes', data),
  updateQuiz: (id, data) => axiosClient.put(`/admin/quizzes/${id}`, data),
  deleteQuiz: (id) => axiosClient.delete(`/admin/quizzes/${id}`),"""
    
    content = content.replace("  deleteTopic: (id) => axiosClient.delete(`/admin/topics/${id}`),", new_endpoints)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated adminApi.js")
else:
    print("Already updated")
