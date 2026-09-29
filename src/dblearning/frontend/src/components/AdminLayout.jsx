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
        { name: 'Tài liệu', href: '/admin/content?tab=documents' },
      ]
    },
    { name: 'Thống kê', href: '/admin/statistics', icon: ChartBarIcon },
    { name: 'Quản lý gợi ý AI', href: '/admin/recommendations', icon: SparklesIcon },
    { name: 'Khảo sát đầu vào', href: '/admin/onboarding', icon: ClipboardDocumentCheckIcon },
    { name: 'Báo cáo', href: '/admin/reports', icon: DocumentChartBarIcon },
    { name: 'Cài đặt hệ thống', href: '/admin/settings', icon: Cog6ToothIcon },
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
            
            {/* Search Bar */}
            <div className="hidden md:flex items-center max-w-md w-full relative">
              <MagnifyingGlassIcon className="w-5 h-5 text-slate-400 absolute left-3" />
              <input 
                type="text" 
                placeholder="Tìm kiếm người dùng, bài học, chủ đề..." 
                className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all placeholder:text-slate-400"
                disabled // TODO: Implement global search API
                title="Tính năng đang được phát triển"
              />
            </div>
          </div>

          <div className="flex items-center gap-4 lg:gap-6">
            {/* Notifications */}
            <button className="relative p-2 text-slate-500 hover:text-slate-700 transition-colors rounded-full hover:bg-slate-100">
              <BellIcon className="w-6 h-6" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full ring-2 ring-white"></span>
            </button>

            <div className="w-px h-8 bg-slate-200 hidden sm:block"></div>

            {/* Profile Dropdown (Static for now) */}
            <div className="flex items-center gap-3 cursor-pointer">
              <div className="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold shadow-sm">
                {user?.full_name?.charAt(0) || 'A'}
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
