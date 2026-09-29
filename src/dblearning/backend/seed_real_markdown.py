# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning" # fallback for local execution if needed

engine = create_engine(db_url)

content_map = {
    'Tổng quan về Cơ sở Dữ liệu': '''## 1. Cơ sở dữ liệu (Database) là gì?
Cơ sở dữ liệu (CSDL) là một tập hợp các dữ liệu có liên quan logic với nhau, được tổ chức và lưu trữ một cách có cấu trúc trên hệ thống máy tính. 
Thay vì lưu dữ liệu lộn xộn trong các file văn bản rời rạc, CSDL giúp tổ chức dữ liệu thành các bảng, hàng và cột để dễ dàng tìm kiếm, cập nhật và quản lý.

## 2. Hệ quản trị CSDL (DBMS) là gì?
**DBMS (Database Management System)** là một phần mềm hệ thống cho phép người dùng định nghĩa, tạo, duy trì và kiểm soát truy cập vào cơ sở dữ liệu. Nó đóng vai trò là cầu nối giữa người dùng/ứng dụng và dữ liệu vật lý.
- **Ví dụ các DBMS phổ biến:** MySQL, PostgreSQL, Microsoft SQL Server, Oracle, MongoDB.

## 3. Hệ thống CSDL vs Hệ thống File truyền thống
Trước khi có CSDL, người ta lưu dữ liệu trong các File. Hệ thống CSDL ra đời để khắc phục các nhược điểm chí mạng của hệ thống File:
- **Giảm dư thừa dữ liệu (Redundancy):** Không lưu trùng lặp một thông tin ở nhiều nơi (ví dụ: thông tin sinh viên chỉ lưu 1 lần, không phải lưu ở cả file Điểm và file Học phí).
- **Đảm bảo tính nhất quán (Consistency):** Khi cập nhật dữ liệu ở 1 nơi, hệ thống tự động đồng bộ.
- **Bảo mật và Phân quyền:** Cho phép giới hạn quyền truy cập từng bảng, từng cột đối với từng user khác nhau.
- **Toàn vẹn dữ liệu (Integrity):** Đảm bảo dữ liệu nhập vào luôn hợp lệ (ví dụ: tuổi phải > 0).
- **Truy cập đồng thời (Concurrency):** Hàng ngàn người có thể truy cập và sửa dữ liệu cùng lúc mà không bị xung đột.
''',

    'Kiến trúc Hệ thống CSDL': '''## 1. Kiến trúc 3 tầng ANSI/SPARC
Để che giấu sự phức tạp của việc lưu trữ dữ liệu với người dùng, một hệ thống CSDL chuẩn được chia làm 3 mức (tầng) trừu tượng:

### Mức ngoài (External Level / View Level)
- Là góc nhìn của người dùng cuối (User View). 
- Mỗi người dùng hoặc ứng dụng chỉ nhìn thấy một phần dữ liệu mà họ quan tâm và được phép thấy. 
- *Ví dụ: Sinh viên chỉ nhìn thấy điểm của mình, không thấy điểm của người khác.*

### Mức khái niệm (Conceptual Level / Logical Level)
- Là góc nhìn tổng thể của toàn bộ CSDL. Tầng này mô tả CSDL chứa **những dữ liệu gì** và **mối quan hệ** giữa chúng ra sao.
- Do Quản trị viên CSDL (DBA) thiết kế bằng mô hình thực thể liên kết (ER) hoặc lược đồ quan hệ.

### Mức nội tại (Internal Level / Physical Level)
- Mô tả cách thức dữ liệu **thực sự được lưu trữ** trên đĩa cứng như thế nào (cấu trúc file, B-Tree index, thuật toán lưu trữ).
- Thuộc về hệ điều hành và DBMS.

## 2. Độc lập dữ liệu (Data Independence)
Nhờ kiến trúc 3 tầng này, hệ thống đạt được tính "Độc lập dữ liệu" - mục tiêu tối thượng của CSDL:
- **Độc lập vật lý:** Thay đổi cách lưu trữ ở tầng vật lý (đổi ổ cứng HDD sang SSD, thêm Index) không làm ảnh hưởng đến cấu trúc bảng ở tầng khái niệm hay các ứng dụng ở tầng ngoài.
- **Độc lập logic:** Việc thêm cột mới, bảng mới ở tầng khái niệm không ảnh hưởng đến các ứng dụng cũ đang chạy ở tầng ngoài.
''',

    'Các mô hình Dữ liệu': '''## 1. Mô hình Dữ liệu là gì?
Mô hình dữ liệu (Data Model) là một tập hợp các công cụ khái niệm dùng để mô tả dữ liệu, mối quan hệ giữa các dữ liệu, ngữ nghĩa dữ liệu và các ràng buộc toàn vẹn.

## 2. Các mô hình dữ liệu lịch sử và hiện tại

### A. Mô hình Phân cấp (Hierarchical Model)
- Dữ liệu được tổ chức theo cấu trúc hình cây (Tree-like structure).
- Mỗi bản ghi con chỉ có đúng **một** bản ghi cha (mối quan hệ 1-N).
- *Ưu điểm:* Truy xuất nhanh theo đường dẫn từ gốc.
- *Nhược điểm:* Cứng nhắc, không biểu diễn được mối quan hệ N-N.

### B. Mô hình Mạng (Network Model)
- Cải tiến từ mô hình phân cấp. Dữ liệu được tổ chức dưới dạng đồ thị (Graph).
- Một bản ghi con có thể có **nhiều** bản ghi cha.
- Khắc phục được nhược điểm của mô hình phân cấp nhưng cực kỳ phức tạp trong việc truy vấn và bảo trì.

### C. Mô hình Quan hệ (Relational Model)
- Là mô hình phổ biến nhất thế giới hiện nay (dùng trong MySQL, SQL Server, Oracle).
- Dữ liệu được biểu diễn dưới dạng các **Bảng (Table) 2 chiều** (gồm cột và hàng).
- Các bảng liên kết với nhau thông qua các **Khóa (Key)**.
- Rất dễ hiểu, tính toán học chặt chẽ và thao tác thông qua ngôn ngữ SQL.

### D. Mô hình Hướng đối tượng (Object-Oriented Model)
- Lưu trữ dữ liệu dưới dạng các Object (giống như trong lập trình OOP).
- Bao gồm cả dữ liệu (thuộc tính) và phương thức (hành vi).

### E. Mô hình NoSQL (Non-Relational)
- Ra đời để xử lý Big Data, dữ liệu phi cấu trúc.
- Bao gồm các dạng: Document (MongoDB), Key-Value (Redis), Column-family (Cassandra), Graph (Neo4j).
''',

    'Mô hình ER: Thực thể và Thuộc tính': '''## 1. Mô hình Thực thể - Liên kết (ER Model) là gì?
Mô hình ER (Entity-Relationship) là một công cụ thiết kế ở mức khái niệm. Nó giúp chúng ta chuyển đổi từ "yêu cầu bài toán thực tế" thành một sơ đồ trực quan (ER Diagram - ERD) trước khi tạo bảng trong CSDL.

## 2. Thực thể (Entity)
- **Thực thể:** Là một đối tượng, sự vật hoặc khái niệm tồn tại độc lập trong thế giới thực mà chúng ta muốn lưu trữ thông tin về nó. 
- *Ví dụ:* SINH VIÊN, MÔN HỌC, NHÂN VIÊN.
- **Ký hiệu trong ERD:** Hình chữ nhật.
- **Thực thể yếu (Weak Entity):** Là thực thể không có đủ thuộc tính để tự làm khóa định danh, sự tồn tại của nó phụ thuộc vào một thực thể khác (thực thể mạnh). *Ký hiệu: Hình chữ nhật nét đôi.*

## 3. Thuộc tính (Attribute)
- Là các đặc trưng, tính chất dùng để mô tả cho một thực thể.
- *Ví dụ:* Thực thể SINH VIÊN có các thuộc tính: MSSV, Họ tên, Ngày sinh.
- **Ký hiệu trong ERD:** Hình Elip.

### Phân loại Thuộc tính:
1. **Thuộc tính Đơn (Simple):** Không thể chia nhỏ được nữa (ví dụ: Giới tính).
2. **Thuộc tính Phức hợp (Composite):** Có thể chia nhỏ (ví dụ: "Địa chỉ" gồm Số nhà, Đường, Quận, Tỉnh).
3. **Thuộc tính Đa trị (Multivalued):** Một thực thể có thể có nhiều giá trị cho thuộc tính này (ví dụ: Số điện thoại - một người có 2 số ĐT). *Ký hiệu: Elip nét đôi.*
4. **Thuộc tính Dẫn xuất (Derived):** Có thể suy ra từ thuộc tính khác (ví dụ: Tuổi suy ra từ Ngày sinh). *Ký hiệu: Elip nét đứt.*
5. **Thuộc tính Khóa (Key Attribute):** Thuộc tính định danh duy nhất mỗi thực thể. *Ký hiệu: Elip có tên gạch dưới.*
''',

    'Mô hình ER: Mối Quan hệ': '''## 1. Mối Quan hệ (Relationship)
- Thể hiện sự liên kết, tương tác giữa hai hay nhiều thực thể với nhau.
- *Ví dụ:* Sinh viên **ĐĂNG KÝ** Môn học; Nhân viên **LÀM VIỆC** cho Phòng ban.
- **Ký hiệu trong ERD:** Hình thoi.

## 2. Bậc của mối quan hệ (Degree)
- **Bậc 1 (Unary/Recursive):** Một thực thể liên kết với chính nó (VD: Nhân viên "Quản lý" Nhân viên khác).
- **Bậc 2 (Binary):** Hai thực thể liên kết với nhau (Phổ biến nhất).
- **Bậc 3 (Ternary):** Ba thực thể liên kết với nhau.

## 3. Tỉ lệ lực lượng (Cardinality Ratio)
Đây là khái niệm quan trọng nhất để thiết kế CSDL chuẩn, chỉ ra số lượng bản thể của thực thể này liên kết với bản thể của thực thể kia.

- **Một - Một (1:1):** 1 thực thể A liên kết với đúng 1 thực thể B và ngược lại. *(VD: 1 Trưởng phòng quản lý đúng 1 Phòng ban).*
- **Một - Nhiều (1:N):** 1 thực thể A liên kết với nhiều thực thể B. Nhưng 1 B chỉ thuộc về 1 A. *(VD: 1 Khoa có nhiều Sinh viên).*
- **Nhiều - Nhiều (M:N):** Nhiều A liên kết nhiều B. *(VD: Sinh viên đăng ký nhiều Môn học, Môn học có nhiều Sinh viên).*

## 4. Ràng buộc tham gia (Participation Constraint)
- **Toàn phần (Total / Bắt buộc):** Mọi bản thể của thực thể PHẢI tham gia vào mối quan hệ. *Ký hiệu: Đường nối nét đôi.* (VD: Mọi Nhân viên bắt buộc phải thuộc một Phòng ban).
- **Bán phần (Partial / Tùy chọn):** Không bắt buộc tất cả phải tham gia. *Ký hiệu: Đường nối nét đơn.*
''',

    'Thực hành vẽ ER Diagram': '''## 1. Các bước vẽ sơ đồ ER (ERD) từ bài toán thực tế
Để thiết kế một hệ thống từ con số 0, hãy làm theo quy trình sau:

1. **Đọc kỹ yêu cầu bài toán:** Gạch dưới các danh từ (thường là Thực thể hoặc Thuộc tính) và động từ (Mối quan hệ).
2. **Xác định các Thực thể (Entity):** Gom nhóm các đối tượng chính.
3. **Xác định các Thuộc tính (Attribute):** Gán các đặc điểm cho từng thực thể.
4. **Xác định Khóa (Key):** Chọn thuộc tính định danh duy nhất cho mỗi thực thể.
5. **Xác định Mối quan hệ (Relationship):** Vẽ hình thoi nối các thực thể lại với nhau.
6. **Xác định Bản số (Cardinality):** Điền tỉ lệ 1:1, 1:N hoặc M:N lên các nhánh của mối quan hệ.

## 2. Ví dụ: Bài toán Quản lý Bán hàng
**Yêu cầu:** Một cửa hàng cần quản lý thông tin KHÁCH HÀNG (Mã KH, Tên, SĐT đa trị). Khách hàng tạo các HÓA ĐƠN (Mã HĐ, Ngày lập). Mỗi hóa đơn mua nhiều SẢN PHẨM (Mã SP, Tên SP, Đơn giá), một sản phẩm có thể nằm trong nhiều hóa đơn.

**Phân tích:**
- **Thực thể:** KHÁCH HÀNG, HÓA ĐƠN, SẢN PHẨM.
- **Khóa:** Mã KH, Mã HĐ, Mã SP.
- **Thuộc tính đa trị:** SĐT của Khách hàng.
- **Mối quan hệ:**
  - KHÁCH HÀNG - (Tạo) - HÓA ĐƠN: Quan hệ **1:N** (1 KH tạo nhiều HĐ, 1 HĐ thuộc về 1 KH).
  - HÓA ĐƠN - (Bao gồm) - SẢN PHẨM: Quan hệ **M:N** (1 HĐ có nhiều SP, 1 SP nằm trong nhiều HĐ). Mối quan hệ này sẽ có thêm thuộc tính "Số lượng mua".

*(Mời bạn xem hình ảnh ERD minh họa chi tiết trong tài liệu PDF đính kèm bên dưới).*
''',

    'Lược đồ Quan hệ': '''## 1. Mô hình Quan hệ (Relational Model)
Được E.F. Codd đề xuất năm 1970, đây là mô hình toán học nền tảng cho mọi CSDL quan hệ hiện nay (MySQL, SQL Server). Dữ liệu được tổ chức thành các **Quan hệ (Relation)**, thường được gọi dân dã là các **Bảng (Table)**.

## 2. Các thuật ngữ cơ bản (Thuật ngữ lý thuyết vs Thực tế)

- **Quan hệ (Relation):** Tương đương với **Bảng (Table)**.
- **Bộ (Tuple):** Tương đương với **Hàng (Row) / Bản ghi (Record)**. Mỗi bộ chứa dữ liệu của một đối tượng cụ thể.
- **Thuộc tính (Attribute):** Tương đương với **Cột (Column) / Trường (Field)**.
- **Lực lượng (Cardinality):** Số lượng bộ (hàng) trong quan hệ.
- **Bậc (Degree):** Số lượng thuộc tính (cột) trong quan hệ.

## 3. Lược đồ Quan hệ (Relational Schema)
Lược đồ quan hệ mô tả cấu trúc của một quan hệ, bao gồm tên quan hệ và danh sách các thuộc tính của nó.

**Cú pháp:** `TEN_QUAN_HE (ThuocTinh1, ThuocTinh2, ..., ThuocTinhN)`

**Ví dụ:**
- `SINH_VIEN (MSSV, HoTen, NgaySinh, MaKhoa)`
- `KHOA (MaKhoa, TenKhoa, NamThanhLap)`

*Trong biểu diễn lược đồ, thuộc tính Khóa chính sẽ được gạch chân.*

## 4. Miền giá trị (Domain)
- Là tập hợp các giá trị hợp lệ mà một thuộc tính có thể nhận.
- *Ví dụ:* Domain của thuộc tính "Giới tính" là {Nam, Nữ}. Domain của "Điểm" là các số thực từ 0.0 đến 10.0. Mọi giá trị trong CSDL phải nằm trong Domain quy định.
''',

    'Khóa và Ràng buộc Toàn vẹn': '''## 1. Các loại Khóa (Keys)
Khóa là một khái niệm cốt lõi giúp phân biệt các hàng dữ liệu và thiết lập liên kết giữa các bảng.

- **Siêu khóa (Superkey):** Là một thuộc tính hoặc tập hợp các thuộc tính có thể xác định duy nhất một bộ (hàng) trong bảng. (Ví dụ: {MSSV}, {MSSV, HoTen} đều là siêu khóa).
- **Khóa ứng cử (Candidate Key):** Là siêu khóa "nhỏ nhất" (không chứa thuộc tính dư thừa). (Ví dụ: {MSSV} hoặc {SoCCCD}).
- **Khóa chính (Primary Key - PK):** Được chọn ra từ các khóa ứng cử để làm định danh chính cho bảng. Khóa chính **không được phép rỗng (NOT NULL)** và **phải duy nhất (UNIQUE)**. Thường được gạch chân trong lược đồ.
- **Khóa ngoại (Foreign Key - FK):** Là một thuộc tính (hoặc tập thuộc tính) trong bảng này nhưng tham chiếu đến Khóa chính của một bảng khác. Nó tạo ra "Mối quan hệ" giữa 2 bảng.

## 2. Ràng buộc toàn vẹn (Integrity Constraints)
Đây là các quy tắc mà dữ liệu phải tuân thủ để đảm bảo CSDL luôn chính xác và hợp lệ.

1. **Ràng buộc miền giá trị (Domain Constraint):** Dữ liệu phải đúng kiểu, đúng định dạng (VD: Điểm phải từ 0-10).
2. **Ràng buộc toàn vẹn thực thể (Entity Integrity):** Không có thuộc tính nào tham gia vào Khóa chính (PK) được phép mang giá trị NULL.
3. **Ràng buộc toàn vẹn tham chiếu (Referential Integrity):** Giá trị của Khóa ngoại (FK) phải khớp với một giá trị Khóa chính hiện có ở bảng được tham chiếu, hoặc phải là NULL. (Không được tồn tại "chìa khóa" mở một "ổ khóa" không có thật).
''',

    'Đại số Quan hệ': '''## 1. Đại số Quan hệ là gì?
Đại số quan hệ (Relational Algebra) là một ngôn ngữ lý thuyết (mang tính thủ tục) bao gồm một tập các phép toán để truy vấn dữ liệu từ các quan hệ (bảng). Nó chính là nền tảng toán học đằng sau ngôn ngữ SQL mà bạn hay gõ.

## 2. Các phép toán cơ bản

### A. Phép Chọn (Selection - Ký hiệu: $\sigma$)
- Lọc ra các **hàng (bộ)** thỏa mãn một điều kiện nhất định.
- *Tương đương trong SQL:* Mệnh đề `WHERE`.
- *Ví dụ:* $\sigma_{Diem > 8}(SINH\_VIEN)$ (Chọn các sinh viên có điểm > 8).

### B. Phép Chiếu (Projection - Ký hiệu: $\pi$)
- Lọc ra các **cột (thuộc tính)** cụ thể và loại bỏ các cột không cần thiết. Kết quả tự động loại bỏ các hàng trùng lặp.
- *Tương đương trong SQL:* Mệnh đề `SELECT`.
- *Ví dụ:* $\pi_{HoTen, NgaySinh}(SINH\_VIEN)$ (Chỉ lấy cột Họ tên và Ngày sinh).

### C. Phép Tích Đề-các (Cartesian Product - Ký hiệu: $\times$)
- Ghép mọi hàng của bảng A với mọi hàng của bảng B.
- Nếu A có 3 hàng, B có 4 hàng $\rightarrow$ Kết quả có 12 hàng. Tương đương `CROSS JOIN`.

### D. Phép Hợp ($\cup$), Giao ($\cap$), Trừ ($-$)
- Thao tác trên tập hợp tương tự toán học. Yêu cầu 2 bảng phải khả hợp (cùng số lượng cột và cùng kiểu dữ liệu).

## 3. Các phép toán mở rộng (Kết nối - JOIN)

- **Kết nối Theta ($\bowtie_\theta$):** Ghép 2 bảng dựa trên một điều kiện $\theta$ bất kỳ.
- **Kết nối Tự nhiên (Natural Join - Ký hiệu: $\bowtie$):** Tự động ghép 2 bảng dựa trên các cột có **cùng tên**. Cột trùng lặp sẽ bị gộp làm 1. Đây là phép toán rất mạnh mẽ giúp liên kết dữ liệu PK-FK.
''',

    'SQL DDL: Tạo và Quản lý Bảng': '''## 1. Ngôn ngữ Định nghĩa Dữ liệu (DDL - Data Definition Language)
DDL là một tập hợp các lệnh SQL dùng để tạo, sửa đổi và xóa bỏ các cấu trúc đối tượng trong CSDL (như Database, Table, Index, View). Các lệnh DDL tương tác trực tiếp với kiến trúc CSDL chứ không đụng chạm đến dữ liệu bên trong hàng/cột.

## 2. Các lệnh DDL cơ bản

### A. Tạo bảng (`CREATE TABLE`)
Dùng để tạo bảng mới, định nghĩa các cột, kiểu dữ liệu và các ràng buộc.
```sql
CREATE TABLE SinhVien (
    MSSV CHAR(8) PRIMARY KEY,
    HoTen VARCHAR(50) NOT NULL,
    NgaySinh DATE,
    Diem FLOAT CHECK (Diem >= 0 AND Diem <= 10),
    MaKhoa INT,
    FOREIGN KEY (MaKhoa) REFERENCES Khoa(MaKhoa)
);
```

### B. Sửa đổi cấu trúc bảng (`ALTER TABLE`)
Dùng khi bạn muốn thêm, xóa cột, hoặc đổi tên cột của một bảng đã tồn tại.
- **Thêm cột:** `ALTER TABLE SinhVien ADD Email VARCHAR(100);`
- **Sửa kiểu dữ liệu:** `ALTER TABLE SinhVien MODIFY HoTen VARCHAR(100);`
- **Xóa cột:** `ALTER TABLE SinhVien DROP COLUMN Email;`

### C. Xóa bảng (`DROP TABLE`)
Xóa hoàn toàn bảng và toàn bộ dữ liệu bên trong khỏi hệ thống (Không thể Rollback).
```sql
DROP TABLE SinhVien;
```

### D. Cắt xén bảng (`TRUNCATE TABLE`)
Xóa toàn bộ dữ liệu trong bảng một cách cực kỳ nhanh chóng nhưng vẫn giữ lại cấu trúc bảng. Nhanh hơn `DELETE` rất nhiều và cũng không thể Rollback.
```sql
TRUNCATE TABLE SinhVien;
```
''',

    'SQL DML: Thêm Sửa Xóa Dữ liệu': '''## 1. Ngôn ngữ Thao tác Dữ liệu (DML - Data Manipulation Language)
DML là nhóm lệnh SQL phổ biến nhất mà các lập trình viên sử dụng hàng ngày. Nó thao tác trực tiếp trên các bản ghi (row) bên trong bảng.

## 2. Thêm dữ liệu (`INSERT INTO`)
Dùng để thêm một hoặc nhiều hàng dữ liệu mới vào bảng.

**Cách 1: Chỉ định rõ các cột (Khuyên dùng)**
```sql
INSERT INTO SinhVien (MSSV, HoTen, MaKhoa) 
VALUES ('SV001', 'Nguyễn Văn A', 1);
```
**Cách 2: Thêm nhiều hàng cùng lúc**
```sql
INSERT INTO SinhVien (MSSV, HoTen) VALUES 
('SV002', 'Trần Thị B'), 
('SV003', 'Lê Văn C');
```

## 3. Cập nhật dữ liệu (`UPDATE`)
Dùng để sửa đổi giá trị dữ liệu hiện có. 
> ⚠️ **CẢNH BÁO NGUY HIỂM:** Luôn nhớ phải có mệnh đề `WHERE` khi chạy lệnh UPDATE. Nếu quên `WHERE`, toàn bộ bảng sẽ bị cập nhật đổi thành dữ liệu giống hệt nhau!

```sql
-- Chỉ cập nhật sinh viên có MSSV = 'SV001'
UPDATE SinhVien 
SET HoTen = 'Nguyễn Văn Anh', Diem = 9.5 
WHERE MSSV = 'SV001';
```

## 4. Xóa dữ liệu (`DELETE`)
Dùng để xóa một hoặc nhiều hàng thỏa mãn điều kiện.
> ⚠️ Tương tự UPDATE, không có `WHERE` sẽ xóa trắng bảng!

```sql
-- Đuổi học sinh viên nợ môn quá nhiều
DELETE FROM SinhVien WHERE Diem < 2.0;
```
*(Lưu ý: Nếu bảng bị ràng buộc Khóa ngoại, bạn có thể không xóa được nếu dữ liệu đang được bảng khác tham chiếu đến).*
''',

    'SQL DQL: Truy vấn Dữ liệu': '''## 1. Ngôn ngữ Truy vấn Dữ liệu (DQL - Data Query Language)
DQL thực chất chỉ bao gồm một lệnh duy nhất nhưng mạnh mẽ nhất trong SQL: `SELECT`. Lệnh này giúp bạn trích xuất dữ liệu từ CSDL ra để xem mà không làm thay đổi dữ liệu gốc.

## 2. Cấu trúc chuẩn của một lệnh SELECT
Một câu truy vấn hoàn chỉnh sẽ đi theo thứ tự các mệnh đề như sau (Đây cũng là thứ tự viết code):

```sql
SELECT cột_hiển_thị
FROM tên_bảng
WHERE điều_kiện_lọc_hàng
GROUP BY cột_cần_nhóm
HAVING điều_kiện_lọc_nhóm
ORDER BY cột_cần_sắp_xếp [ASC|DESC]
LIMIT số_lượng_dòng_giới_hạn;
```

## 3. Các thành phần cơ bản

### Mệnh đề SELECT & FROM
- `SELECT * FROM SinhVien;` (Lấy tất cả các cột)
- `SELECT HoTen, Diem FROM SinhVien;` (Chỉ lấy cột Họ tên và Điểm)
- Sử dụng `DISTINCT` để loại bỏ các hàng trùng lặp: `SELECT DISTINCT MaKhoa FROM SinhVien;`

### Mệnh đề WHERE (Lọc dữ liệu)
- Hỗ trợ các phép toán: `=`, `>`, `<`, `>=`, `<=`, `<>` hoặc `!=`
- Hỗ trợ các toán tử logic: `AND`, `OR`, `NOT`
- **Toán tử IN:** `WHERE MaKhoa IN (1, 3, 5)`
- **Toán tử BETWEEN:** `WHERE Diem BETWEEN 5 AND 8` (Lấy từ 5 đến 8)
- **Toán tử LIKE (Tìm kiếm chuỗi):** 
  - `%` đại diện cho 0 hoặc nhiều ký tự. 
  - `_` đại diện cho 1 ký tự.
  - `WHERE HoTen LIKE 'Nguyễn%'` (Tìm người họ Nguyễn).

### Mệnh đề ORDER BY (Sắp xếp)
- `ASC` (Tăng dần - Mặc định).
- `DESC` (Giảm dần).
- `ORDER BY Diem DESC, HoTen ASC` (Xếp điểm giảm dần, nếu điểm bằng nhau xếp tên theo ABC).
''',

    'Hàm Tổng hợp trong SQL': '''## 1. Hàm Tổng hợp (Aggregate Functions) là gì?
Hàm tổng hợp là các hàm tính toán trên một tập hợp các giá trị (nhiều hàng) và trả về một giá trị duy nhất. Chúng thường được dùng để thống kê dữ liệu.

Các hàm phổ biến nhất:
- `COUNT(*)`: Đếm tổng số hàng (kể cả hàng chứa NULL).
- `COUNT(cột)`: Đếm số lượng giá trị KHÔNG NULL của cột đó.
- `SUM(cột)`: Tính tổng các giá trị (chỉ dùng cho số).
- `AVG(cột)`: Tính trung bình cộng (chỉ dùng cho số).
- `MAX(cột)` / `MIN(cột)`: Tìm giá trị lớn nhất / nhỏ nhất.

**Ví dụ cơ bản:**
```sql
SELECT COUNT(*) AS TongSoSV, AVG(Diem) AS DiemTrungBinh 
FROM SinhVien;
```

## 2. Mệnh đề GROUP BY (Nhóm dữ liệu)
GROUP BY dùng để chia các bản ghi thành các nhóm dựa trên giá trị của một hoặc nhiều cột. Sau khi nhóm, các hàm tổng hợp sẽ được tính TOÁN RIÊNG CHO TỪNG NHÓM (thay vì toàn bảng).

**Ví dụ:** Tìm điểm trung bình của từng Khoa:
```sql
SELECT MaKhoa, AVG(Diem) AS DiemTrungBinh
FROM SinhVien
GROUP BY MaKhoa;
```
> ⚠️ **Quy tắc vàng:** Bất kỳ cột nào nằm trên dòng `SELECT` mà KHÔNG nằm trong hàm tổng hợp, thì BẮT BUỘC phải có mặt trong `GROUP BY`.

## 3. Mệnh đề HAVING (Lọc dữ liệu sau khi nhóm)
Không thể dùng `WHERE` để lọc kết quả của hàm tổng hợp (VD: Lọc các khoa có Điểm TB > 5). `WHERE` chỉ lọc từng hàng TRƯỚC khi nhóm. Để lọc SAU khi nhóm, ta dùng `HAVING`.

```sql
SELECT MaKhoa, AVG(Diem) AS DiemTrungBinh
FROM SinhVien
GROUP BY MaKhoa
HAVING AVG(Diem) > 5.0;
```
''',

    'SQL JOIN: Kết nối Bảng': '''## 1. Tại sao phải JOIN (Kết nối)?
Trong CSDL quan hệ, để tránh dư thừa, dữ liệu được chia nhỏ ra nhiều bảng (Ví dụ: Bảng SINHVIEN chứa mã khoa, bảng KHOA chứa tên khoa). Để lấy được "Tên sinh viên" và "Tên khoa" trên cùng một báo cáo, ta phải KẾT NỐI (JOIN) hai bảng này lại với nhau thông qua khóa chính và khóa ngoại.

## 2. Các loại JOIN phổ biến

### A. INNER JOIN (Giao nhau)
- Chỉ trả về các hàng có sự trùng khớp ở CẢ HAI bảng. Nếu một sinh viên chưa có khoa, hoặc một khoa không có sinh viên, các dòng đó sẽ bị loại bỏ.
- *Đây là loại JOIN mặc định và dùng nhiều nhất.*
```sql
SELECT SV.HoTen, K.TenKhoa
FROM SinhVien SV
INNER JOIN Khoa K ON SV.MaKhoa = K.MaKhoa;
```

### B. LEFT JOIN (Lấy hết bên trái)
- Trả về TẤT CẢ các hàng từ bảng bên trái (SinhVien), cộng với dữ liệu khớp từ bảng bên phải (Khoa). 
- Nếu bảng bên phải không có dữ liệu khớp, các cột của bảng phải sẽ trả về `NULL`.
```sql
SELECT SV.HoTen, K.TenKhoa
FROM SinhVien SV
LEFT JOIN Khoa K ON SV.MaKhoa = K.MaKhoa;
-- Kết quả sẽ có cả các sinh viên chưa được phân khoa (TenKhoa = NULL)
```

### C. RIGHT JOIN (Lấy hết bên phải)
- Ngược lại với LEFT JOIN. Trả về toàn bộ dữ liệu bảng bên phải (Khoa), bên trái không có thì để NULL.

### D. FULL OUTER JOIN (Lấy tất cả)
- Kết hợp cả LEFT và RIGHT JOIN. Trả về tất cả các hàng từ cả hai bảng. (Lưu ý: MySQL không hỗ trợ từ khóa này trực tiếp, phải dùng UNION nối LEFT và RIGHT join).

### E. CROSS JOIN (Tích Đề-các)
- Ghép mỗi hàng của bảng A với mọi hàng của bảng B. Rất nguy hiểm vì tạo ra khối lượng dữ liệu khổng lồ (A * B hàng).
''',

    'Subquery và CTE': '''## 1. Truy vấn con (Subquery)
Subquery là một câu lệnh SELECT được lồng bên trong một câu lệnh SELECT, INSERT, UPDATE, hoặc DELETE khác. Nó dùng để lấy dữ liệu làm điều kiện cho câu lệnh cha.

### A. Subquery trong WHERE (Lọc dữ liệu)
- Lấy sinh viên có điểm lớn hơn điểm trung bình của toàn trường:
```sql
SELECT HoTen, Diem FROM SinhVien
WHERE Diem > (SELECT AVG(Diem) FROM SinhVien);
```

### B. Toán tử IN và EXISTS với Subquery
- `IN`: So sánh một giá trị với một danh sách trả về từ subquery.
- `EXISTS`: Trả về TRUE nếu subquery trả về ít nhất 1 hàng. Thường chạy nhanh hơn IN khi dữ liệu lớn vì nó dừng tìm kiếm ngay khi tìm thấy dòng đầu tiên.
```sql
-- Tìm các khoa CÓ sinh viên
SELECT TenKhoa FROM Khoa K
WHERE EXISTS (SELECT 1 FROM SinhVien SV WHERE SV.MaKhoa = K.MaKhoa);
```

### C. Subquery trong FROM (Bảng dẫn xuất / Derived Table)
- Lấy một kết quả SELECT làm một "bảng tạm" để SELECT tiếp.
```sql
SELECT T.HoTen FROM (SELECT * FROM SinhVien WHERE Diem > 8) AS T;
```

## 2. CTE (Common Table Expression) - Mệnh đề WITH
CTE là phiên bản "sang chảnh", dễ đọc hơn của Subquery. Nó cho phép bạn định nghĩa một bảng tạm thời có tên ở đầu câu lệnh và sử dụng nó bên dưới.
Điều này giúp code SQL gọn gàng, có cấu trúc và dễ bảo trì hơn rất nhiều so với subquery lồng nhau chằng chịt.

```sql
WITH SinhVienGioi AS (
    SELECT MSSV, HoTen, MaKhoa FROM SinhVien WHERE Diem >= 8.0
)
SELECT S.HoTen, K.TenKhoa 
FROM SinhVienGioi S
JOIN Khoa K ON S.MaKhoa = K.MaKhoa;
```
''',

    'Phụ thuộc Hàm': '''## 1. Khái niệm Phụ thuộc Hàm (Functional Dependency - FD)
Phụ thuộc hàm là khái niệm toán học quan trọng nhất dùng để Chuẩn hóa CSDL. 
Ta nói thuộc tính **Y phụ thuộc hàm vào thuộc tính X** (Ký hiệu: $X \\rightarrow Y$) nếu: 
*Với mọi cặp bản ghi bất kỳ, nếu chúng có cùng giá trị X thì BẮT BUỘC phải có cùng giá trị Y.*

- **X** được gọi là vế trái (Determinant - Yếu tố quyết định).
- **Y** được gọi là vế phải (Dependent).
- *Ví dụ:* $MSSV \\rightarrow HoTen$ (Nếu biết MSSV là "SV01", ta chắc chắn biết duy nhất 1 họ tên là "Nguyễn A". Không thể có 2 người cùng MSSV mà khác tên).
- *Ví dụ sai:* $HoTen \\rightarrow MSSV$ (Sai vì 2 người có thể trùng tên "Nguyễn A" nhưng MSSV khác nhau).

## 2. Phân loại Phụ thuộc Hàm

### A. Phụ thuộc hàm Hiển nhiên (Trivial FD)
X $\\rightarrow$ Y được gọi là hiển nhiên nếu Y là một tập con của X.
*Ví dụ:* {MSSV, HoTen} $\\rightarrow$ {MSSV}. (Điều này luôn luôn đúng về mặt toán học, không mang lại giá trị thực tế).

### B. Phụ thuộc hàm Bộ phận (Partial FD)
Xảy ra khi khóa chính có NHIỀU thuộc tính (ví dụ khóa PK là tập {A, B}), nhưng thuộc tính C chỉ phụ thuộc vào một phần của khóa (chỉ phụ thuộc vào A, không cần B).
*Ví dụ:* PK là {MaSV, MaMonHoc}. Ta có {MaSV} $\\rightarrow$ {TenSV}. Vậy TenSV phụ thuộc bộ phận vào Khóa. **(Gây lỗi dư thừa 2NF).**

### C. Phụ thuộc hàm Đầy đủ (Full FD)
Y phụ thuộc đầy đủ vào X nếu Y phụ thuộc X, và không phụ thuộc vào bất kỳ tập con nào của X.

### D. Phụ thuộc hàm Bắc cầu (Transitive FD)
X $\\rightarrow$ Y và Y $\\rightarrow$ Z (Trong đó Y không phải là khóa dự tuyển). Vậy suy ra X $\\rightarrow$ Z là phụ thuộc bắc cầu.
*Ví dụ:* MSSV $\\rightarrow$ MaKhoa, MaKhoa $\\rightarrow$ TenKhoa. Do đó MSSV $\\rightarrow$ TenKhoa thông qua MaKhoa. **(Gây lỗi dư thừa 3NF).**
''',

    'Chuẩn hóa 1NF và 2NF': '''## 1. Chuẩn hóa CSDL (Normalization) là gì?
Là quá trình phân rã một bảng (relation) lớn chứa nhiều dị thường dữ liệu thành các bảng nhỏ hơn và liên kết chúng lại nhằm:
- Loại bỏ sự dư thừa dữ liệu (Data Redundancy).
- Tránh các dị thường (Anomaly) khi Thêm, Sửa, Xóa dữ liệu.

## 2. Dạng chuẩn 1 (1NF - First Normal Form)
Một bảng đạt 1NF nếu nó thỏa mãn các quy tắc:
1. **Giá trị nguyên tử (Atomic):** Mỗi ô (intersection của cột và hàng) chỉ được chứa một giá trị duy nhất, không được chứa danh sách hay mảng.
2. **Không có nhóm thuộc tính lặp lại.**

*Ví dụ lỗi 1NF:* Bảng SINHVIEN có cột "Số điện thoại" chứa `090123, 098456`.
*Cách sửa:* Tách cột SĐT ra thành một bảng riêng (MaSV, SDT), mỗi số ĐT làm một hàng.

## 3. Dạng chuẩn 2 (2NF - Second Normal Form)
Một bảng đạt 2NF nếu:
1. Đã đạt 1NF.
2. **Không có phụ thuộc hàm bộ phận:** Mọi thuộc tính không khóa phải phụ thuộc ĐẦY ĐỦ vào khóa chính.

**Dấu hiệu nhận biết lỗi 2NF:** Bảng có Khóa chính gồm NHIỀU cột (Khóa phức hợp).
*Ví dụ lỗi 2NF:* Bảng DIEM_THI (PK={MaSV, MaMonHoc}, Diem, TenMonHoc). Ở đây `TenMonHoc` chỉ phụ thuộc vào `MaMonHoc` (1 phần của khóa). Điều này gây dư thừa tên môn học trên mỗi sinh viên thi môn đó.
*Cách sửa:* Tách thành 2 bảng:
- Bảng MONHOC (MaMonHoc, TenMonHoc)
- Bảng DIEM_THI (MaSV, MaMonHoc, Diem)
''',

    'Chuẩn hóa 3NF và BCNF': '''## 1. Dạng chuẩn 3 (3NF - Third Normal Form)
Một bảng đạt 3NF nếu:
1. Đã đạt 2NF.
2. **Không có phụ thuộc hàm bắc cầu:** Mọi thuộc tính không khóa phải phụ thuộc TRỰC TIẾP vào khóa chính, không được phụ thuộc gián tiếp qua một thuộc tính không khóa khác.

*Ví dụ lỗi 3NF:* Bảng SINHVIEN (MSSV, HoTen, MaKhoa, TenKhoa). 
Khóa chính là `MSSV`. Ta thấy `MSSV -> MaKhoa` và `MaKhoa -> TenKhoa`. Do đó `TenKhoa` phụ thuộc bắc cầu vào `MSSV` qua trung gian là `MaKhoa`. Điều này làm tên khoa bị lặp lại nhiều lần với mỗi sinh viên thuộc khoa đó.

*Cách sửa:* Tách thành 2 bảng:
- Bảng KHOA (MaKhoa, TenKhoa)
- Bảng SINHVIEN (MSSV, HoTen, MaKhoa)

## 2. Dạng chuẩn Boyce-Codd (BCNF)
BCNF là phiên bản "chặt chẽ hơn" của 3NF. Đa số các bảng đạt 3NF đều đạt BCNF. Nhưng 3NF vẫn có lỗ hổng nếu một bảng có **nhiều khóa ứng cử (candidate keys) bị chồng lấp lên nhau**.

Quy tắc BCNF: Một bảng đạt BCNF nếu với MỌI phụ thuộc hàm $X \\rightarrow Y$ tồn tại trong bảng, thì vế trái **X bắt buộc phải là một Siêu khóa (Superkey)**.

Nếu có bất kỳ thuộc tính nào (dù là thuộc tính khóa hay không khóa) bị phụ thuộc vào một thuộc tính KHÔNG PHẢI LÀ KHÓA, bảng đó vi phạm BCNF. 
BCNF xử lý được triệt để các dị thường mà 3NF còn bỏ sót. Trong thực tế thiết kế phần mềm, thông thường thiết kế đạt đến 3NF hoặc BCNF là đã an toàn tuyệt đối.
''',

    'Giao dịch và Thuộc tính ACID': '''## 1. Giao dịch (Transaction) là gì?
Giao dịch là một chuỗi các thao tác trên CSDL (như nhiều lệnh INSERT, UPDATE, DELETE) được thực thi như một **đơn vị công việc logic duy nhất**. 

*Ví dụ kinh điển:* Chuyển 100k từ tài khoản A sang tài khoản B gồm 2 thao tác:
1. Trừ 100k ở tài khoản A (UPDATE A = A - 100)
2. Cộng 100k vào tài khoản B (UPDATE B = B + 100)
Hai thao tác này phải cùng thành công, hoặc cùng thất bại. Không thể có chuyện trừ tiền A rồi cúp điện, B không nhận được tiền!

## 2. Các lệnh điều khiển Giao dịch
- `BEGIN TRANSACTION`: Bắt đầu giao dịch.
- `COMMIT`: Xác nhận lưu vĩnh viễn các thay đổi vào CSDL.
- `ROLLBACK`: Hủy bỏ toàn bộ các thay đổi từ đầu giao dịch, đưa dữ liệu về trạng thái ban đầu.

## 3. Bốn thuộc tính ACID
Để đảm bảo an toàn dữ liệu, một DBMS phải tuân thủ 4 tính chất (ACID):

1. **Atomicity (Tính nguyên tử - All or Nothing):** Một transaction không thể chia nhỏ. Hoặc tất cả lệnh chạy thành công, hoặc không có lệnh nào có hiệu lực.
2. **Consistency (Tính nhất quán):** Sau khi transaction hoàn tất, CSDL phải chuyển từ trạng thái hợp lệ này sang trạng thái hợp lệ khác (tuân thủ mọi ràng buộc khóa ngoại, CHECK...). Tổng tiền A và B trước và sau khi chuyển phải bằng nhau.
3. **Isolation (Tính cô lập):** Các transaction chạy đồng thời không được nhìn thấy dữ liệu "đang sửa dở" của nhau.
4. **Durability (Tính bền vững):** Một khi transaction đã `COMMIT`, dữ liệu phải được lưu vĩnh viễn vào ổ cứng, dù sau đó có bị rút phích cắm điện.
''',

    'Kiểm soát Tương tranh': '''## 1. Vấn đề của Tương tranh (Concurrency)
Hệ thống CSDL thực tế có hàng ngàn user cùng đọc/ghi dữ liệu một lúc (Concurrency). Nếu không kiểm soát tốt (Isolation không chặt), sẽ xảy ra 3 vấn đề nghiêm trọng:

### A. Đọc dữ liệu bẩn (Dirty Read)
Giao dịch T1 đọc dữ liệu đang bị chỉnh sửa bởi T2 nhưng T2 **chưa COMMIT**. Nếu T2 bị lỗi và ROLLBACK, dữ liệu T1 đọc được là dữ liệu "ma" không hề tồn tại.

### B. Đọc không lặp lại (Non-repeatable Read)
Trong cùng một giao dịch T1, đọc cùng 1 hàng 2 lần nhưng ra 2 kết quả khác nhau. (Do ở giữa 2 lần đọc, một giao dịch T2 đã kịp nhảy vào UPDATE/DELETE hàng đó và COMMIT).

### C. Đọc ảo (Phantom Read)
Giao dịch T1 đếm số lượng hàng thỏa điều kiện ra 10 hàng. Giao dịch T2 nhảy vào INSERT một hàng mới. Khi T1 đếm lại thì ra 11 hàng (xuất hiện hàng "bóng ma").

## 2. Các cơ chế kiểm soát (Concurrency Control)
Để ngăn chặn các lỗi trên, DBMS sử dụng các kỹ thuật:

### A. Khóa (Locking)
- **Shared Lock (S-Lock):** Khóa đọc. Nhiều người có thể đọc cùng lúc, nhưng cấm ghi.
- **Exclusive Lock (X-Lock):** Khóa ghi. Đã khóa để ghi thì cấm kẻ khác vào đọc hoặc ghi.
- *Nguy cơ:* Dễ dẫn đến **Deadlock** (Bế tắc) - T1 giữ khóa A chờ khóa B, T2 giữ khóa B chờ khóa A. Chờ nhau mãi mãi.

### B. Mức độ Cô lập (Isolation Levels)
SQL chuẩn định nghĩa 4 mức cô lập từ lỏng lẻo đến nghiêm ngặt:
1. **Read Uncommitted:** Cho phép Dirty Read (Tốc độ nhanh nhất, nguy hiểm nhất).
2. **Read Committed:** Ngăn Dirty Read (Mặc định của SQL Server, PostgreSQL).
3. **Repeatable Read:** Ngăn Dirty Read & Non-repeatable Read (Mặc định của MySQL/InnoDB).
4. **Serializable:** Ngăn chặn mọi lỗi trên, chạy các transaction tuần tự như xếp hàng. (An toàn nhất, nhưng chậm nhất).
'''
}

