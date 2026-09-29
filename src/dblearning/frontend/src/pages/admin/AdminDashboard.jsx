import { useState, useEffect } from 'react';
import { adminApi } from '../../api/adminApi';
import { motion } from 'framer-motion';
import { 
  UsersIcon, 
  BookOpenIcon, 
  ClipboardDocumentCheckIcon, 
  ChartBarSquareIcon,
  CalendarDaysIcon,
  TrophyIcon,
  FireIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  CheckBadgeIcon,
  DocumentTextIcon,
  PlayIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [userGrowth, setUserGrowth] = useState([]);
  const [topicStats, setTopicStats] = useState([]);
  const [performance, setPerformance] = useState(null);
  const [activeStudents, setActiveStudents] = useState([]);
  const [popularLessons, setPopularLessons] = useState([]);
  const [recentActivities, setRecentActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [
          statsData, growthData, topicData, perfData, 
          studentsData, lessonsData, activityData
        ] = await Promise.all([
          adminApi.getDashboardStats(),
          adminApi.getUserGrowthChart(),
          adminApi.getTopicLearningChart(),
          adminApi.getPerformanceStats(),
          adminApi.getActiveStudents(),
          adminApi.getPopularLessons(),
          adminApi.getRecentActivities()
        ]);
        
        // Format dates in userGrowth to DD/MM
        const formattedGrowth = growthData.map(d => {
          const date = new Date(d.date);
          return { ...d, displayDate: `${date.getDate()}/${date.getMonth() + 1}` };
        });

        setStats(statsData);
        setUserGrowth(formattedGrowth);
        setTopicStats(topicData);
        setPerformance(perfData);
        setActiveStudents(studentsData);
        setPopularLessons(lessonsData);
        setRecentActivities(activityData);
      } catch (err) {
        console.error("Error fetching admin stats", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[70vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const statCards = [
    { 
      name: 'Tổng người dùng', 
      value: stats?.total_users || 0, 
      increase: stats?.user_growth_rate || 0,
      subtext: `${stats?.total_students || 0} sinh viên | ${stats?.total_admins || 0} quản trị viên`,
      icon: UsersIcon, color: 'text-blue-600', bg: 'bg-blue-100', iconBg: 'bg-blue-50' 
    },
    { 
      name: 'Tổng bài học', 
      value: stats?.total_learning_items || 0, 
      increase: stats?.item_growth_rate || 0,
      subtext: `${stats?.total_topics || 0} chủ đề | ${stats?.total_learning_items || 0} bài học`,
      icon: BookOpenIcon, color: 'text-green-600', bg: 'bg-green-100', iconBg: 'bg-green-50' 
    },
    { 
      name: 'Tổng quiz', 
      value: stats?.total_quizzes || 0, 
      increase: stats?.quiz_growth_rate || 0,
      subtext: `${stats?.total_questions || 0} câu hỏi`,
      icon: ClipboardDocumentCheckIcon, color: 'text-rose-600', bg: 'bg-rose-100', iconBg: 'bg-rose-50' 
    },
    { 
      name: 'Lượt học hôm nay', 
      value: stats?.today_sessions || 0, 
      increase: stats?.session_growth_rate || 0,
      subtext: `Tăng ${Math.max(0, (stats?.today_sessions || 0) - (stats?.yesterday_sessions || 0))} lượt so với hôm qua`,
      icon: ChartBarSquareIcon, color: 'text-purple-600', bg: 'bg-purple-100', iconBg: 'bg-purple-50' 
    },
  ];

  // Helper for pie chart colors if API doesn't provide enough
  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6', '#F43F5E', '#64748B'];

  return (
    <div className="space-y-6">
      {/* Header Area */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Tổng quan hệ thống</h1>
          <p className="text-slate-500 mt-1 text-sm">Theo dõi tình hình hoạt động và hiệu quả học tập của sinh viên</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 shadow-sm transition-colors">
          <CalendarDaysIcon className="w-5 h-5 text-slate-400" />
          30 ngày gần đây
        </button>
      </div>

      {/* 4 Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, idx) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col justify-between hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start mb-4">
              <div className={`p-3 rounded-xl ${stat.iconBg}`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-slate-500">{stat.name}</p>
                <div className="flex items-end justify-end gap-2 mt-1">
                  <span className="text-3xl font-bold text-slate-900 leading-none">{stat.value}</span>
                  <span className="flex items-center text-sm font-semibold text-green-600 mb-0.5">
                    <ArrowTrendingUpIcon className="w-4 h-4 mr-0.5" />
                    {stat.increase}%
                  </span>
                </div>
              </div>
            </div>
            <p className="text-xs text-slate-500 font-medium">{stat.subtext}</p>
          </motion.div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* User Growth Chart */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <div className="flex items-center gap-2 mb-6">
            <UsersIcon className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-bold text-slate-800">Số lượng người dùng mới</h2>
          </div>
          <div className="h-[280px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={userGrowth} margin={{ top: 5, right: 20, bottom: 5, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="displayDate" tick={{fontSize: 12, fill: '#64748b'}} tickMargin={10} axisLine={false} tickLine={false} />
                <YAxis allowDecimals={false} tick={{fontSize: 12, fill: '#64748b'}} axisLine={false} tickLine={false} />
                <Tooltip 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  labelStyle={{ fontWeight: 'bold', color: '#0F172A', marginBottom: '4px' }}
                />
                <Line type="monotone" dataKey="count" name="Đăng ký mới" stroke="#2563EB" strokeWidth={3} dot={{ r: 4, fill: '#2563EB', strokeWidth: 0 }} activeDot={{ r: 6, stroke: '#DBEAFE', strokeWidth: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Topic Learning Pie Chart */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <div className="flex items-center gap-2 mb-2">
            <ChartBarSquareIcon className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-bold text-slate-800">Lượt học theo chủ đề</h2>
          </div>
          <div className="h-[280px] w-full flex items-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={topicStats.length > 0 ? topicStats : [{name: 'Chưa có', sessions: 1}]}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="sessions"
                >
                  {topicStats.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color || COLORS[index % COLORS.length]} />
                  ))}
                  {topicStats.length === 0 && <Cell fill="#cbd5e1" />}
                </Pie>
                <Tooltip 
                  formatter={(value) => [value, 'Lượt học']}
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Legend layout="vertical" verticalAlign="middle" align="right" wrapperStyle={{ fontSize: '13px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row 3: 3 Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Performance Stats */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex flex-col">
          <div className="flex items-center gap-2 mb-6">
            <ChartBarSquareIcon className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-bold text-slate-800">Hiệu quả học tập</h2>
          </div>
          <div className="space-y-6 flex-1 flex flex-col justify-center">
            {[
              { label: 'Tỷ lệ hoàn thành bài học', val: performance?.completion_rate || 0, icon: CheckBadgeIcon, color: 'bg-blue-500', iconBg: 'bg-blue-100 text-blue-600' },
              { label: 'Điểm quiz trung bình', val: performance?.avg_quiz_score || 0, icon: TrophyIcon, color: 'bg-green-500', iconBg: 'bg-green-100 text-green-600' },
              { label: 'Tỷ lệ làm quiz', val: performance?.quiz_attempt_rate || 0, icon: PlayIcon, color: 'bg-amber-500', iconBg: 'bg-amber-100 text-amber-600' },
              { label: 'Tỷ lệ xem tài liệu', val: performance?.document_view_rate || 0, icon: DocumentTextIcon, color: 'bg-purple-500', iconBg: 'bg-purple-100 text-purple-600' }
            ].map((item, i) => (
              <div key={i} className="flex items-center gap-4">
                <div className={`p-2 rounded-lg ${item.iconBg}`}>
                  <item.icon className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-end mb-1">
                    <span className="text-sm font-medium text-slate-700">{item.label}</span>
                    <span className="text-sm font-bold text-slate-900">{item.val}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                    <div className={`${item.color} h-2 rounded-full`} style={{ width: `${item.val}%` }}></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Active Students */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <TrophyIcon className="w-5 h-5 text-amber-500" />
              <h2 className="text-lg font-bold text-slate-800">Sinh viên hoạt động nhiều nhất</h2>
            </div>
            <button className="text-sm font-medium text-blue-600 hover:text-blue-700">Xem tất cả &rarr;</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-y border-slate-100">
                <tr>
                  <th className="px-4 py-3 font-medium">#</th>
                  <th className="px-4 py-3 font-medium">Tên sinh viên</th>
                  <th className="px-4 py-3 font-medium text-center">Bài học đã học</th>
                  <th className="px-4 py-3 font-medium text-center">Quiz đã làm</th>
                  <th className="px-4 py-3 font-medium text-center">Điểm TB</th>
                  <th className="px-4 py-3 font-medium text-right">Thời gian học</th>
                </tr>
              </thead>
              <tbody>
                {activeStudents.map((student, idx) => (
                  <tr key={student.id} className="border-b border-slate-50 last:border-0 hover:bg-slate-50">
                    <td className="px-4 py-3 font-medium text-slate-500">{idx + 1}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-xs font-bold">
                          {student.full_name.charAt(0)}
                        </div>
                        <span className="font-medium text-slate-900">{student.full_name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center text-slate-600">{student.completed_items}</td>
                    <td className="px-4 py-3 text-center text-slate-600">{student.quizzes_taken}</td>
                    <td className="px-4 py-3 text-center font-semibold text-green-600">{student.avg_score}</td>
                    <td className="px-4 py-3 text-right text-slate-500">{student.total_hours}h</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Row 4: 2 Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Popular Lessons */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <FireIcon className="w-5 h-5 text-red-500" />
              <h2 className="text-lg font-bold text-slate-800">Bài học truy cập nhiều nhất</h2>
            </div>
            <button className="text-sm font-medium text-blue-600 hover:text-blue-700">Xem tất cả &rarr;</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-y border-slate-100">
                <tr>
                  <th className="px-4 py-3 font-medium">#</th>
                  <th className="px-4 py-3 font-medium">Tên bài học</th>
                  <th className="px-4 py-3 font-medium text-right">Lượt truy cập</th>
                </tr>
              </thead>
              <tbody>
                {popularLessons.map((lesson, idx) => (
                  <tr key={lesson.id} className="border-b border-slate-50 last:border-0 hover:bg-slate-50">
                    <td className="px-4 py-3 font-medium text-slate-500">{idx + 1}</td>
                    <td className="px-4 py-3 flex items-center gap-2">
                      <DocumentTextIcon className="w-4 h-4 text-slate-400" />
                      <span className="font-medium text-slate-900 truncate max-w-[200px]">{lesson.title}</span>
                    </td>
                    <td className="px-4 py-3 text-right font-medium text-slate-700">{lesson.view_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Activities */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <ClockIcon className="w-5 h-5 text-blue-600" />
              <h2 className="text-lg font-bold text-slate-800">Hoạt động gần đây</h2>
            </div>
            <button className="text-sm font-medium text-blue-600 hover:text-blue-700">Xem tất cả &rarr;</button>
          </div>
          <div className="space-y-4 mt-2">
            {recentActivities.map((act) => (
              <div key={act.id} className="flex items-start gap-4">
                <div className={`p-2 rounded-lg mt-1 ${
                  act.type === 'quiz' ? 'bg-rose-100 text-rose-600' :
                  act.type === 'document' ? 'bg-purple-100 text-purple-600' :
                  'bg-green-100 text-green-600'
                }`}>
                  {act.type === 'quiz' ? <ClipboardDocumentCheckIcon className="w-4 h-4" /> : 
                   act.type === 'document' ? <DocumentTextIcon className="w-4 h-4" /> : 
                   <BookOpenIcon className="w-4 h-4" />}
                </div>
                <div className="flex-1">
                  <p className="text-sm text-slate-800">
                    <span className="font-semibold">{act.user_name}</span> {act.action} <span className="font-medium">{act.target}</span>
                  </p>
                  <p className="text-xs text-slate-400 mt-0.5">{act.time_ago}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
}
