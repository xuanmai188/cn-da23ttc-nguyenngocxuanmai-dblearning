from sqlalchemy import create_engine, text
import os

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    db_url = "mysql+pymysql://root:root@localhost:3306/dblearning" # fallback if script runs outside container

engine = create_engine(db_url)
with engine.connect() as conn:
    res = conn.execute(text("SELECT content_body FROM learning_items WHERE id = 7")).fetchone()
    if res:
        content = res[0]
        
        old_text = "*(Mời bạn xem hình ảnh ERD minh họa chi tiết trong tài liệu PDF đính kèm bên dưới).*"
        
        new_text = """**Mô hình ERD (Crow's Foot notation minh họa):**

```text
[KHÁCH HÀNG] 1 ||────────o< N [HÓA ĐƠN]
                                | 1
                                |
                                | N
                             [SẢN PHẨM]
```

**Chi tiết các thực thể:**

| Thực thể | Khóa chính (PK) | Các thuộc tính khác |
| :--- | :--- | :--- |
| **KHÁCH HÀNG** | Mã KH | Tên, SĐT (Đa trị) |
| **HÓA ĐƠN** | Mã HĐ | Ngày lập |
| **SẢN PHẨM** | Mã SP | Tên SP, Đơn giá |

*Lưu ý: Mối quan hệ M:N giữa HÓA ĐƠN và SẢN PHẨM sẽ có thêm thuộc tính "Số lượng mua" nằm trên đường nối mối quan hệ (khi chuyển sang Database thực tế, nó sẽ biến thành bảng trung gian ChiTietHoaDon).*"""

        if old_text in content:
            new_content = content.replace(old_text, new_text)
            
            # Using raw SQL with parameterized query to avoid SQL injection / formatting issues
            conn.execute(
                text("UPDATE learning_items SET content_body = :cb WHERE id = 7"),
                {"cb": new_content}
            )
            conn.commit()
            print("Content updated successfully!")
        else:
            print("Old text not found in content!")
            print("Current content ends with:")
            print(content[-200:])
