file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/ForgotPassword.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove the demo badge section
old = """
                  {/* Demo badge */}
                  <div className="bg-amber-50 border-t border-amber-200 px-4 py-2 flex items-center gap-2">
                    <span className="text-xs text-amber-700">
                      🔧 <strong>Chế độ Demo:</strong> Email mô phỏng hiển thị trực tiếp thay vì gửi vào hộp thư
                    </span>
                  </div>"""

content = content.replace(old, "")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Demo badge removed")
