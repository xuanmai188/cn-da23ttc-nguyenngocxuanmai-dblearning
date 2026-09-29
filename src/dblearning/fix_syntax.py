filepath = 'D:/DemoCN2026/dblearning/frontend/src/pages/LearningItem.jsx'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('src={http://localhost:8000 + item.content_url}', 'src={"http://localhost:8000" + item.content_url}')
# Let's also fix the Link tag which had the same backtick issue:
content = content.replace('to={/topics/ + item.topic_id}', 'to={"/topics/" + item.topic_id}')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
