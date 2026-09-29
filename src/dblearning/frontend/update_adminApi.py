file_path = "D:/DemoCN2026/dblearning/frontend/src/api/adminApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the closing brace with the new endpoints and closing brace
new_endpoints = """  getTopicLearningChart: () => axiosClient.get('/admin/charts/topic-learning'),
  getPerformanceStats: () => axiosClient.get('/admin/performance'),
  getActiveStudents: () => axiosClient.get('/admin/active-students'),
  getPopularLessons: () => axiosClient.get('/admin/popular-lessons'),
  getRecentActivities: () => axiosClient.get('/admin/recent-activities'),
};"""

content = content.replace("};", new_endpoints)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated adminApi.js")
