# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

expansions = {
    'View trong SQL': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Materialized View (Khung nhìn Vật lý)
Khung nhìn bình thường (View) là Bảng ảo. Nó chỉ lưu câu lệnh SQL. Nếu View đó lấy dữ liệu từ 5 bảng nối nhau (hàng tỷ dòng), mỗi lần bạn `SELECT * FROM View`, Database sẽ cong mông chạy lại câu JOIN đó mất 5 phút. Rất chậm!
**Giải pháp:** Materialized View. 
Nó LƯU TRỮ HẲN KẾT QUẢ ra đĩa cứng! Khi bạn `SELECT`, nó lấy liền ra như bảng bình thường (0.1 giây). Bù lại, bạn phải cài đặt lịch trình (Job) để làm mới (Refresh) cái View này mỗi đêm, chấp nhận dữ liệu báo cáo bị trễ 1 ngày. Rất hay dùng trong Data Warehouse.

### 3.2. View có update được không? (Updatable View)
Có! Nhưng với điều kiện ngặt nghèo: Cái View đó phải được tạo từ ĐÚNG MỘT BẢNG DUY NHẤT (không xài JOIN, không xài GROUP BY). 
Khi đó, nếu bạn gọi lệnh `UPDATE View SET ...`, CSDL sẽ thông minh tự động truyền lệnh Update đó xuyên qua View và ghi thẳng xuống Bảng gốc.
''',

    'Stored Procedure và Trigger': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Cuộc chiến không hồi kết: Nên để logic ở DB (Stored Proc) hay ở App (Python/Java)?
- **Phe ủng hộ DB (Truyền thống):** Tốc độ cực nhanh vì không tốn băng thông mạng. DB xử lý số liệu là vô địch.
- **Phe ủng hộ App (Hiện đại - Microservices):** Stored Proc cực kỳ khó debug (gỡ lỗi). Không có framework Test tự động (Unit Test) xịn xò. Mã nguồn SQL bị trói chặt vào hãng MySQL/Oracle, muốn chuyển qua hãng khác là viết lại từ đầu.
👉 **Kết luận thực tế:** Các hệ thống Ngân hàng cũ vẫn xài Stored Proc rất nhiều. Nhưng các Startup công nghệ mới hiện nay chuyển 90% logic về code Backend, chỉ coi DB là cái kho chứa đồ để dễ nâng cấp và chuyển đổi.

### 3.2. Các bẫy nguy hiểm của Trigger
Trigger là "bóng ma" trong hệ thống. Một junior DEV chèn 1 dòng code vào bảng `A`. Tự nhiên thấy bảng `B` và `C` cũng bị thay đổi. Cậu ta hoảng loạn vì đọc file code Python không thấy chỗ nào ra lệnh đó cả! Hóa ra một tay DBA đã lén cài Trigger dưới DB.
Do đó, quy tắc vàng: Hạn chế tối đa dùng Trigger cho các logic nghiệp vụ phức tạp. Chỉ dùng Trigger cho các công việc liên quan đến Giám sát hệ thống (Ghi lịch sử chỉnh sửa - Audit Log).
''',

    'Phụ thuộc Hàm': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Thuật toán tìm Bao đóng (Closure) của Tập thuộc tính
Làm sao để biết tập các cột {A, B} có đủ sức làm Khóa chính của Bảng hay không? Các nhà khoa học CSDL dùng một thuật toán gọi là "Tìm Bao Đóng", ký hiệu là $(AB)^+$.
Cách làm: Từ A và B, dựa vào các định lý toán học Armstrong (Phản xạ, Tăng trưởng, Bắc cầu), bạn xem mình có thể suy ra (với tới) TOÀN BỘ các cột còn lại trong bảng hay không. Nếu với tới được hết, nó chính là Siêu Khóa (Superkey)!

### 3.2. Cạm bẫy thiết kế dư thừa thuộc tính
Nhiều sinh viên khi tìm được một Siêu khóa (VD: `Mã SV` + `Tên SV`), họ hồn nhiên chọn nó làm Khóa chính. SAI LẦM!
Khóa chính phải là một Khóa Ứng Cử (Candidate Key) - tức là Siêu khóa NHỎ NHẤT, không thể bỏ bớt cột nào được nữa. Rõ ràng chỉ cần `Mã SV` là đã phân biệt được người rồi, nhét thêm `Tên SV` vào Khóa chính vừa dài dòng, vừa làm giảm hiệu năng hệ thống khi dò tìm.
''',

    'Kiểm soát Tương tranh': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Two-Phase Locking (2PL - Khóa 2 giai đoạn)
Để không bị dữ liệu rác khi hàng ngàn người truy cập, CSDL xài thuật toán 2PL gồm 2 pha:
- **Pha Mở Rộng (Growing Phase):** Giao dịch đi gom và "khóa" tất cả các tài nguyên nó cần.
- **Pha Thu Hẹp (Shrinking Phase):** Giao dịch thực hiện xong và mở khóa, trả tài nguyên lại.
Tuyệt đối không có chuyện vừa mở khóa cái này lại đi khóa tiếp cái kia. Nhờ 2PL, CSDL đảm bảo được Tính Tuần tự hóa (Serializable) nhưng cái giá phải trả là dễ sinh ra Deadlock (bế tắc).

### 3.2. MVCC (Multi-Version Concurrency Control) - Đỉnh cao công nghệ
Đây là công nghệ "Thần thánh" có trong PostgreSQL và MySQL InnoDB giúp giải quyết triệt để sự cố nghẽn cổ chai của thuật toán Khóa (Locking).
**Triết lý của MVCC:** "Người đọc không bao giờ phải chờ người viết. Người viết không bao giờ cản người đọc".
Làm sao hay vậy? Mỗi khi có lệnh UPDATE, hệ thống không khóa dòng cũ lại, mà nó tạo ra một **PHIÊN BẢN (VERSION) mới** của dòng dữ liệu đó, đóng dấu thời gian (Timestamp).
Ai vào sau (thời gian lớn hơn) thì nhìn thấy bản mới. Ai vào trước (chạy lâu quá chưa xong) thì vẫn được phép đọc cái phiên bản Cũ đã lưu tạm ở đâu đó. Cực kỳ uyển chuyển và mượt mà!
''',

    'Phục hồi Dữ liệu': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Thuật toán ARIES - Tiêu chuẩn vàng của Phục hồi
Hầu hết các hệ quản trị danh tiếng (IBM DB2, SQL Server) dùng thuật toán ARIES khi máy chủ có điện lại sau sự cố:
1. **Analysis Phase (Phân tích):** Quét nhật ký để xem lúc cúp điện, Giao dịch nào đang làm dở dang, Giao dịch nào đã xong.
2. **Redo Phase (Làm lại):** Làm lại MỌI THỨ theo đúng thứ tự lịch sử (Kể cả mấy cái dở dang) để đưa hệ thống RAM về đúng ngay cái tích tắc trước khi cúp điện.
3. **Undo Phase (Hoàn tác):** Bắt đầu truy ngược lại để hủy và xóa sạch dấu vết của mấy cái giao dịch đang làm dở dang đó. 

### 3.2. Shadow Paging (Trang bóng)
Thay vì xài Nhật ký (Log) rườm rà, một số hệ thống cũ xài Shadow Paging. Nó tạo ra một "bản sao nháp" của dữ liệu. Giao dịch cứ sửa trên bản nháp. Nếu cúp điện, bản nháp bị vứt sọt rác, dữ liệu gốc không suy suyển. Khi nào lệnh COMMIT được gõ, nó chỉ việc trỏ cái link từ bản nháp thành bản chính thức (giống như thao tác Rename file). Tuy nhiên cách này bị tình trạng phân mảnh ổ cứng nặng nề.
''',

    'Chỉ mục (Index) trong CSDL': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Clustered Index (Chỉ mục Cụm) vs Non-Clustered Index
- **Clustered Index:** Đây là Index tối thượng. Nó quyết định VỊ TRÍ VẬT LÝ của dữ liệu trên đĩa cứng. (Thường CSDL tự tạo nó trên Khóa Chính). Vì dữ liệu chỉ có thể sắp xếp trên đĩa theo 1 kiểu duy nhất (Ví dụ từ bé đến lớn theo ID), nên MỖI BẢNG CHỈ CÓ DUY NHẤT 1 Clustered Index.
- **Non-Clustered Index:** Giống như cái mục lục cuối sách. Nó tạo ra một bảng phụ lục riêng biệt trỏ tới vị trí thực tế của dữ liệu. Bạn có thể tạo hàng chục cái Non-clustered index (Theo tên, theo ngày sinh). Quét nó thì nhanh, nhưng tốn công bước thêm 1 nhịp là "chạy về trang sách chứa dữ liệu gốc" để lấy đầy đủ các cột.

### 3.2. Hiện tượng Index Fragmentation (Phân mảnh Mục lục)
Khi bạn INSERT hoặc DELETE liên tục, cây B-Tree của Index sẽ bị thủng lỗ rỗng, hoặc các nhánh mọc lệch nhau, dài thò lò ra. Tốc độ tìm kiếm bắt đầu chậm lại.
Giống như bảo dưỡng xe hơi, CSDL thỉnh thoảng cần được chạy lệnh **REBUILD INDEX** hoặc **REORGANIZE INDEX** (đặc biệt vào ban đêm Chủ Nhật) để sắp xếp lại cây B-Tree cho gọn gàng và cân bằng trở lại.
''',

    'Giới thiệu NoSQL': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Định lý CAP (CAP Theorem) - Nỗi đau của hệ thống phân tán
Tại sao NoSQL nhanh như chớp nhưng ngành tài chính không dám xài? Vì Định lý CAP. Hệ thống phân tán không bao giờ thỏa mãn đồng thời 3 yếu tố:
1. **Consistency (Nhất quán):** Mọi máy chủ đều trả về cùng một dữ liệu.
2. **Availability (Sẵn sàng):** Mọi lệnh đọc/ghi đều luôn thành công.
3. **Partition tolerance (Chịu lỗi phân mảnh):** Đứt dây mạng giữa các máy chủ, hệ thống vẫn chạy.
Relational DB (SQL) chọn C và A (Hy sinh P).
NoSQL thường chọn A và P (Hy sinh C). Tức là NoSQL xài cơ chế *Eventual Consistency (Nhất quán cuối cùng)*: Bây giờ bạn vừa đăng status, bạn bè ở Châu Mỹ có thể chưa thấy (tạm thời bất nhất), nhưng 10 giây sau hệ thống đồng bộ xong thì họ sẽ thấy. Trải nghiệm người dùng không hề hấn gì!

### 3.2. Polyglot Persistence (Lưu trữ đa ngôn ngữ)
Các hãng công nghệ hiện nay không cãi nhau xem SQL hay NoSQL giỏi hơn nữa. Họ dùng cả hai!
Họ dùng **MySQL** (Relational) để lưu Bill thanh toán của bạn. Kẹp thêm **Redis** (Key-Value) làm Cache để load thông tin User vèo vèo. Đẩy log hoạt động click chuột vào **Cassandra** (Column-family) để đội Data chạy AI. Cuối cùng nhét file hình ảnh của bạn vào ổ cứng S3 của Amazon (Object storage).
''',

    'MongoDB Cơ bản': '''
---
## PHẦN 3: ĐÀO SÂU VÀ THỰC CHIẾN

### 3.1. Nghệ thuật Embed (Nhúng) vs Reference (Tham chiếu)
Trong SQL, bạn bắt buộc phải xẻ dọc dữ liệu ra nhiều bảng và dùng JOIN (Reference).
Trong MongoDB, bạn có đặc quyền gộp tất.
- **Dùng Embed (Nhúng tài liệu con):** Ví dụ: 1 Bài viết có nhiều Bình luận. Hãy nhúng mảng (Array) chứa các Bình luận vào TRỰC TIẾP bên trong Document Bài Viết đó. Khi người dùng mở trang web, Database truy xuất đúng 1 phát là lấy được cả bài viết lẫn bình luận, tốc độ load siêu nhanh (vì ổ cứng không phải chạy đi kiếm ở chỗ khác).
- **Khi nào dùng Reference (Tham chiếu ID như SQL):** Nếu bài viết đó thuộc về idol nổi tiếng, có tới 10 triệu bình luận. Nếu bạn nhúng hết vào, một cái Document sẽ phình to cả Megabyte, vượt quá giới hạn 16MB/Document của Mongo. Lúc này, bạn bắt buộc phải xẻ nó ra Collection khác và lưu ID tham chiếu!

### 3.2. Aggregation Framework - Vũ khí hạng nặng của Mongo
Mongo không có JOIN, vậy làm báo cáo tổng hợp bằng cách nào? Bằng cơ chế Aggregation (Đường ống xử lý).
Dữ liệu sẽ chảy qua một đường ống gồm nhiều đoạn (Stage): 
- Bước 1 (`$match`): Lọc ra hóa đơn tháng 5.
- Bước 2 (`$group`): Gom nhóm theo mã nhân viên.
- Bước 3 (`$sort`): Sắp xếp doanh thu từ cao xuống thấp.
Đây là một quy trình tương tự như khái niệm MapReduce nổi tiếng trong Big Data!
'''
}

with engine.connect() as conn:
    for title, content_add in expansions.items():
        conn.execute(text("UPDATE learning_items SET content_body = CONCAT(content_body, :add) WHERE title = :title"), {'add': content_add, 'title': title})
    conn.commit()
