import { useState, useEffect } from 'react';
import { XMarkIcon, PlusIcon, PencilSquareIcon, TrashIcon } from '@heroicons/react/24/outline';
import { adminApi } from '../../../api/adminApi';

export default function FlashcardsModal({ item, onClose }) {
  const [flashcards, setFlashcards] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Form State
  const [isEditing, setIsEditing] = useState(false);
  const [editingCardId, setEditingCardId] = useState(null);
  const [formData, setFormData] = useState({
    question: '',
    answer: '',
    hint: '',
    order_index: 0
  });

  const fetchFlashcards = async () => {
    setLoading(true);
    try {
      const data = await adminApi.getFlashcardsByItem(item.id);
      setFlashcards(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (item) {
      fetchFlashcards();
    }
  }, [item]);

  const handleOpenForm = (card = null) => {
    if (card) {
      setEditingCardId(card.id);
      setFormData({
        question: card.question,
        answer: card.answer,
        hint: card.hint || '',
        order_index: card.order_index
      });
    } else {
      setEditingCardId(null);
      setFormData({
        question: '',
        answer: '',
        hint: '',
        order_index: flashcards.length
      });
    }
    setIsEditing(true);
  };

  const handleCloseForm = () => {
    setIsEditing(false);
    setEditingCardId(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editingCardId) {
        await adminApi.updateFlashcard(editingCardId, formData);
      } else {
        await adminApi.createFlashcard(item.id, formData);
      }
      handleCloseForm();
      fetchFlashcards();
    } catch (err) {
      console.error(err);
      alert('Đã có lỗi xảy ra');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa thẻ này?')) {
      try {
        await adminApi.deleteFlashcard(id);
        fetchFlashcards();
      } catch (err) {
        console.error(err);
        alert('Lỗi khi xóa thẻ');
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
              Quản lý Thẻ (Flashcards)
            </h2>
            <p className="text-sm text-slate-500">Bộ thẻ: {item?.title}</p>
          </div>
          <button onClick={onClose} className="p-2 text-slate-400 hover:text-slate-600 transition-colors">
            <XMarkIcon className="w-5 h-5" />
          </button>
        </div>
        
        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-50/50">
          {isEditing ? (
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm max-w-2xl mx-auto">
              <h3 className="text-md font-semibold text-slate-800 mb-4 border-b pb-2">
                {editingCardId ? 'Chỉnh sửa thẻ' : 'Thêm thẻ mới'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Mặt trước (Câu hỏi / Thuật ngữ) <span className="text-red-500">*</span></label>
                  <textarea
                    required
                    rows={3}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-slate-900 font-medium"
                    value={formData.question}
                    onChange={e => setFormData({...formData, question: e.target.value})}
                    placeholder="Nhập nội dung mặt trước..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Mặt sau (Câu trả lời / Định nghĩa) <span className="text-red-500">*</span></label>
                  <textarea
                    required
                    rows={3}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-slate-700"
                    value={formData.answer}
                    onChange={e => setFormData({...formData, answer: e.target.value})}
                    placeholder="Nhập nội dung mặt sau..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Gợi ý (Tùy chọn)</label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm text-slate-600"
                    placeholder="Gợi ý giúp người học dễ nhớ hơn..."
                    value={formData.hint}
                    onChange={e => setFormData({...formData, hint: e.target.value})}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Thứ tự hiển thị</label>
                  <input
                    type="number"
                    className="w-32 px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                    value={formData.order_index}
                    onChange={e => setFormData({...formData, order_index: parseInt(e.target.value) || 0})}
                  />
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
                    Lưu thẻ
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
                  <span>Thêm thẻ mới</span>
                </button>
              </div>

              {loading ? (
                <div className="text-center py-8 text-slate-500">Đang tải...</div>
              ) : flashcards.length === 0 ? (
                <div className="bg-white p-8 rounded-xl border border-slate-200 text-center text-slate-500">
                  Bộ Flashcard này chưa có thẻ nào.
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {flashcards.map((card, idx) => (
                    <div key={card.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm relative group hover:border-blue-300 transition-colors">
                      <div className="absolute top-3 right-3 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity bg-white p-1 rounded-md shadow-sm border border-slate-100">
                        <button onClick={() => handleOpenForm(card)} className="p-1.5 text-slate-400 hover:text-blue-600 rounded hover:bg-blue-50 transition-colors">
                          <PencilSquareIcon className="w-4 h-4" />
                        </button>
                        <button onClick={() => handleDelete(card.id)} className="p-1.5 text-slate-400 hover:text-red-600 rounded hover:bg-red-50 transition-colors">
                          <TrashIcon className="w-4 h-4" />
                        </button>
                      </div>

                      <div className="mb-4">
                        <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1 block">Mặt trước</span>
                        <p className="font-semibold text-slate-900 text-base">{card.question}</p>
                      </div>
                      
                      <div className="pt-3 border-t border-slate-100 border-dashed">
                        <span className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1 block">Mặt sau</span>
                        <p className="text-slate-700">{card.answer}</p>
                      </div>

                      {card.hint && (
                        <div className="mt-3 text-xs text-orange-600 bg-orange-50 px-2 py-1.5 rounded inline-block">
                          💡 Gợi ý: {card.hint}
                        </div>
                      )}
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
