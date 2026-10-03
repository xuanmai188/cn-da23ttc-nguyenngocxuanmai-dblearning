import { useState, useEffect } from 'react';
import { adminApi } from '../../../api/adminApi';
import { PlusIcon, PencilSquareIcon, TrashIcon, XMarkIcon, Square3Stack3DIcon } from '@heroicons/react/24/outline';
import FlashcardsModal from './FlashcardsModal';

export default function FlashcardManagement() {
  const [flashcardSets, setFlashcardSets] = useState([]);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingSet, setEditingSet] = useState(null);
  const [managingCardsFor, setManagingCardsFor] = useState(null);
  
  // Form State
  const [formData, setFormData] = useState({
    topic_id: '',
    title: '',
    description: '',
    content_type: 'flashcard_set',
    difficulty: 'beginner',
    estimated_minutes: 10,
    is_active: true
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [itemsData, topicsData] = await Promise.all([
        adminApi.getItems(),
        adminApi.getTopics()
      ]);
      setFlashcardSets(itemsData.filter(i => i.content_type === 'flashcard_set'));
      setTopics(topicsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleOpenModal = (flashcardSet = null) => {
    if (flashcardSet) {
      setEditingSet(flashcardSet);
      setFormData({
        topic_id: flashcardSet.topic_id,
        title: flashcardSet.title,
        description: flashcardSet.description || '',
        content_type: 'flashcard_set',
        difficulty: flashcardSet.difficulty || 'beginner',
        estimated_minutes: flashcardSet.estimated_minutes || 10,
        is_active: true
      });
    } else {
      setEditingSet(null);
      setFormData({
        topic_id: topics.length > 0 ? topics[0].id : '',
        title: '',
        description: '',
        content_type: 'flashcard_set',
        difficulty: 'beginner',
        estimated_minutes: 10,
        is_active: true
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingSet(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingSet) {
        await adminApi.updateItem(editingSet.id, formData);
      } else {
        await adminApi.createItem(formData);
      }
      handleCloseModal();
      fetchData();
    } catch (err) {
      console.error(err);
      alert('Đã có lỗi xảy ra');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa bộ Flashcard này?')) {
      try {
        await adminApi.deleteItem(id);
        fetchData();
      } catch (err) {
        console.error(err);
        alert('Lỗi khi xóa');
      }
    }
  };

  const getTopicName = (topicId) => {
    const t = topics.find(t => t.id === topicId);
    return t ? t.name : 'Không xác định';
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Quản lý Flashcard</h1>
          <p className="text-slate-500 mt-1">Quản lý các bộ thẻ ghi nhớ của hệ thống</p>
        </div>
        <button 
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          <span>Thêm Bộ Flashcard</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase tracking-wider text-slate-500 font-semibold">
                <th className="px-6 py-4">Tên Bộ thẻ</th>
                <th className="px-6 py-4">Thuộc Chủ đề</th>
                <th className="px-6 py-4">Độ khó</th>
                <th className="px-6 py-4">Thời gian học</th>
                <th className="px-6 py-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {flashcardSets.length === 0 ? (
                <tr>
                  <td colSpan="5" className="px-6 py-8 text-center text-slate-500">
                    Chưa có bộ Flashcard nào.
                  </td>
                </tr>
              ) : (
                flashcardSets.map(set => (
                  <tr key={set.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-900">{set.title}</div>
                      <div className="text-sm text-slate-500 truncate max-w-xs">{set.description}</div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600">
                      {getTopicName(set.topic_id)}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${
                        set.difficulty === 'easy' || set.difficulty === 'beginner' ? 'bg-green-100 text-green-800' : 
                        set.difficulty === 'hard' || set.difficulty === 'advanced' ? 'bg-red-100 text-red-800' : 
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {set.difficulty === 'beginner' ? 'Dễ' : set.difficulty === 'advanced' ? 'Khó' : 'Trung bình'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600">
                      {set.estimated_minutes} phút
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button 
                          onClick={() => setManagingCardsFor(set)} 
                          className="px-3 py-1.5 flex items-center gap-1.5 text-xs font-medium text-orange-600 bg-orange-50 hover:bg-orange-100 rounded-lg transition-colors mr-2"
                        >
                          <Square3Stack3DIcon className="w-4 h-4" />
                          Quản lý Thẻ
                        </button>
                        <button onClick={() => handleOpenModal(set)} className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
                          <PencilSquareIcon className="w-5 h-5" />
                        </button>
                        <button onClick={() => handleDelete(set.id)} className="p-2 text-slate-400 hover:text-red-600 transition-colors">
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

      {/* Edit Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={handleCloseModal} />
          <div className="relative bg-white rounded-xl shadow-xl w-full max-w-md animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between p-6 border-b border-slate-100">
              <h2 className="text-lg font-bold text-slate-900">
                {editingSet ? 'Chỉnh sửa Bộ Flashcard' : 'Thêm Bộ Flashcard mới'}
              </h2>
              <button onClick={handleCloseModal} className="text-slate-400 hover:text-slate-600 transition-colors">
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Thuộc Chủ đề <span className="text-red-500">*</span></label>
                <select
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  value={formData.topic_id}
                  onChange={e => setFormData({...formData, topic_id: parseInt(e.target.value)})}
                >
                  <option value="" disabled>-- Chọn chủ đề --</option>
                  {topics.map(t => (
                    <option key={t.id} value={t.id}>{t.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Tên bộ thẻ <span className="text-red-500">*</span></label>
                <input
                  type="text"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  value={formData.title}
                  onChange={e => setFormData({...formData, title: e.target.value})}
                  placeholder="VD: Thuật ngữ SQL cơ bản"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Mô tả ngắn</label>
                <textarea
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  value={formData.description}
                  onChange={e => setFormData({...formData, description: e.target.value})}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Thời gian học (phút)</label>
                  <input
                    type="number"
                    min="1"
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.estimated_minutes}
                    onChange={e => setFormData({...formData, estimated_minutes: parseInt(e.target.value) || 10})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Độ khó</label>
                  <select
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.difficulty}
                    onChange={e => setFormData({...formData, difficulty: e.target.value})}
                  >
                    <option value="beginner">Dễ</option>
                    <option value="intermediate">Trung bình</option>
                    <option value="advanced">Khó</option>
                  </select>
                </div>
              </div>

              <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="px-4 py-2 text-slate-700 font-medium bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-white font-medium bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                >
                  Lưu thay đổi
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Cards Management Modal */}
      {managingCardsFor && (
        <FlashcardsModal 
          item={managingCardsFor} 
          onClose={() => setManagingCardsFor(null)} 
        />
      )}
    </div>
  );
}
