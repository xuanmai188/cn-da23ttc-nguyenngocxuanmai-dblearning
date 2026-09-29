# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

def create_mock_data():
    with engine.connect() as conn:
        # Create 2 test users
        conn.execute(text("""
            INSERT IGNORE INTO users (id, email, password_hash, full_name, role) 
            VALUES 
            (101, 'sql_lover@student.edu.vn', 'hash', 'SQL Lover', 'student'),
            (102, 'theory_fan@student.edu.vn', 'hash', 'Theory Fan', 'student')
        """))
        
        # Clear old mock data
        conn.execute(text("DELETE FROM learning_sessions WHERE user_id IN (101, 102)"))
        conn.execute(text("DELETE FROM quiz_results WHERE user_id IN (101, 102)"))
        
        # User 101: Loves SQL (Item IDs 10,11,12,13,14,15 are SQL related usually)
        # Let's get actual item IDs for SQL
        items = conn.execute(text("SELECT id, title FROM learning_items")).fetchall()
        
        sql_items = [i[0] for i in items if 'SQL' in i[1]]
        theory_items = [i[0] for i in items if 'Mô hình' in i[1] or 'Tổng quan' in i[1] or 'Chuẩn hóa' in i[1]]
        
        now = datetime.utcnow()
        
        # SQL Lover finishes SQL items
        for item_id in sql_items:
            duration = random.randint(300, 1200)
            conn.execute(text("""
                INSERT INTO learning_sessions (user_id, item_id, started_at, ended_at, duration_seconds, completion_rate, status)
                VALUES (:uid, :iid, :start, :end, :dur, 1.0, 'completed')
            """), {
                'uid': 101, 'iid': item_id, 
                'start': now - timedelta(days=2), 'end': now - timedelta(days=2) + timedelta(seconds=duration),
                'dur': duration
            })
            
            # High quiz scores for SQL Lover
            quiz = conn.execute(text("SELECT id, total_questions FROM quizzes WHERE item_id = :iid"), {'iid': item_id}).first()
            if quiz:
                conn.execute(text("""
                    INSERT INTO quiz_results (user_id, quiz_id, score, total_questions, correct_answers, time_spent_seconds, is_passed)
                    VALUES (:uid, :qid, 90.0, :tq, :ca, :time, 1)
                """), {
                    'uid': 101, 'qid': quiz[0], 'tq': quiz[1], 'ca': int(quiz[1]*0.9), 'time': 300
                })
        
        # Theory Fan finishes Theory items
        for item_id in theory_items:
            duration = random.randint(600, 1500)
            conn.execute(text("""
                INSERT INTO learning_sessions (user_id, item_id, started_at, ended_at, duration_seconds, completion_rate, status)
                VALUES (:uid, :iid, :start, :end, :dur, 1.0, 'completed')
            """), {
                'uid': 102, 'iid': item_id, 
                'start': now - timedelta(days=1), 'end': now - timedelta(days=1) + timedelta(seconds=duration),
                'dur': duration
            })
            
            # High quiz scores for Theory Fan
            quiz = conn.execute(text("SELECT id, total_questions FROM quizzes WHERE item_id = :iid"), {'iid': item_id}).first()
            if quiz:
                conn.execute(text("""
                    INSERT INTO quiz_results (user_id, quiz_id, score, total_questions, correct_answers, time_spent_seconds, is_passed)
                    VALUES (:uid, :qid, 95.0, :tq, :ca, :time, 1)
                """), {
                    'uid': 102, 'qid': quiz[0], 'tq': quiz[1], 'ca': int(quiz[1]*0.95), 'time': 400
                })

        conn.commit()
        print("Mock data generated successfully!")

if __name__ == "__main__":
    create_mock_data()
