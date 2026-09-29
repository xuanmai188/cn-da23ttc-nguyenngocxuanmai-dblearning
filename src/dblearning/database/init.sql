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
