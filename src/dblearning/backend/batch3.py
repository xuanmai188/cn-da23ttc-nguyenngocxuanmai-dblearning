# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

content = {
    'Chuẩn hóa 1NF và 2NF': '''
## Chuẩn hóa CSDL (Normalization) - Nghệ thuật "Dọn dẹp nhà cửa"

Nếu bạn nhét tất cả quần áo, bát đĩa, sách vở vào cùng một cái tủ khổng lồ, khi lấy một chiếc tất, bạn sẽ phải bới tung cả tủ. Hơn nữa, bạn có nguy cơ làm vỡ bát.
Trong CSDL cũng vậy, nếu bạn thiết kế một Bảng (Table) chứa hàng chục cột thập cẩm, bạn sẽ gặp "Thảm họa Dị thường dữ liệu" (Anomaly).
**Chuẩn hóa (Normalization)** là quá trình băm nhỏ cái bảng khổng lồ đó ra thành các bảng nhỏ gọn, logic và liên kết chúng lại bằng Khóa ngoại.

---

### 1. Dạng chuẩn 1 (1NF) - Quy tắc "Giá trị Đơn"

<div class="bg-gray-50 border-l-4 border-gray-400 p-4 my-6">
  <h4 class="text-gray-800 font-bold mt-0 mb-1">Luật 1NF:</h4>
  <p class="text-gray-700 m-0">Mỗi ô trong bảng (Giao của 1 hàng và 1 cột) chỉ được chứa DUY NHẤT 1 GIÁ TRỊ. Không được nhét mảng (Array) hay danh sách (List) vào đó.</p>
</div>

**🚫 Ví dụ Vi phạm 1NF:**
Một bảng `KhachHang` có cột `Số điện thoại` chứa giá trị: `090123, 098456`. (Một ô chứa 2 số điện thoại).
Lỗi: Khi cần tìm khách hàng có số đuôi 456, câu lệnh SQL `WHERE` sẽ chạy cực chậm vì phải quét chuỗi!

**✅ Cách sửa:**
Tách riêng số ĐT ra một bảng khác `DienThoai_KH (Mã KH, Số ĐT)`. Khách hàng đó sẽ có 2 dòng trong bảng mới.

### 2. Dạng chuẩn 2 (2NF) - Quy tắc "Không nịnh nọt kẻ yếu"

Để hiểu 2NF, bạn phải biết về **Khóa chính phức hợp** (Khóa tạo bởi 2 cột trở lên). Ví dụ: Bảng `DiemThi` có khóa chính là `(Mã SV, Mã Môn)`.

<div class="bg-gray-50 border-l-4 border-gray-400 p-4 my-6">
  <h4 class="text-gray-800 font-bold mt-0 mb-1">Luật 2NF:</h4>
  <p class="text-gray-700 m-0">Bảng phải đạt 1NF. Mọi thuộc tính không khóa phải phụ thuộc vào TOÀN BỘ Khóa chính, chứ không được phụ thuộc vào một nửa khóa chính.</p>
</div>

**🚫 Ví dụ Vi phạm 2NF:**
Bảng `DiemThi` gồm các cột: `(Mã SV, Mã Môn, Điểm, Tên Môn)`.
Lỗi: Cột `Tên Môn` chỉ phụ thuộc vào `Mã Môn` (Một nửa của khóa chính), chứ không liên quan gì đến `Mã SV`.
**Hậu quả:** Tên môn "Nhập môn Lập trình" bị lặp lại 1000 lần cho 1000 sinh viên thi môn đó. Lãng phí ổ cứng vô ích!

**✅ Cách sửa:**
Tách chữ `Tên Môn` ra một bảng `MonHoc (Mã Môn, Tên Môn)`. Bảng điểm lúc này chỉ còn `(Mã SV, Mã Môn, Điểm)`. Sạch sẽ!
''',

    'Chuẩn hóa 3NF và BCNF': '''
## Nâng cấp lên Chuẩn hóa 3NF - "Không qua trung gian"

Đạt 2NF là CSDL của bạn đã khá ổn, nhưng vẫn còn một kẽ hở dẫn đến lặp dữ liệu: **Phụ thuộc bắc cầu (Qua trung gian)**.

<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-6">
  <h4 class="text-blue-800 font-bold mt-0 mb-1">Luật 3NF:</h4>
  <p class="text-blue-700 m-0">Bảng phải đạt 2NF. Mọi cột không khóa phải phụ thuộc TRỰC TIẾP vào Khóa chính, tuyệt đối không được thông qua một cột trung gian (A truyền qua B rồi mới tới C).</p>
</div>

**🚫 Ví dụ Vi phạm 3NF:**
Bảng `SinhVien (Mã SV, Họ Tên, Mã Khoa, Tên Khoa)`. 
- Khóa chính là `Mã SV`.
- Ta có: `Mã Khoa` phụ thuộc vào `Mã SV` (Hợp lý).
- NHƯNG: `Tên Khoa` (Vật lý) lại phụ thuộc vào `Mã Khoa` (VL01). 
- Dẫn đến: `Tên Khoa` phụ thuộc gián tiếp (bắc cầu) vào `Mã SV` thông qua `Mã Khoa`.
**Hậu quả:** Chữ "Khoa Vật lý" lại bị lặp lại hàng ngàn lần ở mỗi dòng sinh viên học khoa đó. Khi khoa đổi tên thành "Khoa Vật lý Ứng dụng", bạn phải chạy lệnh UPDATE hàng ngàn dòng (rất dễ xót dữ liệu).

**✅ Cách sửa:** Tách bảng `Khoa (Mã Khoa, Tên Khoa)` riêng biệt. Bảng Sinh viên chỉ giữ lại `Mã Khoa` làm khóa ngoại.

---

## Dạng chuẩn Boyce-Codd (BCNF) - Boss cuối

Thông thường, thiết kế tới 3NF là đã kết thúc dự án. BCNF (đặt theo tên 2 nhà khoa học Raymond Boyce và Edgar Codd) là một dạng "chặt chẽ hơn" của 3NF.

**Quy tắc BCNF:** "Nếu có bất kỳ thuộc tính nào trong bảng quyết định các thuộc tính khác (Vế trái của mũi tên phụ thuộc), thì nó BẮT BUỘC phải là Siêu khóa."

<div class="p-4 bg-yellow-50 rounded-lg text-sm my-6 border border-yellow-200">
  <strong>💡 Tip dành cho người đi làm:</strong> Đa số các bảng 3NF tự động đạt BCNF. BCNF chỉ bị vi phạm trong một trường hợp cực hiếm: Bảng có <strong>Nhiều Khóa ứng cử</strong> và các khóa này bị <strong>Chồng lấp lên nhau</strong>. Trong thực tế đi làm (ví dụ thiết kế app bán hàng), bạn chỉ cần đảm bảo Database đạt chuẩn 3NF là đã loại bỏ được 99.9% rác dữ liệu!
</div>
''',

    'Giao dịch và Thuộc tính ACID': '''
## Giao dịch (Transaction) - Sinh ra để xử lý "Tai nạn"

Bạn đang cầm điện thoại dùng app Momo chuyển 100.000đ cho bạn của bạn. Quá trình này gồm 2 bước trong CSDL:
1. `UPDATE`: Trừ 100k ở tài khoản của bạn.
2. `UPDATE`: Cộng 100k vào tài khoản của bạn kia.

**KỊCH BẢN THẢM HỌA:**
Lệnh 1 chạy xong (bạn bị trừ tiền). Vừa lúc đó... "BỤP!" - Trạm điện bốc cháy, server tắt ngúm. Lệnh 2 chưa kịp chạy.
Hậu quả: Tiền của bạn mất trắng, mà bạn kia thì không nhận được! 

Để giải quyết vấn đề cực kỳ nan giải này của ngành khoa học máy tính, khái niệm **Giao dịch (Transaction)** và chuẩn **ACID** ra đời.

<div class="my-6 rounded-xl overflow-hidden shadow-lg border border-gray-200 p-2 bg-white">
  <img src="https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?w=1200&q=80" alt="Bảo mật giao dịch" class="w-full object-cover h-64 rounded-lg" />
  <div class="bg-white p-2 text-center text-sm text-gray-500 italic">Mọi hệ thống thanh toán ngân hàng đều dựa vào chuẩn ACID của CSDL.</div>
</div>

---

### Bộ tứ siêu đẳng ACID

Để được gọi là một DBMS chuẩn (như SQL Server, Oracle, PostgreSQL), hệ thống đó bắt buộc phải đáp ứng đủ 4 tiêu chí ACID cho một Transaction:

<div class="space-y-4 my-6">
  <div class="flex items-start p-4 bg-gray-50 rounded-lg border-l-4 border-red-500">
    <div class="text-3xl mr-4">🅰️</div>
    <div>
      <h4 class="mt-0 mb-1 font-bold text-red-700">Atomicity (Tính Nguyên Tử)</h4>
      <p class="text-sm text-gray-700 m-0">"All or Nothing". Một là tất cả các lệnh cùng thành công (COMMIT). Hai là nếu có 1 lệnh lỗi (dù cúp điện), hệ thống sẽ TỰ ĐỘNG ROLLBACK (phục hồi) về y như cũ. Không bao giờ có chuyện làm dang dở.</p>
    </div>
  </div>

  <div class="flex items-start p-4 bg-gray-50 rounded-lg border-l-4 border-yellow-500">
    <div class="text-3xl mr-4">🅲️</div>
    <div>
      <h4 class="mt-0 mb-1 font-bold text-yellow-700">Consistency (Tính Nhất Quán)</h4>
      <p class="text-sm text-gray-700 m-0">Đảm bảo luật lệ. Tổng tiền trước khi chuyển và sau khi chuyển phải bằng nhau. Nếu lệnh chuyển tiền làm vi phạm quy tắc CHECK (ví dụ số dư âm), Transaction sẽ bị hủy ngay lập tức.</p>
    </div>
  </div>

  <div class="flex items-start p-4 bg-gray-50 rounded-lg border-l-4 border-blue-500">
    <div class="text-3xl mr-4">🅸️</div>
    <div>
      <h4 class="mt-0 mb-1 font-bold text-blue-700">Isolation (Tính Cô Lập)</h4>
      <p class="text-sm text-gray-700 m-0">Hàng ngàn người đang chuyển tiền cùng lúc, nhưng CSDL phải cô lập chúng. Không để tiến trình này "đọc lén" dữ liệu đang sửa dở dang của tiến trình khác, gây ra hiệu ứng bươm bướm.</p>
    </div>
  </div>

  <div class="flex items-start p-4 bg-gray-50 rounded-lg border-l-4 border-green-500">
    <div class="text-3xl mr-4">🅳️</div>
    <div>
      <h4 class="mt-0 mb-1 font-bold text-green-700">Durability (Tính Bền Vững)</h4>
      <p class="text-sm text-gray-700 m-0">Một khi hệ thống báo "Chuyển khoản thành công" (COMMIT), thì dù 1 giây sau Server nổ tung, dữ liệu đó vẫn đã được lưu vĩnh viễn vào ổ cứng và khôi phục được.</p>
    </div>
  </div>
</div>
'''
}

with engine.connect() as conn:
    for title, body in content.items():
        conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = :title'), {'body': body, 'title': title})
    conn.commit()

print("Batch 3 completed!")
