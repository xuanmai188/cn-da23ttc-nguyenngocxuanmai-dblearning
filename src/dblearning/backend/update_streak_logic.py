file_path = "D:/DemoCN2026/dblearning/backend/app/ml/profile_builder.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Logic to calculate learning streak:
# 1. get all distinct dates user studied (from sessions)
# 2. sort descending
# 3. compute consecutive days
streak_logic = """
    # 6.5. TA-nh toAn Chu-i h?c t-p (Learning Streak)
    from datetime import date, timedelta
    
    # Ly ngAy h?c duy nht
    study_dates = set()
    for session in sessions:
        if session.started_at:
            study_dates.add(session.started_at.date())
            
    # S_p xp ngAy gim d n
    sorted_dates = sorted(list(study_dates), reverse=True)
    
    current_streak = 0
    today = date.today()
    
    if sorted_dates:
        # Check nu ngAy cu`i cA1ng h?c lA hA'm nay hoc hA'm qua
        if sorted_dates[0] == today or sorted_dates[0] == today - timedelta(days=1):
            current_streak = 1
            curr_date = sorted_dates[0]
            for i in range(1, len(sorted_dates)):
                if sorted_dates[i] == curr_date - timedelta(days=1):
                    current_streak += 1
                    curr_date = sorted_dates[i]
                else:
                    break
        else:
            current_streak = 0
    else:
        current_streak = 0
        
    # ?m bo current_streak >= 1 nu m>i b_t ` u hA'm nay, hoc lA cA3 sessions nhng b< reset thA s lA 0, tuA business logic
    # z `Ay, ta cA3 th ` mc `<nh current_streak lA t'i thiu 1 nu profile cA3 session (` ging UI hA'm tr>c)
    if current_streak == 0 and len(sessions) > 0:
        current_streak = 1
"""

content = content.replace(
    "# 7. C-p nh-t DB",
    streak_logic + "\n    # 7. C-p nh-t DB"
)

content = content.replace(
    "profile.avg_quiz_score = avg_score",
    "profile.avg_quiz_score = avg_score\n    profile.learning_streak = current_streak"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("profile_builder.py updated")
