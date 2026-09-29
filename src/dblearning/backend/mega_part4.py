# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

expansions = {
    'Các mô hình Dữ liệu': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Sự trỗi dậy của Multi-model Database
Trước đây, các công ty phân chia rạch ròi: Dùng MySQL cho dữ liệu quan hệ, Neo4j cho đồ thị, Redis cho cache. Hệ quả là hệ thống bị phân mảnh, bảo trì mệt mỏi.
Hiện nay, xu hướng là **Đa mô hình (Multi-model)**. Ví dụ: PostgreSQL không chỉ là CSDL Quan hệ, nó hỗ trợ lưu trữ và truy vấn file JSON cực kỳ mạnh mẽ (như NoSQL), thậm chí hỗ trợ cả tìm kiếm văn bản (Full-text search). Việc nắm vững 1 hệ thống Multi-model giúp tiết kiệm 50% chi phí máy chủ.

### 3.2. Cạm bẫy khi chọn sai Mô hình dữ liệu
Một startup mạng xã hội chọn MySQL để lưu "Ai đang follow ai". Khi số lượng user lên 1 triệu, câu lệnh truy vấn "Bạn của bạn của bạn là ai" (truy vấn lồng 3 cấp) làm MySQL đứng hình vì phải `JOIN` bảng cả tỷ lần.
Nếu họ hiểu về **Graph Database (Mô hình đồ thị)**, họ sẽ chọn Neo4j. Việc tìm bạn của bạn trong Graph DB chỉ mất 0.01 giây vì các node được kết nối vật lý với nhau!
''',

    'Mô hình ER: Mối Quan hệ': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Ràng buộc tham gia (Participation Constraints)
Khi vẽ nét nối giữa Thực thể và Hình thoi, có 2 loại nét vẽ quyết định sự sống còn của dữ liệu:
- **Nét đơn (Tham gia một phần - Partial):** Một Giảng viên có thể "Chủ nhiệm" một Lớp, hoặc KHÔNG chủ nhiệm lớp nào cả.
- **Nét đôi (Tham gia toàn phần - Total):** Một Sinh viên BẮT BUỘC phải thuộc về 1 Khoa. Không thể có Sinh viên lơ lửng không thuộc Khoa nào. 
Khi dịch sang SQL, nét đôi chính là ràng buộc `NOT NULL` ở cột khóa ngoại!

### 3.2. Mối quan hệ đệ quy (Recursive Relationship)
Một thực thể có thể có mối quan hệ với CHÍNH NÓ!
- *Ví dụ:* Thực thể NHÂN VIÊN. Mối quan hệ là "Quản lý". Một Nhân viên (Sếp) sẽ quản lý nhiều Nhân viên (Lính).
Khi gặp trường hợp này, bảng tạo ra sẽ chứa 1 cột khóa ngoại trỏ ngược lại đúng cột khóa chính của bảng đó (`MaNguoiQuanLy` trỏ về `MaNV`).
''',

    'Thực hành vẽ ER Diagram': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Tiêu chuẩn thiết kế ERD Quốc tế
Khi đi làm thực tế, không ai dùng bút vẽ hình elip hay hình thoi nữa (vì nó tốn diện tích). Mọi người dùng chuẩn **Crow's Foot (Chân chim)**.
- **1:** Ký hiệu bằng 2 vạch thẳng đứng (||).
- **Nhiều:** Ký hiệu bằng hình chân chim bám vào thực thể.
- **0 (Tùy chọn):** Ký hiệu bằng 1 hình tròn (o).
👉 Nếu bạn thấy ký hiệu `o|<`, nghĩa là "Có thể không có, hoặc có nhiều" (0 to Many).

### 3.2. Case Study thực hành: Thiết kế App Đặt Xe (như Grab)
- **Bước 1 (Xác định Thực thể):** KHACH_HANG, TAI_XE, XE, CHUYEN_DI.
- **Bước 2 (Xác định Quan hệ):** KHACH_HANG [Đặt] CHUYEN_DI (1-N). TAI_XE [Nhận] CHUYEN_DI (1-N). TAI_XE [Lái] XE (1-1 hoặc 1-N).
- **Bước 3 (Thuộc tính):** CHUYEN_DI phải có `Điểm_Đón`, `Điểm_Đến`, `Giá_Tiền`, `Trạng_Thái`.
*Lưu ý:* Giá tiền không phải thuộc tính suy diễn, vì giá Grab thay đổi theo giờ cao điểm, phải lưu cứng (hardcode) giá trị vào lúc đặt xe!
''',

    'Lược đồ Quan hệ': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Thuật toán chuyển ERD sang Lược đồ Quan hệ
Đây là quy tắc bất di bất dịch mà Coder nào cũng phải thuộc lòng:
1. **Thực thể Mạnh:** Biến thành 1 Bảng. Khóa của thực thể làm Khóa chính (PK).
2. **Quan hệ 1-N:** Nhét Khóa chính của bảng "1" sang làm Khóa ngoại (FK) ở bảng "Nhiều". (Ghi nhớ: Bọn "Nhiều" luôn chứa chìa khóa).
3. **Quan hệ 1-1:** Tùy ý chọn 1 bên để chứa Khóa ngoại của bên kia. Nên chọn bên nào có "Tham gia toàn phần".
4. **Quan hệ M-N:** BẮT BUỘC phải tạo ra Bảng thứ 3 (Bảng trung gian). Lấy khóa chính của cả 2 bảng kia vào làm Khóa chính phức hợp cho bảng thứ 3 này.

### 3.2. Cạm bẫy thiết kế ngược (Reverse Engineering)
Đi làm, ít khi bạn được thiết kế CSDL mới từ đầu. Thường sếp sẽ vứt cho bạn một đống Bảng rác rưởi 10 năm tuổi và bắt bạn đoán xem ngày xưa người ta vẽ ERD thế nào. Nếu các bảng đó KHÔNG có Khóa ngoại (do người cũ lười cài đặt), bạn sẽ phải tự soi dữ liệu bằng tay để đoán mối quan hệ. Rất kinh hoàng!
''',

    'Đại số Quan hệ': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Tại sao Lập trình viên phải học Toán (Đại số quan hệ)?
Nhiều bạn thắc mắc: "Tôi chỉ cần gõ lệnh SQL SELECT, học mấy cái ký hiệu toán học Π, σ làm gì cho đau đầu?"
**Bí mật của Database Engine:** SQL là ngôn ngữ Khai báo. Khi bạn gõ SQL, CSDL không chạy SQL! CSDL sẽ **dịch câu SQL của bạn sang Đại số Quan hệ**. 
Bộ Tối ưu hóa Truy vấn (Query Optimizer) sẽ dùng các định lý Toán học của Đại số Quan hệ để đảo vị trí các phép toán sao cho thời gian chạy nhanh nhất, sau đó mới xuất ra kết quả!

### 3.2. Định lý Tối ưu hóa cơ bản (Push-down Selection)
Giả sử có câu SQL: `Lấy Tên của Sinh viên thuộc khoa CNTT`.
- **Cách ngốc nghếch:** Nối (JOIN) bảng SINHVIEN và bảng KHOA lại với nhau (Phép ⨝). Tạo ra bảng tạm 10 triệu dòng. Rồi mới Chọn (Phép σ) ra những người khoa CNTT.
- **Tối ưu bằng Toán học:** Thay vì Nối trước, hệ thống sẽ thực hiện Chọn (σ) lọc ra khoa CNTT trước. Bảng tạm chỉ còn 1 dòng. Sau đó mới Nối. Tốc độ tăng 1 triệu lần! 
Nếu bạn hiểu Đại số quan hệ, bạn sẽ viết SQL đúng chuẩn để CSDL dễ tối ưu nhất.
''',

    'SQL DDL: Tạo và Quản lý Bảng': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Cạm bẫy ALTER TABLE trên hệ thống đang chạy (Zero-downtime)
Tạo bảng bằng `CREATE TABLE` thì quá dễ. Nhưng sửa bảng (`ALTER TABLE`) lại là cơn ác mộng.
**Tình huống:** Bảng KhachHang đang có 50 triệu dòng. Công ty đang chạy flash-sale. Sếp yêu cầu bạn gõ lệnh: `ALTER TABLE KhachHang ADD COLUMN SoDienThoai VARCHAR(15)`.
**Thảm họa:** Lệnh ALTER sẽ KHÓA (Lock) toàn bộ cái bảng đó. Không ai mua được hàng trong suốt 30 phút hệ thống chèn cột mới. Công ty mất hàng tỷ đồng.
**Giải pháp thực chiến:** Sử dụng công cụ của hãng thứ 3 như `pt-online-schema-change` hoặc tạo một bảng mới v2, copy dần dữ liệu sang ở background, rồi đổi tên bảng (Rename).

### 3.2. Các kiểu dữ liệu tốn kém (Anti-patterns)
- Khai báo `VARCHAR(255)` vô tội vạ cho mọi cột chữ. Tốn bộ nhớ RAM khi truy vấn. Hãy suy nghĩ kỹ độ dài thực tế.
- Khai báo `INT` cho cột trạng thái (Chỉ có 0, 1, 2). Hãy dùng `TINYINT` (1 byte) để tiết kiệm 75% ổ cứng!
- Dùng chuỗi `VARCHAR` để lưu Ngày tháng. Tuyệt đối không! Hãy dùng định dạng `DATE` hoặc `TIMESTAMP` để SQL còn dùng được hàm thời gian tính toán tuổi tác!
''',

    'SQL DQL: Truy vấn Dữ liệu': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Đằng sau sự kỳ diệu của mệnh đề LIKE (Tìm kiếm chuỗi)
Dùng `LIKE '%Nguyễn%'` rất tiện. Nhưng nó là sát thủ hiệu năng.
**Kỹ thuật nâng cao:** 
1. Nếu chỉ muốn tìm đầu chuỗi: `LIKE 'Nguyễn%'`. Lúc này CSDL có thể sử dụng Index!
2. Nếu muốn tìm bất cứ đâu: Hãy bỏ LIKE đi và sử dụng **Full-Text Search (FTS)** của hệ quản trị. Nó tạo ra một "Từ điển" (Inverted Index) giống như Google, tìm chuỗi tỷ dòng mất chưa tới 0.1 giây.

### 3.2. CASE WHEN - Viết logic IF ELSE ngay trong SQL
Thay vì kéo toàn bộ dữ liệu về Python/NodeJS rồi dùng `if else` để phân loại, hãy làm điều đó ngay từ lúc truy vấn để giảm băng thông.
```sql
SELECT HoTen, 
    CASE 
        WHEN Diem >= 8 THEN 'Giỏi'
        WHEN Diem >= 5 THEN 'Khá'
        ELSE 'Yếu'
    END AS XepLoai
FROM SinhVien;
```
Câu lệnh này đẩy gánh nặng tính toán về cho máy chủ CSDL (thường rất trâu bò), giúp Tầng Web Server chạy nhẹ nhàng hơn rất nhiều!
''',

    'Subquery và CTE': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Từ bỏ Subquery, chuyển sang CTE (WITH clause)
Lập trình viên đời đầu rất thích nhét Subquery lồng 3, 4 tầng vào mệnh đề `FROM`. Kết quả là nhìn câu lệnh SQL giống như 1 bát mì spaghetti rối rắm, người khác đọc không hiểu gì.
**Công cụ tối thượng:** CTE (Common Table Expressions) bắt đầu bằng chữ `WITH`.
Nó cho phép bạn định nghĩa các bảng tạm ĐẶT TÊN ngay trên đầu file, sau đó dùng lại ở dưới.
```sql
WITH DoanhThuTungThang AS (
    SELECT Thang, SUM(Tien) AS Tong FROM HoaDon GROUP BY Thang
),
ThangKyLuc AS (
    SELECT MAX(Tong) AS MaxTong FROM DoanhThuTungThang
)
SELECT * FROM DoanhThuTungThang 
WHERE Tong = (SELECT MaxTong FROM ThangKyLuc);
```
Code được phân chia module cực kỳ rành mạch, có thể xài đi xài lại!

### 3.2. Subquery tương quan (Correlated Subquery) - Con quái vật hiệu năng
Là subquery mà điều kiện bên trong nó phụ thuộc vào dữ liệu của vòng lặp bên ngoài.
Nó buộc Database phải chạy cái Subquery đó lại từ đầu CHO MỖI MỘT DÒNG kết quả. Nếu vòng ngoài có 1 triệu dòng, Subquery chạy 1 triệu lần!
**Luật bất thành văn:** Bất cứ khi nào bạn định viết Correlated Subquery, hãy dừng lại và tìm cách chuyển nó thành mệnh đề `JOIN` ngay lập tức!
'''
}

with engine.connect() as conn:
    for title, content_add in expansions.items():
        conn.execute(text("UPDATE learning_items SET content_body = CONCAT(content_body, :add) WHERE title = :title"), {'add': content_add, 'title': title})
    conn.commit()
