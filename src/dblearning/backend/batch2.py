# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

content = {
    'SQL DML: Thêm Sửa Xóa Dữ liệu': '''
## SQL DML - Nghệ thuật "Chọc ngoáy" Dữ liệu

Nếu DDL (Data Definition Language) dùng để XÂY NHÀ (Tạo bảng), thì **DML (Data Manipulation Language)** chính là việc MUA ĐỒ NỘI THẤT (Thêm, Sửa, Xóa dữ liệu) để bỏ vào trong cái nhà đó.
Đây là nhóm lệnh mà Lập trình viên Backend sử dụng 99% thời gian khi làm việc!

---

### 1. Thêm dữ liệu mới (INSERT INTO)

Giống như việc bạn tạo một tài khoản Facebook mới, ứng dụng sẽ chạy một lệnh INSERT dưới nền.

<div class="my-6 bg-slate-900 rounded-xl overflow-hidden shadow-lg">
  <div class="bg-slate-800 px-4 py-2 text-xs text-slate-400 font-mono">Thêm 1 sinh viên mới</div>
  <pre class="m-0 p-4 text-sm font-mono text-green-400"><code>INSERT INTO SinhVien (MSSV, HoTen, Diem) 
VALUES ('SV001', 'Alan Turing', 9.5);</code></pre>
</div>

*Lưu ý:* Phải thêm đúng thứ tự cột, và nếu cột đó là khóa ngoại, giá trị đó phải thực sự tồn tại ở bảng kia.

### 2. Cập nhật dữ liệu (UPDATE)

Giống như việc bạn đổi Avatar hoặc chỉnh sửa Bio trên Tiktok.

<div class="bg-red-50 border border-red-200 p-4 my-6 rounded-lg">
  <h4 class="text-red-800 font-bold mt-0 mb-1">🚨 LỖI CHẾT NGƯỜI (Cần ghi nhớ suốt đời)</h4>
  <p class="text-red-700 text-sm m-0">
    Lệnh UPDATE <strong>luôn luôn phải có mệnh đề <code>WHERE</code> (điều kiện)</strong>. <br/>
    Nếu bạn gõ: <code>UPDATE SinhVien SET Diem = 10;</code> (Không có WHERE) -> Toàn bộ sinh viên trong trường sẽ được 10 điểm! Bạn sẽ bị đuổi việc ngay lập tức.
  </p>
</div>

**Cách viết chuẩn:**
<div class="my-4 bg-slate-900 rounded-xl overflow-hidden shadow-lg">
  <pre class="m-0 p-4 text-sm font-mono text-blue-400"><code>-- Chỉ cập nhật sinh viên có mã là SV001
UPDATE SinhVien 
SET Diem = 10 
WHERE MSSV = 'SV001';</code></pre>
</div>

### 3. Xóa dữ liệu (DELETE)

Chức năng "Hủy kết bạn" hoặc "Xóa bài viết".
- Giống như UPDATE, **DELETE không có WHERE = XÓA TRẮNG BẢNG!**
- *Mẹo nhỏ:* Trong thực tế, các công ty lớn (như Facebook) không bao giờ dùng lệnh DELETE. Thay vào đó, họ thêm 1 cột is_deleted = 1 (gọi là Soft Delete - Xóa mềm) để lỡ có hối hận thì vẫn khôi phục được!
''',

    'SQL JOIN: Kết nối Bảng': '''
## Nghệ thuật "Chắp Vá" dữ liệu bằng JOIN

Một triết lý cốt lõi của CSDL Quan hệ là: **Chia để trị**.
Thay vì nhét mọi thông tin (Tên sinh viên, Tên môn học, Mã giáo viên) vào 1 bảng khổng lồ (rất lag và rác), ta chia ra nhiều bảng nhỏ.
Nhưng khi xếp sếp cần xem một Báo cáo tổng hợp, ta phải ghép các bảng nhỏ đó lại. Quá trình đó gọi là **JOIN**.

<div class="my-6 rounded-xl overflow-hidden shadow-lg border border-gray-200 p-2 bg-white">
  <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&q=80" alt="Data Analytics" class="w-full object-cover h-64 rounded-lg" />
  <div class="bg-white p-2 text-center text-sm text-gray-500 italic">Mọi Dashboard phân tích dữ liệu hoành tráng đều được vận hành bởi các lệnh JOIN phức tạp ở phía sau.</div>
</div>

---

### 1. INNER JOIN (Điểm giao thoa)
Đây là loại JOIN phổ biến nhất (90% thời gian). Nó chỉ lấy những dòng dữ liệu **khớp ở cả 2 bảng**.

*Ví dụ:* Bảng SINHVIEN và bảng KHOA.
- Sinh viên A chưa có Khoa -> Bỏ.
- Khoa "Vật lý hạt nhân" chưa có sinh viên nào đăng ký -> Bỏ.
- Chỉ lấy các Sinh viên có Khóa khớp với Khoa.

<div class="my-4 bg-slate-900 rounded-xl overflow-hidden">
  <pre class="m-0 p-4 text-sm font-mono text-emerald-400"><code>SELECT SV.HoTen, K.TenKhoa
FROM SinhVien SV
INNER JOIN Khoa K ON SV.MaKhoa = K.MaKhoa;</code></pre>
</div>

### 2. LEFT JOIN (Bảo vệ phe Trái)
Giữ lại **TẤT CẢ** dữ liệu của bảng bên Trái (sau chữ FROM), dù nó có tìm thấy đối tác ở bảng bên Phải hay không. Nếu không tìm thấy, bảng bên phải sẽ bị in là NULL.

<div class="bg-blue-50 p-4 my-6 rounded-lg text-sm">
  <strong>🔥 Ứng dụng thực tế:</strong> Bạn làm cho Tiki. Sếp yêu cầu lấy "Danh sách tất cả khách hàng, kèm theo đơn hàng gần nhất của họ".<br/>
  Bạn PHẢI dùng <strong>LEFT JOIN</strong> từ bảng Khách_Hàng sang Đơn_Hàng. Tại sao? Vì có những khách hàng "đăng ký tài khoản nhưng chưa mua gì". Nếu dùng INNER JOIN, những khách hàng đó sẽ bốc hơi khỏi báo cáo của sếp!
</div>

### 3. CROSS JOIN (Thảm họa tích Đề-các)
Ghép mù quáng MỌI DÒNG của bảng A với MỌI DÒNG của bảng B.
- Bảng A có 1000 dòng. Bảng B có 1000 dòng.
- CROSS JOIN sinh ra bảng tạm 1.000.000 dòng (1 Triệu dòng). Đứng máy chủ lập tức! Hãy tránh xa nó!
'''
}

with engine.connect() as conn:
    for title, body in content.items():
        conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = :title'), {'body': body, 'title': title})
    conn.commit()

print("Batch 2 completed!")
