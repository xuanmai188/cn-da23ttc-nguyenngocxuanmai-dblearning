import { UsersIcon, AcademicCapIcon, ShieldCheckIcon, NoSymbolIcon, ArrowTrendingUpIcon, ArrowTrendingDownIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

export default function UserStatsCards({ stats }) {
  if (!stats) return null;

  const cards = [
    {
      title: 'Tổng người dùng',
      value: stats.total,
      increase: stats.growth_rate,
      subtext: 'so với tháng trước',
      icon: UsersIcon,
      color: 'text-blue-600',
      bg: 'bg-blue-50',
    },
    {
      title: 'Sinh viên',
      value: stats.students,
      increase: null,
      subtext: `${stats.student_rate}% tổng số`,
      icon: AcademicCapIcon,
      color: 'text-green-600',
      bg: 'bg-green-50',
    },
    {
      title: 'Quản trị viên',
      value: stats.admins,
      increase: null,
      subtext: `${stats.admin_rate}% tổng số`,
      icon: ShieldCheckIcon,
      color: 'text-purple-600',
      bg: 'bg-purple-50',
    },
    {
      title: 'Tài khoản bị khóa',
      value: stats.blocked,
      increase: null,
      subtext: `${stats.blocked_rate}% tổng số`,
      icon: NoSymbolIcon,
      color: 'text-red-600',
      bg: 'bg-red-50',
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
      {cards.map((card, idx) => (
        <motion.div
          key={card.title}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.1 }}
          className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center gap-4"
        >
          <div className={`p-4 rounded-xl ${card.bg}`}>
            <card.icon className={`w-8 h-8 ${card.color}`} />
          </div>
          <div>
            <p className="text-sm font-medium text-slate-500 mb-1">{card.title}</p>
            <div className="flex items-end gap-2">
              <span className="text-2xl font-bold text-slate-900 leading-none">{card.value}</span>
              {card.increase !== null && (
                <span className={`flex items-center text-sm font-semibold mb-0.5 ${card.increase >= 0 ? 'text-green-600' : 'text-red-500'}`}>
                  {card.increase >= 0 ? <ArrowTrendingUpIcon className="w-4 h-4 mr-0.5" /> : <ArrowTrendingDownIcon className="w-4 h-4 mr-0.5" />}
                  {Math.abs(card.increase)}%
                </span>
              )}
            </div>
            <p className="text-xs text-slate-500 mt-1">{card.subtext}</p>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
