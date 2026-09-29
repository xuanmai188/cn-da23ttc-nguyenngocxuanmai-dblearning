import os

# Fix Flashcard.jsx
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Flashcard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("flashcards[currentIndex].front_content", "flashcards[currentIndex].question")
content = content.replace("flashcards[currentIndex].back_content", "flashcards[currentIndex].answer")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

# Fix Quiz.jsx
file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/Quiz.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("const [questions, setQuestions] = useState([]);", "const [quizInfo, setQuizInfo] = useState(null);\n  const [questions, setQuestions] = useState([]);")

old_fetch = """        const data = await quizApi.getQuiz(itemId);
        setQuestions(data);"""
new_fetch = """        const data = await quizApi.getQuiz(itemId);
        setQuizInfo(data);
        setQuestions(data.questions || []);"""
content = content.replace(old_fetch, new_fetch)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Flashcard.jsx and Quiz.jsx variables fixed")
