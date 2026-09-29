file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "deleteTopic: (id) => axiosClient.delete(`/admin/topics/${id}`)\n  getTopicLearningChart",
    "deleteTopic: (id) => axiosClient.delete(`/admin/topics/${id}`),\n  getTopicLearningChart"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed missing comma in adminApi.js")
