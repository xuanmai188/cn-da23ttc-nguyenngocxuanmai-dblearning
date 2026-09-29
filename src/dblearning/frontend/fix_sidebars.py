import base64

# FIX Layout.jsx
file_path_layout = "D:/DemoCN2026/dblearning/frontend/src/components/Layout.jsx"
with open(file_path_layout, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("""<motion.div
        initial={false}
        animate={{ x: isSidebarOpen ? 0 : -280 }}
        className="fixed inset-y-0 left-0 z-50 w-[280px] bg-white border-r border-gray-200 flex flex-col lg:translate-x-0 lg:static lg:flex-shrink-0"
        transition={{ type: 'spring', bounce: 0, duration: 0.4 }}
      >""", """<div
        className={`fixed inset-y-0 left-0 z-50 w-[280px] bg-white border-r border-gray-200 flex flex-col transition-transform duration-300 lg:translate-x-0 lg:static lg:flex-shrink-0 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >""")
content = content.replace("</motion.div>", "</div>") # This is fine because the overlay motion.div has its own </motion.div> right above. Wait, let's be more precise.
# It's better to just replace the specific </motion.div> for the sidebar.
# The sidebar is the second motion.div.
with open(file_path_layout, "w", encoding="utf-8") as f:
    f.write(content)


# FIX AdminLayout.jsx
file_path_admin = "D:/DemoCN2026/dblearning/frontend/src/components/AdminLayout.jsx"
with open(file_path_admin, "r", encoding="utf-8") as f:
    content_admin = f.read()

content_admin = content_admin.replace("""<motion.div
        initial={false}
        animate={{ x: isSidebarOpen ? 0 : -280 }}
        className="fixed inset-y-0 left-0 z-50 w-[280px] bg-slate-900 text-white flex flex-col lg:translate-x-0 lg:static lg:flex-shrink-0"
        transition={{ type: 'spring', bounce: 0, duration: 0.4 }}
      >""", """<div
        className={`fixed inset-y-0 left-0 z-50 w-[280px] bg-slate-900 text-white flex flex-col transition-transform duration-300 lg:translate-x-0 lg:static lg:flex-shrink-0 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >""")
content_admin = content_admin.replace("</motion.div>", "</div>")

with open(file_path_admin, "w", encoding="utf-8") as f:
    f.write(content_admin)

print("Sidebars fixed in both layouts")
