file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/content/QuizManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# 1. Add import
if "QuestionManagementModal" not in content:
    content = content.replace(
        "import { XMarkIcon, PlusIcon, PencilSquareIcon, TrashIcon } from '@heroicons/react/24/outline';", 
        "import { XMarkIcon, PlusIcon, PencilSquareIcon, TrashIcon, ListBulletIcon } from '@heroicons/react/24/outline';\nimport QuestionManagementModal from './QuestionManagementModal';"
    )

# 2. Add state
if "const [managingQuestionsFor," not in content:
    content = content.replace(
        "const [editingQuiz, setEditingQuiz] = useState(null);",
        "const [editingQuiz, setEditingQuiz] = useState(null);\n  const [managingQuestionsFor, setManagingQuestionsFor] = useState(null);"
    )

# 3. Add button to the table
old_td = """                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button onClick={() => handleOpenModal(quiz)} className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
                          <PencilSquareIcon className="w-5 h-5" />
                        </button>"""

new_td = """                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button 
                          onClick={() => setManagingQuestionsFor(quiz)} 
                          className="px-3 py-1.5 flex items-center gap-1.5 text-xs font-medium text-purple-600 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors mr-2"
                        >
                          <ListBulletIcon className="w-4 h-4" />
                          Câu hỏi ({quiz.total_questions || 0})
                        </button>
                        <button onClick={() => handleOpenModal(quiz)} className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
                          <PencilSquareIcon className="w-5 h-5" />
                        </button>"""
content = content.replace(old_td, new_td)

# 4. Add the Modal render
old_render_end = """        </div>
      )}
    </div>
  );
}"""

new_render_end = """        </div>
      )}

      {/* Question Management Modal */}
      {managingQuestionsFor && (
        <QuestionManagementModal 
          quiz={managingQuestionsFor} 
          onClose={() => {
            setManagingQuestionsFor(null);
            fetchData(); // Refresh to update question count
          }} 
        />
      )}
    </div>
  );
}"""
content = content.replace(old_render_end, new_render_end)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated QuizManagement.jsx with QuestionManagementModal")
