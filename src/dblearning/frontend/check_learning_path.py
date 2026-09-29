import os

file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/LearningPath.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

if "completedItems" not in content:
    # 1. Import CheckCircleIcon
    content = content.replace("import { BookOpenIcon, CheckCircleIcon as SolidCheckCircle } from '@heroicons/react/24/solid';", "import { BookOpenIcon, CheckCircleIcon as SolidCheckCircle, CheckCircleIcon } from '@heroicons/react/24/solid';")
    
    # 2. Add state
    content = content.replace("const [topics, setTopics] = useState([]);", "const [topics, setTopics] = useState([]);\n  const [completedItems, setCompletedItems] = useState([]);")
    
    # 3. Add to fetchData
    old_fetch = """        const data = await learningApi.getTopics();
        setTopics(data);"""
    new_fetch = """        const data = await learningApi.getTopics();
        setTopics(data);
        try {
            const completed = await learningApi.getCompletedItems();
            setCompletedItems(completed || []);
        } catch (e) {}"""
    content = content.replace(old_fetch, new_fetch)
    
    # Wait, in LearningPath.jsx, does it show items? No! LearningPath only shows topics!
    # Topic level: LearningPath.jsx doesn't render items directly, it just renders topics with progress!
    # Wait, let me check what LearningPath.jsx renders.
