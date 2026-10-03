import React, { useState, useEffect } from 'react';
import { adminApi } from '../../../api/adminApi';
import { XMarkIcon, PlusIcon, TrashIcon, PencilSquareIcon } from '@heroicons/react/24/outline';

export default function SurveyQuestionsModal({ survey, onClose }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const [isEditing, setIsEditing] = useState(false);
  const [topics, setTopics] = useState([]);
  
  const [formData, setFormData] = useState({
    content: '',
    question_type: 'single_choice',
    category: 'knowledge',
    topic_id: '',
    difficulty: 'beginner',
    is_required: true,
    weight: 1.0,
    order_index: 0,
    options: []
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [qData, tData] = await Promise.all([
        adminApi.getSurveyQuestions(survey.id),
        adminApi.getTopics()
      ]);
      setQuestions(qData);
      setTopics(tData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (survey) {
      fetchData();
    }
  }, [survey]);

  const handleOpenForm = () => {
    setFormData({
      content: '',
      question_type: 'single_choice',
      category: 'knowledge',
      topic_id: '',
      difficulty: 'beginner',
      is_required: true,
      weight: 1.0,
      order_index: questions.length,
      options: [
        { content: '', value: '', score: 0, is_correct: false }
      ]
    });
    setIsEditing(true);
  };

  const handleCloseForm = () => {
    setIsEditing(false);
  };

  const handleAddOption = () => {
    setFormData({
      ...formData,
      options: [...formData.options, { content: '', value: '', score: 0, is_correct: false }]
    });
  };

  const handleUpdateOption = (index, field, val) => {
    const newOptions = [...formData.options];
    newOptions[index][field] = val;
    setFormData({ ...formData, options: newOptions });
  };

  const handleRemoveOption = (index) => {
    const newOptions = [...formData.options];
    newOptions.splice(index, 1);
    setFormData({ ...formData, options: newOptions });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.question_type !== 'text' && formData.options.length === 0) {
      alert('Vui lòng thêm ít nhất 1 phương án trả lời.');
      return;
    }
    
    // Prepare payload
    const payload = {
      ...formData,
      topic_id: formData.topic_id ? parseInt(formData.topic_id) : null
    };

    try {
      await adminApi.createSurveyQuestion(survey.id, payload);
      handleCloseForm();
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Lỗi khi lưu câu hỏi');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Xóa câu hỏi này?')) {
      try {
        await adminApi.deleteSurveyQuestion(id);
        fetchData();
      } catch (err) {
        console.error(err);
        alert('Lỗi xóa câu hỏi');
      }
    }
  };

  const getCategoryName = (cat) => {
    const map = {
      'knowledge': 'Kiến thức ban đầu',
      'goal': 'Mục tiêu học tập',
      'interest': 'Nhu cầu/Quan tâm',
      'self_assessment': 'Tự đánh giá'
    };
    return map[cat] || cat;
  };

  const getTypeName = (type) => {
    const map = {
      'single_choice': 'Một lựa chọn',
      'multiple_choice': 'Nhiều lựa chọn',
      'rating': 'Đánh giá 1-5',
      'text': 'Tự luận'
    };
    return map[type] || type;
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-5xl max-h-[90vh] flex flex-col animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-100 bg-white flex items-center justify-between rounded-t-xl shrink-0">
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Quản lý Câu hỏi
            </h2>
            <p className="text-sm text-slate-500">Khảo sát: {survey?.title}</p>
          </div>
          <button onClick={onClose} className="p-2 text-slate-400 hover:text-slate-600 transition-colors">
            <XMarkIcon className="w-5 h-5" />
          </button>
        </div>
        
        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-50/50">
          {isEditing ? (
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm max-w-3xl mx-auto">
              <h3 className="text-md font-semibold text-slate-800 mb-4 border-b pb-2">
                Thêm câu hỏi mới
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Nội dung câu hỏi <span className="text-red-500">*</span></label>
                  <textarea
                    required
                    rows={2}
                    className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-medium"
                    value={formData.content}
                    onChange={e => setFormData({...formData, content: e.target.value})}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Nhóm câu hỏi <span className="text-red-500">*</span></label>
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none"
                      value={formData.category}
                      onChange={e => setFormData({...formData, category: e.target.value})}
                    >
                      <option value="knowledge">Đánh giá Kiến thức (Knowledge)</option>
                      <option value="goal">Mục tiêu học tập (Goal)</option>
                      <option value="interest">Nhu cầu/Chủ đề quan tâm (Interest)</option>
                      <option value="self_assessment">Tự đánh giá năng lực</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Loại câu hỏi <span className="text-red-500">*</span></label>
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none"
                      value={formData.question_type}
                      onChange={e => setFormData({...formData, question_type: e.target.value})}
                    >
                      <option value="single_choice">Một lựa chọn (Radio)</option>
                      <option value="multiple_choice">Nhiều lựa chọn (Checkbox)</option>
                      <option value="rating">Thang đánh giá 1-5</option>
                      <option value="text">Nhập text tự luận</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Chủ đề liên quan</label>
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg outline-none"
                      value={formData.topic_id}
                      onChange={e => setFormData({...formData, topic_id: e.target.value})}
                    >
                      <option value="">-- Không xác định --</option>
                      {topics.map(t => (
                        <option key={t.id} value={t.id}>{t.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Mức độ / Bắt buộc</label>
                    <div className="flex gap-4">
                      <select
                        className="flex-1 px-3 py-2 border border-slate-300 rounded-lg outline-none"
                        value={formData.difficulty}
                        onChange={e => setFormData({...formData, difficulty: e.target.value})}
                      >
                        <option value="beginner">Cơ bản</option>
                        <option value="intermediate">Trung bình</option>
                        <option value="advanced">Nâng cao</option>
                      </select>
                      <label className="flex items-center gap-2">
                        <input type="checkbox" checked={formData.is_required} onChange={e => setFormData({...formData, is_required: e.target.checked})} />
                        <span className="text-sm">Bắt buộc</span>
                      </label>
                    </div>
                  </div>
                </div>

                {formData.question_type !== 'text' && (
                  <div className="mt-6">
                    <div className="flex justify-between items-center mb-2">
                      <label className="block text-sm font-bold text-slate-700">Các phương án trả lời</label>
                      <button type="button" onClick={handleAddOption} className="text-xs text-blue-600 hover:underline flex items-center gap-1">
                        <PlusIcon className="w-4 h-4" /> Thêm phương án
                      </button>
                    </div>
                    <div className="space-y-2 border border-slate-200 p-3 rounded-lg bg-slate-50">
                      {formData.options.map((opt, idx) => (
                        <div key={idx} className="flex gap-2 items-start">
                          <input 
                            type="text" 
                            className="flex-1 px-3 py-1.5 border border-slate-300 rounded outline-none text-sm" 
                            placeholder="Nội dung phương án..."
                            value={opt.content}
                            onChange={e => handleUpdateOption(idx, 'content', e.target.value)}
                            required
                          />
                          {formData.category === 'knowledge' && (
                            <label className="flex items-center gap-1 mt-1 text-sm shrink-0">
                              <input 
                                type="checkbox" 
                                checked={opt.is_correct}
                                onChange={e => handleUpdateOption(idx, 'is_correct', e.target.checked)}
                              />
                              Đúng
                            </label>
                          )}
                          {(formData.category === 'knowledge' || formData.question_type === 'rating') && (
                            <input 
                              type="number" 
                              className="w-16 px-2 py-1.5 border border-slate-300 rounded outline-none text-sm shrink-0" 
                              placeholder="Điểm"
                              value={opt.score}
                              onChange={e => handleUpdateOption(idx, 'score', parseFloat(e.target.value) || 0)}
                            />
                          )}
                          <button type="button" onClick={() => handleRemoveOption(idx)} className="p-1.5 text-red-500 hover:bg-red-100 rounded shrink-0">
                            <TrashIcon className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                      {formData.options.length === 0 && <p className="text-sm text-slate-400 italic">Chưa có phương án nào.</p>}
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100 mt-6">
                  <button type="button" onClick={handleCloseForm} className="px-4 py-2 bg-slate-50 text-slate-700 font-medium rounded-lg hover:bg-slate-100">
                    Hủy
                  </button>
                  <button type="submit" className="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700">
                    Lưu câu hỏi
                  </button>
                </div>
              </form>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-end mb-4">
                <button
                  onClick={() => handleOpenForm()}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  <PlusIcon className="w-4 h-4" />
                  <span>Thêm câu hỏi</span>
                </button>
              </div>

              {loading ? (
                <div className="text-center py-8 text-slate-500">Đang tải...</div>
              ) : questions.length === 0 ? (
                <div className="bg-white p-8 rounded-xl border border-slate-200 text-center text-slate-500">
                  Bộ khảo sát này chưa có câu hỏi nào.
                </div>
              ) : (
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase text-slate-500 font-semibold">
                        <th className="px-4 py-3 w-10 text-center">STT</th>
                        <th className="px-4 py-3">Câu hỏi</th>
                        <th className="px-4 py-3">Nhóm / Loại</th>
                        <th className="px-4 py-3 text-center">Bắt buộc</th>
                        <th className="px-4 py-3 text-right">Thao tác</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {questions.map((q, idx) => (
                        <tr key={q.id} className="hover:bg-slate-50/50">
                          <td className="px-4 py-3 text-center font-medium text-slate-500">{q.order_index + 1}</td>
                          <td className="px-4 py-3">
                            <p className="font-medium text-slate-900">{q.content}</p>
                            {q.topic_id && (
                              <span className="inline-block mt-1 text-xs px-2 py-0.5 bg-blue-50 text-blue-600 rounded">
                                {topics.find(t => t.id === q.topic_id)?.name || 'Chủ đề'}
                              </span>
                            )}
                          </td>
                          <td className="px-4 py-3 text-sm">
                            <div className="text-slate-900 font-medium">{getCategoryName(q.category)}</div>
                            <div className="text-slate-500 text-xs">{getTypeName(q.question_type)}</div>
                          </td>
                          <td className="px-4 py-3 text-center">
                            {q.is_required ? (
                              <span className="text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded text-xs font-medium">Có</span>
                            ) : (
                              <span className="text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-xs">Không</span>
                            )}
                          </td>
                          <td className="px-4 py-3 text-right">
                            <div className="flex items-center justify-end gap-1">
                              <button onClick={() => handleDelete(q.id)} className="p-1.5 text-slate-400 hover:text-red-600 rounded hover:bg-red-50">
                                <TrashIcon className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
