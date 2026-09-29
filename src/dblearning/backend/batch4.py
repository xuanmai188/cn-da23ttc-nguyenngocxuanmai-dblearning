# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

content = {
    'View trong SQL': '''
## View (Khung nhìn) - Chiếc "Cửa Sổ" nhìn vào Dữ liệu

Hãy tưởng tượng Database của bạn là một tòa nhà chọc trời bí mật chứa hàng tỷ bộ hồ sơ. Bạn (Giám đốc) không muốn cho nhân viên bảo vệ nhìn thấy mức lương của mọi người. Bạn chỉ muốn họ nhìn thấy bảng `Tên` và `Biển số xe`.
Bạn sẽ làm gì? Chẳng lẽ copy ra một bảng mới? Không! Sẽ rất lãng phí ổ cứng và dữ liệu bị cũ ngay lập tức.
Giải pháp chính là tạo một **View (Khung nhìn)**.

<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-6">
  <h4 class="text-blue-800 font-bold mt-0 mb-1">Định nghĩa:</h4>
  <p class="text-blue-700 m-0">View thực chất là một <strong>Bảng Ảo (Virtual Table)</strong>. Nó không lưu trữ dữ liệu vật lý. Nó chỉ lưu lại <strong>Câu lệnh SELECT</strong>. Mỗi khi bạn MỞ cửa sổ View, Database sẽ tự động chạy câu lệnh SELECT đó và hiển thị kết quả mới nhất cho bạn.</p>
</div>

### 1. Tại sao phải dùng View?

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
  <div class="bg-white border border-gray-200 p-4 rounded-xl shadow-sm">
    <div class="text-2xl mb-2">🛡️</div>
    <h3 class="text-md font-bold mt-0 text-gray-800">Tăng cường bảo mật</h3>
    <p class="text-gray-600 text-sm m-0">Ẩn các cột nhạy cảm (như Mật khẩu, Lương, Doanh thu). Cấp quyền cho user chỉ được SELECT trên View thay vì truy cập thẳng vào Bảng gốc.</p>
  </div>
  <div class="bg-white border border-gray-200 p-4 rounded-xl shadow-sm">
    <div class="text-2xl mb-2">✂️</div>
    <h3 class="text-md font-bold mt-0 text-gray-800">Rút gọn code phức tạp</h3>
    <p class="text-gray-600 text-sm m-0">Thay vì mỗi lần làm báo cáo phải JOIN 10 cái bảng lại với nhau (code dài 50 dòng), bạn gom 50 dòng đó thành 1 View tên là <code>V_BaoCao</code>. Sau này chỉ cần gõ <code>SELECT * FROM V_BaoCao</code>.</p>
  </div>
</div>

### 2. Cách tạo View cơ bản

<div class="my-4 bg-slate-900 rounded-xl overflow-hidden">
  <div class="bg-slate-800 px-4 py-2 text-xs text-slate-400 font-mono">Tạo View giấu điểm số</div>
  <pre class="m-0 p-4 text-sm font-mono text-green-400"><code>CREATE VIEW View_ThongTinChung AS
SELECT MSSV, HoTen, MaKhoa 
FROM SinhVien;
-- Cột 'Diem' đã bị giấu đi!</code></pre>
</div>
''',

    'Stored Procedure và Trigger': '''
## Stored Procedure và Trigger - Đưa "Não" vào CSDL

Từ trước đến nay, CSDL chỉ đóng vai trò là "Cái Kho" ngu ngốc: Kêu lấy thì lấy, kêu cất thì cất. Trí thông minh (Logic tính toán) đều do phía Lập trình (Backend bằng Python, Java) đảm nhận.
Nhưng nếu bạn muốn "nhét" một phần não bộ tính toán vào thẳng bên trong CSDL để chạy cho nhanh thì sao? 
Đó là lúc **Stored Procedure (Thủ tục lưu trữ)** và **Trigger (Cò súng / Trình kích hoạt)** xuất hiện!

---

### 1. Stored Procedure (Thủ tục lưu trữ)

**Nó là gì?** Nó giống như một hàm (Function) trong lập trình, nhưng được viết bằng SQL và lưu sẵn bên trong hệ quản trị CSDL.

**Tại sao dùng?**
1. **Bảo mật:** Không cấp quyền SELECT/UPDATE cho Backend. Backend chỉ được phép gọi (CALL) hàm Procedure. Tránh bị Hack SQL Injection tuyệt đối.
2. **Hiệu năng siêu tốc:** Code SQL bình thường gửi từ Backend sang DB sẽ bị phân tích (Parse) lại từ đầu. Còn Procedure đã được DB biên dịch sẵn thành mã máy, gọi là chạy ngay!
3. **Giảm băng thông mạng:** Thay vì gửi 100 dòng lệnh SQL từ Server web sang Server DB, ta chỉ cần gửi 1 lệnh: `CALL Tinh_Luong_Thang_12();`

### 2. Trigger - Quả bom hẹn giờ

<div class="bg-red-50 border border-red-200 p-4 my-6 rounded-lg">
  <h4 class="text-red-800 font-bold mt-0 mb-1 flex items-center">
    <span class="mr-2 text-xl">🔫</span> Trigger là gì?
  </h4>
  <p class="text-red-700 text-sm m-0">
    Trigger (Cò súng) là một đoạn code <strong>tự động bắn ra (kích hoạt)</strong> khi có một hành động <code>INSERT</code>, <code>UPDATE</code>, hoặc <code>DELETE</code> xảy ra trên một bảng cụ thể. Bạn không thể chủ động gọi nó bằng tay!
  </p>
</div>

**Ví dụ kinh điển về Trigger (Ghi Log Hệ Thống):**
- **Yêu cầu:** Sếp bắt phạt 5 triệu nếu nhân viên nào dám xóa đơn hàng. Nhưng làm sao biết ai xóa?
- **Giải pháp:** Viết một Trigger. Cứ hễ có lệnh `DELETE` bắn vào bảng `DonHang`, Trigger sẽ tự động nhảy ra, bắt lấy dữ liệu vừa bị xóa, kèm theo tên nhân viên và giờ phút giây, nhét vào bảng `LichSu_Xoa`. Không kẻ gian nào có thể lách qua được hàng rào này!

*(⚠️ Cảnh báo: Lạm dụng Trigger sẽ khiến hệ thống chạy cực kỳ chậm và khó Debug (gỡ lỗi) vì các tác vụ chạy ngầm rất khó lường).*
''',

    'Phục hồi Dữ liệu': '''
## Phục hồi Dữ liệu (Database Recovery) - Cứu tinh ngày tận thế

CSDL là tài sản sống còn của công ty. Lỡ một ngày đẹp trời ổ cứng máy chủ bốc cháy, hoặc đang chạy một giao dịch hàng tỷ đồng thì... CÚP ĐIỆN. 
Làm sao DBMS có thể đưa dữ liệu trở về trạng thái toàn vẹn như lúc chưa cúp điện? Đó là nhờ cơ chế **Phục hồi (Recovery)**.

<div class="my-6 rounded-xl overflow-hidden shadow-lg border border-gray-200 bg-white">
  <img src="https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=1200&q=80" alt="Máy chủ ngắt kết nối" class="w-full object-cover h-64 rounded-lg" />
</div>

---

### 1. Bí kíp sinh tồn: Log File (Nhật ký)

Nguyên tắc vàng của DBMS: **"Ghi sổ trước khi làm" (Write-Ahead Logging - WAL)**.
Bất kỳ thao tác Thêm, Sửa, Xóa nào, trước khi thực sự ghi vào dữ liệu vật lý (Data files), nó PHẢI ĐƯỢC ghi lại vào một file nhật ký gọi là `Transaction Log`. File nhật ký này được ghi thẳng xuống đĩa cứng ngay lập tức.
Nếu cúp điện, dữ liệu RAM mất hết, nhưng cuốn sổ nhật ký (Log) nằm trên ổ cứng vẫn còn! Khi có điện lại, DBMS chỉ việc đọc sổ và khôi phục.

### 2. Hai phép thuật: UNDO và REDO

Khi hệ thống khởi động lại sau sự cố, thuật toán khôi phục (như ARIES) sẽ quét qua File Log và thực hiện 2 hành động:

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
  <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg shadow-sm">
    <div class="text-2xl mb-2">⏪</div>
    <h3 class="text-md font-bold mt-0 text-red-800">UNDO (Quay ngược thời gian)</h3>
    <p class="text-red-700 text-sm m-0">Áp dụng cho các Giao dịch <strong>đang chạy dở dang</strong> (Chưa có chữ COMMIT trong nhật ký). DBMS sẽ đọc nhật ký ngược từ dưới lên trên, khôi phục lại giá trị cũ (Old Value), xóa bỏ mọi dấu vết đang làm dở.</p>
  </div>
  <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg shadow-sm">
    <div class="text-2xl mb-2">⏩</div>
    <h3 class="text-md font-bold mt-0 text-green-800">REDO (Làm lại từ đầu)</h3>
    <p class="text-green-700 text-sm m-0">Áp dụng cho các Giao dịch <strong>đã COMMIT</strong> nhưng chưa kịp lưu vào đĩa cứng (bị rớt trong RAM). DBMS sẽ đọc nhật ký từ trên xuống, ghi lại các giá trị mới (New Value) vào đĩa. Đảm bảo tính Bền vững (Durability).</p>
  </div>
</div>

### 3. Checkpoint (Điểm chốt lưu)
File nhật ký cứ dài vô tận thì đọc bao giờ cho xong? Do đó, DBMS thường xuyên tạo ra các **Checkpoint**. Tại điểm này, nó tống toàn bộ dữ liệu trong RAM xuống ổ cứng. 
Khi có sự cố, hệ thống chỉ cần đọc file Log tính từ Checkpoint gần nhất thay vì đọc từ đầu năm!
''',

    'Chỉ mục (Index) trong CSDL': '''
## Chỉ mục (Index) - Phép thuật biến Rùa thành Thỏ

Giả sử bạn có cuốn từ điển Oxford 1 triệu từ. Bạn muốn tìm từ "Database".
- **Không có Index:** Bạn lật từng trang, từ trang 1 đến trang 1000. Mất nửa ngày. Trong CSDL gọi là **Full Table Scan (Quét toàn bộ bảng)**. Hệ thống sẽ đứng hình!
- **Có Index:** Bạn lật ra "Mục lục chữ D" ở đầu sách, lướt xuống vần "Da-", và mở thẳng ra trang 205. Mất 3 giây!

**Index (Chỉ mục)** trong CSDL cũng y hệt như vậy. Nó là một cấu trúc dữ liệu đặc biệt (thường là B-Tree) được tạo thêm để tăng tốc độ truy vấn `SELECT` lên hàng nghìn lần!

---

### 1. Cấu trúc Cây B-Tree (Cây nhiều nhánh)

<div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 my-6">
  <p class="text-yellow-800 text-sm m-0">
    Hầu hết các Database hiện nay lưu Index dưới dạng B-Tree. Khi bạn tìm kiếm số `55`, thay vì quét 100 dòng, cây B-Tree đi từ gốc: "55 lớn hơn 50 nên rẽ phải", "55 nhỏ hơn 70 nên rẽ trái", bùm! Tìm thấy 55 chỉ sau 2 bước nhảy! Mức độ tối ưu là <code>O(log n)</code>.
  </p>
</div>

### 2. Hai mặt của một đồng xu

Tốt như vậy sao không đánh Index cho TOÀN BỘ các cột đi cho nhanh? Đừng dại! 

- **Ưu điểm:** `SELECT`, `WHERE`, `ORDER BY` chạy cực kỳ nhanh (như tốc độ ánh sáng).
- **Nhược điểm:**
  1. Tốn dung lượng ổ cứng (Tạo Index tức là bạn đang tạo ra một cuốn danh bạ mới sao chép lại một phần dữ liệu).
  2. **Làm chậm thao tác Thêm/Sửa/Xóa (INSERT/UPDATE/DELETE).** Mỗi khi bạn thêm 1 hàng dữ liệu mới vào Bảng, DBMS phải cập nhật lại cuốn mục lục Index. Đánh 10 cái Index, hệ thống phải chạy cập nhật 10 cái mục lục khi Thêm 1 dòng dữ liệu!

### 3. Khi nào nên dùng Index?

<table class="min-w-full divide-y divide-gray-200 my-6 shadow-sm border border-gray-200 rounded-lg overflow-hidden">
  <thead class="bg-gray-50">
    <tr>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase text-green-600">Nên đánh Index (✅)</th>
      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase text-red-600">Không nên đánh Index (🚫)</th>
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200 text-sm">
    <tr>
      <td class="px-6 py-4">Khóa chính (PK), Khóa ngoại (FK)</td>
      <td class="px-6 py-4">Bảng có quá ít dữ liệu (VD: 100 dòng)</td>
    </tr>
    <tr>
      <td class="px-6 py-4">Cột thường xuyên dùng trong `WHERE`</td>
      <td class="px-6 py-4">Cột có dữ liệu lặp lại nhiều (VD: Giới tính)</td>
    </tr>
    <tr>
      <td class="px-6 py-4">Cột thường xuyên `ORDER BY`, `GROUP BY`</td>
      <td class="px-6 py-4">Cột bị thay đổi (UPDATE) liên tục</td>
    </tr>
  </tbody>
</table>
''',

    'Tối ưu hóa Truy vấn SQL': '''
## Tối ưu Truy vấn SQL (Query Tuning) - Cứu rỗi máy chủ

Cùng một yêu cầu xuất báo cáo, lập trình viên A viết câu SQL mất 0.1 giây, lập trình viên B viết câu SQL bắt hệ thống xoay vòng vòng 5 phút rồi chết (Timeout). Sự khác biệt nằm ở nghệ thuật **Tối ưu hóa Truy vấn**.

---

### 1. Các "Tội ác" phổ biến khi viết SQL

<div class="space-y-4 my-6">
  <div class="bg-white border border-red-200 p-4 rounded-xl shadow-sm">
    <h3 class="text-md font-bold mt-0 text-red-600">🚫 Lỗi 1: Dùng <code>SELECT *</code></h3>
    <p class="text-gray-600 text-sm m-0">Thay vì chỉ lấy cột Cần thiết, bạn kéo sạch toàn bộ 50 cột (kể cả cột hình ảnh dung lượng khủng). Hậu quả: Băng thông mạng tắc nghẽn, tốn RAM máy chủ Web vô ích.</p>
    <p class="mt-2 text-green-600 text-sm">✅ <strong>Sửa:</strong> Ghi đích danh tên cột: <code>SELECT HoTen, NgaySinh FROM...</code></p>
  </div>
  
  <div class="bg-white border border-red-200 p-4 rounded-xl shadow-sm">
    <h3 class="text-md font-bold mt-0 text-red-600">🚫 Lỗi 2: Dùng LIKE '%chuỗi%'</h3>
    <p class="text-gray-600 text-sm m-0">Gõ <code>WHERE HoTen LIKE '%Nguyễn'</code> (Tìm đuôi). Dấu % ở đằng trước khiến Database bị mù lòa, không thể sử dụng Index mục lục mà phải cày cuốc quét từng dòng một (Full Table Scan).</p>
    <p class="mt-2 text-green-600 text-sm">✅ <strong>Sửa:</strong> Nếu có thể, chỉ dùng dấu % ở sau: <code>LIKE 'Nguyễn%'</code> hoặc dùng Full-text Search.</p>
  </div>

  <div class="bg-white border border-red-200 p-4 rounded-xl shadow-sm">
    <h3 class="text-md font-bold mt-0 text-red-600">🚫 Lỗi 3: Dùng Hàm lên cột có Index</h3>
    <p class="text-gray-600 text-sm m-0">Gõ <code>WHERE YEAR(NgaySinh) = 2000</code>. Dù cột Ngày Sinh có đánh Index cũng vô dụng, vì nó bị nhốt trong hàm YEAR(). Database phải tính hàm cho 1 triệu dòng mới so sánh được!</p>
    <p class="mt-2 text-green-600 text-sm">✅ <strong>Sửa:</strong> <code>WHERE NgaySinh >= '2000-01-01' AND NgaySinh <= '2000-12-31'</code></p>
  </div>
</div>

### 2. Sử dụng công cụ EXPLAIN

Bí quyết của các chuyên gia DBA (Database Administrator) là dùng lệnh **EXPLAIN** (hoặc Execution Plan trong SQL Server).
Chỉ cần gõ `EXPLAIN SELECT ...`, CSDL sẽ vẽ ra một bản kế hoạch: Nó định quét bao nhiêu bảng, nó có dùng Index nào không, mất bao lâu. Nhìn vào đó, bạn sẽ biết ngay code của mình đang bị "thắt cổ chai" ở đâu!
'''
}

with engine.connect() as conn:
    for title, body in content.items():
        conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = :title'), {'body': body, 'title': title})
    conn.commit()

print("Batch 4 completed!")
