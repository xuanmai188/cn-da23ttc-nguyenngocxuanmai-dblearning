import os

file_path = "D:/DemoCN2026/dblearning/frontend/src/api/quizApi.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "getQuizHistory" not in content:
    content = content.replace("submitQuiz: (itemId, data) => axiosClient.post(\"/quiz/item/\" + itemId + \"/submit\", data),", "submitQuiz: (itemId, data) => axiosClient.post(\"/quiz/item/\" + itemId + \"/submit\", data),\n  getQuizHistory: (itemId) => axiosClient.get(\"/quiz/item/\" + itemId + \"/history\"),")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

file_path2 = "D:/DemoCN2026/dblearning/frontend/src/api/learningApi.js"
with open(file_path2, "r", encoding="utf-8") as f:
    content2 = f.read()

if "getCompletedItems" not in content2:
    content2 = content2.replace("endSession: (sessionId) => axiosClient.put(\"/learning/sessions/\" + sessionId, { status: \"completed\" }),", "endSession: (sessionId) => axiosClient.put(\"/learning/sessions/\" + sessionId, { status: \"completed\" }),\n  getCompletedItems: () => axiosClient.get(\"/learning/completed-items\"),")
    with open(file_path2, "w", encoding="utf-8") as f:
        f.write(content2)

print("Updated API clients")
