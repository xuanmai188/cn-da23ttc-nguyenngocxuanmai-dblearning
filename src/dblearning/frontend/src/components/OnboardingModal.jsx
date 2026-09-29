import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { learningApi } from '../api/learningApi';
import { recommendationApi } from '../api/recommendationApi';

export default function OnboardingModal({ onComplete }) {
  const [topics, setTopics] = useState([]);
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [difficulty, setDifficulty] = useState('beginner');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    learningApi.getTopics().then(setTopics).catch(console.error);
  }, []);

  const toggleTopic = (id) => {
    setSelectedTopics(prev => 
      prev.includes(id) ? prev.filter(t => t !== id) : [...prev, id]
    );
  };

  const handleSubmit = async () => {
    if (selectedTopics.length === 0) return alert("Vui lòng chọn ít nhất 1 chủ đề");
    setLoading(true);
    try {
      await recommendationApi.submitOnboarding({
        preferred_difficulty: difficulty,
        interested_topic_ids: selectedTopics
      });
      onComplete(); // callback to refresh dashboard
    } catch (err) {
      console.error(err);
      alert("Đã xảy ra lỗi khi lưu khảo sát.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <motion.div 
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full"
      >
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Chào mừng bạn đến với DBLearning! 🎉</h2>
        <p className="text-gray-600 mb-8">Để bắt đầu, hãy cho AI biết mục tiêu học tập của bạn để chúng tôi xây dựng lộ trình tốt nhất nhé.</p>

        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">1. Đánh giá mức độ hiện tại của bạn:</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { id: 'beginner', label: 'Người mới bắt đầu', desc: 'Chưa biết gì về Database' },
              { id: 'intermediate', label: 'Đã biết cơ bản', desc: 'Cần củng cố và nâng cao' },
              { id: 'advanced', label: 'Nâng cao', desc: 'Tập trung chuyên sâu' }
            ].map(lvl => (
              <div 
                key={lvl.id}
                onClick={() => setDifficulty(lvl.id)}
                className={`cursor-pointer rounded-xl p-4 border-2 transition-all ${
                  difficulty === lvl.id ? 'border-indigo-600 bg-indigo-50' : 'border-gray-200 hover:border-indigo-300'
                }`}
              >
                <div className="font-semibold text-gray-900">{lvl.label}</div>
                <div className="text-xs text-gray-500 mt-1">{lvl.desc}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">2. Bạn muốn tập trung vào chủ đề nào nhất? (Chọn nhiều)</h3>
          <div className="flex flex-wrap gap-3">
            {topics.map(t => (
              <button
                key={t.id}
                onClick={() => toggleTopic(t.id)}
                className={`px-4 py-2 rounded-full border transition-all ${
                  selectedTopics.includes(t.id) 
                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-md' 
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }`}
              >
                {t.name}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleSubmit}
            disabled={loading || selectedTopics.length === 0}
            className={`px-8 py-3 rounded-lg font-bold text-white transition-all ${
              loading || selectedTopics.length === 0 ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 shadow-lg'
            }`}
          >
            {loading ? 'Đang xử lý...' : 'Bắt đầu hành trình'}
          </button>
        </div>
      </motion.div>
    </div>
  );
}
