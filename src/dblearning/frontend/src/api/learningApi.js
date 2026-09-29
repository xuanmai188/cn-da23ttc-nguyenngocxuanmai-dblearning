import axiosClient from './axiosClient';

export const learningApi = {
  getTopics: () => axiosClient.get('/learning/topics'),
  getTopicDetails: (topicId) => axiosClient.get("/learning/topics/" + topicId),
  getLearningItem: (itemId) => axiosClient.get("/learning/items/" + itemId),
  startSession: (itemId) => axiosClient.post("/learning/sessions", { item_id: itemId }),
  endSession: (sessionId) => axiosClient.put("/learning/sessions/" + sessionId, { status: "completed", completion_rate: 1.0 }),
  getCompletedItems: () => axiosClient.get("/learning/completed-items")
};
