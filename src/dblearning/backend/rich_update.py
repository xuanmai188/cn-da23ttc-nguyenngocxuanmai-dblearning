# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_url = "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning"

engine = create_engine(db_url)

content_tong_quan = '''
## 1. Cơ sở dữ liệu (Database) là gì?
Cơ sở dữ liệu (CSDL) là một tập hợp các dữ liệu có liên quan logic với nhau, được tổ chức và lưu trữ một cách có cấu trúc trên hệ thống máy tính. 

<div class="my-6 rounded-xl overflow-hidden shadow-lg">
  <img src="https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1200&q=80" alt="Máy chủ Cơ sở dữ liệu" class="w-full object-cover h-64 hover:scale-105 transition-transform duration-500" />
  <div class="bg-gray-100 p-3 text-center text-sm text-gray-500 italic">Hệ thống máy chủ lưu trữ Cơ sở dữ liệu hiện đại.</div>
</div>

Thay vì lưu dữ liệu lộn xộn trong các file văn bản rời rạc, CSDL giúp tổ chức dữ liệu thành các bảng, hàng và cột để dễ dàng tìm kiếm, cập nhật và quản lý.

## 2. Hệ quản trị CSDL (DBMS) là gì?

<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-6 rounded-r-lg">
  <h4 class="text-blue-800 font-bold mt-0 mb-2 flex items-center">
    <span class="mr-2 text-xl">💡</span> Hiểu đơn giản
  </h4>
  <p class="text-blue-700 m-0">
    Nếu <strong>Dữ liệu (Database)</strong> là kho chứa hàng, thì <strong>DBMS</strong> chính là người thủ kho. Bạn không thể tự ý lấy hàng ra mà phải nói với người thủ kho để họ tìm và đưa cho bạn.
  </p>
</div>

**DBMS (Database Management System)** là một phần mềm hệ thống cho phép người dùng định nghĩa, tạo, duy trì và kiểm soát truy cập vào cơ sở dữ liệu. Nó đóng vai trò là cầu nối giữa người dùng/ứng dụng và dữ liệu vật lý.
- **Ví dụ các DBMS phổ biến:** MySQL, PostgreSQL, Microsoft SQL Server, Oracle, MongoDB.

## 3. Hệ thống CSDL vs Hệ thống File truyền thống
Trước khi có CSDL, người ta lưu dữ liệu trong các File. Hệ thống CSDL ra đời để khắc phục các nhược điểm chí mạng của hệ thống File:

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
  <div class="bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition-shadow">
    <div class="text-3xl mb-3">🔄</div>
    <h3 class="text-lg font-bold mt-0 text-gray-800">Giảm dư thừa dữ liệu</h3>
    <p class="text-gray-600 text-sm">Không lưu trùng lặp một thông tin ở nhiều nơi (VD: thông tin sinh viên chỉ lưu 1 lần).</p>
  </div>
  <div class="bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition-shadow">
    <div class="text-3xl mb-3">🛡️</div>
    <h3 class="text-lg font-bold mt-0 text-gray-800">Toàn vẹn và Bảo mật</h3>
    <p class="text-gray-600 text-sm">Đảm bảo dữ liệu nhập vào luôn hợp lệ và phân quyền truy cập chặt chẽ cho từng người.</p>
  </div>
</div>
'''

content_kien_truc = '''
## 1. Kiến trúc 3 tầng ANSI/SPARC

Để che giấu sự phức tạp của việc lưu trữ dữ liệu với người dùng, một hệ thống CSDL chuẩn được chia làm 3 mức (tầng) trừu tượng:

<div class="my-6 rounded-xl overflow-hidden border border-gray-200 shadow-sm p-6 bg-slate-50 relative">
  <div class="absolute top-0 right-0 p-4 opacity-10 text-6xl">🏢</div>
  <h3 class="text-blue-600 font-bold mt-0 border-b pb-2">1. Mức ngoài (External Level)</h3>
  <p class="text-sm">Góc nhìn của người dùng. Mỗi ứng dụng (App sinh viên, App giảng viên) chỉ nhìn thấy một phần dữ liệu cần thiết.</p>
  
  <div class="flex justify-center my-2 text-gray-400">⬇️</div>

  <h3 class="text-purple-600 font-bold mt-0 border-b pb-2">2. Mức khái niệm (Conceptual Level)</h3>
  <p class="text-sm">Góc nhìn tổng thể của toàn bộ CSDL, mô tả các bảng dữ liệu và mối quan hệ giữa chúng.</p>
  
  <div class="flex justify-center my-2 text-gray-400">⬇️</div>

  <h3 class="text-emerald-600 font-bold mt-0 border-b pb-2">3. Mức nội tại (Internal Level)</h3>
  <p class="text-sm">Mô tả cách thức dữ liệu thực sự được lưu trữ trên đĩa cứng như thế nào (cấu trúc file, B-Tree index).</p>
</div>

## 2. Độc lập dữ liệu (Data Independence)

<div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 my-6 rounded-r-lg">
  <h4 class="text-yellow-800 font-bold mt-0 mb-2">⚡ Mục tiêu tối thượng của CSDL</h4>
  <p class="text-yellow-700 m-0 text-sm">
    Nhờ kiến trúc 3 tầng này, hệ thống đạt được tính "Độc lập dữ liệu": <strong>Thay đổi ở tầng dưới không làm hỏng tầng trên.</strong> 
    Ví dụ, khi bạn nâng cấp ổ cứng từ HDD sang SSD (Tầng vật lý), thì ứng dụng của người dùng (Tầng ngoài) vẫn hoạt động bình thường mà không cần sửa code.
  </p>
</div>
'''

