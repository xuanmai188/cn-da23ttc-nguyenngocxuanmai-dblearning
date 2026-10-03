file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Add import
if "import FlashcardManagement" not in content:
    content = content.replace(
        "import QuizManagement from '../../components/admin/content/QuizManagement';",
        "import QuizManagement from '../../components/admin/content/QuizManagement';\nimport FlashcardManagement from '../../components/admin/content/FlashcardManagement';"
    )

# Replace placeholder
old_placeholder = """        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12 text-center">
          <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <BeakerIcon className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 mb-2">Đang phát triển module này</h3>
          <p className="text-slate-500 max-w-sm mx-auto">
            Hệ thống dữ liệu cho {currentTab} đang được thiết kế. Vui lòng quay lại sau!
          </p>
        </div>"""

new_render = """        {currentTab === 'flashcards' ? (
          <FlashcardManagement />
        ) : (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12 text-center">
            <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <BeakerIcon className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-slate-900 mb-2">Đang phát triển module này</h3>
            <p className="text-slate-500 max-w-sm mx-auto">
              Hệ thống dữ liệu cho {currentTab} đang được thiết kế. Vui lòng quay lại sau!
            </p>
          </div>
        )}"""

content = content.replace(old_placeholder, new_render)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated ContentManagement.jsx to render FlashcardManagement")
