file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/OnboardingStats.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add activeTab and results states
content = content.replace("const [totalCompleted, setTotalCompleted] = useState(0);", "const [totalCompleted, setTotalCompleted] = useState(0);\n  const [activeTab, setActiveTab] = useState('questions');\n  const [results, setResults] = useState([]);")

# Add fetch for results
content = content.replace("""adminApi.getSurveys(),
        adminApi.getSurveyStats(),
        adminApi.getTopics()""", """adminApi.getSurveys(),
        adminApi.getSurveyStats(),
        adminApi.getTopics(),
        adminApi.getSurveyResults()""")

content = content.replace("const [surveysData, statsData, topicsData] = await Promise.all([", "const [surveysData, statsData, topicsData, resultsData] = await Promise.all([")

content = content.replace("setTopics(topicsData);", "setTopics(topicsData);\n      setResults(resultsData || []);")


# Add the Tab UI
tab_ui = """
      <div className="flex gap-4 border-b border-slate-200 mb-6">
        <button 
          onClick={() => setActiveTab('questions')} 
          className={`pb-3 px-1 font-medium border-b-2 transition-colors ${activeTab === 'questions' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          Quản lý câu hỏi
        </button>
        <button 
          onClick={() => setActiveTab('results')} 
          className={`pb-3 px-1 font-medium border-b-2 transition-colors ${activeTab === 'results' ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          Kết quả khảo sát
        </button>
      </div>
"""
content = content.replace("{/* Danh sách câu hỏi */}", tab_ui + "\n      {/* Nội dung Tabs */}\n      {activeTab === 'questions' ? (\n        <div className=\"bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden\">")

# Close the questions div and add the results div
content = content.replace("{/* Modal Thêm Câu Hỏi */}", """      </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-6">
          {results.length === 0 ? (
            <p className="text-center text-slate-500 py-8">Chưa có sinh viên nào hoàn thành khảo sát.</p>
          ) : (
            results.map((r, i) => (
              <div key={r.id} className="border border-slate-100 rounded-lg p-5 bg-slate-50">
                <div className="flex justify-between items-center mb-4 border-b border-slate-200 pb-3">
                  <div>
                    <h3 className="font-bold text-slate-900">{r.user_name}</h3>
                    <p className="text-sm text-slate-500">{r.email}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-slate-600">{new Date(r.completed_at).toLocaleString('vi-VN')}</p>
                    <p className="text-xs text-emerald-600 font-medium">Hoàn thành</p>
                  </div>
                </div>
                <div className="space-y-3">
                  {r.answers.map((a, j) => (
                    <div key={j} className="bg-white p-3 rounded border border-slate-100">
                      <p className="text-sm font-medium text-slate-800 mb-1">Q: {a.question}</p>
                      <p className="text-sm text-blue-600 font-medium">A: {a.answer}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Modal Thêm Câu Hỏi */}""")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated OnboardingStats.jsx with Results tab")
