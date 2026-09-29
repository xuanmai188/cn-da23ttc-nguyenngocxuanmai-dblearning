# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, text

db_url = os.environ.get('DATABASE_URL', "mysql+pymysql://dbuser:dbpassword@127.0.0.1:3306/dblearning")
engine = create_engine(db_url)

content = {
    'Tổng quan về Cơ sở Dữ liệu': '''
## Phần 1: Khởi động (Tư duy Cốt lõi)

Chào mừng bạn bước vào thế giới của Cơ sở dữ liệu! Nếu bạn từng thắc mắc làm thế nào Facebook có thể lưu trữ hàng tỷ bài viết, hay Shopee làm sao nhớ được giỏ hàng của bạn, câu trả lời chính là **Cơ sở dữ liệu (Database)**. 

### 1. Dữ liệu (Data) vs Thông tin (Information)
- **Dữ liệu (Data):** Là những con số thô (VD: 38.5, "Nguyễn A").
- **Thông tin (Information):** Là dữ liệu đã xử lý có ý nghĩa (VD: "Bệnh nhân Nguyễn A sốt 38.5 độ").
- 👉 **Mục tiêu của CSDL:** Lưu trữ dữ liệu thông minh để truy xuất ra thông tin nhanh nhất.

### 2. Hệ quản trị CSDL (DBMS) là gì?
Nếu Database là một "Kho chứa hàng" khổng lồ, thì DBMS chính là "Người thủ kho" kết hợp hệ thống robot tự động. Bạn không tự ý lục kho, bạn dùng ngôn ngữ SQL để ra lệnh cho DBMS lấy hàng cho bạn.

<div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-6">
  <h4 class="text-blue-800 font-bold mt-0 mb-1">So sánh Excel và Database</h4>
  <p class="text-blue-700 m-0">Excel giới hạn 1 triệu dòng, dễ gõ sai (nhập chữ vào cột số) và chỉ 1-2 người sửa cùng lúc. Database chịu được tỷ dòng, ép buộc kiểu dữ liệu chặt chẽ và cho phép hàng triệu người truy cập đồng thời mà không bị treo.</p>
</div>

<hr class="my-8" />

## Phần 2: Chuyên sâu Kỹ thuật (Deep Dive)

<details class="group bg-slate-50 border border-slate-200 rounded-lg p-4 cursor-pointer mb-4">
  <summary class="font-bold text-slate-800 text-lg flex justify-between items-center outline-none">
    <span>🔍 Khám phá Kiến trúc chi tiết và Phân loại DBMS</span>
    <span class="transition group-open:rotate-180">⬇️</span>
  </summary>
  <div class="mt-4 pt-4 border-t border-slate-200 text-slate-700">
    <h3 class="font-bold text-md mt-0">1. Các loại Database Model trong lịch sử</h3>
    <ul class="list-disc pl-5">
      <li><strong>Hierarchical (Phân cấp):</strong> Hình cây (Tree). Truy xuất cực nhanh từ gốc xuống lá nhưng không biểu diễn được quan hệ N-N. Dùng trong hệ thống mainframe cũ.</li>
      <li><strong>Network (Mạng):</strong> Hình đồ thị (Graph). Khắc phục nhược điểm của phân cấp nhưng cực kỳ phức tạp để bảo trì.</li>
      <li><strong>Relational (Quan hệ - RDBMS):</strong> Kẻ thống trị hiện tại. Dữ liệu chia thành Bảng (Cột/Hàng). Nền tảng toán học chặt chẽ. Đảm bảo ACID. <em>Ví dụ: MySQL, PostgreSQL, Oracle.</em></li>
      <li><strong>NoSQL (Not Only SQL):</strong> Sinh ra cho Big Data. Bỏ qua ràng buộc khắt khe để đổi lấy tốc độ và khả năng mở rộng ngang (Horizontal Scaling). <em>Ví dụ: MongoDB, Redis.</em></li>
    </ul>

    <h3 class="font-bold text-md mt-6">2. Vòng đời phát triển Cơ sở dữ liệu (DBLC)</h3>
    <p>Một chuyên gia không bao giờ lao vào gõ code SQL ngay. Họ tuân theo quy trình chuẩn:</p>
    <ol class="list-decimal pl-5">
      <li><strong>Requirement Analysis:</strong> Gặp khách hàng, xác định cần lưu gì.</li>
      <li><strong>Conceptual Design (Thiết kế khái niệm):</strong> Vẽ sơ đồ ERD trên giấy. Bỏ qua yếu tố kỹ thuật.</li>
      <li><strong>Logical Design (Thiết kế logic):</strong> Chuyển ERD thành các Bảng. Thực hiện Chuẩn hóa (Normalization) để triệt tiêu dư thừa.</li>
      <li><strong>Physical Design (Thiết kế vật lý):</strong> Quyết định chọn MySQL hay Oracle. Tạo Index, cấp quyền, cấu hình ổ cứng.</li>
    </ol>
  </div>
</details>
''',

    'Mô hình ER: Thực thể và Thuộc tính': '''
## Phần 1: Khởi động (Tư duy Cốt lõi)

Khi xây nhà Landmark 81, kỹ sư phải vẽ bản thiết kế trước khi trộn hồ. Lập trình viên CSDL cũng vậy! Bản vẽ đó gọi là **Sơ đồ Thực thể - Liên kết (ER Diagram)**.

### 1. Thực thể (Entity) - Ký hiệu: Hình chữ nhật
Bất cứ đối tượng nào tồn tại độc lập mà ta cần lưu thông tin (VD: SINH VIÊN, SẢN PHẨM, KHÁCH HÀNG).

### 2. Thuộc tính (Attribute) - Ký hiệu: Hình Elip
Đặc điểm nhận dạng của Thực thể. (VD: Sinh viên có Mã SV, Họ tên, Ngày sinh).

### 3. Mối quan hệ (Relationship) - Ký hiệu: Hình thoi
Sợi dây liên kết các thực thể. (VD: Sinh viên [ĐĂNG KÝ] Môn học).

<div class="bg-green-50 border-l-4 border-green-500 p-4 my-6">
  <h4 class="text-green-800 font-bold mt-0 mb-1">Tỉ lệ lực lượng (Cardinality)</h4>
  <ul class="m-0 pl-5 text-green-700">
    <li><strong>1-1:</strong> 1 công dân có 1 thẻ CCCD.</li>
    <li><strong>1-N (Một-Nhiều):</strong> 1 người Mẹ có nhiều Con.</li>
    <li><strong>M-N (Nhiều-Nhiều):</strong> Khách hàng mua nhiều Sản phẩm, Sản phẩm được mua bởi nhiều Khách hàng.</li>
  </ul>
</div>

<hr class="my-8" />

## Phần 2: Chuyên sâu Kỹ thuật (Deep Dive)

<details class="group bg-slate-50 border border-slate-200 rounded-lg p-4 cursor-pointer mb-4">
  <summary class="font-bold text-slate-800 text-lg flex justify-between items-center outline-none">
    <span>🔍 Các bẫy thiết kế ERD và Kỹ thuật nâng cao</span>
    <span class="transition group-open:rotate-180">⬇️</span>
  </summary>
  <div class="mt-4 pt-4 border-t border-slate-200 text-slate-700">
    
    <h3 class="font-bold text-md mt-0">1. Thực thể Yếu (Weak Entity)</h3>
    <p>Là thực thể không có đủ thuộc tính để tự làm khóa. Sự tồn tại của nó phụ thuộc 100% vào Thực thể Mạnh. <strong>Ký hiệu: Hình chữ nhật nét đôi.</strong></p>
    <p><em>Ví dụ thực tế:</em> Bảng "Người Phụ Thuộc" (Vợ/Con của Nhân viên) trong CSDL công ty. Nếu Nhân viên nghỉ việc (bị xóa), toàn bộ dữ liệu Người phụ thuộc của nhân viên đó cũng trở nên vô nghĩa và phải bị xóa theo (ON DELETE CASCADE).</p>

    <h3 class="font-bold text-md mt-6">2. Xử lý Thuộc tính Đa trị (Multivalued Attribute)</h3>
    <p>Ví dụ: Sinh viên có 3 số điện thoại. <strong>Ký hiệu: Elip nét đôi.</strong></p>
    <p class="text-red-600 font-bold">⚠️ Cảnh báo chuẩn hóa:</p>
    <p>Tuyệt đối không lưu chuỗi <code>"0901, 0902, 0903"</code> vào 1 cột trong SQL. Khi chuyển từ ERD sang bảng, thuộc tính đa trị BẮT BUỘC phải tách ra thành một bảng mới (ví dụ bảng <code>DienThoai_SV(MaSV, SoDT)</code>).</p>

    <h3 class="font-bold text-md mt-6">3. Phá vỡ quan hệ Nhiều-Nhiều (M:N)</h3>
    <p>Trong ERD trên giấy, bạn thoải mái vẽ quan hệ M:N. Nhưng CSDL Quan hệ (MySQL, SQL Server) <strong>không thể cài đặt trực tiếp quan hệ M:N</strong>.</p>
    <p><strong>Giải pháp:</strong> Sinh ra một <em>Thực thể kết hợp (Associative Entity)</em> đứng ở giữa. <br/>
    VD: Thay vì KHÁCH HÀNG <code>(M:N)</code> SẢN PHẨM. Ta tách thành:<br/>
    KHÁCH HÀNG <code>(1:N)</code> <strong>CHI_TIẾT_ĐƠN_HÀNG</strong> <code>(N:1)</code> SẢN PHẨM.<br/>
    Thực thể ở giữa sẽ chứa các "Thuộc tính của mối quan hệ" như: Số lượng mua, Đơn giá lúc mua.</p>
  </div>
</details>
''',

    'SQL JOIN: Kết nối Bảng': '''
## Phần 1: Khởi động (Tư duy Cốt lõi)

Trong Database, dữ liệu bị "băm nhỏ" ra nhiều bảng để tránh trùng lặp. (VD: Tên SinhVien ở 1 bảng, Tên Khoa ở bảng khác).
Khi sếp yêu cầu xem Báo cáo có cả Tên Sinh Viên và Tên Khoa, bạn phải "chắp vá" chúng lại bằng **JOIN**.

- **INNER JOIN:** Chỉ lấy những người khớp (Sinh viên đã có khoa).
- **LEFT JOIN:** Lấy tất cả Sinh viên, ai chưa có Khoa thì cột Tên Khoa để trống (NULL). Cực kỳ hữu dụng để tìm "những khách hàng đăng ký tài khoản nhưng chưa mua gì".

<div class="my-4 bg-slate-900 rounded-xl overflow-hidden shadow-lg">
  <pre class="m-0 p-4 text-sm font-mono text-emerald-400"><code>SELECT SV.HoTen, K.TenKhoa
FROM SinhVien SV
INNER JOIN Khoa K ON SV.MaKhoa = K.MaKhoa;</code></pre>
</div>

<hr class="my-8" />

## Phần 2: Chuyên sâu Kỹ thuật (Deep Dive)

<details class="group bg-slate-50 border border-slate-200 rounded-lg p-4 cursor-pointer mb-4">
  <summary class="font-bold text-slate-800 text-lg flex justify-between items-center outline-none">
    <span>🔍 Giải phẫu JOIN: Self Join, Anti-Join và Tối ưu hiệu năng</span>
    <span class="transition group-open:rotate-180">⬇️</span>
  </summary>
  <div class="mt-4 pt-4 border-t border-slate-200 text-slate-700">
    
    <h3 class="font-bold text-md mt-0">1. SELF JOIN (Tự kết nối với chính mình)</h3>
    <p>Dùng để truy vấn dữ liệu có cấu trúc phân cấp (cây) nằm trong CÙNG MỘT BẢNG.</p>
    <p><em>Bài toán:</em> Bảng <code>NhanVien(MaNV, TenNV, MaNguoiQuanLy)</code>. In ra tên Nhân viên và tên Sếp của họ.</p>
    <div class="bg-slate-900 rounded-lg p-3 my-2 text-sm text-green-300 font-mono overflow-x-auto">
      <code>SELECT NhanVien.TenNV AS TenNhanVien, Sep.TenNV AS TenSep<br/>
      FROM NhanVien<br/>
      LEFT JOIN NhanVien AS Sep ON NhanVien.MaNguoiQuanLy = Sep.MaNV;</code>
    </div>

    <h3 class="font-bold text-md mt-6">2. ANTI-JOIN (Tìm kẻ ngoại đạo)</h3>
    <p>Đây là kỹ thuật kinh điển để tìm các bản ghi ở bảng A mà KHÔNG tồn tại ở bảng B.</p>
    <p><em>Bài toán:</em> Tìm các Khách hàng (bảng A) chưa từng mua Đơn hàng nào (bảng B).</p>
    <div class="bg-slate-900 rounded-lg p-3 my-2 text-sm text-yellow-300 font-mono overflow-x-auto">
      <code>SELECT KhachHang.TenKH <br/>
      FROM KhachHang<br/>
      LEFT JOIN DonHang ON KhachHang.MaKH = DonHang.MaKH<br/>
      WHERE DonHang.MaDonHang IS NULL; -- Điều kiện cốt lõi của Anti-Join</code>
    </div>

    <h3 class="font-bold text-md mt-6">3. Tối ưu hiệu năng JOIN (Best Practices)</h3>
    <ul class="list-disc pl-5">
      <li><strong>Index trên cột Khóa ngoại:</strong> Đây là bắt buộc. Nếu bạn JOIN 2 bảng triệu dòng mà cột Khóa ngoại không có Index, Database sẽ phải quét Full Table, câu lệnh có thể mất hàng chục phút.</li>
      <li><strong>Lọc trước khi JOIN:</strong> Đừng JOIN 2 bảng siêu bự rồi mới WHERE. Hãy lọc bảng cho nhỏ lại bằng Subquery/CTE rồi mới JOIN.</li>
      <li><strong>Thứ tự bảng trong LEFT JOIN:</strong> Bảng ở bên trái chữ LEFT JOIN phải là bảng chứa toàn tập dữ liệu bạn muốn bảo toàn. Đặt sai vị trí, kết quả sẽ sai hoàn toàn.</li>
    </ul>
  </div>
</details>
''',

    'Chuẩn hóa 3NF và BCNF': '''
## Phần 1: Khởi động (Tư duy Cốt lõi)

Chuẩn hóa (Normalization) là quá trình "dọn rác" cấu trúc bảng, băm các bảng khổng lồ thành các bảng nhỏ gọn để tránh trùng lặp dữ liệu.

- **1NF:** Không được nhét 2 số điện thoại vào cùng 1 ô dữ liệu.
- **2NF:** Mọi cột phải phụ thuộc vào TOÀN BỘ Khóa chính (Tránh việc cột "Tên Môn Học" lặp lại ngàn lần trong bảng Điểm thi).
- **3NF:** Bỏ qua khâu trung gian! Mọi cột phải phụ thuộc TRỰC TIẾP vào khóa chính. Nếu SinhVien có Mã Khoa, thì đừng lưu Tên Khoa vào bảng SinhVien. Tên Khoa nên nằm ở bảng Khoa riêng.

<div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-6">
  <p class="text-yellow-800 m-0">
    <strong>💡 Tóm gọn siêu tốc:</strong> "Mọi thuộc tính phải phụ thuộc vào khóa (1NF), toàn bộ khóa (2NF), và không gì ngoài khóa (3NF) - Thế là Amen." (Câu thần chú nổi tiếng của Edgar Codd).
  </p>
</div>

<hr class="my-8" />

## Phần 2: Chuyên sâu Kỹ thuật (Deep Dive)

<details class="group bg-slate-50 border border-slate-200 rounded-lg p-4 cursor-pointer mb-4">
  <summary class="font-bold text-slate-800 text-lg flex justify-between items-center outline-none">
    <span>🔍 Chứng minh Toán học và Trường hợp vi phạm BCNF</span>
    <span class="transition group-open:rotate-180">⬇️</span>
  </summary>
  <div class="mt-4 pt-4 border-t border-slate-200 text-slate-700">
    
    <h3 class="font-bold text-md mt-0">1. Lý thuyết Phụ thuộc hàm (FD - Functional Dependency)</h3>
    <p>Ký hiệu: $X \\rightarrow Y$ (X xác định Y).<br/>
    Nghĩa là: Bất cứ 2 dòng nào trong bảng có cùng giá trị X, thì chắc chắn phải có cùng giá trị Y.</p>
    <ul class="list-disc pl-5 mt-2">
      <li><strong>2NF Toán học:</strong> Không tồn tại Phụ thuộc hàm bộ phận ($X \\rightarrow Y$, với X chỉ là tập con thực sự của Khóa chính).</li>
      <li><strong>3NF Toán học:</strong> Mọi phụ thuộc hàm $X \\rightarrow Y$ thỏa mãn 1 trong 2 điều kiện: X là Siêu khóa (Superkey), HOẶC Y là thuộc tính khóa (Prime attribute).</li>
    </ul>

    <h3 class="font-bold text-md mt-6">2. Lỗ hổng của 3NF và sự ra đời của BCNF</h3>
    <p>3NF vẫn có kẽ hở cho phép $X \\rightarrow Y$ nếu Y là thuộc tính khóa. Điều này gây lỗi khi bảng có <strong>Nhiều Khóa Ứng Cử chồng lấp lên nhau</strong>.</p>
    
    <div class="bg-red-50 p-3 rounded border border-red-200 mt-2">
      <strong>Case Study Vi phạm BCNF: Bảng Giảng Dạy</strong><br/>
      Bảng: <code>(MãSinhVien, MônHoc, GiaoVien)</code>.<br/>
      - Khóa ứng cử 1: <code>(MãSinhVien, MônHoc)</code>.<br/>
      - Khóa ứng cử 2: <code>(MãSinhVien, GiaoVien)</code> (Giả sử 1 GV chỉ dạy 1 môn).<br/>
      Ta có phụ thuộc hàm: <code>GiaoVien -> MônHoc</code>.<br/>
      Vì <code>MônHoc</code> là thuộc tính khóa, nên bảng này <strong>ĐẠT chuẩn 3NF</strong>!<br/>
      <strong>Hậu quả (Dị thường chèn):</strong> Nếu trường tuyển thêm giáo viên mới dạy môn Hóa, nhưng chưa có sinh viên nào đăng ký, ta không thể `INSERT` dữ liệu được vì `MãSinhVien` là PK không được phép rỗng!
    </div>
    
    <p class="mt-2 font-bold text-emerald-600">Cách BCNF giải quyết:</p>
    <p>Luật BCNF chặt hơn: Mọi $X \\rightarrow Y$ thì X bắt buộc phải là Siêu khóa (Không có ngoại lệ). Trong ví dụ trên, <code>GiaoVien</code> không phải Siêu khóa, nên vi phạm BCNF. Ta băm ra làm 2 bảng: <code>DangKy(MaSV, GiaoVien)</code> và <code>GiangDay(GiaoVien, MonHoc)</code>. Dị thường biến mất!</p>

    <h3 class="font-bold text-md mt-6">3. Đánh đổi (Trade-off) trong thực tế (Denormalization)</h3>
    <p>Trong môi trường Data Warehouse phân tích dữ liệu lớn, việc băm bảng tới 3NF khiến lệnh JOIN quá nhiều, làm hệ thống cực chậm. Người ta cố tình <strong>Khử chuẩn hóa (Denormalization)</strong>: Gom ngược dữ liệu về 1 bảng để đọc siêu nhanh, chấp nhận rủi ro lặp dữ liệu dư thừa. Chuẩn hóa không phải lúc nào cũng là tối ưu nhất!</p>
  </div>
</details>
'''
}

with engine.connect() as conn:
    for title, body in content.items():
        conn.execute(text('UPDATE learning_items SET content_body = :body WHERE title = :title'), {'body': body, 'title': title})
    conn.commit()

print("Deep dive batch applied successfully!")
