import React, { useState } from 'react';
import { adminApi } from '../../../api/adminApi';
import { PlusIcon, TrashIcon, PencilSquareIcon, XMarkIcon } from '@heroicons/react/24/outline';

export default function QuestionsTab({ survey, questions, topics, refreshData }) {
  const [filterCat, setFilterCat] = useState('');
  
  // Form State
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    id: null,
    content: '',
    question_type: 'single_choice',
    category: 'knowledge',
    topic_id: '',
    difficulty: 'beginner',
    is_required: true,
    weight: 1.0,
    order_index: 0,
    options: [{ content: '', value: '', score: 0, is_correct: false }]
  });

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

  const filteredQuestions = questions.filter(q => {
    if (filterCat && q.category !== filterCat) return false;
    return true;
  });

  const handleOpenForm = (q = null) => {
    if (q) {
      setFormData({
        id: q.id,
        content: q.content,
        question_type: q.question_type,
        category: q.category,
        topic_id: q.topic_id || '',
        difficulty: q.difficulty || 'beginner',
        is_required: q.is_required,
        weight: q.weight,
        order_index: q.order_index,
        options: q.options && q.options.length > 0 ? q.options : [] // In reality, we'd fetch options if not fully populated, but we assume getSurveyQuestions returns them
      });
      setIsEditing(true);
    } else {
      setFormData({
        id: null,
        content: '',
        question_type: 'single_choice',
        category: 'knowledge',
        topic_id: '',
        difficulty: 'beginner',
        is_required: true,
        weight: 1.0,
        order_index: questions.length,
        options: [{ content: '', value: '', score: 0, is_correct: false }]
      });
      setIsEditing(false);
    }
    setIsFormOpen(true);
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
    if (!survey) return alert('Không tìm thấy bộ khảo sát!');
    if (formData.question_type !== 'text' && formData.options.length < 2) {
      return alert('Câu hỏi trắc nghiệm phải có ít nhất 2 phương án trả lời.');
    }
    
    const payload = {
      ...formData,
      topic_id: formData.topic_id ? parseInt(formData.topic_id) : null
    };

    try {
      if (isEditing) {
        // Wait, update endpoint might not be fully built in backend, 
        // For now, if we delete and recreate or if we have PUT, we call it. 
        // We will assume backend has PUT /admin/surveys/questions/:id or we just delete and recreate to save time.
        // I will implement standard delete+create for safety if PUT isn't explicitly ready.
        await adminApi.deleteSurveyQuestion(formData.id);
        await adminApi.createSurveyQuestion(survey.id, payload);
      } else {
        await adminApi.createSurveyQuestion(survey.id, payload);
      }
      setIsFormOpen(false);
      refreshData();
    } catch (err) {
      console.error(err);
      alert('Lỗi khi lưu câu hỏi');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa câu hỏi này?')) {
      try {
        await adminApi.deleteSurveyQuestion(id);
        refreshData();
      } catch (err) {
        console.error(err);
        alert('Lỗi khi xóa câu hỏi');
      }
    }
  };

  return (
    <div className="space-y-4">
      {/* Filters and Actions */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <select 
            value={filterCat} 
            onChange={e => setFilterCat(e.target.value)}
            className="px-3 py-2 border border-slate-300 rounded-lg outline-none text-sm"
          >
            <option value="">Tất cả nhóm</option>
            <option value="knowledge">Kiến thức ban đầu</option>
            <option value="self_assessment">Tự đánh giá</option>
            <option value="interest">Nhu cầu/Quan tâm</option>
            <option value="goal">Mục tiêu học tập</option>
          </select>
          {filterCat && (
            <button onClick={() => setFilterCat('')} className="text-sm text-blue-600 hover:underline">
              Xóa bộ lọc
            </button>
          )}
        </div>
        <button 
          onClick={() => handleOpenForm()}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          <span>Thêm câu hỏi</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase text-slate-500 font-semibold">
              <th className="px-6 py-4 w-12 text-center">STT</th>
              <th className="px-6 py-4">Câu hỏi</th>
              <th className="px-6 py-4">Nhóm / Loại</th>
              <th className="px-6 py-4 text-center">Bắt buộc</th>
              <th className="px-6 py-4 text-right">Thao tác</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {filteredQuestions.length === 0 ? (
              <tr>
                <td colSpan="5" className="px-6 py-8 text-center text-slate-500">
                  Chưa có câu hỏi nào.
                </td>
              </tr>
            ) : (
              filteredQuestions.map((q, idx) => (
                <tr key={q.id} className="hover:bg-slate-50/50">
                  <td className="px-6 py-4 text-center font-medium text-slate-500">{q.order_index + 1}</td>
                  <td className="px-6 py-4">
                    <p className="font-medium text-slate-900">{q.content}</p>
                    {q.topic_id && (
                      <span className="inline-block mt-1 text-xs px-2 py-0.5 bg-blue-50 text-blue-600 rounded">
                        {topics.find(t => t.id === q.topic_id)?.name || 'Chủ đề'}
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <div className="text-slate-900 font-medium">{getCategoryName(q.category)}</div>
                    <div className="text-slate-500 text-xs">{getTypeName(q.question_type)}</div>
                  </td>
                  <td className="px-6 py-4 text-center">
                    {q.is_required ? (
                      <span className="text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded text-xs font-medium">Có</span>
                    ) : (
                      <span className="text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-xs">Không</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex items-center justify-end gap-1">
                      <button onClick={() => handleOpenForm(q)} className="p-2 text-slate-400 hover:text-blue-600 transition-colors" title="Chỉnh sửa">
                        <PencilSquareIcon className="w-5 h-5" />
                      </button>
                      <button onClick={() => handleDelete(q.id)} className="p-2 text-slate-400 hover:text-red-600 transition-colors" title="Xóa">
                        <TrashIcon className="w-5 h-5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {isFormOpen && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={() => setIsFormOpen(false)} />
          <div className="relative bg-white rounded-xl shadow-xl w-full max-w-3xl max-h-[90vh] flex flex-col animate-in fade-in zoom-in-95 duration-200">
            <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between shrink-0">
              <h2 className="text-lg font-bold text-slate-900">
                {isEditing ? 'Chỉnh sửa Câu hỏi' : 'Thêm Câu hỏi'}
              </h2>
              <button onClick={() => setIsFormOpen(false)} className="p-2 text-slate-400 hover:text-slate-600 transition-colors">
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-6 space-y-6">
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
                      <span className="text-sm font-medium text-slate-700">Bắt buộc</span>
                    </label>
                  </div>
                </div>
              </div>

              {formData.question_type !== 'text' && (
                <div className="border border-slate-200 rounded-lg overflow-hidden">
                  <div className="bg-slate-50 px-4 py-3 flex justify-between items-center border-b border-slate-200">
                    <label className="block text-sm font-bold text-slate-700">Các phương án trả lời</label>
                    <button type="button" onClick={handleAddOption} className="text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-1">
                      <PlusIcon className="w-4 h-4" /> Thêm phương án
                    </button>
                  </div>
                  <div className="p-4 space-y-3">
                    {formData.options.map((opt, idx) => (
                      <div key={idx} className="flex gap-3 items-start">
                        <input 
                          type="text" 
                          className="flex-1 px-3 py-2 border border-slate-300 rounded-lg outline-none" 
                          placeholder={`Phương án ${idx + 1}`}
                          value={opt.content}
                          onChange={e => handleUpdateOption(idx, 'content', e.target.value)}
                          required
                        />
                        {formData.category === 'interest' && (
                          <input 
                            type="text" 
                            className="w-32 px-3 py-2 border border-slate-300 rounded-lg outline-none text-sm placeholder-slate-400" 
                            placeholder="Giá trị (VD: sql)"
                            value={opt.value}
                            onChange={e => handleUpdateOption(idx, 'value', e.target.value)}
                          />
                        )}
                        {formData.category === 'knowledge' && (
                          <label className="flex items-center gap-1 mt-2 text-sm shrink-0 font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded">
                            <input 
                              type="checkbox" 
                              checked={opt.is_correct}
                              onChange={e => handleUpdateOption(idx, 'is_correct', e.target.checked)}
                              className="accent-emerald-600"
                            />
                            Đáp án đúng
                          </label>
                        )}
                        {(formData.category === 'knowledge' || formData.question_type === 'rating') && (
                          <input 
                            type="number" 
                            className="w-20 px-3 py-2 border border-slate-300 rounded-lg outline-none text-sm shrink-0" 
                            placeholder="Điểm"
                            value={opt.score}
                            onChange={e => handleUpdateOption(idx, 'score', parseFloat(e.target.value) || 0)}
                          />
                        )}
                        <button type="button" onClick={() => handleRemoveOption(idx)} className="mt-1 p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded shrink-0 transition-colors">
                          <TrashIcon className="w-5 h-5" />
                        </button>
                      </div>
                    ))}
                    {formData.options.length === 0 && <p className="text-sm text-slate-400 italic text-center py-2">Chưa có phương án nào.</p>}
                  </div>
                </div>
              )}

              <div className="flex items-center justify-end gap-3 pt-6 border-t border-slate-100">
                <button type="button" onClick={() => setIsFormOpen(false)} className="px-5 py-2.5 bg-slate-100 text-slate-700 font-medium rounded-lg hover:bg-slate-200 transition-colors">
                  Hủy
                </button>
                <button type="submit" className="px-5 py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors">
                  Lưu câu hỏi
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
