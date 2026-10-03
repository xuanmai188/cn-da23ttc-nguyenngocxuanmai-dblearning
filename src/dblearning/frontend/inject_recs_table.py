file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/Reports.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add headers
new_headers = """                          {activeTab === 'recommendations' && (
                            <>
                              <th className="px-6 py-4">Sinh viên</th>
                              <th className="px-6 py-4">Nội dung đề xuất</th>
                              <th className="px-6 py-4">Loại</th>
                              <th className="px-6 py-4 text-center">Độ phù hợp</th>
                              <th className="px-6 py-4 text-center">Trạng thái</th>
                            </>
                          )}
"""
surveys_header = "{activeTab === 'surveys' && ("
if "activeTab === 'recommendations'" not in content.split("<thead>")[1].split("</thead>")[0]:
    content = content.replace(surveys_header, new_headers + surveys_header)

# 2. Add rows
new_rows = """                              {activeTab === 'recommendations' && (
                                <>
                                  <td className="px-6 py-4 font-bold text-slate-900">{row.user_name}</td>
                                  <td className="px-6 py-4 font-medium text-slate-800">{row.item_title}</td>
                                  <td className="px-6 py-4 text-sm text-slate-500 uppercase">{row.item_type}</td>
                                  <td className="px-6 py-4 text-center text-blue-600 font-bold">{row.score}</td>
                                  <td className="px-6 py-4 text-center">
                                    {row.is_clicked ? (
                                      <span className="px-2 py-1 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded-full">Đã Click</span>
                                    ) : (
                                      <span className="px-2 py-1 bg-slate-100 text-slate-500 text-xs font-semibold rounded-full">Bỏ qua</span>
                                    )}
                                  </td>
                                </>
                              )}
"""
surveys_row = "{activeTab === 'surveys' && ("
# Find the second occurrence of surveys_row which is inside tbody
parts = content.split(surveys_row)
if len(parts) >= 3:
    # the second occurrence is index 2 in parts if we split
    # wait, it's safer to just replace inside tbody
    tbody_start = content.find("<tbody")
    if tbody_start != -1:
        surveys_idx = content.find(surveys_row, tbody_start)
        if surveys_idx != -1 and "activeTab === 'recommendations'" not in content[tbody_start:surveys_idx]:
            content = content[:surveys_idx] + new_rows + content[surveys_idx:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Injected recommendations table columns")
