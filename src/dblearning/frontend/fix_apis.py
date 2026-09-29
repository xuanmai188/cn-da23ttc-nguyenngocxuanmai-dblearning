import os

file_path = "D:/DemoCN2026/dblearning/frontend/src/api/quizApi.js"
content = """import axiosClient from './axiosClient';

export const quizApi = {
  getFlashcards: (itemId) => axiosClient.get("/quiz/flashcards/item/" + itemId),
  getQuiz: (quizId) => axiosClient.get("/quiz/item/" + quizId),
  submitQuiz: (quizId, answers, timeSpentSeconds = 0) => axiosClient.post("/quiz/item/" + quizId + "/submit", { answers: answers, time_spent_seconds: timeSpentSeconds }),
  logFlashcard: (flashcardId, result, responseTimeMs) => axiosClient.post("/quiz/flashcards/log", { flashcard_id: flashcardId, result: result, response_time_ms: responseTimeMs }),
  getQuizHistory: (itemId) => axiosClient.get("/quiz/item/" + itemId + "/history")
};"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

file_path2 = "D:/DemoCN2026/dblearning/frontend/src/api/learningApi.js"
with open(file_path2, "r", encoding="utf-8") as f:
    content2 = f.read()

if "getCompletedItems" not in content2:
    # Just append it before the last closing brace
    content2 = content2.replace("\n};", ",\n  getCompletedItems: () => axiosClient.get(\"/learning/completed-items\")\n};")
    with open(file_path2, "w", encoding="utf-8") as f:
        f.write(content2)

print("Fixed APIs")
