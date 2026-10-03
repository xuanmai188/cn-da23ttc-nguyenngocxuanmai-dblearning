import { useState, useEffect } from 'react';
import { XMarkIcon, PlusIcon, PencilSquareIcon, TrashIcon } from '@heroicons/react/24/outline';
import { adminApi } from '../../../api/adminApi';

export default function QuestionManagementModal({ quiz, onClose }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Form State
  const [isEditing, setIsEditing] = useState(false);
  const [editingQuestionId, setEditingQuestionId] = useState(null);
  const [formData, setFormData] = useState({
    content: '',
    options: ['', '', '', ''],
    correct_option: 0,
    explanation: '',
    difficulty: 'medium',
    order_index: 0
  });

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const data = await adminApi.getQuestionsByQuiz(quiz.id);
      setQuestions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (quiz) {
      fetchQuestions();
    }
  }, [quiz]);

  const handleOptionChange = (index, value) => {
    const newOptions = [...formData.options];
    newOptions[index] = value;
    setFormData({ ...formData, options: newOptions });
  };

  const handleAddOption = () => {
    setFormData({ ...formData, options: [...formData.options, ''] });
  };

  const handleRemoveOption = (index) => {
    if (formData.options.length <= 2) return;
    const newOptions = formData.options.filter((_, i) => i !== index);
    let newCorrect = formData.correct_option;
    if (newCorrect === index) newCorrect = 0;
    else if (newCorrect > index) newCorrect--;
    setFormData({ ...formData, options: newOptions, correct_option: newCorrect });
  };

  const handleOpenForm = (question = null) => {
    if (question) {
      setEditingQuestionId(question.id);
      setFormData({
        content: question.content,
        options: question.options,
        correct_option: question.correct_option,
        explanation: question.explanation || '',
        difficulty: question.difficulty,
        order_index: question.order_index
      });
    } else {
      setEditingQuestionId(null);
      setFormData({
        content: '',
        options: ['', '', '', ''],
        correct_option: 0,
        explanation: '',
        difficulty: 'medium',
        order_index: questions.length
      });
    }
    setIsEditing(true);
  };

  const handleCloseForm = () => {
    setIsEditing(false);
    setEditingQuestionId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate empty options
    if (formData.options.some(opt => opt.trim() === '')) {
      alert("Các lựa chọn không được để trống");
      return;
    }

    try {
      if (editingQuestionId) {
        await adminApi.updateQuestion(editingQuestionId, formData);
      } else {
        await adminApi.createQuestion(quiz.id, formData);
      }
      handleCloseForm();
      fetchQuestions();
    } catch (err) {
      console.error(err);
      alert('Đã có lỗi xảy ra');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa câu hỏi này?')) {
      try {
        await adminApi.deleteQuestion(id);
        fetchQuestions();
      } catch (err) {
        console.error(err);
        alert('Lỗi khi xóa câu hỏi');
      }
    }
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-xl shadow-xl w-full max-w-4xl max-h-[90vh] flex flex-col animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-100 bg-white flex items-center justify-between rounded-t-xl shrink-0">
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Quản lý Câu hỏi
            </h2>
            <p className="text-sm text-slate-500">Quiz: {quiz?.title}</p>
          </div>
          <button onClick={onClose} className="p-2 text-slate-400 hover:text-slate-600 transition-colors">
            <XMarkIcon className="w-5 h-5" />
          </button>
        </div>
        
        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-50/50">
          {isEditing ? (
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
              <h3 className="text-md font-semibold text-slate-800 mb-4 border-b pb-2">
                {editingQuestionId ? 'Chỉnh sửa câu hỏi' : 'Thêm câu hỏi mới'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Nội dung câu hỏi <span className="text-red-500">*</span></label>
                  <textarea
                    required
                    rows={3}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.content}
                    onChange={e => setFormData({...formData, content: e.target.value})}
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-slate-700">Các lựa chọn (Tick vào đáp án đúng) <span className="text-red-500">*</span></label>
                    <button type="button" onClick={handleAddOption} className="text-xs font-medium text-blue-600 hover:text-blue-700">
                      + Thêm lựa chọn
                    </button>
                  </div>
                  <div className="space-y-3">
                    {formData.options.map((opt, index) => (
                      <div key={index} className="flex items-center gap-3">
                        <input
                          type="radio"
                          name="correct_option"
                          checked={formData.correct_option === index}
                          onChange={() => setFormData({...formData, correct_option: index})}
                          className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                        />
                        <span className="text-sm font-medium text-slate-500 w-6">
                          {String.fromCharCode(65 + index)}.
                        </span>
                        <input
                          type="text"
                          required
                          className={`flex-1 px-3 py-2 border rounded-lg focus:ring-2 outline-none ${formData.correct_option === index ? 'border-blue-500 bg-blue-50/30' : 'border-slate-300 focus:ring-blue-500'}`}
                          value={opt}
                          onChange={e => handleOptionChange(index, e.target.value)}
                          placeholder={`Lựa chọn ${index + 1}`}
                        />
                        {formData.options.length > 2 && (
                          <button
                            type="button"
                            onClick={() => handleRemoveOption(index)}
                            className="p-2 text-slate-400 hover:text-red-600 transition-colors"
                          >
                            <XMarkIcon className="w-5 h-5" />
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Giải thích (Tùy chọn)</label>
                  <textarea
                    rows={2}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm text-slate-600"
                    placeholder="Giải thích vì sao đáp án đó là đúng..."
                    value={formData.explanation}
                    onChange={e => setFormData({...formData, explanation: e.target.value})}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Độ khó</label>
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                      value={formData.difficulty}
                      onChange={e => setFormData({...formData, difficulty: e.target.value})}
                    >
                      <option value="easy">Dễ</option>
                      <option value="medium">Trung bình</option>
                      <option value="hard">Khó</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Thứ tự</label>
                    <input
                      type="number"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                      value={formData.order_index}
                      onChange={e => setFormData({...formData, order_index: parseInt(e.target.value) || 0})}
                    />
                  </div>
                </div>

                <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={handleCloseForm}
                    className="px-4 py-2 bg-slate-50 text-slate-700 font-medium rounded-lg hover:bg-slate-100 transition-colors"
                  >
                    Hủy
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Lưu câu hỏi
                  </button>
                </div>
              </form>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex justify-end mb-2">
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
                  Quiz này chưa có câu hỏi nào.
                </div>
              ) : (
                <div className="space-y-3">
                  {questions.map((q, idx) => (
                    <div key={q.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative group">
                      <div className="absolute top-4 right-4 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onClick={() => handleOpenForm(q)} className="p-1.5 text-slate-400 hover:text-blue-600 bg-slate-50 rounded hover:bg-blue-50 transition-colors">
                          <PencilSquareIcon className="w-4 h-4" />
                        </button>
                        <button onClick={() => handleDelete(q.id)} className="p-1.5 text-slate-400 hover:text-red-600 bg-slate-50 rounded hover:bg-red-50 transition-colors">
                          <TrashIcon className="w-4 h-4" />
                        </button>
                      </div>

                      <div className="pr-16">
                        <div className="flex items-start gap-3 mb-3">
                          <span className="flex items-center justify-center w-6 h-6 rounded bg-slate-100 text-slate-600 font-bold text-xs shrink-0 mt-0.5">
                            {idx + 1}
                          </span>
                          <p className="font-medium text-slate-900">{q.content}</p>
                        </div>
                        
                        <div className="pl-9 space-y-2">
                          {q.options.map((opt, optIdx) => (
                            <div 
                              key={optIdx} 
                              className={`px-3 py-2 rounded-lg text-sm border ${q.correct_option === optIdx ? 'bg-green-50 border-green-200 text-green-800 font-medium' : 'bg-slate-50 border-transparent text-slate-600'}`}
                            >
                              <span className="mr-2 font-semibold opacity-50">{String.fromCharCode(65 + optIdx)}.</span>
                              {opt}
                            </div>
                          ))}
                        </div>

                        {q.explanation && (
                          <div className="pl-9 mt-3 text-sm text-slate-500 italic">
                            <span className="font-medium not-italic mr-1">Giải thích:</span> 
                            {q.explanation}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
