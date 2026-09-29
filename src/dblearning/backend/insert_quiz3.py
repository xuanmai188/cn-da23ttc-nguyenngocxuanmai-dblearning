from sqlalchemy import create_engine, text
import os
import json

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@localhost:3306/dblearning?charset=utf8mb4"

engine = create_engine(db_url)

questions = [
    {
        "quiz_id": 3,
        "topic_id": 3,
        "content": "Khái niệm cốt lõi nhất để lưu trữ dữ liệu trong Mô hình quan hệ là gì?",
        "options": json.dumps(["Danh sách liên kết", "Bảng (Relation)", "Cây (Tree)", "Đồ thị (Graph)"], ensure_ascii=False),
        "correct_option": 1,
        "explanation": "Mô hình quan hệ (Relational Model) lưu trữ dữ liệu dưới dạng các Bảng 2 chiều (gọi là Relation).",
        "difficulty": "easy"
    },
    {
        "quiz_id": 3,
        "topic_id": 3,
        "content": "Khóa chính (Primary Key) của một bảng có đặc điểm bắt buộc nào sau đây?",
        "options": json.dumps(["Có thể chứa giá trị NULL", "Phải là kiểu số nguyên (Integer)", "Phải duy nhất (Unique) và không được rỗng (NOT NULL)", "Được phép trùng lặp giữa các dòng"], ensure_ascii=False),
        "correct_option": 2,
        "explanation": "Khóa chính dùng để định danh duy nhất mỗi dòng trong bảng, do đó nó bắt buộc phải Unique và NOT NULL.",
        "difficulty": "easy"
    },
    {
        "quiz_id": 3,
        "topic_id": 3,
        "content": "Mục đích chính của Khóa ngoại (Foreign Key) là gì?",
        "options": json.dumps(["Tăng tốc độ tìm kiếm dữ liệu", "Mã hóa dữ liệu bảo mật", "Tạo mối liên kết giữa các bảng và đảm bảo tính toàn vẹn tham chiếu", "Tự động tăng giá trị khi thêm dòng mới"], ensure_ascii=False),
        "correct_option": 2,
        "explanation": "Khóa ngoại tham chiếu đến Khóa chính của bảng khác, giúp liên kết dữ liệu giữa các bảng và giữ cho dữ liệu toàn vẹn.",
        "difficulty": "medium"
    },
    {
        "quiz_id": 3,
        "topic_id": 3,
        "content": "Trong lý thuyết mô hình quan hệ, một Thuộc tính (Attribute) tương đương với khái niệm nào trong thực tế?",
        "options": json.dumps(["Cột (Column)", "Hàng (Row)", "Bảng (Table)", "Cơ sở dữ liệu (Database)"], ensure_ascii=False),
        "correct_option": 0,
        "explanation": "Thuộc tính (Attribute) chính là các Cột (Column) trong bảng, mô tả đặc điểm của thực thể.",
        "difficulty": "easy"
    },
    {
        "quiz_id": 3,
        "topic_id": 3,
        "content": "Một Bộ (Tuple) trong mô hình quan hệ tương đương với khái niệm nào?",
        "options": json.dumps(["Một cột dữ liệu", "Một hàng dữ liệu (Row / Record)", "Tên của một bảng", "Một ràng buộc toàn vẹn"], ensure_ascii=False),
        "correct_option": 1,
        "explanation": "Bộ (Tuple) đại diện cho một bản ghi cụ thể, tương đương với một Hàng (Row) trong bảng.",
        "difficulty": "easy"
    }
]

with engine.connect() as conn:
    for q in questions:
        conn.execute(
            text("""INSERT INTO questions (quiz_id, topic_id, content, options, correct_option, explanation, difficulty)
                    VALUES (:quiz_id, :topic_id, :content, :options, :correct_option, :explanation, :difficulty)"""),
            q
        )
    
    # Update the total_questions for this quiz
    conn.execute(text("UPDATE quizzes SET total_questions = 5 WHERE id = 3"))
    conn.commit()

print("Inserted 5 questions for Quiz 3 successfully!")