content_er_diagram = '''
## 1. Mô hình Thực thể - Liên kết (ER Model) là gì?
Mô hình ER (Entity-Relationship) là một công cụ thiết kế giúp chuyển đổi "yêu cầu bài toán thực tế" thành một sơ đồ trực quan trước khi tạo bảng trong CSDL.

<div class="my-6 rounded-xl overflow-hidden shadow-lg border border-gray-200 p-2 bg-white">
  <img src="https://images.unsplash.com/photo-1581291518633-83b4ebd1d83e?w=1200&q=80" alt="Bản vẽ sơ đồ ER" class="w-full object-cover h-64 rounded-lg" />
  <div class="bg-white p-2 text-center text-sm text-gray-500 italic">Sơ đồ thiết kế giúp hình dung luồng dữ liệu trước khi viết code.</div>
</div>

## 2. Các thành phần chính

<div class="space-y-4 my-6">
  <div class="flex items-start p-4 bg-gray-50 rounded-lg border border-gray-100">
    <div class="w-12 h-12 bg-blue-100 rounded-md border-2 border-blue-500 flex items-center justify-center font-bold text-blue-600 mr-4 shrink-0">Entity</div>
    <div>
      <h4 class="mt-0 mb-1 text-gray-800">Thực thể (Hình chữ nhật)</h4>
      <p class="text-sm text-gray-600 m-0">Là một đối tượng thực tế. Ví dụ: SINH VIÊN, MÔN HỌC.</p>
    </div>
  </div>
  
  <div class="flex items-start p-4 bg-gray-50 rounded-lg border border-gray-100">
    <div class="w-12 h-12 bg-purple-100 rotate-45 border-2 border-purple-500 flex items-center justify-center mr-4 shrink-0 mt-2"><span class="-rotate-45 font-bold text-purple-600 text-xs">Rel</span></div>
    <div>
      <h4 class="mt-0 mb-1 text-gray-800">Mối quan hệ (Hình thoi)</h4>
      <p class="text-sm text-gray-600 m-0">Thể hiện sự liên kết. Ví dụ: Sinh viên <strong>ĐĂNG KÝ</strong> Môn học.</p>
    </div>
  </div>

  <div class="flex items-start p-4 bg-gray-50 rounded-lg border border-gray-100">
    <div class="w-16 h-10 bg-green-100 rounded-[50%] border-2 border-green-500 flex items-center justify-center font-bold text-green-600 text-xs mr-2 shrink-0">Attr</div>
    <div>
      <h4 class="mt-0 mb-1 text-gray-800">Thuộc tính (Hình Elip)</h4>
      <p class="text-sm text-gray-600 m-0">Đặc trưng của thực thể. Ví dụ: Họ tên, Ngày sinh.</p>
    </div>
  </div>
</div>
'''

content_sql_ddl = '''
## 1. Ngôn ngữ Định nghĩa Dữ liệu (DDL - Data Definition Language)
DDL dùng để tạo, sửa đổi và xóa bỏ các cấu trúc đối tượng trong CSDL (như Database, Table, Index). Nó tương tác trực tiếp với kiến trúc CSDL.

<div class="my-6 bg-slate-900 rounded-xl overflow-hidden shadow-lg border border-slate-700">
  <div class="bg-slate-800 px-4 py-2 border-b border-slate-700 flex items-center">
    <div class="flex space-x-2">
      <div class="w-3 h-3 rounded-full bg-red-500"></div>
      <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
      <div class="w-3 h-3 rounded-full bg-green-500"></div>
    </div>
    <div class="ml-4 text-xs text-slate-400 font-mono">Ví dụ tạo bảng sinh viên</div>
  </div>
  <pre class="m-0 p-4 text-sm font-mono text-green-400 bg-transparent overflow-x-auto"><code>CREATE TABLE SinhVien (
    MSSV CHAR(8) PRIMARY KEY,
    HoTen VARCHAR(50) NOT NULL,
    NgaySinh DATE,
    Diem FLOAT CHECK (Diem >= 0 AND Diem <= 10)
);</code></pre>
</div>

## 2. Các lệnh DDL cốt lõi

<table class="min-w-full divide-y divide-gray-200 my-6 shadow-sm border border-gray-200 rounded-lg overflow-hidden">
  <thead class="bg-gray-50">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Lệnh</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mô tả</th>
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200">
    <tr>
      <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600 font-mono">CREATE TABLE</td>
      <td class="px-6 py-4 text-sm text-gray-500">Tạo bảng mới cùng các cột và kiểu dữ liệu.</td>
    </tr>
    <tr>
      <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600 font-mono">ALTER TABLE</td>
      <td class="px-6 py-4 text-sm text-gray-500">Thêm, xóa hoặc sửa đổi cột của bảng hiện có.</td>
    </tr>
    <tr>
      <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-red-600 font-mono">DROP TABLE</td>
      <td class="px-6 py-4 text-sm text-gray-500">Xóa vĩnh viễn bảng (bao gồm cả dữ liệu và cấu trúc).</td>
    </tr>
  </tbody>
</table>
'''

with engine.connect() as conn:
    conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = "Tổng quan về Cơ sở Dữ liệu"'), {'body': content_tong_quan})
    conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = "Kiến trúc Hệ thống CSDL"'), {'body': content_kien_truc})
    conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = "Mô hình ER: Thực thể và Thuộc tính"'), {'body': content_er_diagram})
    conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = "SQL DDL: Tạo và Quản lý Bảng"'), {'body': content_sql_ddl})
    conn.commit()

print("Successfully injected rich HTML/Markdown content with images and stylized components for selected topics!")
