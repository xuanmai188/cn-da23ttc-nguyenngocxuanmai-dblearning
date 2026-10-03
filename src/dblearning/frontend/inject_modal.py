file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/AdminDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add states for Modal
state_idx = content.find("const [loading, setLoading] = useState(true);")
if state_idx != -1:
    modal_state = "const [isActivityModalOpen, setIsActivityModalOpen] = useState(false);\n  const [fullActivities, setFullActivities] = useState([]);\n  const [loadingActivities, setLoadingActivities] = useState(false);\n  "
    content = content[:state_idx] + modal_state + content[state_idx:]

# Add handler function
handler_fn = """
  const handleViewAllActivities = async () => {
    setIsActivityModalOpen(true);
    setLoadingActivities(true);
    try {
      const data = await adminApi.getRecentActivities(50); // Fetch up to 50
      setFullActivities(data);
    } catch (err) {
      console.error('Failed to fetch full activities', err);
    } finally {
      setLoadingActivities(false);
    }
  };
"""
# insert before return (
ret_idx = content.rfind("  return (")
if ret_idx != -1:
    content = content[:ret_idx] + handler_fn + content[ret_idx:]

# Replace the onClick handler for the button
old_button = "onClick={() => navigate(\"/admin/reports\")} className=\"text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer\">Xem tt c &rarr;</button>"
# since encoding can be weird, we use regex or string replace with wildcard
import re
content = re.sub(r'onClick=\{\(\) => navigate\([^)]+\)\}\s*className="text-sm font-medium text-blue-600[^>]+>Xem t[^<]+&rarr;</button>', 
                 r'onClick={handleViewAllActivities} className="text-sm font-medium text-blue-600 hover:text-blue-700 cursor-pointer">Xem tất cả &rarr;</button>', 
                 content)

# Add Modal JSX before the final closing div
modal_jsx = """
      {/* Activity Log Modal */}
      {isActivityModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-3xl max-h-[85vh] overflow-hidden flex flex-col">
            <div className="flex items-center justify-between p-6 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                  <ClockIcon className="w-6 h-6" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-slate-800">Nhật ký hoạt động</h2>
                  <p className="text-sm text-slate-500">Danh sách 50 hoạt động gần đây nhất của sinh viên</p>
                </div>
              </div>
              <button 
                onClick={() => setIsActivityModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              {loadingActivities ? (
                <div className="text-center py-12 text-slate-500">Đang tải dữ liệu...</div>
              ) : fullActivities.length === 0 ? (
                <div className="text-center py-12 text-slate-500">Chưa có hoạt động nào.</div>
              ) : (
                <div className="space-y-4">
                  {fullActivities.map((act) => (
                    <div key={act.id} className="flex items-start gap-4 p-3 hover:bg-slate-50 rounded-xl transition-colors">
                      <div className={`p-2 rounded-lg mt-1 ${
                        act.type === 'quiz' ? 'bg-rose-100 text-rose-600' : 
                        act.type === 'flashcard_set' ? 'bg-amber-100 text-amber-600' :
                        'bg-blue-100 text-blue-600'
                      }`}>
                        {act.type === 'quiz' ? <CheckBadgeIcon className="w-5 h-5" /> : 
                         act.type === 'flashcard_set' ? <DocumentTextIcon className="w-5 h-5" /> :
                         <PlayIcon className="w-5 h-5" />}
                      </div>
                      <div className="flex-1">
                        <p className="text-slate-700">
                          <span className="font-semibold text-slate-900">{act.user_name}</span> {act.action} <span className="font-medium">{act.item_title}</span>
                        </p>
                        <p className="text-sm text-slate-500 mt-1">{act.time_ago}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
"""
content = content.replace("    </div>\n  );\n}", modal_jsx + "    </div>\n  );\n}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Injected Activity Modal into AdminDashboard")
