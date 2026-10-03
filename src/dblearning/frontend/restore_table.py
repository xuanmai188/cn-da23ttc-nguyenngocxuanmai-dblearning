file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/Reports.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the "hidden message" block for recommendations
start_msg = "{activeTab === 'recommendations' && (\n              <div className=\"bg-slate-50 rounded-xl border border-slate-200 p-8 text-center mt-4\">"
end_msg = "</div>\n            )}"

if start_msg in content:
    idx_start = content.find(start_msg)
    idx_end = content.find(end_msg, idx_start) + len(end_msg)
    content = content[:idx_start] + content[idx_end:]

# 2. Remove the condition that hides the table for recommendations
content = content.replace("{activeTab !== 'recommendations' && (\n              <>\n                <div className=\"bg-white rounded-xl", "<>\n                <div className=\"bg-white rounded-xl")
content = content.replace("</div>\n                  </div>\n                )}\n              </>\n            )}", "</div>\n                  </div>\n                )}\n              </>")

# Wait, the ending tags might be different. Let's do a more robust string replacement for the table hiding condition.
content = content.replace("{activeTab !== 'recommendations' && (\n              <>\n", "<>\n")
content = content.replace("                )}\n              </>\n            )}\n          </div>\n        )}\n      </div>", "                )}\n              </>\n          </div>\n        )}\n      </div>")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Restored the paginated table for recommendations")
