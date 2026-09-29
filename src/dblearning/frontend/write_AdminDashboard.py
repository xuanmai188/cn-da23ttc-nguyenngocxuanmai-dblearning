file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
import os
os.makedirs(os.path.dirname(file_path), exist_ok=True)
content = """import { useState, useEffect } from 'react';
import { adminApi } from '../../api/adminApi';
import { motion } from 'framer-motion';
import { UsersIcon, CheckBadgeIcon, PlayIcon, AcademicCapIcon } from '@heroicons/react/24/outline';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await adminApi.getDashboardStats();
        setStats(data);
      } catch (err) {
        console.error("Error fetching admin stats", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const statCards = [
    { name: 'Tổng học viên', value: stats?.total_users || 0, icon: UsersIcon, color: 'text-blue-600', bg: 'bg-blue-100' },
    { name: 'Đang hoạt động', value: stats?.active_users || 0, icon: CheckBadgeIcon, color: 'text-green-600', bg: 'bg-green-100' },
    { name: 'Tổng số phiên học', value: stats?.total_sessions || 0, icon: PlayIcon, color: 'text-purple-600', bg: 'bg-purple-100' },
    { name: 'Tỷ lệ hoàn thành', value: `${stats?.avg_completion_rate || 0}%`, icon: AcademicCapIcon, color: 'text-amber-600', bg: 'bg-amber-100' },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Tổng quan hệ thống</h1>
        <p className="text-gray-500 mt-1">Xem nhanh các chỉ số hoạt động của DB Learning</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat, idx) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex items-center gap-4"
          >
            <div className={`p-4 rounded-lg ${stat.bg}`}>
              <stat.icon className={`w-8 h-8 ${stat.color}`} />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500">{stat.name}</p>
              <p className="text-3xl font-bold text-gray-900 mt-1">{stat.value}</p>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Placeholder for future charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 min-h-[300px] flex items-center justify-center">
          <p className="text-gray-400">Biểu đồ người dùng (Đang phát triển)</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 min-h-[300px] flex items-center justify-center">
          <p className="text-gray-400">Biểu đồ tiến trình học tập (Đang phát triển)</p>
        </div>
      </div>
    </div>
  );
}
"""
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("AdminDashboard.jsx written")
