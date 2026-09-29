# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

content = {
    'Mô hình ER: Thực thể và Thuộc tính': '''
## Thiết kế CSDL trên giấy: Xây nhà phải có Bản vẽ

Khi xây một tòa nhà Landmark 81, kỹ sư không bao giờ lấy gạch ra xây ngay lập tức. Họ phải vẽ một bản thiết kế (Blueprint) trên giấy trước. 
Lập trình viên CSDL cũng vậy! Trước khi viết code tạo bảng (Table), chúng ta cần vẽ một "bản thiết kế" cho CSDL. Bản thiết kế phổ biến nhất thế giới chính là **Sơ đồ Thực thể - Liên kết (ER Diagram)**.

<div class="my-6 rounded-xl overflow-hidden shadow-lg">
  <img src="https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?w=1200&q=80" alt="Bản vẽ sơ đồ ER" class="w-full object-cover h-64 hover:scale-105 transition-transform duration-500" />
  <div class="bg-gray-100 p-3 text-center text-sm text-gray-500 italic">Sơ đồ thiết kế giúp hình dung luồng dữ liệu trước khi viết code.</div>
</div>

---

### 1. Thực thể (Entity) - "Nhân vật chính"

<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-6">
  <h4 class="text-blue-800 font-bold mt-0 mb-2">Thực thể là gì?</h4>
  <p class="text-blue-700 m-0">
    Bất cứ thứ gì <strong>tồn tại độc lập trong thế giới thực</strong> mà bạn muốn lưu trữ thông tin về nó, thì nó là Thực thể. Ký hiệu là <strong>Hình chữ nhật</strong>.
  </p>
</div>

- **Ví dụ trong trường học:** SINH VIÊN, GIÁO VIÊN, MÔN HỌC.
- **Ví dụ trên Shopee:** KHÁCH HÀNG, SẢN PHẨM, ĐƠN HÀNG.

### 2. Thuộc tính (Attribute) - "Đặc điểm nhận dạng"

Thực thể là một đối tượng chung chung. Để phân biệt sinh viên này với sinh viên khác, chúng ta cần các **Thuộc tính** (Ký hiệu: Hình Elip).

- Thực thể **SINH VIÊN** có các thuộc tính: Mã SV, Họ tên, Ngày sinh.
- Thực thể **SẢN PHẨM** có các thuộc tính: Mã SP, Tên SP, Giá bán.

<table class="min-w-full divide-y divide-gray-200 my-6 border rounded-lg overflow-hidden">
  <thead class="bg-gray-50">
    <tr><th class="px-4 py-2 text-left">Loại thuộc tính</th><th class="px-4 py-2 text-left">Ví dụ thực tế</th><th class="px-4 py-2 text-left">Lưu ý</th></tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200 text-sm">
    <tr><td class="px-4 py-2 font-bold text-gray-700">Đơn (Simple)</td><td class="px-4 py-2">Giới tính (Nam/Nữ)</td><td class="px-4 py-2">Không chia nhỏ được nữa.</td></tr>
    <tr><td class="px-4 py-2 font-bold text-gray-700">Phức hợp (Composite)</td><td class="px-4 py-2">Họ tên (Gồm: Họ, Tên lót, Tên)</td><td class="px-4 py-2">Có thể chẻ nhỏ ra để quản lý (ví dụ để sắp xếp theo Tên chữ cái).</td></tr>
    <tr><td class="px-4 py-2 font-bold text-gray-700">Đa trị (Multivalued)</td><td class="px-4 py-2">Số điện thoại (Một người có 2 sim)</td><td class="px-4 py-2">Ký hiệu là Elip nét đôi. Cực kỳ nguy hiểm khi lưu CSDL, thường phải tách thành bảng riêng!</td></tr>
  </tbody>
</table>
''',

    'Mô hình ER: Mối Quan hệ': '''
## Sợi dây liên kết các Thực thể

Nếu hệ thống chỉ có Thực thể đứng cô lập thì vô nghĩa. Sinh viên phải có liên kết với Môn học. Khách hàng phải có liên kết với Đơn hàng. Đó gọi là **Mối quan hệ (Relationship)**.
- **Ký hiệu trong sơ đồ:** Hình thoi (Kèm theo một động từ ở giữa).
- *Ví dụ:* Sinh viên **[ĐĂNG KÝ]** Môn học.

---

### Tỉ lệ lực lượng (Cardinality) - Trái tim của Thiết kế CSDL

Để CSDL không bị sập hay lưu sai dữ liệu, bạn phải xác định đúng Tỉ lệ (Số lượng) của mối quan hệ. Đừng coi thường bước này, sai một ly đi một dặm!

<div class="grid grid-cols-1 gap-6 my-6">
  
  <div class="bg-white border-2 border-green-200 p-5 rounded-xl shadow-sm">
    <h3 class="text-green-700 font-bold mt-0 flex items-center text-lg"><span class="mr-2 text-2xl">🤝</span> Quan hệ 1 - 1 (Một - Một)</h3>
    <p class="text-gray-600"><strong>Định nghĩa:</strong> 1 đối tượng bên A liên kết với duy nhất 1 đối tượng bên B, và ngược lại.</p>
    <div class="bg-green-50 p-3 rounded mt-2 text-sm">
      <em>Ví dụ:</em> 1 Công dân chỉ có 1 Căn cước công dân (CCCD). Và 1 thẻ CCCD chỉ thuộc về 1 Công dân.
    </div>
  </div>

  <div class="bg-white border-2 border-blue-200 p-5 rounded-xl shadow-sm">
    <h3 class="text-blue-700 font-bold mt-0 flex items-center text-lg"><span class="mr-2 text-2xl">👨‍👧‍👦</span> Quan hệ 1 - N (Một - Nhiều)</h3>
    <p class="text-gray-600"><strong>Định nghĩa:</strong> 1 A có nhiều B, nhưng 1 B chỉ thuộc về duy nhất 1 A.</p>
    <div class="bg-blue-50 p-3 rounded mt-2 text-sm">
      <em>Ví dụ:</em> 1 Mẹ có thể sinh ra Nhiều Con. Nhưng 1 Người Con thì chỉ do 1 Người Mẹ sinh ra.<br/>
      <em>Trong Tech:</em> 1 Người dùng (User) có thể đăng nhiều Bài viết (Posts).
    </div>
  </div>

  <div class="bg-white border-2 border-purple-200 p-5 rounded-xl shadow-sm">
    <h3 class="text-purple-700 font-bold mt-0 flex items-center text-lg"><span class="mr-2 text-2xl">🕸️</span> Quan hệ M - N (Nhiều - Nhiều)</h3>
    <p class="text-gray-600"><strong>Định nghĩa:</strong> Nhiều A liên kết nhiều B và ngược lại.</p>
    <div class="bg-purple-50 p-3 rounded mt-2 text-sm">
      <em>Ví dụ Shopee:</em> 1 Khách hàng có thể mua Nhiều Sản phẩm. Và 1 Sản phẩm (như iPhone) có thể được mua bởi Nhiều Khách hàng khác nhau.
    </div>
    <div class="mt-2 text-red-500 font-bold text-sm">⚠️ Cảnh báo: Trong CSDL thực tế, không thể lưu trực tiếp quan hệ M-N. Bắt buộc phải sinh ra một "Bảng trung gian" (Ví dụ: Chi tiết đơn hàng).</div>
  </div>

</div>
''',

    'Khóa và Ràng buộc Toàn vẹn': '''
## Thế giới cần Pháp luật, Database cần Ràng buộc (Constraints)

Nếu bạn thiết kế một app Ngân hàng mà không có "ràng buộc", người dùng có thể chuyển số tiền là -50.000đ (tiền âm) để tự hack tiền của chính mình.
**Ràng buộc toàn vẹn** chính là các "cảnh sát" túc trực 24/7 để chặn mọi dữ liệu rác, phi logic xâm nhập vào hệ thống.

---

### 1. Khóa chính (Primary Key - PK)
Là "Căn cước công dân" của mỗi dòng dữ liệu. 
- **Quy tắc thép số 1:** KHÔNG ĐƯỢC TRÙNG NHAU (UNIQUE).
- **Quy tắc thép số 2:** KHÔNG ĐƯỢC RỖNG (NOT NULL). Chắc chắn ai cũng phải có CCCD!

*Ví dụ:* Mã SV, Số CCCD, Mã Hóa Đơn. (Tên người không thể làm khóa chính vì rất dễ có 2 người cùng tên Nguyễn Văn A).

### 2. Khóa ngoại (Foreign Key - FK) và Toàn vẹn Tham chiếu

Khóa ngoại là sợi dây thừng móc từ bảng này sang bảng kia (dựa vào Khóa chính của bảng kia).

<div class="bg-red-50 border-l-4 border-red-500 p-4 my-6">
  <h4 class="text-red-800 font-bold mt-0 mb-2">Thảm họa "Chìa khóa ma"</h4>
  <p class="text-red-700 m-0 text-sm">
    Giả sử bảng <strong>SINH VIÊN</strong> có cột Mã Khoa (Khóa ngoại) trỏ sang bảng <strong>KHOA</strong>.<br/>
    Sinh viên A nhập Mã Khoa = "CNTT". Mọi thứ bình thường.<br/>
    Một ngày nọ, Giám đốc lỡ tay nhấn nút XÓA khoa CNTT khỏi bảng KHOA. <br/>
    <strong>Điều gì xảy ra?</strong> Sinh viên A giờ đây đang thuộc về một cái Khoa "không tồn tại" (Chìa khóa ma không có ổ khóa tương ứng). Dữ liệu bị rác nghiêm trọng!
  </p>
</div>

**Giải pháp của DBMS:** Kích hoạt tính năng **Toàn vẹn tham chiếu**. 
Khi bạn cố xóa Khoa CNTT, DBMS sẽ hét lên lỗi: *"Không được xóa! Đang có 1000 sinh viên xài khóa này!"*. Nhờ vậy hệ thống của bạn không bao giờ bị lỗi.

### 3. Các ràng buộc phổ biến khác
- **CHECK Constraint:** Giới hạn dữ liệu. *Ví dụ: Tuổi > 18, hoặc Số_dư_tài_khoản >= 0.*
- **DEFAULT Constraint:** Nếu người dùng lười không nhập, tự điền giá trị mặc định. *Ví dụ: Trạng thái đơn hàng = 'Chờ xử lý'.*
'''
}

with engine.connect() as conn:
    for title, body in content.items():
        conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = :title'), {'body': body, 'title': title})
    conn.commit()

print("Batch 1 completed!")
