# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

expansions = {
    'Chuẩn hóa 1NF và 2NF': '''
---
## PHẦN 3: BÀI TẬP THỰC HÀNH CHUẨN HÓA

### Case Study: Bảng hóa đơn siêu thị
Giả sử cô thu ngân đưa cho bạn một file Excel có cấu trúc các cột như sau:
`[Mã_Hóa_Đơn, Ngày_Lập, Mã_Khách, Tên_Khách, Mã_Hàng, Tên_Hàng, Số_Lượng, Đơn_Giá]`

Rõ ràng đây là một cái "Lẩu thập cẩm". Hãy cùng chuẩn hóa nó:

**Bước 1: Áp dụng 1NF (Giá trị nguyên tử)**
File Excel này mỗi ô chỉ chứa 1 giá trị. Tạm coi là đạt 1NF.
Tuy nhiên, Khóa chính của bảng này bắt buộc phải là Tổ hợp của 2 cột: `(Mã_Hóa_Đơn, Mã_Hàng)` thì mới phân biệt được các dòng. Vì 1 hóa đơn có thể có nhiều hàng.

**Bước 2: Áp dụng 2NF (Khử phụ thuộc một phần)**
Ta xét các cột còn lại xem chúng có phụ thuộc vào TOÀN BỘ khóa chính `(Mã Hóa Đơn, Mã Hàng)` không?
- `Ngày_Lập`: Chỉ phụ thuộc vào `Mã_Hóa_Đơn`. Không liên quan đến Hàng. => VI PHẠM 2NF.
- `Mã_Khách`: Chỉ phụ thuộc vào `Mã_Hóa_Đơn`. => VI PHẠM 2NF.
- `Tên_Hàng`: Chỉ phụ thuộc vào `Mã_Hàng`. Không liên quan đến Hóa đơn. => VI PHẠM 2NF.
- `Số_Lượng`: Phụ thuộc vào CẢ `Mã Hóa Đơn` (hóa đơn nào?) và `Mã Hàng` (mua món nào?). => ĐẠT 2NF.

**Băm bảng ra để sửa lỗi:**
- Bảng HÓA ĐƠN: `(Mã_Hóa_Đơn, Ngày_Lập, Mã_Khách, Tên_Khách)`.
- Bảng HÀNG HÓA: `(Mã_Hàng, Tên_Hàng, Đơn_Giá)`.
- Bảng CHI TIẾT HÓA ĐƠN: `(Mã_Hóa_Đơn, Mã_Hàng, Số_Lượng)`.

Thật kỳ diệu! Chỉ bằng quy tắc 2NF, chúng ta đã tách 1 bảng Lẩu thập cẩm ra thành 3 bảng cực kỳ chuẩn mực của ngành Kế toán!
''',

    'Giao dịch và Thuộc tính ACID': '''
---
## PHẦN 3: KIỂM SOÁT TƯƠNG TRANH & DEADLOCK (BẾ TẮC)

### 3.1. Deadlock (Bế tắc) là gì?
Ở trên chúng ta đã nói về ACID, đặc biệt là tính Cô lập (Isolation). Để đảm bảo cô lập, Database sử dụng cơ chế **Lock (Khóa)**. Khi một Giao dịch A đang sửa một dòng, nó "khóa" dòng đó lại, Giao dịch B muốn sửa phải đứng ngoài cửa chờ.

Nhưng điều gì xảy ra nếu:
- Giao dịch A: Khóa Bảng X, chờ Bảng Y.
- Giao dịch B: Khóa Bảng Y, chờ Bảng X.
👉 Hai anh ôm khư khư đồ của mình và chờ nhau VĨNH VIỄN. Đó gọi là **Deadlock (Bế tắc)**. Máy chủ sẽ bị treo.

### 3.2. CSDL giải quyết Deadlock như thế nào?
DBMS rất thông minh. Nó có một tiến trình ngầm (Deadlock Monitor) liên tục vẽ biểu đồ đồ thị chờ đợi. Nếu nó phát hiện đồ thị có 1 Vòng Tròn khép kín (A chờ B, B chờ A), nó sẽ ngay lập tức "bắn bỏ" (Kill / Rollback) một trong hai giao dịch. 
Giao dịch bị bắn (thường là giao dịch ít quan trọng hơn hoặc mới chạy) sẽ báo lỗi ra màn hình. App của lập trình viên phải bắt lấy lỗi này và hiển thị "Mạng bận, vui lòng thử lại".

### 3.3. Các Mức độ Cô Lập (Isolation Levels)
Bạn hoàn toàn có thể ra lệnh cho CSDL hạ thấp độ an toàn xuống để đổi lấy tốc độ cao hơn.
1. `READ UNCOMMITTED`: Mức thấp nhất. Bạn có thể đọc được dữ liệu mà người khác đang sửa dở dang (chưa COMMIT). Dễ bị đọc sai (Dirty Read), nhưng bù lại tốc độ cực nhanh vì chẳng ai phải chờ ai. Rất hay dùng trên Facebook (Số lượng Like nhảy lung tung cũng chả sao).
2. `READ COMMITTED`: Mức mặc định của SQL Server. Chỉ đọc dữ liệu đã COMMIT. An toàn.
3. `REPEATABLE READ`: Mức mặc định của MySQL. Ngăn chặn việc cùng 1 giao dịch đọc 2 lần ra 2 kết quả khác nhau.
4. `SERIALIZABLE`: Mức cao nhất. Bắt tất cả các giao dịch xếp hàng chạy lần lượt (như đi vào 1 cái hẻm nhỏ). Chậm như rùa, nhưng tuyệt đối không bao giờ sai 1 đồng. Ngân hàng dùng mức này khi quyết toán.
''',
    
    'Tối ưu hóa Truy vấn SQL': '''
---
## PHẦN 3: CASE STUDY TỐI ƯU CỰC HẠN

### 3.1. Bài toán N+1 Queries (Kẻ thù số 1 của Framework)
Hầu hết các lập trình viên hiện nay không viết SQL tay mà dùng các ORM Framework (như Entity Framework, Hibernate, Eloquent). Framework tạo ra một lỗi kinh điển gọi là N+1.

**Tình huống:** Bạn muốn in ra danh sách 100 Sinh Viên và tên Khoa của họ.
Thay vì Framework chạy 1 câu lệnh JOIN:
`SELECT * FROM SinhVien JOIN Khoa ...` (Chỉ tốn 1 truy vấn).
Framework "ngốc nghếch" sẽ làm như sau:
1. `SELECT * FROM SinhVien` (Ra 100 sinh viên. Tốn 1 truy vấn).
2. Nó viết vòng lặp `for` chạy 100 lần. Mỗi lần gọi thêm: `SELECT TenKhoa FROM Khoa WHERE MaKhoa = ?`.
👉 Tổng cộng: Nó gọi xuống Database **101 lần** (1 + N lần). Làm sập Server trong tích tắc!
**Cách sửa:** Yêu cầu Framework sử dụng `Eager Loading` (thực chất là ép nó xài JOIN ngay từ đầu).

### 3.2. Nghệ thuật Đánh Chỉ Mục (Indexing Strategy)
- **Composite Index (Chỉ mục phức hợp):** Bạn hay dùng `WHERE HoTen = 'X' AND NgaySinh = 'Y'`. Nếu bạn đánh 2 cái index rời rạc lên HoTen và NgaySinh, CSDL sẽ rất bối rối. Hãy đánh 1 cái Index gộp cả 2 cột: `CREATE INDEX idx_name_dob ON SinhVien(HoTen, NgaySinh)`. Tốc độ sẽ tăng gấp bội!
- **Index selectivity (Độ phân cực):** Không bao giờ đánh Index cho cột Giới Tính. Cột giới tính chỉ có 2 giá trị: Nam/Nữ. Dữ liệu bị lặp 50%. Việc dùng mục lục cho một thứ có ở một nửa số trang sách là vô nghĩa. CSDL sẽ lờ cái Index đó đi và tự quét (Full scan).

### 3.3. Sử dụng Bảng Tạm (Temp Tables) thay cho Subquery lồng 5 tầng
Một câu SQL dài 200 dòng lồng 5 cái Subquery bên trong nhau không làm bạn trông ngầu hơn, nó làm DBA (Quản trị viên) muốn đánh bạn! Nó rất khó bảo trì và CSDL phải nặn óc ra để tính toán bộ nhớ.
Thay vào đó, hãy chia nhỏ bài toán. `SELECT` phần 1 ném vào Bảng Tạm. Lấy Bảng Tạm `JOIN` với phần 2 để ném vào Bảng Tạm 3. Code trong sáng, dễ debug, và Database tối ưu bộ đệm dễ dàng hơn nhiều.
'''
}

with engine.connect() as conn:
    for title, content_add in expansions.items():
        conn.execute(text("UPDATE learning_items SET content_body = CONCAT(content_body, :add) WHERE title = :title"), {'add': content_add, 'title': title})
    conn.commit()
