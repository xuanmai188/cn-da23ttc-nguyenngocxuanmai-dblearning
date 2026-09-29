# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

expansions = {
    'Tổng quan về Cơ sở Dữ liệu': '''
---
## PHẦN 3: ĐÀO SÂU VÀO HỆ QUẢN TRỊ CSDL (MEGA DIVE)

### 3.1. Phân phẫu bên trong một DBMS
Một DBMS không chỉ là một cái kho. Nó là một cỗ máy khổng lồ gồm nhiều thành phần:
1. **Query Processor (Bộ xử lý truy vấn):** Khi bạn gõ `SELECT`, thành phần này sẽ dịch câu lệnh tiếng Anh đó thành ngôn ngữ máy, phân tích cú pháp (Parse), và tìm ra con đường lấy dữ liệu nhanh nhất (Query Optimizer).
2. **Storage Manager (Quản lý lưu trữ):** Xin hệ điều hành ổ cứng để lưu file, quản lý bộ nhớ đệm (Buffer/Cache) trên RAM để đọc ghi siêu tốc.
3. **Transaction Manager (Quản lý giao dịch):** Đảm bảo an toàn khi cúp điện (ACID). Đảm bảo 1000 người mua hàng cùng lúc không bị kẹt xe (Concurrency Control).

### 3.2. Case Study: Shopee lưu dữ liệu như thế nào?
Bạn nghĩ Shopee lưu toàn bộ mọi thứ vào 1 con server MySQL? Không!
- Dữ liệu **Sản phẩm, Đơn hàng, Tiền bạc:** Lưu ở Relational DB (MySQL/Oracle) vì cần độ chính xác tuyệt đối (ACID). Lỗi 1 đồng cũng đền ốm.
- Dữ liệu **Lịch sử click, Lịch sử tìm kiếm:** Lưu ở NoSQL (MongoDB, Cassandra) vì nó quá khổng lồ (hàng tỷ tỷ dòng) và không cần chính xác 100%. Nếu lỡ mất 1 dòng lịch sử tìm kiếm, chả ai quan tâm.
- Dữ liệu **Giỏ hàng (Cart):** Lưu ở Redis (In-memory DB). Vì giỏ hàng cần load siêu nhanh, lưu thẳng trên RAM để trải nghiệm người dùng không bị lag.

### 3.3. Các câu hỏi thường gặp (FAQ dành cho người mới)
- **Hỏi:** Tôi làm web bán quần áo nhỏ, dùng Excel hay Access được không?
- **Đáp:** KHÔNG. Ngay cả web nhỏ nhất hiện nay cũng xài MySQL hoặc SQLite. Excel/Access sẽ sập ngay lập tức khi có 10 người truy cập web cùng lúc.
- **Hỏi:** Học SQL có khó bằng học Python/Java không?
- **Đáp:** SQL là ngôn ngữ Khai báo (Declarative). Bạn chỉ cần mô tả "Bạn muốn lấy cái gì" (Ví dụ: `SELECT HoTen`), còn "Lấy như thế nào" là do CSDL tự lo. Nó dễ học hơn Python rất nhiều!
''',

    'Kiến trúc Hệ thống CSDL': '''
---
## PHẦN 3: THIẾT KẾ KIẾN TRÚC CLIENT-SERVER THỰC CHIẾN

### 3.1. Kiến trúc 1 Tầng (Tier-1) vs 2 Tầng vs 3 Tầng
Trong thực tế phát triển phần mềm, Kiến trúc CSDL không chỉ đứng một mình mà gắn liền với kiến trúc Mạng:
- **Kiến trúc 1 Tầng (Standalone):** App và Database nằm chung 1 máy (Ví dụ: App quản lý kho cài trên máy tính cô thu ngân). Dễ bị mất trộm máy là mất hết dữ liệu.
- **Kiến trúc 2 Tầng (Client-Server):** Có 1 con Server để góc phòng cài Database. Các máy con (Client) cài App, cắm dây mạng LAN nối vào Server để lấy dữ liệu. Rất phổ biến ở các siêu thị.
- **Kiến trúc 3 Tầng (Web Architecture):** Đây là kiến trúc của 99% website hiện đại. 
  - Tầng 1: Trình duyệt Web (Client).
  - Tầng 2: Web Server (Backend code bằng Python/NodeJS).
  - Tầng 3: Database Server (MySQL).
  - *Tại sao phải có Tầng 2?* Vì lý do bảo mật. Tầng Client (Trình duyệt) tuyệt đối KHÔNG BAO GIỜ được quyền nói chuyện trực tiếp với Database. Mọi câu lệnh SQL phải được Backend kiểm duyệt kỹ lưỡng để chống Hacker.

### 3.2. Data Dictionary (Từ điển dữ liệu)
Một thành phần cực kỳ quan trọng ở Tầng Khái niệm. Nó là "Dữ liệu về Dữ liệu" (Metadata). 
Khi bạn tạo bảng `SinhVien`, DBMS sẽ tự động ghi vào Từ điển dữ liệu rằng: Bảng `SinhVien` có 5 cột, cột `HoTen` độ dài tối đa 50 ký tự, người tạo là Admin lúc 10h sáng. 
Bất kỳ lúc nào bạn cũng có thể mở Từ điển dữ liệu ra để xem cấu trúc toàn bộ hệ thống.

### 3.3. Case Study: Chống sập hệ thống (Scaling)
Khi hệ thống có 1 triệu người dùng, 1 con Server Database sẽ bốc cháy. Các kỹ sư giải quyết bằng cách:
- **Scale Up (Nâng cấp dọc):** Mua RAM, CPU xịn hơn, gắn ổ cứng SSD siêu tốc cho Server đó. (Đắt tiền và có giới hạn).
- **Scale Out (Nâng cấp ngang):** Mua thêm 5 con Server rẻ tiền, kết nối chúng lại thành một cụm (Cluster). Phân chia công việc: 1 con chuyên ghi dữ liệu (Master), 4 con chuyên đọc dữ liệu (Slaves). Đây là kiến trúc mà mọi tập đoàn lớn đang dùng!
''',

    'Mô hình ER: Thực thể và Thuộc tính': '''
---
## PHẦN 3: BÍ QUYẾT THIẾT KẾ ERD CHUYÊN NGHIỆP

### 3.1. Thực thể Yếu (Weak Entity) và Khóa từng phần
Một thực thể yếu không có thuộc tính nào đủ sức làm Khóa chính. 
Ví dụ: Thực thể **PHÒNG_HỌC**. Thuộc tính của nó là `Tên phòng` (Ví dụ: "Phòng 101"). Nhưng "Phòng 101" có thể nằm ở Tòa nhà A, và cũng có "Phòng 101" nằm ở Tòa nhà B.
Do đó, "Phòng 101" không thể làm Khóa chính. PHÒNG_HỌC là Thực thể yếu. Nó phải dựa dẫm vào Thực thể mạnh là **TÒA_NHÀ**.
Khóa chính của PHÒNG_HỌC sẽ là sự kết hợp: `Mã Tòa Nhà` + `Tên phòng`.

### 3.2. 5 Lỗi "Chết người" khi vẽ ERD của Lính mới
1. **Dùng Động từ làm Thực thể:** Thực thể phải là Danh từ! Không ai tạo thực thể "Đăng ký". "Đăng ký" phải là Mối quan hệ (Hình thoi) giữa Sinh viên và Môn học.
2. **Quên mất Thuộc tính Đa trị:** Lưu 3 số điện thoại vào 1 cột. Hậu quả: Khi sếp yêu cầu "Tìm khách hàng có đuôi SĐT là 888", câu lệnh SQL sẽ chạy mất 10 phút. Giải pháp: Vẽ nó là Elip nét đôi để lát sau tách thành Bảng riêng!
3. **Nhầm lẫn Thuộc tính Suy diễn (Derived):** Lưu cột `Tuổi`. Ngày mai qua năm mới, tuổi của mọi người bị sai bét. Giải pháp: Cột tuổi phải vẽ là Elip nét đứt, nghĩa là nó KHÔNG được lưu vào DB, mà sẽ được tính bằng công thức: `Tuổi = Năm Hiện Tại - Năm Sinh` lúc chạy lệnh SELECT.
4. **Không xác định Khóa:** Một thực thể (Hình chữ nhật) mà không có bất kỳ thuộc tính nào được gạch chân (Khóa). Đó là một cái kho không có số thẻ, dữ liệu sẽ biến thành một đống rác không thể truy xuất.
5. **Vẽ quá nhiều thuộc tính rác:** Thiết kế bảng `NhanVien` lưu cả Chiều cao, Cân nặng, Cung hoàng đạo... trong khi công ty bạn làm về kế toán. Nguyên tắc: Chỉ lưu cái gì mà NGHIỆP VỤ yêu cầu.
'''
}

with engine.connect() as conn:
    for title, content_add in expansions.items():
        conn.execute(text("UPDATE learning_items SET content_body = CONCAT(content_body, :add) WHERE title = :title"), {'add': content_add, 'title': title})
    conn.commit()
