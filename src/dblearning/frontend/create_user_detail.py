file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
content = """import { useState, useEffect } from 'react';
import { XMarkIcon, EnvelopeIcon, PhoneIcon, CalendarIcon, ClockIcon, BookOpenIcon, CheckBadgeIcon, ChartBarIcon, PencilIcon, LockClosedIcon, KeyIcon } from '@heroicons/react/24/outline';
import { adminApi } from '../../../api/adminApi';

export default function UserDetailPanel({ user, onClose }) {
  const [activeTab, setActiveTab] = useState('info');
  const [details, setDetails] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;
    const fetchDetailData = async () => {
      setLoading(true);
      try {
        const [detailData, historyData] = await Promise.all([
          adminApi.getUserDetails(user.id),
          adminApi.getUserHistory(user.id)
        ]);
        setDetails(detailData);
        setHistory(historyData.history);
      } catch (err) {
        console.error("Error fetching user details", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDetailData();
  }, [user]);

  if (!user) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-slate-900/20 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />
      
      {/* Panel */}
      <div className="absolute inset-y-0 right-0 max-w-md w-full bg-white shadow-2xl flex flex-col transform transition-transform duration-300">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <h2 className="text-lg font-bold text-slate-900">Thông tin người dùng</h2>
          <button onClick={onClose} className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-full transition-colors">
            <XMarkIcon className="w-5 h-5" />
          </button>
        </div>

        {loading ? (
          <div className="flex-1 flex items-center justify-center">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto">
            {/* User Profile Summary */}
            <div className="px-6 py-6 border-b border-slate-100">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xl font-bold">
                  {details?.full_name?.charAt(0)}
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900">{details?.full_name}</h3>
                  <div className="mt-1 flex items-center gap-2">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
                      details?.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${details?.is_active ? 'bg-green-500' : 'bg-red-500'}`}></span>
                      {details?.is_active ? 'Hoạt động' : 'Tạm khóa'}
                    </span>
                    <span className="text-xs text-slate-500 bg-slate-100 px-2 py-1 rounded">
                      {details?.role === 'admin' ? 'Quản trị viên' : 'Sinh viên'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Tabs */}
            <div className="px-6 border-b border-slate-200">
              <div className="flex gap-6 -mb-px">
                {['info', 'progress', 'history'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`py-3 text-sm font-medium border-b-2 transition-colors ${
                      activeTab === tab 
                        ? 'border-blue-600 text-blue-600' 
                        : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                    }`}
                  >
                    {tab === 'info' ? 'Thông tin' : tab === 'progress' ? 'Tiến độ học tập' : 'Lịch sử'}
                  </button>
                ))}
              </div>
            </div>

            {/* Tab Content */}
            <div className="px-6 py-6">
              
              {/* INFO TAB */}
              {activeTab === 'info' && (
                <div className="space-y-6">
                  <div className="space-y-4">
                    <div className="flex items-center gap-3">
                      <EnvelopeIcon className="w-5 h-5 text-slate-400" />
                      <div className="flex-1">
                        <p className="text-xs text-slate-500 font-medium">Email</p>
                        <p className="text-sm font-medium text-slate-900">{details?.email}</p>
                      </div>
                    </div>
                    {details?.phone_number && (
                      <div className="flex items-center gap-3">
                        <PhoneIcon className="w-5 h-5 text-slate-400" />
                        <div className="flex-1">
                          <p className="text-xs text-slate-500 font-medium">Số điện thoại</p>
                          <p className="text-sm font-medium text-slate-900">{details?.phone_number}</p>
                        </div>
                      </div>
                    )}
                    <div className="flex items-center gap-3">
                      <CalendarIcon className="w-5 h-5 text-slate-400" />
                      <div className="flex-1">
                        <p className="text-xs text-slate-500 font-medium">Ngày đăng ký</p>
                        <p className="text-sm font-medium text-slate-900">
                          {new Date(details?.created_at + 'Z').toLocaleDateString('vi-VN')}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <ClockIcon className="w-5 h-5 text-slate-400" />
                      <div className="flex-1">
                        <p className="text-xs text-slate-500 font-medium">Hoạt động cuối</p>
                        <p className="text-sm font-medium text-slate-900">{details?.last_activity_at || 'Chưa có hoạt động'}</p>
                      </div>
                    </div>
                  </div>

                  {details?.role === 'student' && (
                    <div className="mt-8">
                      <h4 className="text-sm font-bold text-slate-900 mb-4">Thống kê nhanh</h4>
                      <div className="grid grid-cols-2 gap-3">
                        <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100">
                          <BookOpenIcon className="w-6 h-6 text-blue-600 mb-2" />
                          <div className="text-xl font-bold text-slate-900 leading-none mb-1">{details?.stats?.completed_lessons}</div>
                          <div className="text-[11px] text-slate-500 font-medium">Bài học đã hoàn thành</div>
                        </div>
                        <div className="bg-green-50/50 p-4 rounded-xl border border-green-100">
                          <CheckBadgeIcon className="w-6 h-6 text-green-600 mb-2" />
                          <div className="text-xl font-bold text-slate-900 leading-none mb-1">{details?.stats?.taken_quizzes}</div>
                          <div className="text-[11px] text-slate-500 font-medium">Quiz đã làm</div>
                        </div>
                        <div className="bg-purple-50/50 p-4 rounded-xl border border-purple-100">
                          <ChartBarIcon className="w-6 h-6 text-purple-600 mb-2" />
                          <div className="text-xl font-bold text-slate-900 leading-none mb-1">{details?.stats?.avg_score}</div>
                          <div className="text-[11px] text-slate-500 font-medium">Điểm trung bình</div>
                        </div>
                        <div className="bg-orange-50/50 p-4 rounded-xl border border-orange-100">
                          <ClockIcon className="w-6 h-6 text-orange-600 mb-2" />
                          <div className="text-xl font-bold text-slate-900 leading-none mb-1">{details?.stats?.total_hours}h</div>
                          <div className="text-[11px] text-slate-500 font-medium">Tổng thời gian học</div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* PROGRESS TAB */}
              {activeTab === 'progress' && (
                <div className="text-center py-10">
                  <ChartBarIcon className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                  <p className="text-slate-500 text-sm">Chi tiết tiến độ học tập (Tính năng đang nâng cấp)</p>
                </div>
              )}

              {/* HISTORY TAB */}
              {activeTab === 'history' && (
                <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
                  {history.length === 0 ? (
                    <p className="text-center text-sm text-slate-500 py-6 relative z-10 bg-white">Không có lịch sử hoạt động</p>
                  ) : (
                    history.map((h, i) => (
                      <div key={h.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                        <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-slate-100 text-slate-500 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                          {h.target_type === 'quiz' ? <CheckBadgeIcon className="w-4 h-4 text-purple-500" /> : <BookOpenIcon className="w-4 h-4 text-blue-500" />}
                        </div>
                        <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-3 rounded-lg border border-slate-200 shadow-sm">
                          <div className="flex items-center justify-between mb-1">
                            <div className="font-bold text-slate-900 text-sm">{h.action}</div>
                            <div className="text-[10px] font-medium text-slate-400">{h.time_ago}</div>
                          </div>
                          <div className="text-xs text-slate-600 truncate">{h.target}</div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Footer Actions */}
        <div className="px-6 py-4 border-t border-slate-100 bg-slate-50">
          <div className="grid grid-cols-2 gap-3 mb-3">
            <button 
              onClick={() => alert('Phase 4')}
              className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
            >
              <PencilIcon className="w-4 h-4" />
              Chỉnh sửa
            </button>
            <button 
              onClick={() => alert('Phase 4')}
              className="flex items-center justify-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
            >
              <LockClosedIcon className="w-4 h-4" />
              Khóa tài khoản
            </button>
          </div>
          <button 
            onClick={() => alert('Phase 4')}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-300 transition-colors"
          >
            <KeyIcon className="w-4 h-4" />
            Đặt lại mật khẩu
          </button>
        </div>

      </div>
    </div>
  );
}
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Created UserDetailPanel.jsx")
