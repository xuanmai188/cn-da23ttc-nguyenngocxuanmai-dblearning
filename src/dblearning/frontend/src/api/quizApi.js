import axiosClient from './axiosClient';

export const quizApi = {
  getFlashcards: (itemId) => axiosClient.get("/quiz/flashcards/item/" + itemId),
  getQuiz: (quizId) => axiosClient.get("/quiz/item/" + quizId),
  submitQuiz: (quizId, answers, timeSpentSeconds = 0) => axiosClient.post("/quiz/item/" + quizId + "/submit", { answers: answers, time_spent_seconds: timeSpentSeconds }),
  logFlashcard: (flashcardId, result, responseTimeMs) => axiosClient.post("/quiz/flashcards/log", { flashcard_id: flashcardId, result: result, response_time_ms: responseTimeMs }),
  getQuizHistory: (itemId) => axiosClient.get("/quiz/item/" + itemId + "/history")
};