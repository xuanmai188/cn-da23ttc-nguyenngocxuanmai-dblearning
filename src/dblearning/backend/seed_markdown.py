import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)

with engine.connect() as conn:
    result = conn.execute(text('SELECT id, title, description FROM learning_items WHERE content_type="document"'))
    items = result.fetchall()
    
    for item in items:
        item_id = item[0]
        title = item[1]
        desc = item[2]
        
        md_content = f'''## {title}

**Mục tiêu bài học:** {desc}

Chào mừng bạn đến với bài học **{title}**. Trong bài này, chúng ta sẽ tìm hiểu các khái niệm cơ bản và quan trọng nhất.

### 1. Tổng quan

Khái niệm cốt lõi của phần này đóng vai trò quan trọng trong việc thiết kế và quản trị cơ sở dữ liệu hiệu quả. Việc nắm vững kiến thức này sẽ giúp bạn:
- Tối ưu hóa hiệu suất hệ thống.
- Đảm bảo tính toàn vẹn và an toàn dữ liệu.
- Dễ dàng mở rộng ứng dụng trong tương lai.

### 2. Nội dung chi tiết

(Nội dung chi tiết của bài học sẽ được cập nhật và biên soạn thêm bởi giảng viên. Tạm thời bạn có thể tham khảo tài liệu PDF gốc ở phần Nguồn tham khảo bên dưới).

> **Lưu ý:** Hãy nhớ làm bài kiểm tra trắc nghiệm (Quiz) hoặc ôn tập qua thẻ nhớ (Flashcard) sau khi hoàn thành bài học này nhé!

### 3. Tóm tắt

- Nắm vững định nghĩa và ý nghĩa của **{title}**.
- Hiểu cách áp dụng vào thực tế.
'''
        conn.execute(
            text('UPDATE learning_items SET content_body = :body WHERE id = :id'),
            {'body': md_content, 'id': item_id}
        )
    
    conn.commit()
    print(f'Updated {len(items)} items with markdown content')
