file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/Reports.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add currentPage state
content = content.replace("const [topics, setTopics] = useState([]);", "const [topics, setTopics] = useState([]);\n  const [currentPage, setCurrentPage] = useState(1);\n  const ITEMS_PER_PAGE = 10;")

# Reset currentPage when tab or filters change
content = content.replace("fetchData();\n  }, [activeTab, filters.topicId, filters.itemType]);", "setCurrentPage(1);\n    fetchData();\n  }, [activeTab, filters.topicId, filters.itemType]);")

# Slice data for pagination in the render part
content = content.replace("data.details.map((row, idx)", "data.details.slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE).map((row, idx)")

# Add pagination controls below the table
pagination_jsx = """
              </div>
            </div>
            
            {data.details.length > ITEMS_PER_PAGE && (
              <div className="flex items-center justify-between bg-white px-4 py-3 border border-slate-200 rounded-xl shadow-sm">
                <div className="text-sm text-slate-500">
                  Hiển thị <span className="font-medium">{(currentPage - 1) * ITEMS_PER_PAGE + 1}</span> đến <span className="font-medium">{Math.min(currentPage * ITEMS_PER_PAGE, data.details.length)}</span> trong số <span className="font-medium">{data.details.length}</span> kết quả
                </div>
                <div className="flex gap-2">
                  <button 
                    onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                    className="px-3 py-1 border border-slate-300 rounded-md text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Trước
                  </button>
                  <button 
                    onClick={() => setCurrentPage(prev => Math.min(prev + 1, Math.ceil(data.details.length / ITEMS_PER_PAGE)))}
                    disabled={currentPage === Math.ceil(data.details.length / ITEMS_PER_PAGE)}
                    className="px-3 py-1 border border-slate-300 rounded-md text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Sau
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
"""

content = content.replace("</div>\n            </div>\n          </div>\n        )}", pagination_jsx)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Added pagination to Reports.jsx")