def update_content():
    with engine.connect() as conn:
        result = conn.execute(text('SELECT id, title, description, content_body FROM learning_items WHERE content_type="document"'))
        items = result.fetchall()
        
        updated_count = 0
        for item in items:
            item_id = item[0]
            title = item[1]
            desc = item[2]
            
            # Lấy nội dung tùy chỉnh nếu có, nếu không thì dùng nội dung mặc định
            custom_content = content_map.get(title)
            
            if custom_content:
                md_content = custom_content
            else:
                # Fallback generator for generic items not explicitly written above
                md_content = f'''## Giới thiệu về {title}

**Mục tiêu bài học:** {desc}

Trong nội dung này, chúng ta sẽ tập trung phân tích các khía cạnh chính của **{title}**. 

### 1. Các khái niệm cốt lõi
- Phần này bao hàm các định nghĩa và thuật ngữ quan trọng.
- Hiểu rõ bản chất giúp bạn dễ dàng áp dụng vào thực tiễn.

### 2. Phân tích chi tiết
Kiến thức này đóng vai trò nền tảng trong Hệ quản trị Cơ sở Dữ liệu. (Nội dung chi tiết được biên soạn trong tài liệu đính kèm bên dưới).

### 3. Tổng kết
- Hệ thống hóa các kiến thức trọng tâm.
- Vận dụng vào việc thiết kế cấu trúc CSDL an toàn, hiệu quả.
'''
            
            conn.execute(
                text('UPDATE learning_items SET content_body = :body WHERE id = :id'),
                {'body': md_content, 'id': item_id}
            )
            updated_count += 1
        
        conn.commit()
        print(f'Thành công! Đã cập nhật nội dung chi tiết cho {updated_count} bài học.')

if __name__ == "__main__":
    update_content()
