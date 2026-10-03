import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ChartBarIcon, 
  UsersIcon, 
  BookOpenIcon, 
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon,
  AcademicCapIcon,
  ChevronDownIcon,
  SparklesIcon,
  ClipboardDocumentCheckIcon,
  DocumentChartBarIcon,
  Cog6ToothIcon,
  MagnifyingGlassIcon,
  BellIcon
} from '@heroicons/react/24/outline';
import { motion, AnimatePresence } from 'framer-motion';

export default function AdminLayout({ children }) {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showNotifMenu, setShowNotifMenu] = useState(false);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const data = await adminApi.getNotifications();
      setNotifications(data.notifications);
      setUnreadCount(data.unreadCount || data.unread_count || 0);
    } catch (error) {
      console.error('Failed to fetch notifications');
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await adminApi.markAllNotificationsRead();
      setUnreadCount(0);
      setNotifications(notifications.map(n => ({...n, is_read: true})));
    } catch (error) {
      console.error(error);
    }
  };

  const handleMarkRead = async (id, is_read) => {
    if (is_read) return;
    try {
      await adminApi.markNotificationRead(id);
      setUnreadCount(prev => Math.max(0, prev - 1));
      setNotifications(notifications.map(n => n.id === id ? {...n, is_read: true} : n));
    } catch (error) {}
  };
  const [isContentMenuOpen, setIsContentMenuOpen] = useState(false);

  // Auto expand content menu if we are in a content route
  useEffect(() => {
    if (location.pathname.startsWith('/admin/content')) {
      setIsContentMenuOpen(true);
    }
  }, [location]);

  const navigation = [
    { name: 'Tổng quan', href: '/admin/dashboard', icon: ChartBarIcon },
    { name: 'Quản lý người dùng', href: '/admin/users', icon: UsersIcon },
    { 
      name: 'Quản lý nội dung', 
      icon: BookOpenIcon,
      isGroup: true,
      isOpen: isContentMenuOpen,
      setIsOpen: setIsContentMenuOpen,
      children: [
        { name: 'Chủ đề', href: '/admin/content?tab=topics' },
        { name: 'Bài học', href: '/admin/content?tab=items' },
        { name: 'Quiz', href: '/admin/content?tab=quiz' },
        { name: 'Flashcard', href: '/admin/content?tab=flashcards' },

      ]
    },
    { name: 'Thống kê', href: '/admin/statistics', icon: ChartBarIcon },
    { name: 'Khảo sát đầu vào', href: '/admin/onboarding', icon: ClipboardDocumentCheckIcon },
    { name: 'Báo cáo', href: '/admin/reports', icon: DocumentChartBarIcon },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-slate-50 flex font-sans text-slate-900">
      {/* Mobile sidebar overlay */}
      <AnimatePresence>
        {isSidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsSidebarOpen(false)}
            className="fixed inset-0 z-40 bg-slate-900/50 backdrop-blur-sm lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-[#0F172A] text-white flex flex-col transition-transform duration-300 lg:translate-x-0 lg:static lg:flex-shrink-0 shadow-xl ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Logo area */}
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/30">
              <AcademicCapIcon className="w-5 h-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-bold tracking-tight leading-tight">DB Learning</span>
              <span className="text-[10px] text-slate-400 font-medium">Học đúng - Tiến xa hơn</span>
            </div>
          </div>
          <button 
            onClick={() => setIsSidebarOpen(false)}
            className="ml-auto lg:hidden p-1 text-slate-400 hover:text-white transition-colors"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>

        {/* Navigation */}
        <div className="flex-1 px-3 py-6 space-y-1 overflow-y-auto custom-scrollbar">
          {navigation.map((item) => {
            if (item.isGroup) {
              const isGroupActive = location.pathname.startsWith('/admin/content');
              return (
                <div key={item.name} className="mb-1">
                  <button
                    onClick={() => item.setIsOpen(!item.isOpen)}
                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                      isGroupActive && !item.isOpen
                        ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20' 
                        : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <item.icon className={`w-5 h-5 ${isGroupActive && !item.isOpen ? 'text-white' : 'text-slate-400'}`} />
                      {item.name}
                    </div>
                    <ChevronDownIcon className={`w-4 h-4 transition-transform duration-200 ${item.isOpen ? 'rotate-180' : ''}`} />
                  </button>
                  
                  <AnimatePresence>
                    {item.isOpen && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                      >
                        <div className="pt-1 pb-2 space-y-1">
                          {item.children.map((child) => {
                            const isChildActive = location.pathname === '/admin/content' && location.search.includes(child.href.split('?')[1]);
                            // If no search params and we are on /admin/content, default to topics
                            const isDefaultActive = location.pathname === '/admin/content' && location.search === '' && child.href.includes('topics');
                            const isActive = isChildActive || isDefaultActive;
                            
                            return (
                              <Link
                                key={child.name}
                                to={child.href}
                                className={`flex items-center gap-3 pl-11 pr-3 py-2 rounded-lg text-sm font-medium transition-colors relative ${
                                  isActive 
                                    ? 'text-white bg-slate-800/50' 
                                    : 'text-slate-400 hover:text-white hover:bg-slate-800/30'
                                }`}
                              >
                                {isActive && (
                                  <div className="absolute left-4 top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full bg-blue-500" />
                                )}
                                {!isActive && (
                                  <div className="absolute left-4 top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full border border-slate-500" />
                                )}
                                {child.name}
                              </Link>
                            );
                          })}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              );
            }

            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 mb-1 ${
                  isActive 
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20' 
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <item.icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                {item.name}
              </Link>
            );
          })}
        </div>

        {/* Logout area */}
        <div className="p-4 border-t border-slate-800">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-3 py-2.5 text-sm font-medium text-red-400 rounded-lg hover:bg-slate-800 hover:text-red-300 transition-colors"
          >
            <ArrowRightOnRectangleIcon className="w-5 h-5" />
            Đăng xuất
          </button>
        </div>
      </div>

      {/* Main content wrapper */}
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center px-4 lg:px-8 justify-between z-10 sticky top-0">
          <div className="flex items-center gap-4 flex-1">
            <button
              onClick={() => setIsSidebarOpen(true)}
              className="lg:hidden p-2 -ml-2 text-slate-500 hover:text-slate-700 transition-colors rounded-lg hover:bg-slate-100"
            >
              <Bars3Icon className="w-6 h-6" />
            </button>
          </div>

          <div className="flex items-center gap-4 lg:gap-6">
                        {/* Notifications */}
            <div className="relative">
              <button 
                onClick={() => setShowNotifMenu(!showNotifMenu)}
                className="relative p-2 text-slate-500 hover:text-slate-700 transition-colors rounded-full hover:bg-slate-100"
              >
                <BellIcon className="w-6 h-6" />
                {unreadCount > 0 && (
                  <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 text-white text-[10px] font-bold flex items-center justify-center rounded-full ring-2 ring-white">
                    {unreadCount > 9 ? '9+' : unreadCount}
                  </span>
                )}
              </button>

              {showNotifMenu && (
                <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden z-50 origin-top-right animate-in fade-in zoom-in-95">
                  <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between bg-slate-50">
                    <h3 className="font-bold text-slate-800">Thông báo</h3>
                    {unreadCount > 0 && (
                      <button 
                        onClick={handleMarkAllRead}
                        className="text-xs font-medium text-blue-600 hover:text-blue-800 cursor-pointer"
                      >
                        Đánh dấu đã đọc
                      </button>
                    )}
                  </div>
                  
                  <div className="max-h-[400px] overflow-y-auto">
                    {notifications.length === 0 ? (
                      <div className="p-6 text-center text-slate-500 text-sm">Chưa có thông báo nào</div>
                    ) : (
                      <div className="divide-y divide-slate-100">
                        {notifications.map(notif => (
                          <div 
                            key={notif.id} 
                            onClick={() => handleMarkRead(notif.id, notif.is_read)}
                            className={`p-4 hover:bg-slate-50 transition-colors cursor-pointer flex gap-3 ${!notif.is_read ? 'bg-blue-50/50' : ''}`}
                          >
                            <div className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${notif.is_read ? 'bg-transparent' : 'bg-blue-600'}`}></div>
                            <div className="flex-1 min-w-0">
                              <p className={`text-sm mb-1 ${!notif.is_read ? 'font-semibold text-slate-900' : 'font-medium text-slate-700'}`}>
                                {notif.title}
                              </p>
                              <p className="text-sm text-slate-500 line-clamp-2">{notif.message}</p>
                              <p className="text-xs text-slate-400 mt-2">
                                {formatDistanceToNow(new Date(notif.created_at), { addSuffix: true, locale: vi })}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            <div className="w-px h-8 bg-slate-200 hidden sm:block"></div>

            {/* Profile Dropdown (Static for now) */}
            <div className="flex items-center gap-3 cursor-pointer">
              <div className="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold shadow-sm">
                {(user?.full_name || '').split(' ').pop().charAt(0).toUpperCase() || 'A'}
              </div>
              <div className="hidden sm:flex flex-col">
                <span className="text-sm font-bold text-slate-700 leading-tight">{user?.full_name || 'Quản trị viên'}</span>
                <span className="text-xs text-slate-500 font-medium">Admin</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto bg-[#F8FAFC] p-4 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
