import { useState, useEffect } from 'react';
import { adminApi } from '../../../api/adminApi';
import { PlusIcon, PencilSquareIcon, TrashIcon, XMarkIcon, ListBulletIcon } from '@heroicons/react/24/outline';
import QuestionManagementModal from './QuestionManagementModal';

export default function QuizManagement() {
  const [quizzes, setQuizzes] = useState([]);
  const [items, setItems] = useState([]); // To link a quiz to a lesson
  const [loading, setLoading] = useState(true);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingQuiz, setEditingQuiz] = useState(null);
  const [managingQuestionsFor, setManagingQuestionsFor] = useState(null);
  
  // Form State
  const [formData, setFormData] = useState({
    item_id: '',
    title: '',
    description: '',
    time_limit_minutes: 30,
    pass_score: 60
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [quizzesData, itemsData] = await Promise.all([
        adminApi.getQuizzes(),
        adminApi.getItems()
      ]);
      setQuizzes(quizzesData);
      setItems(itemsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleOpenModal = (quiz = null) => {
    if (quiz) {
      setEditingQuiz(quiz);
      setFormData({
        item_id: quiz.item_id,
        title: quiz.title,
        description: quiz.description || '',
        time_limit_minutes: quiz.time_limit_minutes,
        pass_score: quiz.pass_score
      });
    } else {
      setEditingQuiz(null);
      setFormData({
        item_id: items.length > 0 ? items[0].id : '',
        title: '',
        description: '',
        time_limit_minutes: 30,
        pass_score: 60
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingQuiz(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingQuiz) {
        await adminApi.updateQuiz(editingQuiz.id, formData);
      } else {
        await adminApi.createQuiz(formData);
      }
      handleCloseModal();
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Đã có lỗi xảy ra');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa Quiz này?')) {
      try {
        await adminApi.deleteQuiz(id);
        fetchData();
      } catch (err) {
        console.error(err);
        alert('Xóa thất bại');
      }
    }
  };

  const getItemName = (id) => {
    const t = items.find(t => t.id === id);
    return t ? t.title : 'Unknown';
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500">Đang tải dữ liệu...</div>;
  }

  return (
    <div className="pb-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Quản lý Quiz</h1>
          <p className="text-slate-500 mt-1">Quản lý các bài kiểm tra trắc nghiệm</p>
        </div>
        <button 
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          <span>Thêm Quiz</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase tracking-wider text-slate-500 font-semibold">
                <th className="px-6 py-4">Tên Quiz</th>
                <th className="px-6 py-4">Thuộc Bài học</th>
                <th className="px-6 py-4">Thời gian</th>
                <th className="px-6 py-4">Tỷ lệ đỗ</th>
                <th className="px-6 py-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {quizzes.length === 0 ? (
                <tr>
                  <td colSpan="5" className="px-6 py-8 text-center text-slate-500">
                    Chưa có Quiz nào.
                  </td>
                </tr>
              ) : (
                quizzes.map(quiz => (
                  <tr key={quiz.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-900">{quiz.title}</div>
                      <div className="text-sm text-slate-500 truncate max-w-xs">{quiz.description}</div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600">
                      {getItemName(quiz.item_id)}
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600">
                      {quiz.time_limit_minutes} phút
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        {quiz.pass_score}%
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button 
                          onClick={() => setManagingQuestionsFor(quiz)} 
                          className="px-3 py-1.5 flex items-center gap-1.5 text-xs font-medium text-purple-600 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors mr-2"
                        >
                          <ListBulletIcon className="w-4 h-4" />
                          Câu hỏi ({quiz.total_questions || 0})
                        </button>
                        <button onClick={() => handleOpenModal(quiz)} className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
                          <PencilSquareIcon className="w-5 h-5" />
                        </button>
                        <button onClick={() => handleDelete(quiz.id)} className="p-2 text-slate-400 hover:text-red-600 transition-colors">
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
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={handleCloseModal} />
          <div className="relative bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="px-6 py-4 border-b border-slate-100 bg-white flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-900">
                {editingQuiz ? 'Chỉnh sửa Quiz' : 'Thêm Quiz mới'}
              </h2>
              <button onClick={handleCloseModal} className="text-slate-400 hover:text-slate-600 transition-colors">
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Thuộc Bài học <span className="text-red-500">*</span></label>
                <select
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  value={formData.item_id}
                  onChange={e => setFormData({...formData, item_id: parseInt(e.target.value)})}
                >
                  <option value="" disabled>-- Chọn bài học --</option>
                  {items.map(t => (
                    <option key={t.id} value={t.id}>{t.title}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Tên Quiz <span className="text-red-500">*</span></label>
                <input
                  type="text"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  value={formData.title}
                  onChange={e => setFormData({...formData, title: e.target.value})}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Mô tả ngắn</label>
                <textarea
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  rows={2}
                  value={formData.description}
                  onChange={e => setFormData({...formData, description: e.target.value})}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Thời gian (phút)</label>
                  <input
                    type="number"
                    min="1"
                    required
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.time_limit_minutes}
                    onChange={e => setFormData({...formData, time_limit_minutes: parseInt(e.target.value)})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Tỷ lệ đỗ tối thiểu (%)</label>
                  <input
                    type="number"
                    min="1"
                    max="100"
                    required
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.pass_score}
                    onChange={e => setFormData({...formData, pass_score: parseInt(e.target.value)})}
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-3 pt-4 mt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="px-4 py-2 bg-slate-50 text-slate-700 font-medium rounded-lg hover:bg-slate-100 transition-colors"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
                >
                  {editingQuiz ? 'Lưu thay đổi' : 'Tạo Quiz'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Question Management Modal */}
      {managingQuestionsFor && (
        <QuestionManagementModal 
          quiz={managingQuestionsFor} 
          onClose={() => {
            setManagingQuestionsFor(null);
            fetchData(); // Refresh to update question count
          }} 
        />
      )}
    </div>
  );
}
