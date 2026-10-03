file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# 1. Add useSearchParams
content = content.replace(
    "import { useState, useEffect } from 'react';",
    "import { useState, useEffect } from 'react';\nimport { useSearchParams } from 'react-router-dom';"
)

# 2. Extract the current return(...) which renders Topics, into a sub-component or just conditional logic.
# Actually, it's easier to just conditionally render the main body.
# Let's find `return (`
return_split = content.split("  return (")
before_return = return_split[0]
after_return = return_split[1]

# Inject tab logic
new_before = before_return + """  const [searchParams] = useSearchParams();
  const currentTab = searchParams.get('tab') || 'topics';
  
  if (currentTab !== 'topics') {
    return (
      <div className="pb-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              {currentTab === 'items' && 'Quản lý Bài học'}
              {currentTab === 'quiz' && 'Quản lý Quiz'}
              {currentTab === 'flashcards' && 'Quản lý Flashcard'}
              {currentTab === 'documents' && 'Quản lý Tài liệu'}
            </h1>
            <p className="text-slate-500 mt-1">Tính năng đang trong quá trình xây dựng và hoàn thiện.</p>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12 text-center">
          <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <h3 className="text-lg font-bold text-slate-900 mb-2">Đang phát triển module này</h3>
          <p className="text-slate-500 max-w-md mx-auto">
            Hệ thống dữ liệu cho {currentTab} đang được thiết kế. Vui lòng quay lại sau!
          </p>
        </div>
      </div>
    );
  }

"""

new_content = new_before + "  return (" + after_return

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Updated ContentManagement.jsx with tab routing.")
