-- ============================================================
-- DB LEARNING - SCHEMA AND SEED DATA (COMBINED)
-- ============================================================

-- ============================================================
-- DB LEARNING - MySQL Schema
-- Môn: Cơ sở Dữ liệu - Hệ thống Cá nhân hóa Lộ trình Học tập
-- ============================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ─── 1. USERS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255) NOT NULL,
    avatar_url      VARCHAR(500) DEFAULT NULL,
    role            ENUM('student', 'admin') DEFAULT 'student',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 2. TOPICS ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS topics (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(255) NOT NULL UNIQUE,
    slug            VARCHAR(255) NOT NULL UNIQUE,
    description     TEXT,
    icon            VARCHAR(100) DEFAULT 'book',
    color           VARCHAR(20)  DEFAULT '#6366f1',
    order_index     INT DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 3. LEARNING ITEMS ────────────────────────────────────
CREATE TABLE IF NOT EXISTS learning_items (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    topic_id            INT NOT NULL,
    title               VARCHAR(500) NOT NULL,
    description         TEXT,
    content_type        ENUM('document','video','flashcard_set','quiz') NOT NULL,
    difficulty          ENUM('beginner','intermediate','advanced') NOT NULL DEFAULT 'beginner',
    content_url         VARCHAR(1000) DEFAULT NULL,
    keywords            JSON DEFAULT NULL,
    tfidf_vector        JSON DEFAULT NULL,
    estimated_minutes   INT DEFAULT 15,
    view_count          INT DEFAULT 0,
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE RESTRICT,
    INDEX idx_topic (topic_id),
    INDEX idx_content_type (content_type),
    INDEX idx_difficulty (difficulty)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 4. FLASHCARDS ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS flashcards (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    item_id         INT NOT NULL,
    question        TEXT NOT NULL,
    answer          TEXT NOT NULL,
    hint            VARCHAR(500) DEFAULT NULL,
    order_index     INT DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES learning_items(id) ON DELETE CASCADE,
    INDEX idx_item (item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 5. QUIZZES ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS quizzes (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    item_id                 INT NOT NULL UNIQUE,
    title                   VARCHAR(500) NOT NULL,
    description             TEXT,
    time_limit_minutes      INT DEFAULT 30,
    pass_score              INT DEFAULT 60,
    shuffle_questions       BOOLEAN DEFAULT TRUE,
    total_questions         INT DEFAULT 0,
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES learning_items(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 6. QUESTIONS ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS questions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    quiz_id         INT NOT NULL,
    topic_id        INT NOT NULL,
    content         TEXT NOT NULL,
    options         JSON NOT NULL,
    correct_option  INT NOT NULL,
    explanation     TEXT DEFAULT NULL,
    difficulty      ENUM('easy','medium','hard') DEFAULT 'medium',
    order_index     INT DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE RESTRICT,
    INDEX idx_quiz (quiz_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 7. LEARNING SESSIONS ─────────────────────────────────
CREATE TABLE IF NOT EXISTS learning_sessions (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL,
    item_id             INT NOT NULL,
    started_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    ended_at            DATETIME DEFAULT NULL,
    duration_seconds    INT DEFAULT 0,
    completion_rate     FLOAT DEFAULT 0.0,
    interaction_score   FLOAT DEFAULT 0.0,
    status              ENUM('in_progress','completed','abandoned') DEFAULT 'in_progress',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES learning_items(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_user_item (user_id, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 8. FLASHCARD LOGS ────────────────────────────────────
CREATE TABLE IF NOT EXISTS flashcard_logs (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL,
    flashcard_id        INT NOT NULL,
    result              ENUM('correct','incorrect','skipped') NOT NULL,
    response_time_ms    INT DEFAULT 0,
    answered_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_user_flashcard (user_id, flashcard_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 9. QUIZ RESULTS ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS quiz_results (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL,
    quiz_id             INT NOT NULL,
    score               FLOAT NOT NULL DEFAULT 0,
    total_questions     INT NOT NULL,
    correct_answers     INT NOT NULL DEFAULT 0,
    answers             JSON DEFAULT NULL,
    time_spent_seconds  INT DEFAULT 0,
    is_passed           BOOLEAN DEFAULT FALSE,
    taken_at            DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_user_quiz (user_id, quiz_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 10. LEARNING PROFILES ────────────────────────────────
CREATE TABLE IF NOT EXISTS learning_profiles (
    user_id                 INT PRIMARY KEY,
    topic_scores            JSON DEFAULT NULL,
    difficulty_distribution JSON DEFAULT NULL,
    preferred_difficulty    ENUM('beginner','intermediate','advanced') DEFAULT 'beginner',
    profile_vector          JSON DEFAULT NULL,
    total_study_hours       FLOAT DEFAULT 0.0,
    total_items_completed   INT DEFAULT 0,
    total_quizzes_taken     INT DEFAULT 0,
    avg_quiz_score          FLOAT DEFAULT 0.0,
    last_updated            DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 11. RECOMMENDATIONS ──────────────────────────────────
CREATE TABLE IF NOT EXISTS recommendations (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    item_id         INT NOT NULL,
    score           FLOAT NOT NULL DEFAULT 0.0,
    reason          VARCHAR(500) DEFAULT NULL,
    rec_type        ENUM('content','path','review') DEFAULT 'content',
    is_clicked      BOOLEAN DEFAULT FALSE,
    generated_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    clicked_at      DATETIME DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES learning_items(id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_item (user_id, item_id),
    INDEX idx_user_score (user_id, score DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─── 12. LEARNING PATHS ───────────────────────────────────
CREATE TABLE IF NOT EXISTS learning_paths (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    user_id             INT NOT NULL,
    title               VARCHAR(500) DEFAULT 'Lộ trình học của tôi',
    item_sequence       JSON DEFAULT NULL,
    progress_percent    FLOAT DEFAULT 0.0,
    is_active           BOOLEAN DEFAULT TRUE,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================
-- SEED DATA - Dữ liệu mẫu cho hệ thống DB Learning
-- ============================================================

SET NAMES utf8mb4;

-- ─── TOPICS ───────────────────────────────────────────────
INSERT INTO topics (name, slug, description, icon, color, order_index) VALUES
('Giới thiệu Cơ sở Dữ liệu', 'gioi-thieu-csdl', 'Khái niệm cơ bản về CSDL, DBMS và kiến trúc hệ thống', 'database', '#6366f1', 1),
('Mô hình Thực thể - Liên kết (ER)', 'mo-hinh-er', 'Thiết kế CSDL bằng mô hình ER, thực thể, thuộc tính, mối quan hệ', 'diagram', '#8b5cf6', 2),
('Mô hình Quan hệ', 'mo-hinh-quan-he', 'Lược đồ quan hệ, khóa chính, khóa ngoại, đại số quan hệ', 'table', '#ec4899', 3),
('SQL Cơ bản', 'sql-co-ban', 'DDL, DML, DQL - Tạo bảng, thêm/sửa/xóa và truy vấn dữ liệu', 'code', '#f59e0b', 4),
('SQL Nâng cao', 'sql-nang-cao', 'JOIN, Subquery, View, Stored Procedure, Trigger', 'code-branch', '#10b981', 5),
('Chuẩn hóa Dữ liệu', 'chuan-hoa', 'Các dạng chuẩn 1NF, 2NF, 3NF, BCNF và phụ thuộc hàm', 'filter', '#3b82f6', 6),
('Giao dịch & Kiểm soát Tương tranh', 'giao-dich', 'Transaction, ACID, Concurrency Control, Deadlock', 'refresh', '#ef4444', 7),
('Chỉ mục & Tối ưu Truy vấn', 'chi-muc-toi-uu', 'Index, Query Optimization, Execution Plan', 'zap', '#f97316', 8),
('NoSQL Cơ bản', 'nosql', 'Giới thiệu MongoDB, so sánh SQL và NoSQL', 'server', '#06b6d4', 9);

-- ─── LEARNING ITEMS ───────────────────────────────────────

-- Topic 1: Giới thiệu CSDL
INSERT INTO learning_items (topic_id, title, description, content_type, difficulty, content_url, keywords, estimated_minutes) VALUES
(1, 'Tổng quan về Cơ sở Dữ liệu', 'Giới thiệu khái niệm CSDL, DBMS, ưu điểm của CSDL so với hệ thống file truyền thống', 'document', 'beginner', '/static/documents/tong-quan-csdl.pdf', '["cơ sở dữ liệu", "DBMS", "database", "hệ quản trị", "dữ liệu"]', 20),
(1, 'Kiến trúc Hệ thống CSDL', 'Ba tầng kiến trúc ANSI/SPARC: nội tại, khái niệm, ngoài. Tính độc lập dữ liệu', 'document', 'beginner', '/static/documents/kien-truc-csdl.pdf', '["kiến trúc", "ANSI SPARC", "tầng vật lý", "tầng khái niệm", "độc lập dữ liệu"]', 25),
(1, 'Các mô hình Dữ liệu', 'So sánh mô hình phân cấp, mạng, quan hệ và hướng đối tượng', 'document', 'beginner', '/static/documents/cac-mo-hinh-dl.pdf', '["mô hình dữ liệu", "quan hệ", "phân cấp", "mạng", "hướng đối tượng"]', 20),
(1, 'Kiểm tra: Giới thiệu CSDL', 'Bài kiểm tra kiến thức về khái niệm CSDL và DBMS', 'quiz', 'beginner', NULL, '["cơ sở dữ liệu", "DBMS", "kiến trúc", "mô hình dữ liệu"]', 15),

-- Topic 2: Mô hình ER
(2, 'Mô hình ER: Thực thể và Thuộc tính', 'Khái niệm thực thể, tập thực thể, thuộc tính đơn, đa trị, dẫn xuất, khóa', 'document', 'beginner', '/static/documents/er-thuc-the.pdf', '["thực thể", "thuộc tính", "ER diagram", "khóa", "entity", "attribute"]', 25),
(2, 'Mô hình ER: Mối Quan hệ', 'Mối quan hệ, bậc, lực lượng tham gia, ràng buộc toàn vẹn tham chiếu', 'document', 'intermediate', '/static/documents/er-quan-he.pdf', '["mối quan hệ", "cardinality", "1-1", "1-n", "n-n", "ràng buộc", "relationship"]', 30),
(2, 'Thực hành vẽ ER Diagram', 'Hướng dẫn vẽ sơ đồ ER cho bài toán quản lý sinh viên, quản lý bán hàng', 'document', 'intermediate', '/static/documents/er-thuc-hanh.pdf', '["ER diagram", "vẽ sơ đồ", "thực hành", "quản lý sinh viên", "ERD"]', 35),
(2, 'Bộ Flashcard: Mô hình ER', 'Ôn tập nhanh các khái niệm mô hình ER', 'flashcard_set', 'beginner', NULL, '["ER diagram", "thực thể", "thuộc tính", "mối quan hệ", "khóa"]', 20),
(2, 'Kiểm tra: Mô hình ER', 'Bài kiểm tra về mô hình thực thể liên kết', 'quiz', 'intermediate', NULL, '["thực thể", "mối quan hệ", "ER diagram", "cardinality", "khóa"]', 20),

-- Topic 3: Mô hình Quan hệ
(3, 'Lược đồ Quan hệ', 'Khái niệm quan hệ, lược đồ quan hệ, bộ, thuộc tính, miền giá trị', 'document', 'beginner', '/static/documents/luoc-do-quan-he.pdf', '["lược đồ quan hệ", "bộ", "thuộc tính", "relation", "tuple", "domain"]', 25),
(3, 'Khóa và Ràng buộc Toàn vẹn', 'Siêu khóa, khóa ứng cử, khóa chính, khóa ngoại, ràng buộc toàn vẹn', 'document', 'intermediate', '/static/documents/khoa-rang-buoc.pdf', '["khóa chính", "khóa ngoại", "primary key", "foreign key", "ràng buộc", "toàn vẹn"]', 30),
(3, 'Đại số Quan hệ', 'Các phép toán: chọn, chiếu, tích Descartes, kết nối tự nhiên, phép trừ, hợp', 'document', 'advanced', '/static/documents/dai-so-quan-he.pdf', '["đại số quan hệ", "phép chiếu", "phép chọn", "kết nối", "join", "select", "project"]', 40),
(3, 'Bộ Flashcard: Mô hình Quan hệ', 'Ôn tập khóa, ràng buộc và đại số quan hệ', 'flashcard_set', 'intermediate', NULL, '["khóa chính", "khóa ngoại", "đại số quan hệ", "ràng buộc toàn vẹn"]', 20),
(3, 'Kiểm tra: Mô hình Quan hệ', 'Bài kiểm tra về lược đồ quan hệ và đại số quan hệ', 'quiz', 'intermediate', NULL, '["lược đồ quan hệ", "khóa", "đại số quan hệ", "ràng buộc"]', 20),

-- Topic 4: SQL Cơ bản
(4, 'SQL DDL: Tạo và Quản lý Bảng', 'CREATE TABLE, ALTER TABLE, DROP TABLE, kiểu dữ liệu MySQL, ràng buộc', 'document', 'beginner', '/static/documents/sql-ddl.pdf', '["DDL", "CREATE TABLE", "ALTER TABLE", "DROP", "SQL", "kiểu dữ liệu"]', 30),
(4, 'SQL DML: Thêm Sửa Xóa Dữ liệu', 'INSERT INTO, UPDATE, DELETE, TRUNCATE với ví dụ thực tế', 'document', 'beginner', '/static/documents/sql-dml.pdf', '["DML", "INSERT", "UPDATE", "DELETE", "SQL", "thêm sửa xóa"]', 25),
(4, 'SQL DQL: Truy vấn Dữ liệu', 'SELECT, WHERE, ORDER BY, GROUP BY, HAVING, DISTINCT, LIMIT', 'document', 'beginner', '/static/documents/sql-dql.pdf', '["DQL", "SELECT", "WHERE", "ORDER BY", "GROUP BY", "HAVING", "SQL query"]', 35),
(4, 'Hàm Tổng hợp trong SQL', 'COUNT, SUM, AVG, MAX, MIN và cách kết hợp với GROUP BY', 'document', 'beginner', '/static/documents/sql-aggregate.pdf', '["aggregate function", "COUNT", "SUM", "AVG", "MAX", "MIN", "GROUP BY"]', 25),
(4, 'Bộ Flashcard: SQL Cơ bản', 'Ôn tập nhanh cú pháp SQL DDL, DML, DQL', 'flashcard_set', 'beginner', NULL, '["SQL", "DDL", "DML", "SELECT", "INSERT", "UPDATE", "DELETE"]', 25),
(4, 'Kiểm tra: SQL Cơ bản', 'Bài kiểm tra về DDL, DML và truy vấn SELECT cơ bản', 'quiz', 'beginner', NULL, '["SQL", "CREATE TABLE", "INSERT", "SELECT", "WHERE", "GROUP BY"]', 25),

-- Topic 5: SQL Nâng cao
(5, 'SQL JOIN: Kết nối Bảng', 'INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN, CROSS JOIN với ví dụ minh họa', 'document', 'intermediate', '/static/documents/sql-join.pdf', '["JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "kết nối bảng", "SQL nâng cao"]', 35),
(5, 'Subquery và CTE', 'Subquery trong SELECT, WHERE, FROM. Common Table Expression (WITH)', 'document', 'intermediate', '/static/documents/sql-subquery.pdf', '["subquery", "CTE", "WITH", "câu truy vấn con", "EXISTS", "IN"]', 35),
(5, 'View trong SQL', 'Tạo, sử dụng và quản lý View. Updatable View', 'document', 'intermediate', '/static/documents/sql-view.pdf', '["VIEW", "CREATE VIEW", "virtual table", "updatable view"]', 25),
(5, 'Stored Procedure và Trigger', 'Tạo và sử dụng Stored Procedure, Function, Trigger trong MySQL', 'document', 'advanced', '/static/documents/sql-procedure.pdf', '["stored procedure", "trigger", "function", "MySQL", "DELIMITER"]', 40),
(5, 'Bộ Flashcard: SQL Nâng cao', 'Ôn tập JOIN, Subquery, View và Stored Procedure', 'flashcard_set', 'intermediate', NULL, '["JOIN", "subquery", "VIEW", "stored procedure", "trigger"]', 25),
(5, 'Kiểm tra: SQL Nâng cao', 'Bài kiểm tra về JOIN, Subquery và View', 'quiz', 'intermediate', NULL, '["JOIN", "INNER JOIN", "LEFT JOIN", "subquery", "VIEW", "CTE"]', 25),

-- Topic 6: Chuẩn hóa
(6, 'Phụ thuộc Hàm', 'Khái niệm phụ thuộc hàm, phụ thuộc hàm đầy đủ, bộ phận, bắc cầu', 'document', 'intermediate', '/static/documents/phu-thuoc-ham.pdf', '["phụ thuộc hàm", "functional dependency", "đầy đủ", "bộ phận", "bắc cầu"]', 30),
(6, 'Chuẩn hóa 1NF và 2NF', 'Dạng chuẩn 1 và 2, cách đưa lược đồ về dạng chuẩn, ví dụ minh họa', 'document', 'intermediate', '/static/documents/1nf-2nf.pdf', '["1NF", "2NF", "chuẩn hóa", "normalization", "phụ thuộc bộ phận"]', 35),
(6, 'Chuẩn hóa 3NF và BCNF', 'Dạng chuẩn 3 và Boyce-Codd, so sánh, khi nào dùng BCNF', 'document', 'advanced', '/static/documents/3nf-bcnf.pdf', '["3NF", "BCNF", "Boyce-Codd", "phụ thuộc bắc cầu", "chuẩn hóa cao"]', 35),
(6, 'Bộ Flashcard: Chuẩn hóa', 'Ôn tập các dạng chuẩn và phụ thuộc hàm', 'flashcard_set', 'intermediate', NULL, '["1NF", "2NF", "3NF", "BCNF", "phụ thuộc hàm", "chuẩn hóa"]', 20),
(6, 'Kiểm tra: Chuẩn hóa', 'Bài kiểm tra về phụ thuộc hàm và chuẩn hóa dữ liệu', 'quiz', 'advanced', NULL, '["1NF", "2NF", "3NF", "BCNF", "phụ thuộc hàm", "normalization"]', 20),

-- Topic 7: Giao dịch
(7, 'Giao dịch và Thuộc tính ACID', 'Khái niệm transaction, 4 thuộc tính ACID: Atomicity, Consistency, Isolation, Durability', 'document', 'intermediate', '/static/documents/transaction-acid.pdf', '["transaction", "giao dịch", "ACID", "atomicity", "consistency", "isolation", "durability"]', 30),
(7, 'Kiểm soát Tương tranh', 'Vấn đề đọc bẩn, đọc không lặp lại, phantom read. Lock-based và timestamp protocol', 'document', 'advanced', '/static/documents/tuong-tranh.pdf', '["concurrency control", "tương tranh", "lock", "deadlock", "isolation level", "dirty read"]', 40),
(7, 'Phục hồi Dữ liệu', 'Log-based recovery, checkpoint, UNDO, REDO', 'document', 'advanced', '/static/documents/phuc-hoi.pdf', '["recovery", "phục hồi", "log", "checkpoint", "UNDO", "REDO", "crash recovery"]', 30),
(7, 'Bộ Flashcard: Giao dịch', 'Ôn tập ACID, concurrency và recovery', 'flashcard_set', 'intermediate', NULL, '["ACID", "transaction", "concurrency", "lock", "recovery", "deadlock"]', 20),
(7, 'Kiểm tra: Giao dịch', 'Bài kiểm tra về transaction và kiểm soát tương tranh', 'quiz', 'advanced', NULL, '["ACID", "transaction", "concurrency control", "isolation", "lock", "deadlock"]', 20),

-- Topic 8: Chỉ mục
(8, 'Chỉ mục (Index) trong CSDL', 'B-Tree Index, Hash Index, cách tạo và sử dụng Index trong MySQL', 'document', 'intermediate', '/static/documents/index.pdf', '["index", "chỉ mục", "B-tree", "hash index", "CREATE INDEX", "tối ưu"]', 30),
(8, 'Tối ưu hóa Truy vấn SQL', 'EXPLAIN ANALYZE, query optimization, tránh full table scan', 'document', 'advanced', '/static/documents/query-optimization.pdf', '["query optimization", "tối ưu truy vấn", "EXPLAIN", "execution plan", "index", "performance"]', 35),
(8, 'Kiểm tra: Chỉ mục & Tối ưu', 'Bài kiểm tra về Index và tối ưu hóa truy vấn', 'quiz', 'advanced', NULL, '["index", "B-tree", "query optimization", "EXPLAIN", "tối ưu"]', 15),

-- Topic 9: NoSQL
(9, 'Giới thiệu NoSQL', 'Lịch sử, các loại NoSQL: Document, Key-Value, Column, Graph. Khi nào dùng NoSQL', 'document', 'beginner', '/static/documents/nosql-intro.pdf', '["NoSQL", "document database", "key-value", "MongoDB", "so sánh SQL NoSQL"]', 25),
(9, 'MongoDB Cơ bản', 'CRUD trong MongoDB: insertOne, find, updateOne, deleteOne. So sánh với SQL', 'document', 'intermediate', '/static/documents/mongodb-basics.pdf', '["MongoDB", "document", "collection", "BSON", "insertOne", "find", "aggregate"]', 35),
(9, 'Kiểm tra: NoSQL', 'Bài kiểm tra về NoSQL và MongoDB cơ bản', 'quiz', 'intermediate', NULL, '["NoSQL", "MongoDB", "document database", "CRUD", "aggregate"]', 15);

-- ─── FLASHCARDS ───────────────────────────────────────────

-- Flashcard Set: Mô hình ER (item_id = 8)
INSERT INTO flashcards (item_id, question, answer, hint, order_index) VALUES
(8, 'Thực thể (Entity) là gì?', 'Thực thể là một đối tượng hoặc khái niệm tồn tại trong thế giới thực mà chúng ta muốn lưu trữ thông tin. Ví dụ: Sinh viên, Khóa học, Giảng viên.', 'Nghĩ về các "vật" hay "người" trong bài toán', 1),
(8, 'Thuộc tính (Attribute) là gì?', 'Thuộc tính là đặc trưng mô tả cho thực thể. Ví dụ: Sinh viên có MSSV, họ tên, ngày sinh, địa chỉ.', 'Đặc điểm/tính chất của thực thể', 2),
(8, 'Khóa (Key Attribute) là gì?', 'Khóa là thuộc tính hoặc tập thuộc tính có thể xác định duy nhất một thực thể trong tập thực thể. Được gạch chân trong ERD.', 'Thuộc tính giúp phân biệt các thực thể với nhau', 3),
(8, 'Mối quan hệ 1-N là gì? Cho ví dụ.', 'Một thực thể ở phía 1 liên kết với nhiều thực thể ở phía N. Ví dụ: Một Khoa có nhiều Sinh viên, nhưng mỗi Sinh viên chỉ thuộc một Khoa.', '1 → nhiều', 4),
(8, 'Mối quan hệ N-N là gì? Xử lý thế nào?', 'Nhiều thực thể ở phía này liên kết với nhiều thực thể ở phía kia. Ví dụ: Sinh viên đăng ký nhiều Môn học, mỗi Môn học có nhiều Sinh viên. Khi chuyển sang quan hệ, cần tạo bảng trung gian.', 'Cần bảng trung gian khi chuyển sang SQL', 5),
(8, 'Thuộc tính đa trị (Multivalued) là gì?', 'Thuộc tính có thể có nhiều giá trị cho một thực thể. Ví dụ: Số điện thoại (1 người có thể có nhiều SĐT). Ký hiệu bằng hình elip đôi trong ERD.', 'Elip đôi trong ERD', 6),
(8, 'Thuộc tính dẫn xuất (Derived) là gì?', 'Thuộc tính có thể tính được từ thuộc tính khác. Ví dụ: Tuổi tính từ Ngày sinh. Ký hiệu bằng elip nét đứt.', 'Tính được từ thuộc tính khác', 7),
(8, 'Thực thể yếu (Weak Entity) là gì?', 'Thực thể không có đủ thuộc tính để tạo khóa, phải phụ thuộc vào thực thể mạnh. Ví dụ: Người phụ thuộc (của nhân viên). Ký hiệu bằng hình chữ nhật đôi.', 'Không có khóa riêng, phụ thuộc thực thể mạnh', 8),

-- Flashcard Set: Mô hình Quan hệ (item_id = 13)
(13, 'Quan hệ (Relation) là gì?', 'Quan hệ là một bảng 2 chiều gồm các hàng (bộ - tuple) và các cột (thuộc tính - attribute). Mỗi hàng là một bộ dữ liệu.', 'Bảng trong CSDL quan hệ', 1),
(13, 'Khóa chính (Primary Key) là gì?', 'Khóa chính là thuộc tính hoặc tập thuộc tính xác định duy nhất mỗi bộ trong quan hệ. Không được NULL và phải là duy nhất.', 'Duy nhất, không NULL', 2),
(13, 'Khóa ngoại (Foreign Key) là gì?', 'Khóa ngoại là thuộc tính trong quan hệ này tham chiếu đến khóa chính của quan hệ khác. Dùng để thể hiện mối quan hệ giữa các bảng.', 'Tham chiếu đến PK của bảng khác', 3),
(13, 'Phép Chọn (Selection σ) trong đại số quan hệ?', 'Phép chọn lọc các bộ (hàng) thỏa điều kiện. Ký hiệu: σ_điều_kiện(Quan_hệ). Tương đương mệnh đề WHERE trong SQL.', 'WHERE trong SQL', 4),
(13, 'Phép Chiếu (Projection π) trong đại số quan hệ?', 'Phép chiếu lấy một số cột nhất định. Ký hiệu: π_thuộc_tính(Quan_hệ). Tương đương SELECT cột trong SQL.', 'SELECT cột trong SQL', 5),
(13, 'Kết nối tự nhiên (Natural Join ⋈) là gì?', 'Kết hợp hai quan hệ dựa trên thuộc tính chung có cùng tên và giá trị bằng nhau. Kết quả không có cột trùng.', 'Join theo cột có tên giống nhau', 6),

-- Flashcard Set: SQL Cơ bản (item_id = 20)
(20, 'Cú pháp CREATE TABLE cơ bản?', 'CREATE TABLE tên_bảng (\n  cột1 kiểu_dữ_liệu ràng_buộc,\n  cột2 kiểu_dữ_liệu,\n  PRIMARY KEY (cột1)\n);', 'CREATE TABLE tên (cột kiểu...)', 1),
(20, 'Sự khác nhau giữa DELETE và TRUNCATE?', 'DELETE: Xóa từng hàng, có thể dùng WHERE, ghi log, có thể rollback. TRUNCATE: Xóa toàn bộ bảng nhanh hơn, không thể rollback, reset AUTO_INCREMENT.', 'DELETE có WHERE, TRUNCATE không có', 2),
(20, 'GROUP BY dùng để làm gì?', 'GROUP BY nhóm các hàng có cùng giá trị ở cột chỉ định thành một nhóm, thường dùng kết hợp với hàm tổng hợp (COUNT, SUM, AVG...).', 'Nhóm hàng để tính tổng hợp', 3),
(20, 'HAVING khác WHERE như thế nào?', 'WHERE lọc hàng TRƯỚC khi nhóm (trước GROUP BY). HAVING lọc nhóm SAU khi nhóm (sau GROUP BY), có thể dùng hàm tổng hợp trong HAVING.', 'HAVING dùng sau GROUP BY', 4),
(20, 'NULL trong SQL là gì? So sánh NULL thế nào?', 'NULL là giá trị chưa biết/không có. Không dùng = NULL mà phải dùng IS NULL hoặc IS NOT NULL. NULL ≠ NULL trong SQL.', 'IS NULL, IS NOT NULL', 5),
(20, 'Hàm COUNT(*) và COUNT(cột) khác nhau thế nào?', 'COUNT(*) đếm tất cả hàng kể cả NULL. COUNT(cột) chỉ đếm các hàng có giá trị không NULL ở cột đó.', 'COUNT(*) đếm cả NULL', 6),

-- Flashcard Set: SQL Nâng cao (item_id = 26)
(26, 'INNER JOIN trả về kết quả gì?', 'INNER JOIN chỉ trả về các hàng có giá trị khớp nhau ở CẢ HAI bảng. Nếu một bên không có khớp, hàng đó bị loại bỏ.', 'Chỉ hàng khớp ở cả hai bảng', 1),
(26, 'LEFT JOIN khác INNER JOIN như thế nào?', 'LEFT JOIN trả về TẤT CẢ hàng từ bảng bên trái, kể cả khi không có khớp ở bảng bên phải (bên phải sẽ là NULL).', 'Giữ tất cả hàng bảng trái', 2),
(26, 'Subquery là gì? Ví dụ?', 'Subquery là câu truy vấn lồng bên trong câu truy vấn khác. Ví dụ: SELECT * FROM sinhvien WHERE diem > (SELECT AVG(diem) FROM sinhvien)', 'Câu SELECT lồng trong SELECT khác', 3),
(26, 'CTE (Common Table Expression) là gì?', 'CTE dùng từ khóa WITH để đặt tên tạm thời cho kết quả truy vấn. Giúp code dễ đọc hơn subquery phức tạp.\nWITH ten_cte AS (SELECT ...) SELECT * FROM ten_cte', 'WITH ... AS (SELECT ...)', 4),
(26, 'Khi nào dùng EXISTS thay vì IN?', 'EXISTS nhanh hơn khi subquery trả về nhiều hàng vì nó dừng ngay khi tìm thấy 1 kết quả. IN phù hợp với danh sách nhỏ cố định.', 'EXISTS dừng ngay khi tìm thấy', 5),

-- Flashcard Set: Chuẩn hóa (item_id = 31)
(30, '1NF yêu cầu gì?', 'Dạng chuẩn 1 (1NF): Tất cả thuộc tính phải là nguyên tử (không thể phân chia), không có nhóm lặp, mỗi ô chỉ chứa 1 giá trị.', 'Không có giá trị đa trị, không nhóm lặp', 1),
(30, '2NF yêu cầu gì?', 'Dạng chuẩn 2 (2NF): Đạt 1NF và mọi thuộc tính không khóa phải PHỤ THUỘC ĐẦY ĐỦ vào khóa chính (không có phụ thuộc bộ phận).', 'Không có phụ thuộc bộ phận', 2),
(30, '3NF yêu cầu gì?', 'Dạng chuẩn 3 (3NF): Đạt 2NF và không có phụ thuộc bắc cầu (A→B→C, trong đó A là khóa nhưng B không phải khóa).', 'Không có phụ thuộc bắc cầu', 3),
(30, 'Phụ thuộc bắc cầu là gì? Ví dụ?', 'A→B và B→C (B không phải khóa) thì A→C là phụ thuộc bắc cầu. Ví dụ: MSSV→Mã Khoa, Mã Khoa→Tên Khoa → vi phạm 3NF.', 'A→B→C với B không phải khóa', 4),
(30, 'BCNF khác 3NF như thế nào?', 'BCNF (Boyce-Codd NF) chặt hơn 3NF: Với MỌI phụ thuộc hàm X→Y, X phải là siêu khóa. 3NF chấp nhận một số ngoại lệ mà BCNF không chấp nhận.', 'X trong X→Y phải là siêu khóa', 5),

-- Flashcard Set: Giao dịch (item_id = 36)
(35, 'ACID là viết tắt của gì?', 'A - Atomicity (Tính nguyên tử): Tất cả hoặc không có gì\nC - Consistency (Nhất quán): Dữ liệu luôn hợp lệ\nI - Isolation (Cô lập): Giao dịch độc lập nhau\nD - Durability (Bền vững): Kết quả được lưu vĩnh viễn', 'Atomicity, Consistency, Isolation, Durability', 1),
(35, 'Dirty Read là gì?', 'Dirty Read xảy ra khi một giao dịch đọc dữ liệu đã được sửa đổi bởi giao dịch khác CHƯA COMMIT. Nếu giao dịch kia rollback, dữ liệu đã đọc là sai.', 'Đọc dữ liệu chưa commit', 2),
(35, 'Deadlock là gì? Xử lý thế nào?', 'Deadlock: Hai giao dịch chờ nhau giải phóng tài nguyên → cả hai bị kẹt mãi. Xử lý: Timeout (hủy 1 giao dịch), Wait-for graph (phát hiện chu trình).', 'Hai giao dịch chờ nhau vô hạn', 3),
(35, 'COMMIT và ROLLBACK khác nhau thế nào?', 'COMMIT: Xác nhận tất cả thay đổi trong giao dịch được lưu vĩnh viễn vào CSDL. ROLLBACK: Hủy bỏ tất cả thay đổi, khôi phục về trạng thái trước giao dịch.', 'COMMIT lưu, ROLLBACK hủy', 4);

-- ─── QUIZZES ──────────────────────────────────────────────
INSERT INTO quizzes (item_id, title, description, time_limit_minutes, pass_score, total_questions) VALUES
(4,  'Kiểm tra: Giới thiệu CSDL', 'Kiểm tra kiến thức về khái niệm CSDL và DBMS', 15, 60, 10),
(9,  'Kiểm tra: Mô hình ER', 'Kiểm tra về mô hình thực thể liên kết', 20, 60, 10),
(14, 'Kiểm tra: Mô hình Quan hệ', 'Kiểm tra về lược đồ quan hệ và đại số quan hệ', 20, 60, 10),
(20, 'Kiểm tra: SQL Cơ bản', 'Kiểm tra về DDL, DML và truy vấn SELECT', 25, 60, 12),
(26, 'Kiểm tra: SQL Nâng cao', 'Kiểm tra về JOIN, Subquery và View', 25, 65, 12),
(31, 'Kiểm tra: Chuẩn hóa', 'Kiểm tra về phụ thuộc hàm và chuẩn hóa', 20, 60, 10),
(36, 'Kiểm tra: Giao dịch', 'Kiểm tra về ACID và concurrency control', 20, 60, 10),
(39, 'Kiểm tra: Chỉ mục & Tối ưu', 'Kiểm tra về Index và tối ưu truy vấn', 15, 60, 8),
(42, 'Kiểm tra: NoSQL', 'Kiểm tra về NoSQL và MongoDB', 15, 60, 8);

-- ─── QUESTIONS ────────────────────────────────────────────

-- Quiz 1: Giới thiệu CSDL
INSERT INTO questions (quiz_id, topic_id, content, options, correct_option, explanation, difficulty) VALUES
(1, 1, 'DBMS là viết tắt của gì?',
 '["Database Management System", "Data Backup Management System", "Dynamic Base Management System", "Database Monitoring System"]',
 0, 'DBMS = Database Management System (Hệ Quản trị Cơ sở Dữ liệu)', 'easy'),
(1, 1, 'Ưu điểm nào sau đây là của CSDL so với hệ thống file?',
 '["Tốn ít dung lượng lưu trữ hơn", "Tránh dư thừa và không nhất quán dữ liệu", "Chạy nhanh hơn file thông thường", "Không cần backup"]',
 1, 'CSDL giúp tránh dư thừa (redundancy) và không nhất quán (inconsistency) nhờ chuẩn hóa và ràng buộc toàn vẹn', 'easy'),
(1, 1, 'Tính độc lập dữ liệu vật lý (Physical Data Independence) có nghĩa là gì?',
 '["Thay đổi cấu trúc logic không ảnh hưởng ứng dụng", "Thay đổi cách lưu trữ vật lý không ảnh hưởng đến lược đồ khái niệm", "Dữ liệu được mã hóa", "Ứng dụng độc lập với phần cứng"]',
 1, 'Độc lập vật lý: thay đổi cách lưu (index, file organization) không ảnh hưởng lược đồ khái niệm và ứng dụng', 'medium'),
(1, 1, 'Kiến trúc ANSI/SPARC có bao nhiêu tầng?',
 '["2 tầng", "3 tầng", "4 tầng", "5 tầng"]',
 1, 'ANSI/SPARC gồm 3 tầng: Ngoài (External), Khái niệm (Conceptual), Nội tại (Internal)', 'easy'),
(1, 1, 'DBA là viết tắt của gì?',
 '["Database Backup Administrator", "Database Administrator", "Data Base Application", "Dynamic Base Access"]',
 1, 'DBA = Database Administrator (Quản trị viên Cơ sở Dữ liệu)', 'easy'),

-- Quiz 2: Mô hình ER
(2, 2, 'Trong ERD, hình chữ nhật biểu diễn gì?',
 '["Thuộc tính", "Thực thể", "Mối quan hệ", "Khóa"]',
 1, 'Trong ký hiệu ERD chuẩn: Hình chữ nhật = Thực thể, Hình thoi = Mối quan hệ, Elip = Thuộc tính', 'easy'),
(2, 2, 'Thực thể yếu (Weak Entity) khác thực thể mạnh ở điểm nào?',
 '["Có ít thuộc tính hơn", "Không có khóa riêng, phụ thuộc vào thực thể mạnh", "Không có mối quan hệ", "Chỉ tồn tại trong lý thuyết"]',
 1, 'Thực thể yếu không đủ thuộc tính để tạo khóa duy nhất, phải phụ thuộc vào thực thể mạnh qua mối quan hệ xác định', 'medium'),
(2, 2, 'Mối quan hệ N-N khi chuyển sang mô hình quan hệ cần làm gì?',
 '["Xóa một trong hai thực thể", "Tạo bảng trung gian", "Thêm khóa ngoại vào một bảng", "Gộp hai bảng làm một"]',
 1, 'Quan hệ N-N cần bảng trung gian chứa khóa ngoại của cả hai thực thể, thường cộng thêm thuộc tính của mối quan hệ', 'medium'),
(2, 2, 'Thuộc tính đa trị (Multivalued Attribute) được ký hiệu trong ERD bằng?',
 '["Hình chữ nhật đôi", "Elip đôi", "Hình thoi đôi", "Elip nét đứt"]',
 1, 'Elip đôi = thuộc tính đa trị. Elip nét đứt = thuộc tính dẫn xuất. Hình chữ nhật đôi = thực thể yếu', 'medium'),
(2, 2, 'Tỉ lệ lực lượng (Cardinality) 1:N có nghĩa là?',
 '["Một thực thể A liên kết với đúng 1 thực thể B", "Một thực thể A liên kết với nhiều thực thể B", "Nhiều thực thể A liên kết với nhiều thực thể B", "Không có ràng buộc số lượng"]',
 1, 'Cardinality 1:N: 1 thực thể phía 1 liên kết với nhiều (N) thực thể phía N. Ví dụ: 1 Khoa có nhiều Sinh viên', 'easy'),

-- Quiz 3: SQL Cơ bản
(4, 4, 'Câu lệnh nào dùng để tạo bảng mới trong SQL?',
 '["INSERT TABLE", "CREATE TABLE", "MAKE TABLE", "NEW TABLE"]',
 1, 'CREATE TABLE là lệnh DDL dùng để tạo bảng mới với định nghĩa cột và ràng buộc', 'easy'),
(4, 4, 'Mệnh đề WHERE trong SELECT dùng để làm gì?',
 '["Sắp xếp kết quả", "Nhóm các hàng", "Lọc hàng theo điều kiện", "Chọn cột hiển thị"]',
 2, 'WHERE lọc hàng thỏa điều kiện. ORDER BY sắp xếp. GROUP BY nhóm. SELECT chọn cột', 'easy'),
(4, 4, 'Sự khác nhau giữa CHAR(10) và VARCHAR(10) trong MySQL?',
 '["Không có khác biệt", "CHAR luôn dùng đúng 10 byte, VARCHAR dùng số byte thực tế +1-2", "VARCHAR nhanh hơn CHAR", "CHAR cho phép Unicode, VARCHAR thì không"]',
 1, 'CHAR(10): cố định 10 byte dù chuỗi ngắn hơn. VARCHAR(10): lưu số byte thực tế + 1-2 byte lưu độ dài → tiết kiệm hơn', 'medium'),
(4, 4, 'Câu lệnh SQL nào sau đây đúng cú pháp?',
 '["SELECT * WHERE name = ''Nam'' FROM users", "FROM users SELECT * WHERE name = ''Nam''", "SELECT * FROM users WHERE name = ''Nam''", "SELECT FROM users * WHERE name = ''Nam''"]',
 2, 'Thứ tự chuẩn: SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT', 'easy'),
(4, 4, 'Hàm COUNT(*) khác COUNT(column) như thế nào?',
 '["Không khác nhau", "COUNT(*) đếm cả hàng có NULL, COUNT(column) bỏ qua NULL", "COUNT(*) chậm hơn", "COUNT(column) đếm cả NULL"]',
 1, 'COUNT(*) đếm tất cả hàng. COUNT(column) chỉ đếm hàng có giá trị không NULL ở cột đó', 'medium'),

-- Quiz 4: SQL Nâng cao
(5, 5, 'INNER JOIN trả về kết quả gì?',
 '["Tất cả hàng từ bảng trái", "Tất cả hàng từ bảng phải", "Chỉ các hàng có giá trị khớp ở cả hai bảng", "Tất cả hàng từ cả hai bảng"]',
 2, 'INNER JOIN chỉ trả về hàng có giá trị khớp ở CẢ HAI bảng theo điều kiện ON', 'easy'),
(5, 5, 'LEFT JOIN khác INNER JOIN ở điểm nào?',
 '["LEFT JOIN nhanh hơn", "LEFT JOIN giữ tất cả hàng bảng trái, kể cả khi không có khớp", "LEFT JOIN chỉ lấy bảng bên trái", "Không có khác biệt"]',
 1, 'LEFT JOIN giữ TẤT CẢ hàng bảng trái. Nếu không có khớp ở phải, cột bảng phải sẽ là NULL', 'medium'),
(5, 5, 'Subquery có thể đặt ở đâu trong câu SELECT?',
 '["Chỉ trong mệnh đề WHERE", "Chỉ trong mệnh đề FROM", "Trong SELECT, FROM, WHERE, HAVING", "Chỉ sau ORDER BY"]',
 2, 'Subquery có thể đặt trong SELECT (scalar), FROM (derived table), WHERE/HAVING (filter)', 'medium'),

-- Quiz 5: Chuẩn hóa
(6, 6, '1NF yêu cầu gì?',
 '["Không có phụ thuộc bộ phận", "Tất cả thuộc tính là nguyên tử, không có nhóm lặp", "Không có phụ thuộc bắc cầu", "Mọi thuộc tính phụ thuộc vào siêu khóa"]',
 1, '1NF: Thuộc tính nguyên tử (atomic), không có nhóm lặp, mỗi ô 1 giá trị', 'easy'),
(6, 6, 'Lược đồ vi phạm 2NF khi nào?',
 '["Có thuộc tính đa trị", "Có thuộc tính không khóa phụ thuộc bộ phận vào khóa chính", "Có phụ thuộc bắc cầu", "Không có khóa chính"]',
 1, 'Vi phạm 2NF khi thuộc tính không khóa chỉ phụ thuộc vào MỘT PHẦN khóa chính (phụ thuộc bộ phận)', 'medium'),
(6, 6, 'Phụ thuộc bắc cầu xảy ra khi nào?',
 '["A→B và A→C", "A→B và B→C với B không phải khóa", "A→B và B→A", "Không có phụ thuộc hàm"]',
 1, 'Phụ thuộc bắc cầu: A→B, B→C (B không phải khóa). Khi A là khóa, C phụ thuộc bắc cầu vi phạm 3NF', 'medium'),

-- Quiz 6: Giao dịch
(7, 7, 'ACID trong giao dịch CSDL là viết tắt của?',
 '["Atomicity, Consistency, Isolation, Durability", "Accuracy, Consistency, Integrity, Data", "Atomicity, Concurrency, Isolation, Dependency", "Availability, Consistency, Integrity, Durability"]',
 0, 'ACID: Atomicity (nguyên tử), Consistency (nhất quán), Isolation (cô lập), Durability (bền vững)', 'easy'),
(7, 7, 'Tính Atomicity trong giao dịch có nghĩa là?',
 '["Giao dịch chạy nhanh như nguyên tử", "Giao dịch hoặc thực hiện toàn bộ hoặc không thực hiện gì", "Giao dịch nhỏ nhất có thể", "Giao dịch không thể chia nhỏ về mặt vật lý"]',
 1, 'Atomicity: All-or-nothing. Nếu một bước thất bại, toàn bộ giao dịch rollback về trạng thái ban đầu', 'easy'),
(7, 7, 'Dirty Read xảy ra khi nào?',
 '["Đọc dữ liệu đã xóa", "Đọc dữ liệu đã được commit", "Đọc dữ liệu đã sửa nhưng chưa commit bởi giao dịch khác", "Đọc dữ liệu bị lỗi định dạng"]',
 2, 'Dirty Read: Giao dịch T1 đọc dữ liệu mà T2 đã sửa nhưng chưa commit. Nếu T2 rollback, T1 đọc dữ liệu sai', 'medium');

-- ─── ADMIN USER ───────────────────────────────────────────
-- Password: Admin@123 (đã hash bằng bcrypt)
INSERT INTO users (email, password_hash, full_name, role) VALUES
('admin@dblearning.edu.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaijsWGUxOaT3pS9pWtGXmhIO', 'Quản trị viên', 'admin'),
('demo@student.edu.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaijsWGUxOaT3pS9pWtGXmhIO', 'Sinh viên Demo', 'student');


-- Added from missing questions fix --
﻿SET NAMES utf8mb4;

-- Xóa các câu hỏi bị lỗi font vừa nãy (quiz_id = 8 và quiz_id = 9)
DELETE FROM questions WHERE quiz_id IN (8, 9);

-- Seed questions for Quiz 8: Chỉ mục & Tối ưu (Topic ID 8)
INSERT INTO questions (quiz_id, topic_id, content, options, correct_option, explanation, difficulty, order_index) VALUES 
(8, 8, 'Chỉ mục (Index) trong CSDL là gì?', '["Một bảng ảo", "Một cấu trúc dữ liệu giúp tăng tốc độ truy xuất dữ liệu", "Một loại khóa ngoại", "Một thủ tục lưu trữ"]', 1, 'Index là cấu trúc dữ liệu được sử dụng để nhanh chóng định vị và truy cập dữ liệu.', 'easy', 1),
(8, 8, 'Loại chỉ mục nào sắp xếp các hàng dữ liệu vật lý trong bảng?', '["Non-clustered index", "Clustered index", "Unique index", "Full-text index"]', 1, 'Clustered index quyết định thứ tự lưu trữ vật lý của các dòng dữ liệu trong bảng.', 'medium', 2),
(8, 8, 'Nhược điểm của việc tạo quá nhiều chỉ mục là gì?', '["Tăng tốc độ INSERT, UPDATE, DELETE", "Giảm tốc độ SELECT", "Giảm tốc độ INSERT, UPDATE, DELETE", "Làm mất dữ liệu"]', 2, 'Mỗi khi dữ liệu thay đổi, các chỉ mục cũng phải được cập nhật, làm chậm các thao tác ghi dữ liệu.', 'easy', 3),
(8, 8, 'Lệnh SQL nào dùng để tạo chỉ mục trên một cột?', '["ADD INDEX index_name ON table_name(column_name)", "CREATE INDEX index_name ON table_name(column_name)", "MAKE INDEX index_name FOR table_name(column_name)", "BUILD INDEX index_name ON table_name(column_name)"]', 1, 'Cú pháp chuẩn là CREATE INDEX...', 'easy', 4),
(8, 8, 'Chỉ mục B-Tree đặc biệt hiệu quả cho loại truy vấn nào?', '["Truy vấn MATCH", "Truy vấn LIKE %abc", "Truy vấn khoảng (Range queries) như BETWEEN, <, >", "Truy vấn nối chuỗi"]', 2, 'Cấu trúc B-Tree giúp tìm kiếm các giá trị trong một khoảng một cách rất nhanh chóng.', 'medium', 5),
(8, 8, 'Tối ưu hóa truy vấn (Query Optimization) là quá trình gì?', '["Viết lại câu truy vấn bằng ngôn ngữ lập trình", "Chọn kế hoạch thực thi hiệu quả nhất cho câu truy vấn", "Nén dữ liệu để truy vấn chạy nhanh hơn", "Xóa các dữ liệu không cần thiết"]', 1, 'Trình tối ưu hóa của DBMS sẽ phân tích và chọn ra execution plan tối ưu nhất.', 'medium', 6),
(8, 8, 'Trong kế hoạch thực thi (Execution Plan), phép toán "Table Scan" (hoặc "Full Table Scan") có ý nghĩa gì?', '["Quét toàn bộ dữ liệu trong bảng để tìm kết quả", "Sử dụng chỉ mục để quét bảng", "Quét các bảng có liên quan bằng JOIN", "Không quét bảng nào cả"]', 0, 'Full Table Scan là thao tác quét toàn bộ dữ liệu từ dòng đầu đến cuối, thường rất chậm đối với bảng lớn.', 'easy', 7),
(8, 8, 'Kỹ thuật nào sau đây KHÔNG phải là một cách tốt để tối ưu hóa truy vấn?', '["Tránh sử dụng SELECT *", "Sử dụng chỉ mục trên các cột thường dùng trong WHERE", "Thay thế JOIN bằng nhiều truy vấn con lồng nhau", "Sử dụng LIMIT khi chỉ cần một số lượng dòng nhất định"]', 2, 'Truy vấn con lồng nhau thường chậm hơn so với việc sử dụng JOIN phù hợp.', 'medium', 8);

-- Seed questions for Quiz 9: NoSQL (Topic ID 9)
INSERT INTO questions (quiz_id, topic_id, content, options, correct_option, explanation, difficulty, order_index) VALUES 
(9, 9, 'NoSQL là viết tắt của từ gì?', '["No SQL", "Not Only SQL", "Non-Relational SQL", "None Of SQL"]', 1, 'NoSQL thường được hiểu là Not Only SQL, ngụ ý rằng hệ thống có thể kết hợp cả các tính năng của CSDL quan hệ và phi quan hệ.', 'easy', 1),
(9, 9, 'Đặc điểm nào sau đây KHÔNG phải của CSDL NoSQL?', '["Linh hoạt về Schema (Schema-less)", "Khả năng mở rộng ngang (Horizontal scaling) tốt", "Đảm bảo tính ACID nghiêm ngặt cho mọi giao dịch", "Thường tối ưu cho dữ liệu lớn và phân tán"]', 2, 'Đa số NoSQL hy sinh tính ACID nghiêm ngặt (ưu tiên BASE) để đổi lấy hiệu suất và khả năng mở rộng ngang.', 'medium', 2),
(9, 9, 'MongoDB thuộc loại CSDL NoSQL nào?', '["Key-Value", "Document-oriented", "Column-family", "Graph"]', 1, 'MongoDB lưu trữ dữ liệu dưới dạng tài liệu (document) tương tự JSON (BSON).', 'easy', 3),
(9, 9, 'Redis thuộc loại CSDL NoSQL nào?', '["Key-Value", "Document-oriented", "Column-family", "Graph"]', 0, 'Redis là một CSDL lưu trữ cấu trúc dữ liệu trong bộ nhớ (in-memory) dưới dạng Key-Value.', 'easy', 4),
(9, 9, 'Neo4j thuộc loại CSDL NoSQL nào?', '["Key-Value", "Document-oriented", "Column-family", "Graph"]', 3, 'Neo4j là một CSDL đồ thị (Graph Database) chuyên dùng để biểu diễn các mối quan hệ phức tạp.', 'easy', 5),
(9, 9, 'Trong MongoDB, một bản ghi dữ liệu được gọi là gì?', '["Row", "Tuple", "Document", "Collection"]', 2, 'Tương đương với một hàng (row) trong RDBMS là một Document trong MongoDB.', 'easy', 6),
(9, 9, 'Trong MongoDB, tương đương của khái niệm "Bảng" (Table) trong RDBMS là gì?', '["Database", "Collection", "Document", "Field"]', 1, 'Một Collection chứa các Documents, giống như một Table chứa các Rows.', 'easy', 7),
(9, 9, 'Định lý CAP phát biểu rằng một hệ thống phân tán chỉ có thể đảm bảo đồng thời tối đa mấy yếu tố?', '["1", "2", "3", "4"]', 1, 'Định lý CAP (Consistency, Availability, Partition tolerance) chỉ ra rằng một hệ thống phân tán chỉ có thể đáp ứng đồng thời 2 trong 3 yếu tố.', 'hard', 8);
