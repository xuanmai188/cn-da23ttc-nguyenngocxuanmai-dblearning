file_path = "D:/DemoCN2026/dblearning/frontend/src/components/admin/content/QuizManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Fix imports
old_import = "import { PlusIcon, PencilSquareIcon, TrashIcon, XMarkIcon } from '@heroicons/react/24/outline';"
new_import = "import { PlusIcon, PencilSquareIcon, TrashIcon, XMarkIcon, ListBulletIcon } from '@heroicons/react/24/outline';\nimport QuestionManagementModal from './QuestionManagementModal';"

content = content.replace(old_import, new_import)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed imports in QuizManagement.jsx")
