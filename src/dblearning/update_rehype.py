filepath = 'D:/DemoCN2026/dblearning/frontend/src/pages/LearningItem.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("import ReactMarkdown from 'react-markdown';", "import ReactMarkdown from 'react-markdown';\nimport rehypeRaw from 'rehype-raw';")
content = content.replace("<ReactMarkdown>{item.content_body}</ReactMarkdown>", "<ReactMarkdown rehypePlugins={[rehypeRaw]}>{item.content_body}</ReactMarkdown>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
