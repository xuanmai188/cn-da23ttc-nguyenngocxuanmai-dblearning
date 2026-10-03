import re

file_path = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the notification button with the dropdown UI
notif_ui = """            {/* Notifications */}
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
            </div>"""

content = re.sub(
    r'\{\/\* Notifications \*\/\}.*?<BellIcon className="w-6 h-6" \/>.*?<\/button>',
    notif_ui,
    content,
    flags=re.DOTALL
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated AdminLayout.jsx UI")
