file_path = "D:/DemoCN2026/dblearning/frontend/src/pages/LearningPath.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_text = "Dựa vào lịch sử học tập và kết quả bài kiểm tra, AI của chúng tôi đã xây dựng lộ trình tiếp theo dành riêng cho bạn."
new_text = "{profile?.total_items_completed === 0 ? 'Dựa vào kết quả khảo sát đầu vào, AI của chúng tôi đã xây dựng lộ trình khởi đầu dành riêng cho bạn.' : 'Dựa vào lịch sử học tập và kết quả bài kiểm tra, AI của chúng tôi đã cập nhật lộ trình tiếp theo dành riêng cho bạn.'}"

content = content.replace(old_text, new_text)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("LearningPath.jsx description updated")
