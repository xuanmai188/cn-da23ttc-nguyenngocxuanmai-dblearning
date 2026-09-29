import os

file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/TopicDetail.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "completedItems" not in content:
    # 1. Import CheckCircleIcon
    content = content.replace("import { PlayCircleIcon } from '@heroicons/react/24/solid';", "import { PlayCircleIcon, CheckCircleIcon } from '@heroicons/react/24/solid';")
    
    # 2. Add state
    content = content.replace("const [topic, setTopic] = useState(null);", "const [topic, setTopic] = useState(null);\n  const [completedItems, setCompletedItems] = useState([]);")
    
    # 3. Add to fetchData
    old_fetch = """        const data = await learningApi.getTopicDetail(id);
        setTopic(data);"""
    new_fetch = """        const data = await learningApi.getTopicDetail(id);
        setTopic(data);
        try {
            const completed = await learningApi.getCompletedItems();
            setCompletedItems(completed || []);
        } catch (e) {}"""
    content = content.replace(old_fetch, new_fetch)
    
    # 4. Render check icon
    # Finding the item title
    old_title = "<h3 className=\"font-bold text-gray-900\">{item.title}</h3>"
    new_title = """<h3 className="font-bold text-gray-900 flex items-center">
                    {item.title}
                    {completedItems.includes(item.id) && <CheckCircleIcon className="h-5 w-5 text-green-500 ml-2" title="Đã hoàn thành" />}
                  </h3>"""
    content = content.replace(old_title, new_title)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("TopicDetail.jsx updated")
