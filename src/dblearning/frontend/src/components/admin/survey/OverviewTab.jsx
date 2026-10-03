import React from 'react';
import { 
  ClipboardDocumentListIcon,
  CheckCircleIcon,
  UsersIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

export default function OverviewTab({ survey, questions, stats, totalStudents, onToggleStatus }) {
  if (!survey) return <div className="text-slate-500">Chưa có bộ khảo sát nào.</div>;

  const totalCompleted = stats.total_completed || 0;
  const completionRate = totalStudents > 0 ? Math.round((totalCompleted / totalStudents) * 100) : 0;
  const activeQuestions = questions.length; // Assumed all fetched are active if survey is active, or filter if status is added

  const getCategoryCount = (cat) => questions.filter(q => q.category === cat).length;

  return (
    <div className="space-y-6">
      {/* 4 Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 shrink-0">
            <ClipboardDocumentListIcon className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Tổng số câu hỏi</p>
            <p className="text-2xl font-bold text-slate-900">{questions.length}</p>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 shrink-0">
            <CheckCircleIcon className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Câu hỏi đang hoạt động</p>
            <p className="text-2xl font-bold text-slate-900">{activeQuestions}</p>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 shrink-0">
            <UsersIcon className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Sinh viên hoàn thành</p>
            <p className="text-2xl font-bold text-slate-900">{totalCompleted}</p>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 shrink-0">
            <ChartBarIcon className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Tỷ lệ hoàn thành</p>
            <p className="text-2xl font-bold text-slate-900">{completionRate}%</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Status */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-bold text-slate-900 mb-4 border-b border-slate-100 pb-3">Thông tin Khảo sát</h3>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-slate-500">Tên khảo sát</p>
              <p className="font-medium text-slate-900">{survey.title}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Trạng thái</p>
              {survey.is_active ? (
                <span className="inline-flex mt-1 items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                  Đang hoạt động
                </span>
              ) : (
                <span className="inline-flex mt-1 items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                  Tạm ngưng
                </span>
              )}
            </div>
            <div className="grid grid-cols-2 gap-4 pt-2">
              <div>
                <p className="text-sm text-slate-500">Số câu hỏi</p>
                <p className="font-medium text-slate-900">{questions.length} câu</p>
              </div>
              <div>
                <p className="text-sm text-slate-500">Sinh viên đã hoàn thành</p>
                <p className="font-medium text-slate-900">{totalCompleted} sinh viên</p>
              </div>
            </div>
            <div className="pt-4 flex gap-3 border-t border-slate-100 mt-2">
              <button 
                onClick={onToggleStatus}
                className={`px-4 py-2 font-medium rounded-lg transition-colors ${
                  survey.is_active ? 'bg-amber-50 text-amber-600 hover:bg-amber-100' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100'
                }`}
              >
                {survey.is_active ? 'Tạm ngưng' : 'Kích hoạt'}
              </button>
            </div>
          </div>
        </div>

        {/* Phân bố câu hỏi */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-bold text-slate-900 mb-4 border-b border-slate-100 pb-3">Phân bố Câu hỏi</h3>
          <div className="space-y-4">
            {[
              { label: 'Kiến thức ban đầu', key: 'knowledge', color: 'bg-blue-500' },
              { label: 'Tự đánh giá', key: 'self_assessment', color: 'bg-emerald-500' },
              { label: 'Nhu cầu / Quan tâm', key: 'interest', color: 'bg-purple-500' },
              { label: 'Mục tiêu học tập', key: 'goal', color: 'bg-amber-500' }
            ].map(cat => {
              const count = getCategoryCount(cat.key);
              const percent = questions.length > 0 ? (count / questions.length) * 100 : 0;
              
              return (
                <div key={cat.key}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium text-slate-700">{cat.label}</span>
                    <span className="text-slate-500">{count} câu</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                    <div className={`${cat.color} h-2 rounded-full`} style={{ width: `${percent}%` }}></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
