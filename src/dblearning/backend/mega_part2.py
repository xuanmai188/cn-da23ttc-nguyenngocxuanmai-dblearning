# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

expansions = {
    'Khóa và Ràng buộc Toàn vẹn': '''
---
## PHẦN 3: CHIẾN LƯỢC ĐẶT KHÓA (KEYS) TRONG THỰC CHIẾN

### 3.1. Trận chiến thế kỷ: Natural Key (Khóa Tự Nhiên) vs Surrogate Key (Khóa Nhân Tạo)
Đây là câu hỏi phỏng vấn kinh điển cho vị trí Backend Developer. 
Giả sử bạn thiết kế bảng `SINHVIEN`. Bạn chọn cột nào làm Khóa chính (PK)?
- **Natural Key (Khóa tự nhiên):** Chọn `Số CMND/CCCD` làm Khóa. Vì nó có sẵn trong thế giới thực và duy nhất.
  - *Ưu điểm:* Dễ hiểu. 
  - *Nhược điểm chết người:* Nếu một ngày Cảnh sát thay đổi format CCCD từ 9 số lên 12 số, bạn sẽ phải UPDATE lại toàn bộ Khóa chính trong DB. Khóa ngoại ở hàng chục bảng khác cũng phải UPDATE theo. Hệ thống sẽ tê liệt!
- **Surrogate Key (Khóa nhân tạo):** Tạo ra 1 cột vô nghĩa, thường là Số nguyên Tự tăng (`ID INT AUTO_INCREMENT`), ví dụ: Sinh viên số 1, số 2... 
  - *Ưu điểm:* Nó tồn tại vĩnh viễn, bất biến, tốc độ tìm kiếm cực nhanh (vì là số nguyên). Nếu sinh viên đổi CCCD, đổi Tên, đổi Khoa... thì ID vẫn là ID đó. 99% công ty công nghệ lớn đều dùng Khóa nhân tạo!

### 3.2. Sức mạnh của Khóa ngoại (Foreign Key - FK)
Nhiều Lập trình viên lười biếng thường KHÔNG tạo Khóa ngoại trong CSDL. Họ tự hứa: "Mình sẽ dùng code Python/PHP để kiểm tra dữ liệu trước khi INSERT". 
Đây là sự lười biếng dẫn đến thảm họa! Code Web có thể bị lỗi, Hacker có thể gọi API trực tiếp. Chỉ có Khóa ngoại ở mức CSDL mới chặn được 100% dữ liệu rác.

**Các tùy chọn hành động khi xóa (ON DELETE CASCADE):**
Khi bạn xóa Khoa CNTT, mà đang có 1000 sinh viên thuộc Khoa đó, điều gì xảy ra?
1. `ON DELETE RESTRICT (Mặc định):` CSDL sẽ hét lên LỖI, từ chối xóa Khoa CNTT. Bảo vệ an toàn 100%.
2. `ON DELETE CASCADE (Xóa dây chuyền):` Bạn xóa Khoa CNTT, CSDL tự động XÓA LUÔN 1000 SINH VIÊN thuộc Khoa đó. Cực kỳ nguy hiểm! Thường chỉ dùng cho Thực thể yếu (Ví dụ: Xóa Bài viết thì Xóa dây chuyền hết Comment của bài đó).
3. `ON DELETE SET NULL:` Xóa Khoa CNTT, 1000 sinh viên kia không bị xóa, mà cột `Mã Khoa` của họ tự động bị biến thành `NULL` (Tức là trở thành sinh viên vô gia cư).
''',

    'SQL DML: Thêm Sửa Xóa Dữ liệu': '''
---
## PHẦN 3: KỸ THUẬT DML NÂNG CAO & GIẢI PHÁP THỰC TẾ

### 3.1. UPSERT (Cập nhật hoặc Thêm mới)
Bài toán: Bạn muốn thêm 1 sản phẩm. Nếu sản phẩm đó CHƯA CÓ thì `INSERT`, nếu CÓ RỒI thì `UPDATE` số lượng.
Thay vì phải viết code `SELECT` ra kiểm tra rồi dùng `IF ELSE`, SQL cung cấp cú pháp tối thượng:
- Trong MySQL: `INSERT ... ON DUPLICATE KEY UPDATE SoLuong = SoLuong + 1`
- Trong PostgreSQL: `INSERT ... ON CONFLICT DO UPDATE`
Kỹ thuật này giúp giảm 50% số lượng truy vấn xuống CSDL!

### 3.2. Bulk Insert (Thêm dữ liệu hàng loạt)
Đừng bao giờ chạy 1000 câu lệnh `INSERT` trong 1 vòng lặp `for` của Python. Mỗi lần gọi `INSERT` là một lần mở kết nối mạng, cực kỳ tốn thời gian.
Hãy gom chúng lại thành 1 câu lệnh duy nhất:
```sql
INSERT INTO SinhVien (MSSV, HoTen) VALUES 
('SV01', 'An'),
('SV02', 'Bình'),
('SV03', 'Cường'); -- 1000 dòng liên tiếp...
```
Tốc độ sẽ nhanh gấp 100 lần!

### 3.3. Xóa dữ liệu an toàn (Soft Delete vs Hard Delete)
Như đã nhắc ở trên, trong các hệ thống doanh nghiệp (ERP, Kế toán), nút "Xóa" trên giao diện thực chất không hề gọi lệnh `DELETE`.
- **Hard Delete (Xóa cứng):** Dùng lệnh `DELETE`. Dữ liệu bốc hơi vĩnh viễn khỏi ổ cứng.
- **Soft Delete (Xóa mềm):** Dùng lệnh `UPDATE Users SET IsDeleted = 1 WHERE ID = 5;`. 
Khi truy vấn danh sách, ta luôn luôn phải gắn thêm đuôi `WHERE IsDeleted = 0`. Dữ liệu vẫn còn đó để phòng khi khách hàng kiện cáo, hoặc phục hồi khi lỡ tay.
''',
    
    'Hàm Tổng hợp trong SQL': '''
---
## PHẦN 3: TUYỆT KỸ BÁO CÁO VỚI GROUP BY VÀ HAVING

### 3.1. Hiểu đúng về hàm COUNT()
Cực kỳ nhiều người không biết sự khác biệt giữa `COUNT(*)` và `COUNT(cột_nào_đó)`.
- `COUNT(*)`: Đếm số lượng DÒNG (Bao gồm cả những dòng toàn là NULL).
- `COUNT(SoDienThoai)`: Chỉ đếm những dòng mà cột SoDienThoai CÓ DỮ LIỆU. Những ai rỗng (NULL) sẽ không được đếm!
=> Nếu sếp bảo "Đếm số nhân viên trong công ty", phải dùng `COUNT(*)`. Nếu sếp bảo "Đếm số nhân viên ĐÃ CẬP NHẬT SỐ ĐIỆN THOẠI", dùng `COUNT(SoDienThoai)`.

### 3.2. Bẫy tư duy của GROUP BY
Luật vàng: Bất cứ cột nào bạn đặt trong hàm tổng hợp (MAX, MIN, SUM), thì những cột còn lại nằm trơ trọi bên ngoài BẮT BUỘC phải đưa vào `GROUP BY`.
Tại sao? Giả sử bạn muốn tính "Tổng Lương của từng Phòng ban". Bạn gõ:
```sql
SELECT TenNhanVien, MaPhong, SUM(Luong) 
FROM NhanVien 
GROUP BY MaPhong;
```
Lệnh này sẽ báo lỗi ngay lập tức! Vì bạn yêu cầu CSDL gộp 10 người phòng Kế Toán lại thành 1 dòng (để tính tổng lương). Vậy tại cột `TenNhanVien` trên cái 1 dòng kết quả đó, CSDL biết in tên của ai trong số 10 người?? Vô lý! 
Do đó, chỉ được SELECT `MaPhong` và `SUM(Luong)`. Không được mang các cột cá nhân vào đây.

### 3.3. Đỉnh cao thống kê: Mệnh đề HAVING
Sếp yêu cầu: "Tính doanh thu của từng cửa hàng, và chỉ in ra những cửa hàng có doanh thu > 1 tỷ".
Nhiều bạn sẽ gõ:
```sql
SELECT MaCuaHang, SUM(DoanhThu) FROM CuaHang
WHERE SUM(DoanhThu) > 1000000000 -- SAI BÉT !!!
GROUP BY MaCuaHang;
```
`WHERE` hoạt động TRƯỚC KHI gom nhóm. Lúc nó chạy, `SUM()` chưa hề được tính, nên nó không thể so sánh được!
Giải pháp là `HAVING`. Mệnh đề này chạy SAU KHI đã gom nhóm xong.
```sql
SELECT MaCuaHang, SUM(DoanhThu) FROM CuaHang
GROUP BY MaCuaHang
HAVING SUM(DoanhThu) > 1000000000; -- CHUẨN XÁC!
```
'''
}

with engine.connect() as conn:
    for title, content_add in expansions.items():
        conn.execute(text("UPDATE learning_items SET content_body = CONCAT(content_body, :add) WHERE title = :title"), {'add': content_add, 'title': title})
    conn.commit()
