import React from 'react';
import { useState, useEffect } from 'react';
import { adminApi } from '../../../api/adminApi';
import { ChevronDownIcon, ChevronRightIcon, PlusIcon, PencilSquareIcon, TrashIcon, XMarkIcon } from '@heroicons/react/24/outline';

export default function LessonManagement() {
  const [items, setItems] = useState([]);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedTopics, setExpandedTopics] = useState({});
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  
  // Form State
  const [formData, setFormData] = useState({
    topic_id: '',
    title: '',
    description: '',
    content_type: 'document',
    difficulty: 'beginner',
    content_url: '',
    content_body: '',
    estimated_minutes: 15,
    is_active: true
  });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [itemsData, topicsData] = await Promise.all([
        adminApi.getItems(),
        adminApi.getTopics()
      ]);
      setItems(itemsData);
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

  const handleOpenModal = (item = null) => {
    if (item) {
      setEditingItem(item);
      setFormData({
        topic_id: item.topic_id,
        title: item.title,
        description: item.description || '',
        content_type: item.content_type,
        difficulty: item.difficulty,
        content_url: item.content_url || '',
        content_body: item.content_body || '',
        estimated_minutes: item.estimated_minutes || 15,
        is_active: item.is_active
      });
    } else {
      setEditingItem(null);
      setFormData({
        topic_id: topics.length > 0 ? topics[0].id : '',
        title: '',
        description: '',
        content_type: 'document',
        difficulty: 'beginner',
        content_url: '',
        content_body: '',
        estimated_minutes: 15,
        is_active: true
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingItem(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await adminApi.updateItem(editingItem.id, formData);
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
    if (window.confirm('Bạn có chắc chắn muốn xóa bài học này?')) {
      try {
        await adminApi.deleteItem(id);
        fetchData();
      } catch (err) {
        console.error(err);
        alert('Xóa thất bại');
      }
    }
  };

  const toggleTopic = (topicId) => {
    setExpandedTopics(prev => ({...prev, [topicId]: !prev[topicId]}));
  };

  const getTopicName = (id) => {
    const t = topics.find(t => t.id === id);
    return t ? t.name : 'Unknown';
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500">Đang tải dữ liệu...</div>;
  }

  return (
    <div className="pb-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Quản lý Bài học</h1>
          <p className="text-slate-500 mt-1">Quản lý các bài học thuộc các chủ đề</p>
        </div>
        <button 
          onClick={() => handleOpenModal()}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          <span>Thêm Bài học</span>
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase tracking-wider text-slate-500 font-semibold">
                <th className="px-6 py-4">Tên bài học</th>
                <th className="px-6 py-4">Thuộc chủ đề</th>
                <th className="px-6 py-4">Loại nội dung</th>
                <th className="px-6 py-4">Trạng thái</th>
                <th className="px-6 py-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {topics.length === 0 ? (
                <tr>
                  <td colSpan="5" className="px-6 py-8 text-center text-slate-500">
                    Chưa có chủ đề nào. Hãy tạo chủ đề trước.
                  </td>
                </tr>
              ) : (
                topics.map(topic => {
                  const topicItems = items.filter(i => (i.content_type === 'document' || i.content_type === 'video') && i.topic_id === topic.id);
                  const isExpanded = expandedTopics[topic.id];
                  
                  return (
                    <React.Fragment key={topic.id}>
                      <tr 
                        className="bg-slate-50 hover:bg-slate-100 cursor-pointer transition-colors border-l-4 border-l-blue-500"
                        onClick={() => toggleTopic(topic.id)}
                      >
                        <td colSpan="5" className="px-6 py-3 font-semibold text-slate-800">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              {isExpanded ? <ChevronDownIcon className="w-5 h-5 text-blue-600"/> : <ChevronRightIcon className="w-5 h-5 text-slate-400"/>}
                              <span>{topic.name}</span>
                              <span className="text-xs font-medium bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full ml-2">
                                {topicItems.length} bài học
                              </span>
                            </div>
                          </div>
                        </td>
                      </tr>
                      {isExpanded && topicItems.length === 0 && (
                        <tr>
                          <td colSpan="5" className="px-8 py-4 text-sm text-slate-400 italic bg-white border-l-4 border-l-transparent">
                            Chưa có bài học nào trong chủ đề này.
                          </td>
                        </tr>
                      )}
                      {isExpanded && topicItems.map(item => (
                        <tr key={item.id} className="hover:bg-slate-50/50 transition-colors bg-white">
                          <td className="px-6 py-4 pl-12 border-l-4 border-l-transparent">
                            <div className="font-semibold text-slate-900">{item.title}</div>
                            <div className="text-sm text-slate-500 truncate max-w-xs">{item.description}</div>
                          </td>
                          <td className="px-6 py-4 text-sm text-slate-600">
                            {topic.name}
                          </td>
                          <td className="px-6 py-4 text-sm text-slate-600">
                            {item.content_type === 'document' && 'Tài liệu'}
                            {item.content_type === 'video' && 'Video'}
                          </td>
                          <td className="px-6 py-4">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${item.is_active ? 'bg-green-100 text-green-800' : 'bg-slate-100 text-slate-800'}`}>
                              {item.is_active ? 'Hiển thị' : 'Đang ẩn'}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-right">
                            <div className="flex items-center justify-end gap-2">
                              <button onClick={() => handleOpenModal(item)} className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
                                <PencilSquareIcon className="w-5 h-5" />
                              </button>
                              <button onClick={() => handleDelete(item.id)} className="p-2 text-slate-400 hover:text-red-600 transition-colors">
                                <TrashIcon className="w-5 h-5" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </React.Fragment>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={handleCloseModal} />
          <div className="relative bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto animate-in fade-in zoom-in-95 duration-200">
            <div className="sticky top-0 z-10 px-6 py-4 border-b border-slate-100 bg-white flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-900">
                {editingItem ? 'Chỉnh sửa Bài học' : 'Thêm Bài học mới'}
              </h2>
              <button onClick={handleCloseModal} className="text-slate-400 hover:text-slate-600 transition-colors">
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
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
                <label className="block text-sm font-medium text-slate-700 mb-1">Tên bài học <span className="text-red-500">*</span></label>
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
                  <label className="block text-sm font-medium text-slate-700 mb-1">Loại nội dung</label>
                  <select
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.content_type}
                    onChange={e => setFormData({...formData, content_type: e.target.value})}
                  >
                    <option value="document">Tài liệu (Document)</option>
                    <option value="video">Video</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Độ khó</label>
                  <select
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.difficulty}
                    onChange={e => setFormData({...formData, difficulty: e.target.value})}
                  >
                    <option value="beginner">Dễ (Beginner)</option>
                    <option value="intermediate">Trung bình (Intermediate)</option>
                    <option value="advanced">Khó (Advanced)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Thời lượng ước tính (phút)</label>
                  <input
                    type="number"
                    min="1"
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.estimated_minutes}
                    onChange={e => setFormData({...formData, estimated_minutes: parseInt(e.target.value)})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Trạng thái</label>
                  <label className="flex items-center mt-2 cursor-pointer">
                    <input
                      type="checkbox"
                      className="sr-only peer"
                      checked={formData.is_active}
                      onChange={e => setFormData({...formData, is_active: e.target.checked})}
                    />
                    <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    <span className="ml-3 text-sm font-medium text-slate-700">{formData.is_active ? 'Hiển thị' : 'Đang ẩn'}</span>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Nội dung / Đường dẫn (Tùy chọn)</label>
                <textarea
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm"
                  rows={4}
                  placeholder="Nhập nội dung bài học bằng Markdown hoặc dán link Youtube vào đây..."
                  value={formData.content_body}
                  onChange={e => setFormData({...formData, content_body: e.target.value})}
                />
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
                  {editingItem ? 'Lưu thay đổi' : 'Tạo Bài học'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
