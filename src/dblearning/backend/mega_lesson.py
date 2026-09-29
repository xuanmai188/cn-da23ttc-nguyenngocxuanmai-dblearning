# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

content = {
    'SQL JOIN: Kết nối Bảng': '''
# BÀI HỌC TOÀN DIỆN: SQL JOIN - NGHỆ THUẬT KẾT NỐI DỮ LIỆU TỪ A-Z

**Thời lượng ước tính:** 45 phút học tập  
**Mục tiêu bài học:** Nắm vững toàn bộ lý thuyết, cách hoạt động nội tại của hệ quản trị CSDL khi thực thi JOIN, các loại JOIN từ cơ bản đến nâng cao, và kỹ năng tối ưu hóa truy vấn thực chiến.

---

## PHẦN 1: TẠI SAO CHÚNG TA PHẢI DÙNG JOIN?

Trong những ngày đầu làm quen với CSDL, một sai lầm cực kỳ phổ biến của người mới là cố gắng nhét tất cả mọi dữ liệu vào một bảng duy nhất (gọi là Flat Table). Ví dụ: một bảng chứa cả Mã sinh viên, Tên sinh viên, Tên khoa, Tên môn học, Tên giáo viên, v.v.

### 1.1. Thảm họa của bảng "Thập cẩm" (Flat Table)
Hãy tưởng tượng bảng QuanLySinhVien có 10.000 dòng. Khoa "Công nghệ Thông tin" có 3000 sinh viên. Như vậy, chuỗi ký tự "Công nghệ Thông tin" bị lặp đi lặp lại đúng 3000 lần.
- **Tốn ổ cứng:** Bạn đang lãng phí hàng Megabyte chỉ để lưu một chuỗi ký tự trùng lặp.
- **Dị thường cập nhật (Update Anomaly):** Nếu trường đổi tên khoa thành "Công nghệ Số", hệ thống phải quét 10.000 dòng để tìm và sửa 3000 dòng. Nếu máy chủ rớt mạng giữa chừng, bạn sẽ có một nửa sinh viên học khoa cũ, một nửa học khoa mới. Dữ liệu bị rác vĩnh viễn!

### 1.2. Giải pháp của CSDL Quan hệ: Chia để trị (Normalization)
Để giải quyết bài toán trên, Edgar F. Codd (cha đẻ của CSDL Quan hệ) đã đề xuất việc **Chuẩn hóa dữ liệu (Normalization)**. 
Chúng ta băm bảng "Thập cẩm" ra thành các bảng nhỏ gọn:
1. Bảng KHOA: Chỉ lưu MaKhoa và TenKhoa. (Chỉ có 1 dòng cho Khoa CNTT).
2. Bảng SINHVIEN: Lưu MaSV, HoTen, và một khóa ngoại là MaKhoa.

**Vấn đề mới phát sinh:** Bây giờ dữ liệu đã sạch, nhưng khi sếp yêu cầu: *"Hãy in cho tôi danh sách Tên Sinh Viên và Tên Khoa mà họ đang học"*. Bạn không thể chỉ SELECT ở 1 bảng được nữa.
👉 **Giải pháp:** Bạn phải dùng lệnh **JOIN** để may các mảnh ghép (bảng) lại với nhau dựa trên điểm chung là MaKhoa.

---

## PHẦN 2: CÚ PHÁP CỐT LÕI CỦA MỘT LỆNH JOIN

Cấu trúc chuẩn của một câu lệnh JOIN luôn tuân theo công thức sau:

`sql
SELECT Bảng_A.Cột_1, Bảng_B.Cột_2
FROM Bảng_A
[LOẠI JOIN] JOIN Bảng_B 
  ON Bảng_A.Khóa_Ngoại = Bảng_B.Khóa_Chính;
`

**Phân tích cú pháp:**
- FROM Bảng_A: Bảng xuất phát (Bảng Trái - Left Table).
- [LOẠI JOIN]: Từ khóa quyết định cách ghép dữ liệu (INNER, LEFT, RIGHT, FULL, CROSS).
- JOIN Bảng_B: Bảng cần ghép vào (Bảng Phải - Right Table).
- ON ...: Đây là **Điều kiện kết nối (Join Condition)**. Rất quan trọng! Nó nói cho Database biết làm sao để ghép đúng dòng của bảng A với dòng của bảng B. Nếu quên chữ ON, hệ thống sẽ thực hiện Cross Join (nhân chéo toàn bộ) gây sập máy chủ.

---

## PHẦN 3: ĐÀO SÂU CÁC LOẠI JOIN CƠ BẢN

Để minh họa cho các ví dụ bên dưới, chúng ta có 2 bảng giả định:
- Bảng NHANVIEN (MaNV, TenNV, MaPhongBan): Có nhân viên không thuộc phòng nào (MaPhongBan = NULL).
- Bảng PHONGBAN (MaPhongBan, TenPhong): Có phòng ban không có nhân viên nào (Ví dụ: Phòng Nghiên cứu).

### 3.1. INNER JOIN (Giao thoa)
Đây là loại JOIN mặc định. Nếu bạn chỉ gõ chữ JOIN, Database sẽ tự hiểu là INNER JOIN.
- **Logic hoạt động:** Chỉ trả về những dòng mà dữ liệu Khóa khớp nhau ở CẢ HAI BẢNG.
- **Biểu đồ Venn:** Phần giao nhau ở giữa 2 hình tròn.

**Code thực chiến:**
`sql
SELECT NV.TenNV, PB.TenPhong
FROM NHANVIEN NV
INNER JOIN PHONGBAN PB ON NV.MaPhongBan = PB.MaPhongBan;
`
**Phân tích kết quả:** Nhân viên không có phòng ban sẽ bị LOẠI BỎ khỏi báo cáo. Phòng ban không có nhân viên cũng bị LOẠI BỎ. Chỉ những nhân viên đã được phân phòng mới được hiển thị.

### 3.2. LEFT JOIN (Bảo vệ phe Trái)
Đây là lệnh quan trọng thứ 2, cực kỳ hay dùng trong phân tích dữ liệu (Data Analytics).
- **Logic hoạt động:** Trả về TẤT CẢ các dòng của Bảng Trái (sau chữ FROM), cộng với dữ liệu khớp của Bảng Phải. Nếu bảng phải không có dữ liệu khớp, nó sẽ điền giá trị NULL.
- **Biểu đồ Venn:** Toàn bộ hình tròn bên Trái.

**Code thực chiến:**
`sql
SELECT NV.TenNV, PB.TenPhong
FROM NHANVIEN NV
LEFT JOIN PHONGBAN PB ON NV.MaPhongBan = PB.MaPhongBan;
`
**Phân tích kết quả:** Lấy TẤT CẢ nhân viên. Anh nhân viên mới vào (chưa có phòng) vẫn sẽ xuất hiện trên báo cáo, nhưng cột TenPhong của anh ta sẽ hiển thị là NULL. 

### 3.3. RIGHT JOIN (Bảo vệ phe Phải)
Hoàn toàn ngược lại với LEFT JOIN. Giữ nguyên toàn bộ Bảng Phải.
*Thực tế đi làm:* Người ta rất hiếm khi dùng RIGHT JOIN. Vì chỉ cần đảo vị trí 2 bảng trong câu lệnh LEFT JOIN là xong. Để code dễ đọc, các Lập trình viên quy ước chỉ dùng LEFT JOIN.

---

## PHẦN 4: KỸ THUẬT JOIN NÂNG CAO (ADVANCED JOINS)

### 4.1. ANTI-JOIN (Truy vấn kẻ ngoại đạo)
Bạn muốn tìm: *"Liệt kê các Phòng Ban hiện đang không có nhân viên nào"* (Có thể để giải tán phòng đó).
Đây không phải là một từ khóa trong SQL, mà là một thủ thuật sử dụng LEFT JOIN kết hợp với WHERE NULL.

`sql
SELECT PB.TenPhong
FROM PHONGBAN PB
LEFT JOIN NHANVIEN NV ON PB.MaPhongBan = NV.MaPhongBan
WHERE NV.MaNV IS NULL; -- Điều kiện cốt lõi
`
**Giải thích thuật toán:** Đầu tiên, LEFT JOIN lấy toàn bộ Phòng Ban. Những phòng không có nhân viên sẽ bị dán nhãn NULL ở các cột của nhân viên. Sau đó, mệnh đề WHERE NV.MaNV IS NULL sẽ lọc ra chính xác những phòng ban cô đơn đó.

### 4.2. SELF JOIN (Tự kết nối với chính mình)
Dùng khi dữ liệu có tính phân cấp (cây) nằm trong cùng 1 bảng. Ví dụ điển hình: Bảng Nhân viên chứa luôn Mã Người Quản Lý (Mã Sếp).
Làm sao in ra báo cáo: Tên Nhân Viên - Tên Sếp?

`sql
SELECT 
    NV_Thuong.TenNV AS "Tên Nhân Viên", 
    NV_Sep.TenNV AS "Tên Sếp của họ"
FROM NHANVIEN NV_Thuong
LEFT JOIN NHANVIEN NV_Sep 
    ON NV_Thuong.MaNguoiQuanLy = NV_Sep.MaNV;
`
**Giải thích:** Ta giả vờ như có 2 bảng khác nhau bằng cách đặt Alias (bí danh) là NV_Thuong và NV_Sep. Cột MaNguoiQuanLy của bảng thường sẽ móc vào cột MaNV của bảng Sếp. Đỉnh cao của sự linh hoạt!

### 4.3. CROSS JOIN (Tích Đề-các)
Mệnh đề này sẽ ghép MỌI DÒNG của bảng A với MỌI DÒNG của bảng B.
Nếu Bảng A có size N, Bảng B có size M, kết quả trả về N * M dòng.
- **Ứng dụng:** Rất ít dùng trong quản lý dữ liệu thông thường. Thường dùng để tạo dữ liệu giả (Mock data) số lượng lớn, hoặc kết hợp mọi size áo (S, M, L) với mọi màu sắc (Đỏ, Xanh, Vàng) để tạo ra bảng SKU sản phẩm.

---

## PHẦN 5: JOIN NHIỀU BẢNG (MULTI-TABLE JOIN) VÀ THỨ TỰ THỰC THI

Trong các hệ thống thực tế (ERP, CRM), một câu lệnh báo cáo có thể JOIN từ 5 đến 10 bảng. 

`sql
SELECT KH.TenKH, SP.TenSP, CT.SoLuong, CT.GiaBan
FROM KHACHHANG KH
INNER JOIN HOADON HD ON KH.MaKH = HD.MaKH
INNER JOIN CHITIET_HOADON CT ON HD.MaHD = CT.MaHD
INNER JOIN SANPHAM SP ON CT.MaSP = SP.MaSP;
`

**Bí quyết hiểu thứ tự thực thi của Database Engine:**
Cơ sở dữ liệu KHÔNG join 4 bảng cùng một lúc. Nó làm từng bước:
1. Nó lấy bảng KHACHHANG INNER JOIN với bảng HOADON.
2. Tạo ra một "Bảng tạm thời trong RAM" (Chứa dữ liệu khách đã nối với hóa đơn).
3. Lấy "Bảng tạm thời" đó INNER JOIN tiếp với CHITIET_HOADON.
4. Tạo ra "Bảng tạm thời số 2".
5. Lấy "Bảng tạm thời số 2" INNER JOIN với SANPHAM để ra kết quả cuối cùng.

---

## PHẦN 6: BÍ QUYẾT TỐI ƯU HIỆU NĂNG TỪ CÁC CHUYÊN GIA DBA (BEST PRACTICES)

Nếu bạn thiết kế sai, một câu lệnh JOIN có thể làm "sập" hoàn toàn máy chủ cơ sở dữ liệu. Hãy ghi nhớ các nguyên tắc vàng sau:

### Quy tắc 1: Bắt buộc phải có Index trên cột JOIN
Khi dùng ON A.MaKhoa = B.MaKhoa, cột MaKhoa ở cả 2 bảng BẮT BUỘC phải được đánh Chỉ mục (Index). Nếu không, Database phải dùng thuật toán Nested Loop (Vòng lặp lồng nhau), độ phức tạp là O(N * M). Nếu 2 bảng có 1 triệu dòng, nó phải thực hiện 1 nghìn tỷ phép so sánh! Máy chủ sẽ bốc khói.

### Quy tắc 2: Luôn sử dụng Alias (Bí danh)
Đừng bao giờ viết: SELECT TenNV, TenPhong FROM NhanVien JOIN PhongBan....
Nếu ngày mai có người thêm cột TenNV vào bảng PhongBan, câu lệnh SQL của bạn sẽ báo lỗi Ambiguous column name (Cột mơ hồ) khiến toàn bộ app bị sập. Luôn viết rõ NV.TenNV.

### Quy tắc 3: Lọc dữ liệu bằng WHERE trước, hay ON trước?
- Với INNER JOIN: Việc bạn đặt điều kiện lọc (VD: Diem > 8) vào chữ ON hay chữ WHERE thì tốc độ chạy là NHƯ NHAU. Bộ tối ưu (Optimizer) của SQL đủ thông minh để xử lý.
- Với LEFT JOIN: Rất khác biệt! Đặt điều kiện vào ON sẽ quyết định dữ liệu nào được ghép. Đặt vào WHERE sẽ lọc kết quả SAU KHI đã ghép xong. Phải cực kỳ cẩn thận.

---

## TỔNG KẾT BÀI HỌC

Bạn đã trải qua một hành trình rất dài để làm chủ nghệ thuật JOIN trong SQL. Hãy nhớ rằng: 
- Thiết kế CSDL tốt (phân rã bảng) là nền tảng.
- Lệnh JOIN là công cụ để đưa dữ liệu phân tán trở lại thành các báo cáo có ý nghĩa.
- Hãy luôn tự vẽ Biểu đồ Venn trong đầu trước khi gõ lệnh, và luôn tự hỏi *"Điều gì xảy ra nếu có dữ liệu NULL ở đây?"* để chọn đúng INNER hay LEFT JOIN.
'''
}

with engine.connect() as conn:
    for title, body in content.items():
        conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = :title'), {'body': body, 'title': title})
    conn.commit()

print("Mega deep dive lesson applied successfully!")
