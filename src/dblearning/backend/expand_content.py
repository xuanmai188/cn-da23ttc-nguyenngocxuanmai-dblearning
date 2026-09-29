# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning"

engine = create_engine(db_url)

content_tong_quan_chi_tiet = '''
## Cơ sở dữ liệu là gì? Hướng dẫn từ con số 0 cho người mới bắt đầu

Chào mừng bạn bước vào thế giới của Cơ sở dữ liệu! Nếu bạn từng thắc mắc làm thế nào Facebook có thể lưu trữ hàng tỷ bài viết, hay Shopee làm sao nhớ được giỏ hàng của bạn dù bạn đăng nhập từ điện thoại hay máy tính, thì câu trả lời chính là **Cơ sở dữ liệu (Database)**. 

Bài học này được thiết kế dành riêng cho người mới bắt đầu. Chúng ta sẽ đi chậm từng bước, từ những khái niệm đời thường nhất.

---

### 1. Phân biệt Dữ liệu (Data) và Thông tin (Information)

Trước khi nói về CSDL, chúng ta cần hiểu viên gạch nền tảng của nó: **Dữ liệu**.
Rất nhiều người nhầm lẫn giữa "Dữ liệu" và "Thông tin". Hãy xem ví dụ sau:

- **Dữ liệu (Data):** Là những sự thật thô, chưa được xử lý. 
  - *Ví dụ:* Con số 20, chữ Nguyễn Văn A, hoặc 38.5. Khi đứng một mình, chúng vô nghĩa. 38.5 là nhiệt độ cơ thể hay là điểm số?
- **Thông tin (Information):** Là dữ liệu đã được xử lý, tổ chức và mang lại ý nghĩa cho người đọc.
  - *Ví dụ:* "Bệnh nhân Nguyễn Văn A đang bị sốt 38.5 độ C". Đây là thông tin.

<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-6 rounded-r-lg">
  <h4 class="text-blue-800 font-bold mt-0 mb-2 flex items-center">
    <span class="mr-2 text-xl">💡</span> Mục đích cuối cùng
  </h4>
  <p class="text-blue-700 m-0">
    Hệ thống Cơ sở dữ liệu sinh ra là để <strong>lưu trữ dữ liệu (Data)</strong> một cách thông minh, nhằm giúp chúng ta <strong>truy xuất ra thông tin (Information)</strong> một cách nhanh chóng và chính xác nhất.
  </p>
</div>

---

### 2. Cơ sở Dữ liệu (Database) thực chất là gì?

<div class="my-6 rounded-xl overflow-hidden shadow-lg">
  <img src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&q=80" alt="Máy chủ Cơ sở dữ liệu" class="w-full object-cover h-64 hover:scale-105 transition-transform duration-500" />
  <div class="bg-gray-100 p-3 text-center text-sm text-gray-500 italic">Hệ thống máy chủ lưu trữ Cơ sở dữ liệu của các tập đoàn lớn.</div>
</div>

Định nghĩa sách vở: *"Cơ sở dữ liệu là một tập hợp các dữ liệu có liên quan logic với nhau, được tổ chức và lưu trữ một cách có cấu trúc trên hệ thống máy tính."*

**Hãy tưởng tượng:** Bạn có một thư viện sách khổng lồ.
- Nếu bạn vứt sách bừa bãi ra sàn nhà (giống như lưu file lộn xộn trong máy tính), khi cần tìm cuốn "Đắc Nhân Tâm", bạn sẽ phải lục tung cả đống sách.
- Nhưng nếu bạn có các kệ sách (Bảng), mỗi kệ chia theo chủ đề, dán nhãn theo thứ tự ABC, mỗi cuốn sách có một mã số (Khóa chính) được ghi vào sổ thủ thư. Lúc này, việc tìm kiếm mất chưa tới 1 phút. 
👉 **Thư viện được sắp xếp ngăn nắp đó chính là hình ảnh thu nhỏ của một Cơ sở dữ liệu.**

---

### 3. Excel có phải là Cơ sở dữ liệu không?

Nhiều bạn mới học thường hỏi: *"Tại sao phải học CSDL phức tạp trong khi tôi có thể lưu danh sách khách hàng vào file Excel?"*

Excel (Spreadsheet) và Database đều dùng để lưu dữ liệu dạng bảng, nhưng chúng có sự khác biệt một trời một vực:

<table class="min-w-full divide-y divide-gray-200 my-6 shadow-sm border border-gray-200 rounded-lg overflow-hidden">
  <thead class="bg-gray-50">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tiêu chí</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider text-blue-600">File Excel</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider text-green-600">Cơ sở Dữ liệu (Database)</th>
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200 text-sm">
    <tr>
      <td class="px-6 py-4 font-medium text-gray-900">Người dùng</td>
      <td class="px-6 py-4 text-gray-600">Thường là cá nhân (1-2 người sửa cùng lúc).</td>
      <td class="px-6 py-4 text-gray-600">Hàng ngàn người truy cập và chỉnh sửa cùng một phần nghìn giây (VD: Shopee lúc sale).</td>
    </tr>
    <tr>
      <td class="px-6 py-4 font-medium text-gray-900">Dung lượng</td>
      <td class="px-6 py-4 text-gray-600">Giới hạn khoảng 1 triệu dòng (rất lag).</td>
      <td class="px-6 py-4 text-gray-600">Lưu trữ hàng tỷ tỷ dòng, hàng trăm Terabyte dữ liệu mà vẫn chạy mượt.</td>
    </tr>
    <tr>
      <td class="px-6 py-4 font-medium text-gray-900">Ràng buộc</td>
      <td class="px-6 py-4 text-gray-600">Dễ nhập sai (Ô SĐT lại nhập chữ).</td>
      <td class="px-6 py-4 text-gray-600">Ép buộc quy tắc chặt chẽ (Nhập chữ vào ô số sẽ báo lỗi ngay lập tức).</td>
    </tr>
  </tbody>
</table>

---

### 4. Hệ quản trị CSDL (DBMS) - "Người thủ thư" quyền lực

Có Database rồi, nhưng máy tính không tự dưng biết cách lấy dữ liệu ra. Bạn cần một phần mềm trung gian gọi là **Hệ quản trị cơ sở dữ liệu (DBMS - Database Management System)**.

<div class="bg-purple-50 border border-purple-200 p-5 my-6 rounded-xl relative">
  <div class="absolute top-0 right-0 p-4 opacity-10 text-6xl">🤖</div>
  <p class="text-purple-800 m-0">
    Nếu <strong>Database</strong> là kho hàng, thì <strong>DBMS</strong> chính là người thủ kho kết hợp với hệ thống robot tự động. 
    Bạn (Lập trình viên) sẽ giao tiếp với DBMS bằng một ngôn ngữ riêng gọi là <strong>SQL (Structured Query Language)</strong>. Bạn ra lệnh: <em>"Lấy cho tôi danh sách sinh viên Khoa CNTT"</em>, DBMS sẽ tự động chạy vào kho, tìm đúng kệ, nhặt dữ liệu và đưa cho bạn.
  </p>
</div>

**Các DBMS nổi tiếng thế giới:**
1. **MySQL / MariaDB:** Nổi tiếng nhất thế giới web mã nguồn mở (Facebook, WordPress đều xài).
2. **PostgreSQL:** Mã nguồn mở nhưng cực kỳ mạnh mẽ, được đánh giá là tiên tiến nhất hiện nay.
3. **Microsoft SQL Server:** Do Microsoft phát triển, xài rất nhiều trong khối doanh nghiệp (Ngân hàng, Bệnh viện).
4. **Oracle:** "Đại gia" của ngành dữ liệu. Đắt đỏ nhưng bảo mật và hiệu năng cực khủng.

---

### 5. Tại sao các doanh nghiệp đều phải dùng DBMS?

Trước khi DBMS ra đời vào những năm 1970, người ta quản lý dữ liệu bằng cách lưu vào các File Text (.txt). Phương pháp cũ kỹ này gây ra những thảm họa sau (mà DBMS đã khắc phục hoàn toàn):

<div class="space-y-4 my-6">
  <div class="bg-white border border-gray-200 p-5 rounded-xl shadow-sm">
    <div class="flex items-center mb-2">
      <div class="text-2xl mr-3">🗑️</div>
      <h3 class="text-lg font-bold mt-0 text-red-600 mb-0">Thảm họa 1: Dư thừa và Bất nhất dữ liệu</h3>
    </div>
    <p class="text-gray-600 text-sm mt-2">
      <strong>Vấn đề:</strong> Trong trường học, Phòng Đào tạo giữ 1 file <code>SinhVien.txt</code>, Phòng Kế toán giữ 1 file <code>HocPhi.txt</code>. Cả 2 file đều ghi "Địa chỉ" của bạn. Nếu bạn chuyển nhà và báo Phòng Đào tạo, họ cập nhật file của họ. Nhưng Kế toán không biết! Dẫn đến dữ liệu <strong>bất nhất (Inconsistency)</strong>. Giấy báo học phí gửi về nhà cũ!<br/>
      <strong>DBMS giải quyết:</strong> Dữ liệu chỉ được lưu <strong>DUY NHẤT 1 LẦN</strong>. Khi cập nhật địa chỉ, mọi phòng ban đều nhìn thấy địa chỉ mới ngay lập tức.
    </p>
  </div>

  <div class="bg-white border border-gray-200 p-5 rounded-xl shadow-sm">
    <div class="flex items-center mb-2">
      <div class="text-2xl mr-3">💥</div>
      <h3 class="text-lg font-bold mt-0 text-orange-600 mb-0">Thảm họa 2: Mất an toàn khi truy cập đồng thời</h3>
    </div>
    <p class="text-gray-600 text-sm mt-2">
      <strong>Vấn đề:</strong> Thử tưởng tượng hệ thống đặt vé xem phim. Còn đúng 1 ghế trống. Hai người A và B cùng bấm mua vé vào đúng một phần nghìn giây. Hệ thống File truyền thống sẽ bị ngốc và bán 1 ghế cho cả 2 người! Cãi nhau to!<br/>
      <strong>DBMS giải quyết:</strong> DBMS có cơ chế <strong>Locking (Khóa)</strong>. Dù nhanh đến mấy, người click trước (chỉ chênh 1 mili-giây) sẽ được cấp quyền mua, hệ thống lập tức khóa ghế đó lại và báo lỗi "Ghế đã có người mua" cho người thứ 2. 
    </p>
  </div>
</div>

---

### 6. Tổng kết bài học

Chúc mừng bạn đã hoàn thành bài học nhập môn! Hãy ghi nhớ 3 từ khóa quan trọng nhất hôm nay:
1. **Dữ liệu (Data):** Đóng vai trò nguyên liệu thô.
2. **Cơ sở dữ liệu (Database - DB):** Kho lưu trữ nguyên liệu một cách ngăn nắp, có cấu trúc.
3. **Hệ quản trị CSDL (DBMS):** Phần mềm giúp thao tác, thêm, sửa, xóa dữ liệu trong kho một cách an toàn tuyệt đối.

> 🚀 **Bước tiếp theo:** Ở bài học sau, chúng ta sẽ tìm hiểu bên trong một Database được cấu tạo từ những thành phần gì qua bài **Kiến trúc Hệ thống CSDL**. Hãy chuẩn bị tinh thần nhé!
'''

with engine.connect() as conn:
    conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = "Tổng quan về Cơ sở Dữ liệu"'), {'body': content_tong_quan_chi_tiet})
    conn.commit()

print("Successfully injected highly detailed content for Tổng quan về Cơ sở Dữ liệu")
