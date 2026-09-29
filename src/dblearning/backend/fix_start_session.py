file_path = "D:/DemoCN2026/dblearning/backend/app/api/endpoints/learning.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''    # Kiểm tra xem có session in_progress không, nếu có thì trả về, không thì tạo mới
    existing_session = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.item_id == session_in.item_id,
        LearningSession.status == "in_progress"
    ).first()

    if existing_session:
        return existing_session

    session = LearningSession(
        user_id=current_user.id,
        item_id=session_in.item_id,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session'''

new_block = '''    # Nếu đã có session in_progress thì trả lại ngay (tránh tạo nhiều session)
    existing_inprogress = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.item_id == session_in.item_id,
        LearningSession.status == "in_progress"
    ).first()

    if existing_inprogress:
        return existing_inprogress

    # Nếu đã có session completed, trả về session đó (không tạo mới)
    existing_completed = db.query(LearningSession).filter(
        LearningSession.user_id == current_user.id,
        LearningSession.item_id == session_in.item_id,
        LearningSession.status == "completed"
    ).order_by(LearningSession.id.desc()).first()

    if existing_completed:
        return existing_completed

    session = LearningSession(
        user_id=current_user.id,
        item_id=session_in.item_id,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Backend startSession fixed!")
else:
    print("Block not found - checking...")
    # Try to find the approximate block
    idx = content.find("existing_session")
    print(content[max(0,idx-50):idx+300])
