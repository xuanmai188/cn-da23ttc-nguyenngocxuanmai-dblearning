# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

content = {
    'Giới thiệu NoSQL': '''
## NoSQL - Kẻ nổi loạn phá vỡ mọi quy tắc

Trong hơn 40 năm, CSDL Quan hệ (như MySQL, SQL Server) thống trị toàn thế giới với các Bảng (Table) gọn gàng và luật lệ (ACID) khắt khe. 
Nhưng khi kỷ nguyên Big Data và Mạng xã hội bùng nổ, hàng triệu dòng status, bình luận, video... đổ về mỗi giây. Bảng quan hệ với các ràng buộc cứng nhắc tỏ ra quá lề mề. Thế là **NoSQL (Not Only SQL)** ra đời.

<div class="bg-gradient-to-r from-purple-500 to-indigo-600 p-6 rounded-xl text-white my-6 shadow-lg">
  <h3 class="mt-0 mb-2 font-bold text-xl">Triết lý NoSQL: Tốc độ và Sự tự do</h3>
  <p class="m-0 text-sm opacity-90">
    Không có Bảng (Table), Không có Cột (Column) cố định, Không cần Khóa ngoại (Foreign Key), Không có JOIN! Dữ liệu được nhét vào tự do, bất chấp hình thù. Đổi lại, tốc độ đọc/ghi đạt mức thần thánh và dễ dàng nhân bản sang hàng ngàn máy chủ (Horizontal Scaling).
  </p>
</div>

---

### Các trường phái NoSQL

Không giống SQL chỉ có 1 kiểu Bảng, NoSQL có tận 4 kiểu lưu trữ tùy thuộc vào mục đích sử dụng:

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
  <div class="bg-white border border-gray-200 p-4 rounded-xl shadow-sm">
    <div class="text-2xl mb-2">📄</div>
    <h3 class="text-md font-bold mt-0 text-gray-800">1. Document-based</h3>
    <p class="text-gray-600 text-sm m-0">Lưu dữ liệu dạng văn bản JSON. Một khách hàng có thể có 1 số điện thoại, khách hàng khác có 10 số. Rất linh hoạt. <br/><em>Đại diện: MongoDB, CouchDB.</em></p>
  </div>
  <div class="bg-white border border-gray-200 p-4 rounded-xl shadow-sm">
    <div class="text-2xl mb-2">🔑</div>
    <h3 class="text-md font-bold mt-0 text-gray-800">2. Key-Value Store</h3>
    <p class="text-gray-600 text-sm m-0">Đơn giản tột cùng. Một Chìa khóa (Key) ứng với một Cục dữ liệu (Value). Tra cứu cực nhanh, thường dùng làm Caching để chống sập Web. <br/><em>Đại diện: Redis, Memcached.</em></p>
  </div>
  <div class="bg-white border border-gray-200 p-4 rounded-xl shadow-sm">
    <div class="text-2xl mb-2">🏛️</div>
    <h3 class="text-md font-bold mt-0 text-gray-800">3. Column-Family</h3>
    <p class="text-gray-600 text-sm m-0">Tối ưu cho việc ghi dữ liệu liên tục không ngừng nghỉ (như dữ liệu cảm biến IOT, hoặc lịch sử click chuột). <br/><em>Đại diện: Cassandra, HBase.</em></p>
  </div>
  <div class="bg-white border border-gray-200 p-4 rounded-xl shadow-sm">
    <div class="text-2xl mb-2">🕸️</div>
    <h3 class="text-md font-bold mt-0 text-gray-800">4. Graph Database</h3>
    <p class="text-gray-600 text-sm m-0">Lưu trữ Mối quan hệ phức tạp như mạng lưới. "A là bạn của B, B là người yêu của C". <br/><em>Đại diện: Neo4j (Facebook hay dùng cái này).</em></p>
  </div>
</div>
''',

    'MongoDB Cơ bản': '''
## Nhập môn MongoDB - Ngôi sao sáng nhất làng NoSQL

Trong thế giới NoSQL, **MongoDB** chính là Vị vua. Hầu hết các startup công nghệ hiện nay đều chọn MongoDB vì nó cực kỳ thân thiện với các Lập trình viên Javascript (NodeJS, React).

### 1. Thuật ngữ MongoDB so với SQL (Bình cũ rượu mới)

<table class="min-w-full divide-y divide-gray-200 my-6 shadow-sm border border-gray-200 rounded-lg overflow-hidden">
  <thead class="bg-gray-50">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Khái niệm SQL (Truyền thống)</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase text-green-600">Khái niệm MongoDB (NoSQL)</th>
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200 text-sm">
    <tr><td class="px-6 py-4">Database</td><td class="px-6 py-4 font-bold text-green-700">Database</td></tr>
    <tr><td class="px-6 py-4">Table (Bảng)</td><td class="px-6 py-4 font-bold text-green-700">Collection (Bộ sưu tập)</td></tr>
    <tr><td class="px-6 py-4">Row (Hàng)</td><td class="px-6 py-4 font-bold text-green-700">Document (Tài liệu JSON)</td></tr>
    <tr><td class="px-6 py-4">Column (Cột)</td><td class="px-6 py-4 font-bold text-green-700">Field (Trường)</td></tr>
  </tbody>
</table>

### 2. Sự "Hỗn loạn" có chủ đích (Schema-less)

Trong SQL, nếu bảng `SinhVien` có 3 cột, bạn bắt buộc phải nhập đúng 3 cột. Nhưng trong Collection của MongoDB, bạn có thể nhét 2 cái Document hoàn toàn khác nhau vào nằm cạnh nhau:

<div class="my-4 bg-slate-900 rounded-xl overflow-hidden shadow-lg grid grid-cols-1 md:grid-cols-2">
  <div class="border-b md:border-b-0 md:border-r border-slate-700">
    <div class="bg-slate-800 px-4 py-2 text-xs text-slate-400">Document 1 (Sinh viên A)</div>
    <pre class="m-0 p-4 text-sm font-mono text-green-400"><code>{
  "_id": 1,
  "HoTen": "Nguyễn A",
  "Tuoi": 20
}</code></pre>
  </div>
  <div>
    <div class="bg-slate-800 px-4 py-2 text-xs text-slate-400">Document 2 (Sinh viên B)</div>
    <pre class="m-0 p-4 text-sm font-mono text-purple-400"><code>{
  "_id": 2,
  "HoTen": "Trần B",
  "Tuoi": 21,
  "SoThich": ["Game", "Đá bóng"],
  "DiaChi": {
     "Quan": "Bình Thạnh",
     "ThanhPho": "HCM"
  }
}</code></pre>
  </div>
</div>

Bạn thấy không? Sinh viên B có thêm mảng (Array) Sở thích, và có một Object Địa chỉ nằm chui vào bên trong. MongoDB cho phép bạn lưu cấu trúc lồng nhau (Nested) một cách vô cùng tự nhiên. Đây chính là sức mạnh khủng khiếp của MongoDB!
'''
}

with engine.connect() as conn:
    for title, body in content.items():
        conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = :title'), {'body': body, 'title': title})
    conn.commit()

print("Batch 5 completed!")
