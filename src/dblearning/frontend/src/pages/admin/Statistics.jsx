import React, { useState, useEffect } from 'react';
import { adminApi } from '../../api/adminApi';
import { 
  UsersIcon, 
  AcademicCapIcon, 
  DocumentDuplicateIcon, 
  ChartBarIcon 
} from '@heroicons/react/24/outline';
import { 
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';

export default function Statistics() {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await adminApi.getFullStatistics();
        setStats(data);
      } catch (err) {
        console.error('Lỗi khi tải thống kê:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="text-center py-10 text-slate-500">
        Không thể tải dữ liệu thống kê. Vui lòng thử lại sau.
      </div>
    );
  }

  // --- DATA MAPPING ---

  // 1. Cơ cấu người dùng
  const roleData = [
    { name: 'Học viên', value: stats.users.students || 0, color: '#3b82f6' },
    { name: 'Quản trị viên', value: stats.users.admins || 0, color: '#8b5cf6' },
  ];
  
  // Tỷ lệ phần trăm
  const totalUsersWithRoles = (stats.users.students || 0) + (stats.users.admins || 0);
  const studentRate = totalUsersWithRoles > 0 ? Math.round((stats.users.students / totalUsersWithRoles) * 100) : 0;

  // 2. Hiệu suất học tập
  const perfData = [
    { name: 'Hoàn thành', value: stats.performance.completion_rate || 0, fill: '#10b981' },
    { name: 'Điểm TB', value: stats.performance.avg_quiz_score || 0, fill: '#f59e0b' },
    { name: 'Làm Quiz', value: stats.performance.quiz_attempt_rate || 0, fill: '#8b5cf6' },
    { name: 'Đọc tài liệu', value: stats.performance.document_view_rate || 0, fill: '#3b82f6' },
  ];

  // 3. Phân bố nội dung
  const contentData = [
    { name: 'Bài học Video', value: stats.content_distribution.video || 0, color: '#ef4444' },
    { name: 'Tài liệu đọc', value: stats.content_distribution.document || 0, color: '#3b82f6' },
    { name: 'Bài kiểm tra', value: stats.content_distribution.quiz || 0, color: '#f59e0b' },
    { name: 'Bộ Flashcard', value: stats.content_distribution.flashcard_set || 0, color: '#10b981' },
  ];
  const hasContentData = contentData.some(d => d.value > 0);

  // Custom Label cho PieChart Nội dung
  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * Math.PI / 180);
    const y = cy + radius * Math.sin(-midAngle * Math.PI / 180);
    if (percent === 0) return null;
    return (
      <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize="12" fontWeight="bold">
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="pb-10">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900">Thống kê hệ thống</h1>
        <p className="text-slate-500 mt-1">Báo cáo tổng quan về người dùng, hiệu suất học tập và hiệu quả hệ thống AI gợi ý.</p>
      </div>

      {/* HÀNG 1: TỔNG QUAN HỆ THỐNG */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Tổng người dùng */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 shrink-0">
            <UsersIcon className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Tổng người dùng</p>
            <p className="text-2xl font-bold text-slate-900">{stats.overview.total_users || 0}</p>
          </div>
        </div>
        
        {/* Người dùng đang hoạt động */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 shrink-0">
            <AcademicCapIcon className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Hoạt động (7 ngày qua)</p>
            <p className="text-2xl font-bold text-slate-900">{stats.overview.active_users || 0}</p>
          </div>
        </div>

        {/* Tổng số nội dung */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 shrink-0">
            <DocumentDuplicateIcon className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Tổng số nội dung</p>
            <p className="text-2xl font-bold text-slate-900">{stats.overview.total_items || 0}</p>
          </div>
        </div>

        {/* Điểm Quiz trung bình */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 shrink-0">
            <ChartBarIcon className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500">Điểm Quiz trung bình</p>
            <p className="text-2xl font-bold text-slate-900">{stats.overview.avg_quiz_score || 0}</p>
          </div>
        </div>
      </div>

      {/* HÀNG 2: NGƯỜI DÙNG & HIỆU SUẤT */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        
        {/* Cơ cấu người dùng */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-800 mb-6">Cơ cấu Người dùng</h2>
          {totalUsersWithRoles === 0 ? (
            <div className="h-[300px] flex items-center justify-center text-slate-400">
              Chưa có dữ liệu thống kê.
            </div>
          ) : (
            <>
              <div className="h-[280px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={roleData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {roleData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value) => [`${value} tài khoản`, 'Số lượng']}
                      contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    />
                    <Legend verticalAlign="bottom" height={36} iconType="circle" />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 grid grid-cols-2 gap-4 text-center border-t border-slate-100 pt-4">
                <div>
                  <p className="text-sm text-slate-500">Tỷ lệ Học viên</p>
                  <p className="text-xl font-bold text-blue-600">{studentRate}%</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Tài khoản bị khóa</p>
                  <p className="text-xl font-bold text-red-500">{stats.users.blocked || 0}</p>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Hiệu suất học tập */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-800 mb-6">Chỉ số Hiệu suất Học tập (%)</h2>
          <div className="h-[280px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={perfData}
                margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} domain={[0, 100]} />
                <Tooltip 
                  cursor={{ fill: '#f8fafc' }}
                  formatter={(value) => [`${value}%`, 'Chỉ số']}
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Bar dataKey="value" radius={[6, 6, 0, 0]} maxBarSize={60}>
                  {perfData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 border-t border-slate-100 pt-4 text-sm text-slate-500 flex items-center justify-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 block"></span>
            Tỷ lệ dựa trên tổng số phiên học đã thực hiện.
          </div>
        </div>

      </div>

      {/* HÀNG 3: NỘI DUNG & HỆ THỐNG GỢI Ý */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Phân bố nội dung */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-800 mb-6">Phân bố Nội dung Học tập</h2>
          {!hasContentData ? (
             <div className="h-[250px] flex items-center justify-center text-slate-400">
               Chưa có nội dung nào.
             </div>
          ) : (
            <div className="h-[250px] w-full flex items-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={contentData}
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    dataKey="value"
                    labelLine={false}
                    label={renderCustomizedLabel}
                  >
                    {contentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value) => [`${value} tài liệu`, 'Số lượng']}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Legend verticalAlign="middle" align="right" layout="vertical" iconType="circle" />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* Hiệu quả hệ thống gợi ý */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col">
          <h2 className="text-lg font-bold text-slate-800 mb-6 flex items-center justify-between">
            <span>Hiệu quả Hệ thống Gợi ý (AI)</span>
            <span className="text-xs font-normal text-blue-600 bg-blue-50 px-2 py-1 rounded">Mới</span>
          </h2>
          
          <div className="flex-1 grid grid-cols-2 gap-4">
            <div className="bg-slate-50 rounded-lg p-4 flex flex-col justify-center">
              <p className="text-sm font-medium text-slate-500 mb-1">Tổng lượt đề xuất</p>
              <p className="text-3xl font-bold text-slate-900">{stats.recommendations.total || 0}</p>
            </div>
            <div className="bg-slate-50 rounded-lg p-4 flex flex-col justify-center">
              <p className="text-sm font-medium text-slate-500 mb-1">Số lượt xem từ gợi ý</p>
              <p className="text-3xl font-bold text-blue-600">{stats.recommendations.clicked || 0}</p>
            </div>
            
            <div className="col-span-2 mt-2">
              <div className="flex justify-between items-end mb-2">
                <span className="text-sm font-semibold text-slate-700">Tỷ lệ xem nội dung được đề xuất (CTR)</span>
                <span className="text-lg font-bold text-emerald-600">{stats.recommendations.click_rate}%</span>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2.5">
                <div 
                  className="bg-emerald-500 h-2.5 rounded-full" 
                  style={{ width: `${stats.recommendations.click_rate || 0}%` }}
                ></div>
              </div>
            </div>

            <div className="col-span-2 mt-4 pt-4 border-t border-slate-100">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-sm font-medium text-slate-600">Lượt hoàn thành nội dung được gợi ý</p>
                  <p className="text-xs text-slate-400 mt-0.5">Sinh viên học xong nội dung được đề xuất</p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-slate-900">{stats.recommendations.completed || 0}</p>
                  <p className="text-xs font-semibold text-emerald-500">
                    {stats.recommendations.completion_rate}% hiệu quả
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
