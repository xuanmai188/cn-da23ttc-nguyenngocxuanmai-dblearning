import React from 'react';

export default function ResultsTab({ results, stats, totalStudents }) {
  const totalCompleted = stats.total_completed || 0;
  const completionRate = totalStudents > 0 ? Math.round((totalCompleted / totalStudents) * 100) : 0;
  const notCompleted = totalStudents - totalCompleted;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <p className="text-sm font-medium text-slate-500">Tổng số sinh viên</p>
          <p className="text-2xl font-bold text-slate-900">{totalStudents}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <p className="text-sm font-medium text-slate-500">Đã hoàn thành</p>
          <p className="text-2xl font-bold text-emerald-600">{totalCompleted}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <p className="text-sm font-medium text-slate-500">Chưa hoàn thành</p>
          <p className="text-2xl font-bold text-amber-600">{notCompleted > 0 ? notCompleted : 0}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <p className="text-sm font-medium text-slate-500">Tỷ lệ hoàn thành</p>
          <p className="text-2xl font-bold text-blue-600">{completionRate}%</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs uppercase text-slate-500 font-semibold">
              <th className="px-6 py-4">Sinh viên</th>
              <th className="px-6 py-4">Trạng thái</th>
              <th className="px-6 py-4">Điểm kiến thức</th>
              <th className="px-6 py-4">Thời gian hoàn thành</th>
              <th className="px-6 py-4 text-right">Chi tiết</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {results.length === 0 ? (
              <tr>
                <td colSpan="5" className="px-6 py-8 text-center text-slate-500">
                  Chưa có sinh viên nào hoàn thành khảo sát.
                </td>
              </tr>
            ) : (
              results.map((r) => (
                <tr key={r.id} className="hover:bg-slate-50/50">
                  <td className="px-6 py-4">
                    <p className="font-bold text-slate-900">{r.user_name}</p>
                    <p className="text-sm text-slate-500">{r.email}</p>
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                      Hoàn thành
                    </span>
                  </td>
                  <td className="px-6 py-4 font-medium text-slate-700">
                    {r.total_score || 0} điểm
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-600">
                    {new Date(r.completed_at).toLocaleString('vi-VN')}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button 
                      onClick={() => alert('Chức năng Xem chi tiết (Modal) sẽ được triển khai. \n\nDữ liệu hiện tại: ' + JSON.stringify(r.answers, null, 2))} 
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      Xem chi tiết
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
