import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { recommendationApi } from '../api/recommendationApi';

export default function OnboardingModal({ onComplete }) {
  const [survey, setSurvey] = useState(null);
  const [loading, setLoading] = useState(true);
  const [answers, setAnswers] = useState({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchActiveSurvey();
  }, []);

  const fetchActiveSurvey = async () => {
    try {
      const data = await recommendationApi.getActiveSurvey();
      setSurvey(data);
    } catch (err) {
      console.error("Lỗi lấy survey:", err);
      // Nếu không có khảo sát nào đang hoạt động, có thể bỏ qua onboarding
      if (err.response?.status === 404) {
        await recommendationApi.skipOnboarding();
        onComplete();
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (questionId, optionId, isMultiple) => {
    setAnswers(prev => {
      const current = prev[questionId] || [];
      if (isMultiple) {
        if (current.includes(optionId)) {
          return { ...prev, [questionId]: current.filter(id => id !== optionId) };
        } else {
          return { ...prev, [questionId]: [...current, optionId] };
        }
      } else {
        return { ...prev, [questionId]: [optionId] };
      }
    });
  };

  const handleTextChange = (questionId, text) => {
    setAnswers(prev => ({ ...prev, [questionId]: text }));
  };

  const handleSubmit = async () => {
    if (!survey) return;
    
    // Validate required questions
    for (const q of survey.questions) {
      if (q.is_required) {
        const ans = answers[q.id];
        if (!ans || (Array.isArray(ans) && ans.length === 0) || (typeof ans === 'string' && ans.trim() === '')) {
          alert('Vui lòng trả lời đầy đủ các câu hỏi bắt buộc.');
          return;
        }
      }
    }

    setSubmitting(true);
    
    // Format payload
    const formattedAnswers = Object.keys(answers).map(qId => {
      const q = survey.questions.find(x => x.id === parseInt(qId));
      const ans = answers[qId];
      if (q.question_type === 'text') {
        return { question_id: parseInt(qId), option_ids: [], text_value: ans };
      } else {
        return { question_id: parseInt(qId), option_ids: ans, text_value: null };
      }
    });

    try {
      await recommendationApi.submitSurvey(survey.id, { answers: formattedAnswers });
      onComplete();
    } catch (err) {
      console.error(err);
      alert("Đã xảy ra lỗi khi lưu kết quả khảo sát.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
      </div>
    );
  }

  if (!survey) {
    return null; // Will trigger onComplete directly in useEffect
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 py-10 overflow-y-auto">
      <motion.div 
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-white rounded-2xl shadow-2xl p-8 max-w-3xl w-full my-auto"
      >
        <h2 className="text-3xl font-bold text-gray-900 mb-2">{survey.title}</h2>
        {survey.description && (
          <p className="text-gray-600 mb-8">{survey.description}</p>
        )}

        <div className="space-y-8">
          {survey.questions.map((q, index) => {
            const isMultiple = q.question_type === 'multiple_choice';
            const currentAns = answers[q.id] || [];

            return (
              <div key={q.id} className="border-b border-gray-100 pb-6 last:border-0 last:pb-0">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  {index + 1}. {q.content}
                  {q.is_required && <span className="text-red-500 ml-1">*</span>}
                </h3>
                
                {q.question_type === 'text' ? (
                  <textarea
                    className="w-full border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                    placeholder="Nhập câu trả lời của bạn..."
                    value={answers[q.id] || ''}
                    onChange={e => handleTextChange(q.id, e.target.value)}
                  />
                ) : (
                  <div className={`grid gap-3 ${q.options.length > 4 ? 'grid-cols-1 sm:grid-cols-2' : 'grid-cols-1'}`}>
                    {q.options.map(opt => {
                      const isSelected = Array.isArray(currentAns) && currentAns.includes(opt.id);
                      return (
                        <div 
                          key={opt.id}
                          onClick={() => handleSelectOption(q.id, opt.id, isMultiple)}
                          className={`cursor-pointer rounded-xl p-4 border-2 transition-all flex items-center gap-3 ${
                            isSelected ? 'border-blue-600 bg-blue-50' : 'border-gray-200 hover:border-blue-300'
                          }`}
                        >
                          <div className={`w-5 h-5 flex-shrink-0 flex items-center justify-center border-2 ${isMultiple ? 'rounded' : 'rounded-full'} ${isSelected ? 'border-blue-600 bg-blue-600' : 'border-gray-300'}`}>
                            {isSelected && <div className={`bg-white ${isMultiple ? 'w-2 h-2' : 'w-2 h-2 rounded-full'}`} />}
                          </div>
                          <div className={`font-medium ${isSelected ? 'text-blue-900' : 'text-gray-700'}`}>
                            {opt.content}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="flex justify-end mt-8 pt-6 border-t border-gray-100">
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className={`px-8 py-3 rounded-lg font-bold text-white transition-all ${
              submitting ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 shadow-lg'
            }`}
          >
            {submitting ? 'Đang xử lý...' : 'Hoàn thành Khảo sát'}
          </button>
        </div>
      </motion.div>
    </div>
  );
}
