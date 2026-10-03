file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_endpoints = """  deleteQuestion: (id) => axiosClient.delete(`/admin/questions/${id}`),
  
  // Flashcards
  getFlashcardsByItem: (itemId) => axiosClient.get(`/admin/items/${itemId}/flashcards`),
  createFlashcard: (itemId, data) => axiosClient.post(`/admin/items/${itemId}/flashcards`, data),
  updateFlashcard: (id, data) => axiosClient.put(`/admin/flashcards/${id}`, data),
  deleteFlashcard: (id) => axiosClient.delete(`/admin/flashcards/${id}`),"""

content = content.replace("  deleteQuestion: (id) => axiosClient.delete(`/admin/questions/${id}`),", new_endpoints)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js with Flashcard endpoints")
