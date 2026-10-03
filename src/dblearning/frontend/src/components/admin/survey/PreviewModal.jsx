import React from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';

export default function PreviewModal({ survey, questions, onClose }) {
  if (!survey) return null;

  return (
    <div className="fixed inset-0 z-[70] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[90vh] flex flex-col animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header (Admin specific, not visible to student) */}
        <div className="bg-indigo-600 text-white px-6 py-3 rounded-t-2xl flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2">
            <span className="bg-white/20 text-xs px-2 py-1 rounded font-bold tracking-wider uppercase">Chế độ xem trước</span>
            <span className="font-medium">Đây là cách sinh viên sẽ nhìn thấy bài khảo sát</span>
          </div>
          <button onClick={onClose} className="p-1 hover:bg-white/20 rounded-lg transition-colors">
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>

        {/* Fake Student View Container */}
        <div className="flex-1 overflow-y-auto bg-gray-50 p-6 md:p-10">
          <div className="bg-white rounded-2xl shadow-lg p-8 max-w-2xl mx-auto border border-gray-100">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">{survey.title}</h2>
            {survey.description && (
              <p className="text-gray-600 mb-8">{survey.description}</p>
            )}

            <div className="space-y-8">
              {questions.length === 0 ? (
                <p className="text-gray-500 italic">Chưa có câu hỏi nào trong bộ khảo sát này.</p>
              ) : (
                questions.map((q, index) => {
                  const isMultiple = q.question_type === 'multiple_choice';

                  return (
                    <div key={q.id} className="border-b border-gray-100 pb-6 last:border-0 last:pb-0">
                      <h3 className="text-lg font-semibold text-gray-800 mb-4">
                        {index + 1}. {q.content}
                        {q.is_required && <span className="text-red-500 ml-1">*</span>}
                      </h3>
                      
                      {q.question_type === 'text' ? (
                        <textarea
                          disabled
                          className="w-full border border-gray-300 rounded-lg p-3 bg-gray-50"
                          rows={3}
                          placeholder="Nhập câu trả lời của bạn..."
                        />
                      ) : (
                        <div className={`grid gap-3 ${q.options && q.options.length > 4 ? 'grid-cols-1 sm:grid-cols-2' : 'grid-cols-1'}`}>
                          {q.options && q.options.map((opt, oIdx) => (
                            <div 
                              key={oIdx}
                              className="rounded-xl p-4 border-2 border-gray-200 flex items-center gap-3 bg-white"
                            >
                              <div className={`w-5 h-5 flex-shrink-0 border-2 border-gray-300 ${isMultiple ? 'rounded' : 'rounded-full'}`}>
                              </div>
                              <div className="font-medium text-gray-700">
                                {opt.content}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>

            <div className="flex justify-end mt-8 pt-6 border-t border-gray-100">
              <button disabled className="px-8 py-3 rounded-lg font-bold text-white bg-blue-600 opacity-50 cursor-not-allowed">
                Hoàn thành Khảo sát
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
