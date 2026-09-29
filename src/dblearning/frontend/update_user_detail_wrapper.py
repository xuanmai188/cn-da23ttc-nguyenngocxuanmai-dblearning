file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/users/UserDetailPanel.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the wrapper
new_wrapper = """  if (!user) return null;

  return (
    <div className="w-full bg-white shadow-sm border border-slate-200 rounded-xl flex flex-col h-[calc(100vh-120px)] sticky top-6">
      
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between shrink-0">"""

content = content.replace("""  if (!user) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-slate-900/20 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />
      
      {/* Panel */}
      <div className="absolute inset-y-0 right-0 max-w-md w-full bg-white shadow-2xl flex flex-col transform transition-transform duration-300">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">""", new_wrapper)

# Update some paddings from px-6 to px-5 to fit smaller width
content = content.replace("px-6 py-6", "px-5 py-5")
content = content.replace("px-6 border-b", "px-5 border-b")
content = content.replace("px-6 py-4", "px-5 py-4")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated UserDetailPanel.jsx wrapper")
