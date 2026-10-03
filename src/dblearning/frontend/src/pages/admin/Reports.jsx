import React, { useState, useEffect } from 'react';
import { reportApi } from '../../api/reportApi';
import { adminApi } from '../../api/adminApi';
import { 
  ArrowDownTrayIcon, 
  FunnelIcon,
  BookOpenIcon,
  CheckBadgeIcon,
  SparklesIcon,
  ClipboardDocumentListIcon
} from '@heroicons/react/24/outline';

export default function Reports() {
  const [activeTab, setActiveTab] = useState('activity');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({ summary: {}, details: [] });
  const [topics, setTopics] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const ITEMS_PER_PAGE = 10;
  
  // Filters
  const [filters, setFilters] = useState({
    startDate: '',
    endDate: '',
    topicId: '',
    itemType: ''
  });

  useEffect(() => {
    adminApi.getTopics().then(setTopics).catch(console.error);
  }, []);

  useEffect(() => {
    setCurrentPage(1);
    fetchData();
  }, [activeTab, filters.topicId, filters.itemType]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filters.startDate) params.start_date = new Date(filters.startDate).toISOString();
      if (filters.endDate) {
        const end = new Date(filters.endDate);
        end.setHours(23, 59, 59, 999);
        params.end_date = end.toISOString();
      }
      if (filters.topicId) params.topic_id = filters.topicId;
      if (filters.itemType) params.item_type = filters.itemType;

      let res;
      switch (activeTab) {
        case 'activity':
          res = await reportApi.getLearningActivity(params);
          break;
        case 'results':
          res = await reportApi.getLearningResults(params);
          break;
        case 'recommendations':
          res = await reportApi.getRecommendations(params);
          break;
        case 'surveys':
          res = await reportApi.getSurveys(params);
          break;
      }
      setData(res || { summary: {}, details: [] });
    } catch (err) {
      console.error(err);
      setData({ summary: {}, details: [] });
    } finally {
      setLoading(false);
    }
  };

  const handleApplyDateFilter = () => {
    if (filters.startDate && filters.endDate && new Date(filters.startDate) > new Date(filters.endDate)) {
      return alert('Ngày bắt đầu không được lớn hơn ngày kết thúc!');
    }
    fetchData();
  };

  const handleResetFilters = () => {
    setFilters({ startDate: '', endDate: '', topicId: '', itemType: '' });
  };

  const exportCSV = () => {
    if (data.details.length === 0) return alert('Không có dữ liệu để xuất!');
    let csv = '';
    const headers = Object.keys(data.details[0]);
    csv += headers.join(',') + '\n';
    
    data.details.forEach(row => {
      const values = headers.map(h => {
        let val = row[h];
        if (typeof val === 'string') {
          val = '"' + val.replace(/"/g, '""') + '"';
        }
        return val;
      });
      csv += values.join(',') + '\n';
    });
    
    const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `DBLearning_Report_${activeTab}_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="pb-10">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Báo cáo</h1>
          <p className="text-slate-500 mt-1">Phân tích hoạt động học tập, kết quả học tập và dữ liệu cá nhân hóa của hệ thống.</p>
        </div>
        <div className="flex gap-3">
          <button onClick={exportCSV} className="flex items-center gap-2 px-4 py-2 bg-emerald-50 text-emerald-700 font-medium rounded-lg hover:bg-emerald-100 transition-colors border border-emerald-100">
            <ArrowDownTrayIcon className="w-5 h-5" />
            <span>Xuất Excel (CSV)</span>
          </button>
          <button onClick={() => window.print()} className="flex items-center gap-2 px-4 py-2 bg-slate-50 text-slate-700 font-medium rounded-lg hover:bg-slate-100 transition-colors border border-slate-200">
            <span>Xuất PDF</span>
          </button>
        </div>
      </div>

      {/* Filters (Compact) */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-3 mb-5 flex flex-wrap items-center gap-3 text-sm">
        <div className="flex items-center gap-2 text-slate-500 shrink-0">
          <FunnelIcon className="w-5 h-5" />
          <span className="font-medium">Bộ lọc:</span>
        </div>
        
        <div className="flex items-center gap-2">
          <span className="text-slate-500 font-medium">Từ:</span>
          <input 
            type="date" 
            className="px-2 py-1.5 border border-slate-300 rounded-md outline-none focus:ring-1 focus:ring-blue-500" 
            value={filters.startDate}
            onChange={e => setFilters({...filters, startDate: e.target.value})}
          />
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-500 font-medium">Đến:</span>
          <input 
            type="date" 
            className="px-2 py-1.5 border border-slate-300 rounded-md outline-none focus:ring-1 focus:ring-blue-500" 
            value={filters.endDate}
            onChange={e => setFilters({...filters, endDate: e.target.value})}
          />
        </div>
        <button 
          onClick={handleApplyDateFilter}
          className="px-3 py-1.5 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700"
        >
          Áp dụng
        </button>
        
        <div className="w-px h-6 bg-slate-200 mx-1"></div>
        
        {activeTab !== 'surveys' && activeTab !== 'recommendations' && (
          <>
            <div className="flex items-center gap-2">
              <span className="text-slate-500 font-medium">Chủ đề:</span>
              <select 
                className="px-2 py-1.5 border border-slate-300 rounded-md outline-none"
                value={filters.topicId}
                onChange={e => setFilters({...filters, topicId: e.target.value})}
              >
                <option value="">Tất cả</option>
                {topics.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
            {activeTab === 'activity' && (
              <div className="flex items-center gap-2">
                <span className="text-slate-500 font-medium">Loại:</span>
                <select 
                  className="px-2 py-1.5 border border-slate-300 rounded-md outline-none"
                  value={filters.itemType}
                  onChange={e => setFilters({...filters, itemType: e.target.value})}
                >
                  <option value="">Tất cả</option>
                  <option value="lesson">Bài học</option>
                  <option value="document">Tài liệu</option>
                  <option value="quiz">Quiz</option>
                  <option value="flashcard">Flashcard</option>
                </select>
              </div>
            )}
          </>
        )}
        
        <button onClick={handleResetFilters} className="px-3 py-1.5 text-slate-500 hover:text-slate-700 font-medium ml-auto">
          Đặt lại
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-200 mb-6 overflow-x-auto">
        <button 
          onClick={() => setActiveTab('activity')} 
          className={`flex items-center gap-2 pb-3 px-4 font-medium border-b-2 whitespace-nowrap transition-colors ${activeTab === 'activity' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          <BookOpenIcon className="w-5 h-5" /> 1. Hoạt động học tập
        </button>
        <button 
          onClick={() => setActiveTab('results')} 
          className={`flex items-center gap-2 pb-3 px-4 font-medium border-b-2 whitespace-nowrap transition-colors ${activeTab === 'results' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          <CheckBadgeIcon className="w-5 h-5" /> 2. Kết quả học tập
        </button>
        <button 
          onClick={() => setActiveTab('recommendations')} 
          className={`flex items-center gap-2 pb-3 px-4 font-medium border-b-2 whitespace-nowrap transition-colors ${activeTab === 'recommendations' ? 'border-purple-600 text-purple-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          <SparklesIcon className="w-5 h-5" /> 3. Hệ thống gợi ý
        </button>
        <button 
          onClick={() => setActiveTab('surveys')} 
          className={`flex items-center gap-2 pb-3 px-4 font-medium border-b-2 whitespace-nowrap transition-colors ${activeTab === 'surveys' ? 'border-emerald-600 text-emerald-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          <ClipboardDocumentListIcon className="w-5 h-5" /> 4. Khảo sát đầu vào
        </button>
      </div>

      {/* Content */}
      <div className="animate-in fade-in duration-200">
        {loading ? (
          <div className="text-center py-12 text-slate-500">Đang tải báo cáo...</div>
        ) : (
          <div className="space-y-6">
            {/* KPI Cards */}
            {activeTab === 'activity' && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Số lượt học</p>
                  <p className="text-2xl font-bold text-slate-900">{data.summary.total_views || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Số lượt hoàn thành</p>
                  <p className="text-2xl font-bold text-emerald-600">{data.summary.total_completed || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Tỷ lệ hoàn thành</p>
                  <p className="text-2xl font-bold text-blue-600">{data.summary.completion_rate || 0}%</p>
                </div>
              </div>
            )}

            {activeTab === 'results' && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Sinh viên làm Quiz</p>
                  <p className="text-2xl font-bold text-slate-900">{data.summary.total_students || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Số lượt làm Quiz</p>
                  <p className="text-2xl font-bold text-slate-900">{data.summary.total_attempts || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Tỷ lệ Đạt (Pass)</p>
                  <p className="text-2xl font-bold text-emerald-600">{data.summary.pass_rate || 0}%</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Điểm trung bình</p>
                  <p className="text-2xl font-bold text-blue-600">{data.summary.avg_score || 0}</p>
                </div>
              </div>
            )}

            {activeTab === 'recommendations' && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 border-l-4 border-l-purple-500">
                  <p className="text-sm font-medium text-slate-500">Tổng lượt đề xuất</p>
                  <p className="text-2xl font-bold text-slate-900">{data.summary.total_recs || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Lượt tương tác (Click)</p>
                  <p className="text-2xl font-bold text-slate-900">{data.summary.clicked_recs || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Tỷ lệ tương tác</p>
                  <p className="text-2xl font-bold text-emerald-600">{data.summary.click_rate || 0}%</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Độ phù hợp (Score)</p>
                  <p className="text-2xl font-bold text-blue-600">{data.summary.avg_score || 0}</p>
                </div>
              </div>
            )}

            {activeTab === 'surveys' && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 border-l-4 border-l-emerald-500">
                  <p className="text-sm font-medium text-slate-500">Tổng Sinh viên</p>
                  <p className="text-2xl font-bold text-slate-900">{data.summary.total_users || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Đã hoàn thành KS</p>
                  <p className="text-2xl font-bold text-emerald-600">{data.summary.completed || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Chưa làm KS</p>
                  <p className="text-2xl font-bold text-amber-600">{data.summary.pending || 0}</p>
                </div>
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                  <p className="text-sm font-medium text-slate-500">Tỷ lệ hoàn thành</p>
                  <p className="text-2xl font-bold text-blue-600">{data.summary.completion_rate || 0}%</p>
                </div>
              </div>
            )}

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse min-w-[800px]">
                  <thead>
                    <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase text-slate-500 font-semibold">
                      {activeTab === 'activity' && (
                        <>
                          <th className="px-6 py-4">Nội dung</th>
                          <th className="px-6 py-4">Chủ đề</th>
                          <th className="px-6 py-4">Loại</th>
                          <th className="px-6 py-4 text-center">Số lượt học</th>
                          <th className="px-6 py-4 text-center">Hoàn thành</th>
                          <th className="px-6 py-4 text-center">Tỷ lệ</th>
                        </>
                      )}
                      {activeTab === 'results' && (
                        <>
                          <th className="px-6 py-4">Chủ đề</th>
                          <th className="px-6 py-4 text-center">Số SV</th>
                          <th className="px-6 py-4 text-center">Số lượt làm</th>
                          <th className="px-6 py-4 text-center">Tỷ lệ Đạt</th>
                          <th className="px-6 py-4 text-center">Điểm TB</th>
                        </>
                      )}
                      {activeTab === 'recommendations' && (
                        <>
                          <th className="px-6 py-4">Sinh viên</th>
                          <th className="px-6 py-4">Nội dung đề xuất</th>
                          <th className="px-6 py-4">Loại</th>
                          <th className="px-6 py-4 text-center">Độ phù hợp</th>
                          <th className="px-6 py-4 text-center">Trạng thái</th>
                        </>
                      )}
                      {activeTab === 'surveys' && (
                        <>
                          <th className="px-6 py-4">Sinh viên</th>
                          <th className="px-6 py-4 text-center">Điểm KT Đầu vào</th>
                          <th className="px-6 py-4">Chủ đề Quan tâm</th>
                          <th className="px-6 py-4">Mục tiêu</th>
                          <th className="px-6 py-4 text-right">Chi tiết</th>
                        </>
                      )}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {data.details.length === 0 ? (
                      <tr>
                        <td colSpan="6" className="px-6 py-12 text-center text-slate-500">
                          Chưa có dữ liệu báo cáo trong khoảng thời gian đã chọn.
                        </td>
                      </tr>
                    ) : (
                      data.details.slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE).map((row, idx) => (
                        <tr key={idx} className="hover:bg-slate-50/50">
                          {activeTab === 'activity' && (
                            <>
                              <td className="px-6 py-4 font-medium text-slate-900">{row.title}</td>
                              <td className="px-6 py-4 text-sm text-slate-600">{row.topic}</td>
                              <td className="px-6 py-4 text-sm text-slate-500 uppercase">{row.type}</td>
                              <td className="px-6 py-4 text-center font-medium">{row.views}</td>
                              <td className="px-6 py-4 text-center text-emerald-600 font-medium">{row.completed}</td>
                              <td className="px-6 py-4 text-center text-blue-600 font-medium">{row.completion_rate}%</td>
                            </>
                          )}
                          {activeTab === 'results' && (
                            <>
                              <td className="px-6 py-4 font-medium text-slate-900">{row.topic}</td>
                              <td className="px-6 py-4 text-center font-medium">{row.students_count}</td>
                              <td className="px-6 py-4 text-center font-medium">{row.attempts}</td>
                              <td className="px-6 py-4 text-center text-emerald-600 font-medium">{row.pass_rate}%</td>
                              <td className="px-6 py-4 text-center text-blue-600 font-bold">{row.avg_score}</td>
                            </>
                          )}
                          {activeTab === 'recommendations' && (
                            <>
                              <td className="px-6 py-4 font-bold text-slate-900">{row.user_name}</td>
                              <td className="px-6 py-4 text-slate-800 font-medium">{row.item_title}</td>
                              <td className="px-6 py-4 text-sm text-slate-500 uppercase">{row.item_type}</td>
                              <td className="px-6 py-4 text-center text-blue-600 font-bold">{row.score}</td>
                              <td className="px-6 py-4 text-center">
                                {row.is_clicked ? (
                                  <span className="px-2 py-1 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded-full">Đã Click</span>
                                ) : (
                                  <span className="px-2 py-1 bg-slate-100 text-slate-500 text-xs font-semibold rounded-full">Bỏ qua</span>
                                )}
                              </td>
                            </>
                          )}
                          {activeTab === 'surveys' && (
                            <>
                              <td className="px-6 py-4 font-bold text-slate-900">{row.user_name}</td>
                              <td className="px-6 py-4 text-center font-bold text-blue-600">{row.knowledge_score}</td>
                              <td className="px-6 py-4 text-sm text-slate-600">{row.interests}</td>
                              <td className="px-6 py-4 text-sm text-slate-600">{row.goals}</td>
                              <td className="px-6 py-4 text-right">
                                <button onClick={() => alert(JSON.stringify(row, null, 2))} className="text-blue-600 hover:underline text-sm font-medium">Xem chi tiết</button>
                              </td>
                            </>
                          )}
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {data.details.length > ITEMS_PER_PAGE && (
              <div className="flex items-center justify-between bg-white px-4 py-3 border border-slate-200 rounded-xl shadow-sm mt-4">
                <div className="text-sm text-slate-500">
                  Hiển thị <span className="font-medium">{(currentPage - 1) * ITEMS_PER_PAGE + 1}</span> đến <span className="font-medium">{Math.min(currentPage * ITEMS_PER_PAGE, data.details.length)}</span> trong số <span className="font-medium">{data.details.length}</span> kết quả
                </div>
                <div className="flex gap-2">
                  <button 
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                    className="px-3 py-1 border border-slate-300 rounded-md text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Trước
                  </button>
                  <button 
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, Math.ceil(data.details.length / ITEMS_PER_PAGE)))}
                    disabled={currentPage === Math.ceil(data.details.length / ITEMS_PER_PAGE)}
                    className="px-3 py-1 border border-slate-300 rounded-md text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Sau
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
