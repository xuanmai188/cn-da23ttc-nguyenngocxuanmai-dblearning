file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/admin/ContentManagement.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

import re

# Add import for LessonManagement
if "LessonManagement" not in content:
    content = content.replace("import { PlusIcon", "import LessonManagement from '../../components/admin/content/LessonManagement';\nimport { PlusIcon")

target = """    return (
      <div className="pb-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              {currentTab === 'items' && 'Quản lý Bài học'}"""

new_block = """  if (currentTab === 'items') {
    return <LessonManagement />;
  }

  if (currentTab !== 'topics') {
    return (
      <div className="pb-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              {currentTab === 'items' && 'Quản lý Bài học'}"""

content = content.replace("""  if (currentTab !== 'topics') {
    return (
      <div className="pb-10">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">
              {currentTab === 'items' && 'Quản lý Bài học'}""", new_block)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated ContentManagement to route to LessonManagement.")
