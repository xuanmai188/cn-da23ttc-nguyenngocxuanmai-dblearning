import os

files = [
    'D:/DemoCN2026/dblearning/frontend/src/pages/Dashboard.jsx',
    'D:/DemoCN2026/dblearning/frontend/src/pages/LearningPath.jsx',
    'D:/DemoCN2026/dblearning/frontend/src/pages/TopicDetail.jsx'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace simple `/learning/ID` with dynamic logic
    if 'to={`/learning/` + rec.item?.id}' in content:
        new_link = 'to={rec.item?.content_type === "quiz" ? `/quiz/${rec.item?.id}` : rec.item?.content_type === "flashcard_set" ? `/flashcard/${rec.item?.id}` : `/learning/${rec.item?.id}`}'
        content = content.replace('to={`/learning/` + rec.item?.id}', new_link)

    if 'to={`/learning/${rec.item?.id}`}' in content:
        new_link = 'to={rec.item?.content_type === "quiz" ? `/quiz/${rec.item?.id}` : rec.item?.content_type === "flashcard_set" ? `/flashcard/${rec.item?.id}` : `/learning/${rec.item?.id}`}'
        content = content.replace('to={`/learning/${rec.item?.id}`}', new_link)

    if 'to={`/learning/` + item.id}' in content:
        new_link = 'to={item.content_type === "quiz" ? `/quiz/${item.id}` : item.content_type === "flashcard_set" ? `/flashcard/${item.id}` : `/learning/${item.id}`}'
        content = content.replace('to={`/learning/` + item.id}', new_link)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Updated links in Dashboard, LearningPath, TopicDetail")
