file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/Reports.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Make the filter block more compact
old_filter_classes = "bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-6 flex flex-wrap items-end gap-4"
new_filter_classes = "bg-white rounded-lg shadow-sm border border-slate-200 p-3 mb-5 flex flex-wrap items-center gap-3 text-sm"
content = content.replace(old_filter_classes, new_filter_classes)

# make inputs smaller
content = content.replace("block text-xs font-medium text-slate-500 mb-1", "hidden") # hide labels to save space or make them inline
content = content.replace('className="px-3 py-1.5 border border-slate-300 rounded-lg text-sm outline-none focus:ring-1 focus:ring-blue-500"', 'className="px-2 py-1.5 border border-slate-300 rounded-md outline-none focus:ring-1 focus:ring-blue-500"')
content = content.replace('className="px-3 py-1.5 border border-slate-300 rounded-lg text-sm outline-none"', 'className="px-2 py-1.5 border border-slate-300 rounded-md outline-none"')

# replace labels with placeholders where applicable (selects have options, dates can't have placeholders, so we'll prepend a short label in a span)
content = content.replace('<label className="hidden">Từ ngày</label>', '<span className="text-slate-500 font-medium">Từ:</span>')
content = content.replace('<label className="hidden">Đến ngày</label>', '<span className="text-slate-500 font-medium">Đến:</span>')
content = content.replace('<label className="hidden">Chủ đề</label>', '<span className="text-slate-500 font-medium">Chủ đề:</span>')
content = content.replace('<label className="hidden">Loại nội dung</label>', '<span className="text-slate-500 font-medium">Loại:</span>')

# Add flex wrapper for label + input
content = content.replace('<div>\n          <span className="text-slate-500 font-medium">Từ:</span>\n          <input', '<div className="flex items-center gap-2">\n          <span className="text-slate-500 font-medium">Từ:</span>\n          <input')
content = content.replace('<div>\n          <span className="text-slate-500 font-medium">Đến:</span>\n          <input', '<div className="flex items-center gap-2">\n          <span className="text-slate-500 font-medium">Đến:</span>\n          <input')
content = content.replace('<div>\n              <span className="text-slate-500 font-medium">Chủ đề:</span>\n              <select', '<div className="flex items-center gap-2">\n              <span className="text-slate-500 font-medium">Chủ đề:</span>\n              <select')
content = content.replace('<div>\n                <span className="text-slate-500 font-medium">Loại:</span>\n                <select', '<div className="flex items-center gap-2">\n                <span className="text-slate-500 font-medium">Loại:</span>\n                <select')

# 2. Hide the table for recommendations
# Find the table block. We only show the table if activeTab !== 'recommendations'
table_start_idx = content.find('<div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">')
if table_start_idx != -1:
    content = content[:table_start_idx] + "{activeTab !== 'recommendations' && (\n            " + content[table_start_idx:]

    table_end_idx = content.find('</div>\n            </div>\n            \n            {data.details.length > ITEMS_PER_PAGE', table_start_idx)
    if table_end_idx != -1:
        # we need to close the JSX condition after the pagination div
        pagination_end_idx = content.find('</div>\n              </div>\n            )}', table_end_idx)
        if pagination_end_idx != -1:
            insert_idx = pagination_end_idx + len('</div>\n              </div>\n            )}')
            content = content[:insert_idx] + "\n          )}" + content[insert_idx:]

# 3. Add a small note for the recommendations tab instead of the table
if "{activeTab !== 'recommendations' && (" in content:
    note_jsx = """
            {activeTab === 'recommendations' && (
              <div className="bg-slate-50 rounded-lg border border-slate-200 p-6 text-center">
                <SparklesIcon className="w-8 h-8 text-purple-400 mx-auto mb-2" />
                <h3 className="text-slate-700 font-medium mb-1">Dữ liệu chi tiết đã được ẩn để tối ưu hiển thị</h3>
                <p className="text-sm text-slate-500 max-w-md mx-auto">
                  Các chỉ số tổng quan ở trên là dữ liệu quan trọng nhất để đánh giá hiệu quả của thuật toán Gợi ý (AI). Nếu bạn cần xem chi tiết danh sách từng lượt gợi ý cho sinh viên, vui lòng nhấn nút <b>Xuất Excel</b> ở góc phải.
                </p>
              </div>
            )}
"""
    # Insert this note right before the table
    content = content.replace("{activeTab !== 'recommendations' && (\n            <div className=\"bg-white", note_jsx + "\n            {activeTab !== 'recommendations' && (\n            <div className=\"bg-white")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Reports.jsx UI")
