import os

pages = {
    "RecommendationManagement.jsx": "Quản lý gợi ý AI",
    "OnboardingStats.jsx": "Khảo sát đầu vào",
    "Statistics.jsx": "Thống kê hệ thống",
    "Reports.jsx": "Báo cáo",
    "AdminSettings.jsx": "Cài đặt hệ thống"
}

for filename, title in pages.items():
    file_path = f"D:/DemoCN2026/dblearning/frontend/src/pages/admin/{filename}"
    content = f"""export default function {filename.split('.')[0]}() {{
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
        <p className="text-slate-500 mt-1">Tính năng đang được phát triển trong Phase tiếp theo.</p>
      </div>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center text-slate-500">
        Comming Soon...
      </div>
    </div>
  );
}}
"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Created dummy components")
