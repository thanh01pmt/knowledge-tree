# Thiết lập Backend Supabase cho LearnWell Platform (Phiên bản Lớp học)

Tài liệu này cung cấp các lệnh SQL và hướng dẫn cần thiết để thiết lập backend Supabase cho ứng dụng LearnWell Platform, **bao gồm bộ tính năng Lớp học đầy đủ**. Điều này bao gồm lược đồ bảng, các chính sách Bảo mật Cấp độ Hàng (RLS), triggers cơ sở dữ liệu và các Lệnh gọi Thủ tục Từ xa (RPC).

## **Mục lục**

- [Thiết lập Backend Supabase cho LearnWell Platform (Phiên bản Lớp học)](#thiết-lập-backend-supabase-cho-quiz-bank-pro-phiên-bản-lớp-học)
  - [**Mục lục**](#mục-lục)
    - [**1. Yêu cầu tiên quyết**](#1-yêu-cầu-tiên-quyết)
    - [**2. Lược đồ Cơ sở dữ liệu (`public`)**](#2-lược-đồ-cơ-sở-dữ-liệu-public)
      - [**Các Kiểu Enum Tiện ích**](#các-kiểu-enum-tiện-ích)
      - [**Bảng Người dùng \& Hồ sơ (User \& Profile)**](#bảng-người-dùng--hồ-sơ-user--profile)
      - [**Các Bảng Metadata**](#các-bảng-metadata)
      - [**Các Bảng Nội dung Cốt lõi (Câu hỏi \& Đề thi)**](#các-bảng-nội-dung-cốt-lõi-câu-hỏi--đề-thi)
      - [**\[MỚI\] Các Bảng Tính năng Lớp học**](#mới-các-bảng-tính-năng-lớp-học)
      - [**\[TÁI CẤU TRÚC\] Các Bảng Hoạt động của Học sinh**](#tái-cấu-trúc-các-bảng-hoạt-động-của-học-sinh)
    - [**3. Bảo mật Cấp độ Hàng (RLS)**](#3-bảo-mật-cấp-độ-hàng-rls)
      - [**Các Hàm Hỗ trợ**](#các-hàm-hỗ-trợ)
      - [**Kích hoạt RLS**](#kích-hoạt-rls)
      - [**Chính sách cho `profiles`**](#chính-sách-cho-profiles)
      - [**Chính sách cho Metadata \& Nội dung**](#chính-sách-cho-metadata--nội-dung)
      - [**\[MỚI\] Chính sách cho Tính năng Lớp học**](#mới-chính-sách-cho-tính-năng-lớp-học)
    - [**4. Triggers Cơ sở dữ liệu**](#4-triggers-cơ-sở-dữ-liệu)
      - [**Trigger để Tạo Hồ sơ cho Người dùng mới**](#trigger-để-tạo-hồ-sơ-cho-người-dùng-mới)
      - [**Trigger để Cập nhật Dấu thời gian `updated_at` / `last_modified`**](#trigger-để-cập-nhật-dấu-thời-gian-updated_at--last_modified)
    - [**5. Hàm Cơ sở dữ liệu (RPCs)**](#5-hàm-cơ-sở-dữ-liệu-rpcs)
      - [**Lấy các KPI hệ thống**](#lấy-các-kpi-hệ-thống)
      - [**Phân tích Điểm yếu của Học sinh**](#phân-tích-điểm-yếu-của-học-sinh)
    - [**6. Nhập Dữ liệu Ban đầu (Tùy chọn)**](#6-nhập-dữ-liệu-ban-đầu-tùy-chọn)

---

### **1. Yêu cầu tiên quyết**

- Một dự án Supabase đã được tạo.
- Quyền truy cập vào Supabase SQL Editor hoặc một client PostgreSQL kết nối đến cơ sở dữ liệu Supabase của bạn.
- Kiến thức cơ bản về SQL.

**Quan trọng:** Chạy các script này bằng người dùng `postgres` hoặc một người dùng có đủ quyền hạn, đặc biệt là để tạo các kiểu dữ liệu, kích hoạt RLS, và tạo các hàm. Đối với các chính sách RLS, hãy chắc chắn rằng bạn hiểu rõ các ý nghĩa về bảo mật.

---

### **2. Lược đồ Cơ sở dữ liệu (`public`)**

Thực thi các lệnh `CREATE TABLE` này trong Supabase SQL Editor của bạn. Chúng được thiết kế để có thể chạy lại nhiều lần một cách an toàn (idempotent).

#### **Các Kiểu Enum Tiện ích**

Các kiểu ENUM này giúp đảm bảo tính nhất quán của dữ liệu cho một số trường nhất định.

```sql
-- Kiểu ENUM tùy chỉnh cho Vai trò người dùng (User Roles)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role_enum') THEN
        CREATE TYPE public.user_role_enum AS ENUM ('student', 'teacher', 'admin', 'user', 'editor');
    END IF;
END$$;

-- Kiểu ENUM tùy chỉnh cho Độ khó tiêu chuẩn (cho questions.difficulty)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'standard_difficulty_enum') THEN
        CREATE TYPE public.standard_difficulty_enum AS ENUM ('easy', 'medium', 'hard');
    END IF;
END$$;
```

#### **Bảng Người dùng & Hồ sơ (User & Profile)**

Lưu trữ thông tin cụ thể của người dùng, mở rộng từ bảng `auth.users`.

```sql
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT,
    avatar_url TEXT,
    role public.user_role_enum DEFAULT 'user'::public.user_role_enum,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Index trên cột role để tra cứu nhanh hơn
CREATE INDEX IF NOT EXISTS idx_profiles_role ON public.profiles(role);
```

#### **Các Bảng Metadata**

Những bảng này lưu trữ các bộ phân loại chung được sử dụng trong toàn bộ ứng dụng.

```sql
-- Bảng Môn học (Subjects)
CREATE TABLE IF NOT EXISTS public.subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_subjects_code ON public.subjects(code);

-- Bảng Cấp học (Grade Levels)
CREATE TABLE IF NOT EXISTS public.grade_levels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_grade_levels_code ON public.grade_levels(code);

-- Bảng Cấp độ Bloom (Bloom Levels)
CREATE TABLE IF NOT EXISTS public.bloom_levels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL, -- vd: "REMEMBER", "APPLY"
    name TEXT NOT NULL,       -- vd: "Ghi nhớ", "Áp dụng"
    description TEXT
);
CREATE INDEX IF NOT EXISTS idx_bloom_levels_code ON public.bloom_levels(code);

-- Bảng Loại câu hỏi (Question Types)
CREATE TABLE IF NOT EXISTS public.question_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL, -- vd: "MCQ", "TF", "SA"
    name TEXT NOT NULL,       -- vd: "Trắc nghiệm", "Đúng/Sai"
    description TEXT
);
CREATE INDEX IF NOT EXISTS idx_question_types_code ON public.question_types(code);

-- Bảng Danh mục (Categories)
CREATE TABLE IF NOT EXISTS public.categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT
);
CREATE INDEX IF NOT EXISTS idx_categories_code ON public.categories(code);

-- Bảng Ngữ cảnh (Contexts)
CREATE TABLE IF NOT EXISTS public.contexts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT
);
CREATE INDEX IF NOT EXISTS idx_contexts_code ON public.contexts(code);

-- Bảng Chủ đề (Topics)
CREATE TABLE IF NOT EXISTS public.topics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    subject_code TEXT NOT NULL REFERENCES public.subjects(code) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_topics_code ON public.topics(code);
CREATE INDEX IF NOT EXISTS idx_topics_subject_code ON public.topics(subject_code);

-- Bảng Mục tiêu học tập (Learning Objectives)
CREATE TABLE IF NOT EXISTS public.learning_objectives (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    subject_code TEXT REFERENCES public.subjects(code) ON DELETE SET NULL ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_learning_objectives_code ON public.learning_objectives(code);

-- Bảng Cách tiếp cận (Approaches)
CREATE TABLE IF NOT EXISTS public.approaches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    verb_en TEXT NOT NULL,
    verb_vi TEXT NOT NULL,
    bloom_level_code TEXT NOT NULL REFERENCES public.bloom_levels(code) ON DELETE RESTRICT ON UPDATE CASCADE,
    -- ... Các cột khác từ schema cũ nếu cần
    difficulty public.standard_difficulty_enum NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_approaches_code ON public.approaches(code);
```

#### **Các Bảng Nội dung Cốt lõi (Câu hỏi & Đề thi)**

```sql
-- Bảng Câu hỏi (với question_config)
CREATE TABLE IF NOT EXISTS public.questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    text TEXT NOT NULL, -- Sao chép từ question_config.prompt để tìm kiếm/xem trước
    question_config JSONB, -- Nguồn dữ liệu duy nhất từ IQ-Kit
    explanation TEXT,
    points INTEGER DEFAULT 1,
    difficulty public.standard_difficulty_enum DEFAULT 'medium'::public.standard_difficulty_enum,
    last_modified TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    question_type_code TEXT NOT NULL REFERENCES public.question_types(code) ON DELETE RESTRICT ON UPDATE CASCADE,
    subject_code TEXT NOT NULL REFERENCES public.subjects(code) ON DELETE RESTRICT ON UPDATE CASCADE,
    topic_code TEXT NOT NULL REFERENCES public.topics(code) ON DELETE RESTRICT ON UPDATE CASCADE,
    grade_level_code TEXT NOT NULL REFERENCES public.grade_levels(code) ON DELETE RESTRICT ON UPDATE CASCADE,
    bloom_level_code TEXT NOT NULL REFERENCES public.bloom_levels(code) ON DELETE RESTRICT ON UPDATE CASCADE,
    approach_code TEXT REFERENCES public.approaches(code) ON DELETE SET NULL ON UPDATE CASCADE,
    learning_objective_code TEXT REFERENCES public.learning_objectives(code) ON DELETE SET NULL ON UPDATE CASCADE,
    context_code TEXT REFERENCES public.contexts(code) ON DELETE SET NULL ON UPDATE CASCADE,
    category_code TEXT REFERENCES public.categories(code) ON DELETE SET NULL ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_questions_gin_config ON public.questions USING GIN (question_config);

-- Bảng Đề thi (Exams)
CREATE TABLE IF NOT EXISTS public.exams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    question_codes TEXT[] NOT NULL,
    settings JSONB NOT NULL DEFAULT '{"timeLimit": 60, "passingScore": 70}',
    last_modified TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL
);
```

#### **[MỚI] Các Bảng Tính năng Lớp học**

```sql
CREATE TABLE IF NOT EXISTS public.classrooms (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    teacher_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    class_code TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
COMMENT ON TABLE public.classrooms IS 'Lưu trữ thông tin về các lớp học do giáo viên tạo ra.';

CREATE TABLE IF NOT EXISTS public.classroom_members (
    classroom_id uuid NOT NULL REFERENCES public.classrooms(id) ON DELETE CASCADE,
    student_id uuid NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    joined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (classroom_id, student_id)
);
COMMENT ON TABLE public.classroom_members IS 'Liên kết học sinh với các lớp học mà họ là thành viên.';

CREATE TABLE IF NOT EXISTS public.assignments (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    classroom_id uuid NOT NULL REFERENCES public.classrooms(id) ON DELETE CASCADE,
    exam_code TEXT NOT NULL REFERENCES public.exams(code) ON DELETE CASCADE,
    title TEXT NOT NULL,
    due_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
COMMENT ON TABLE public.assignments IS 'Đại diện cho một bài kiểm tra được giao cho một lớp học bởi giáo viên.';
```

#### **[TÁI CẤU TRÚC] Các Bảng Hoạt động của Học sinh**

```sql
-- Bảng này thay thế bảng 'student_test_attempts' cũ
CREATE TABLE IF NOT EXISTS public.submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    classroom_id UUID NULL REFERENCES public.classrooms(id) ON DELETE SET NULL,
    assignment_id UUID NULL REFERENCES public.assignments(id) ON DELETE SET NULL,
    submission_type TEXT NOT NULL CHECK (submission_type IN ('assignment', 'practice')),
    session_data JSONB NOT NULL, -- Chứa PracticeSession hoặc QuizResultType
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ -- Có thể được trích xuất từ session_data nếu cần
);
COMMENT ON TABLE public.submissions IS 'Bảng thống nhất cho tất cả bài làm của học sinh (bài tập và luyện tập).';
COMMENT ON COLUMN public.submissions.session_data IS 'Lưu trữ PracticeSession (cho luyện tập) hoặc QuizResultType (cho bài tập).';

CREATE TABLE IF NOT EXISTS public.submission_reviews (
    id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    submission_id uuid NOT NULL UNIQUE REFERENCES public.submissions(id) ON DELETE CASCADE,
    review_content JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
COMMENT ON TABLE public.submission_reviews IS 'Lưu trữ các bài đánh giá do AI tạo ra cho các bài nộp.';

-- Cập nhật bảng student_attempt_bloom_stats để tham chiếu đến bảng submissions mới
-- Điều này yêu cầu xóa ràng buộc cũ và thêm một ràng buộc mới.
CREATE TABLE IF NOT EXISTS public.student_attempt_bloom_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID NOT NULL, -- Sẽ được tham chiếu đến submissions.id
    bloom_level_code TEXT NOT NULL REFERENCES public.bloom_levels(code) ON DELETE CASCADE,
    correct_count INTEGER NOT NULL DEFAULT 0,
    total_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (attempt_id, bloom_level_code)
);

-- Chạy đoạn này sau khi đảm bảo bảng submissions đã tồn tại.
DO $$
BEGIN
  IF EXISTS(SELECT 1 FROM information_schema.table_constraints WHERE constraint_name = 'fk_student_attempt_bloom_stats_attempt' AND table_name = 'student_attempt_bloom_stats') THEN
    ALTER TABLE public.student_attempt_bloom_stats DROP CONSTRAINT fk_student_attempt_bloom_stats_attempt;
  END IF;
  
  IF NOT EXISTS(SELECT 1 FROM information_schema.table_constraints WHERE constraint_name = 'fk_student_attempt_bloom_stats_submission' AND table_name = 'student_attempt_bloom_stats') THEN
    ALTER TABLE public.student_attempt_bloom_stats
      ADD CONSTRAINT fk_student_attempt_bloom_stats_submission 
      FOREIGN KEY (attempt_id) REFERENCES public.submissions(id) ON DELETE CASCADE;
  END IF;
END $$;
```

---

### **3. Bảo mật Cấp độ Hàng (RLS)**

Phần này chứa các chính sách RLS cuối cùng, an toàn với đệ quy.

#### **Các Hàm Hỗ trợ**

```sql
CREATE OR REPLACE FUNCTION get_my_role()
RETURNS TEXT AS $$
BEGIN
  RETURN (SELECT role FROM public.profiles WHERE id = auth.uid());
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION is_teacher_of_class(p_classroom_id uuid)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM public.classrooms
    WHERE id = p_classroom_id AND teacher_id = auth.uid()
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION is_member_of_class(p_classroom_id uuid, p_student_id uuid)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM public.classroom_members
    WHERE classroom_id = p_classroom_id AND student_id = p_student_id
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

#### **Kích hoạt RLS**

Chạy lệnh này cho tất cả các bảng, bao gồm cả các bảng mới.

```sql
-- Bảng người dùng và lớp học
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.classrooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.classroom_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.submission_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_attempt_bloom_stats ENABLE ROW LEVEL SECURITY;

-- Các bảng metadata
ALTER TABLE public.subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.grade_levels ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bloom_levels ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.question_types ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contexts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.learning_objectives ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.approaches ENABLE ROW LEVEL SECURITY;

-- Các bảng nội dung
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exams ENABLE ROW LEVEL SECURITY;
```

#### **Chính sách cho `profiles`**

```sql
-- Admin có thể xem tất cả hồ sơ
CREATE POLICY "Admin co toan quyen tren profiles"
ON public.profiles FOR ALL
USING (get_my_role() = 'admin')
WITH CHECK (get_my_role() = 'admin');

-- Người dùng có thể xem hồ sơ của chính mình
CREATE POLICY "Nguoi dung co the xem ho so cua minh"
ON public.profiles FOR SELECT
USING (auth.uid() = id);

-- Người dùng có thể cập nhật hồ sơ của chính mình
CREATE POLICY "Nguoi dung co the cap nhat ho so cua minh"
ON public.profiles FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);
```

#### **Chính sách cho Metadata & Nội dung**

```sql
-- Chính sách chung cho phép đọc Metadata cho người dùng đã xác thực (áp dụng cho subjects, grade_levels, v.v.)
CREATE POLICY "Nguoi dung da xac thuc co the doc metadata"
ON public.subjects FOR SELECT
TO authenticated
USING (true);
-- ... lặp lại cho các bảng metadata khác

-- Chính sách chung cho phép quản lý Metadata cho Admin/Teacher/Editor
CREATE POLICY "Admin/Teacher co the quan ly metadata"
ON public.subjects FOR ALL
USING (get_my_role() IN ('admin', 'teacher', 'editor'))
WITH CHECK (get_my_role() IN ('admin', 'teacher', 'editor'));
-- ... lặp lại cho các bảng metadata khác

-- Chính sách cho `questions` và `exams`
CREATE POLICY "Nguoi tao noi dung co the doc questions va exams"
ON public.questions FOR SELECT
USING (get_my_role() IN ('admin', 'teacher', 'editor'));

CREATE POLICY "Nguoi tao noi dung co the quan ly questions va exams"
ON public.questions FOR ALL
USING (get_my_role() IN ('admin', 'teacher', 'editor'));

-- Lặp lại các chính sách tương tự cho bảng `exams`
CREATE POLICY "Nguoi tao noi dung co the doc exams" ON public.exams FOR SELECT USING (get_my_role() IN ('admin', 'teacher', 'editor'));
CREATE POLICY "Nguoi tao noi dung co the quan ly exams" ON public.exams FOR ALL USING (get_my_role() IN ('admin', 'teacher', 'editor'));
```

#### **[MỚI] Chính sách cho Tính năng Lớp học**

```sql
-- Chính sách cho 'classrooms'
DROP POLICY IF EXISTS "Giao vien co the quan ly lop hoc cua minh" ON public.classrooms;
CREATE POLICY "Giao vien co thể quan ly lop hoc cua minh" ON public.classrooms FOR ALL USING (get_my_role() = 'teacher' AND teacher_id = auth.uid()) WITH CHECK (get_my_role() = 'teacher' AND teacher_id = auth.uid());

DROP POLICY IF EXISTS "Hoc sinh co the xem lop hoc cua minh" ON public.classrooms;
CREATE POLICY "Hoc sinh co the xem lop hoc cua minh" ON public.classrooms FOR SELECT USING (is_member_of_class(id, auth.uid()));

-- Chính sách cho 'classroom_members'
DROP POLICY IF EXISTS "Giao vien co the quan ly thanh vien trong lop cua minh" ON public.classroom_members;
CREATE POLICY "Giao vien co the quan ly thanh vien trong lop cua minh" ON public.classroom_members FOR ALL USING (is_teacher_of_class(classroom_id) AND get_my_role() = 'teacher');

DROP POLICY IF EXISTS "Hoc sinh co the xem tu cach thanh vien cua minh" ON public.classroom_members;
CREATE POLICY "Hoc sinh co the xem tu cach thanh vien cua minh" ON public.classroom_members FOR SELECT USING (student_id = auth.uid());

-- Chính sách cho 'assignments'
DROP POLICY IF EXISTS "Giao vien co the quan ly bai tap trong lop cua minh" ON public.assignments;
CREATE POLICY "Giao vien co the quan ly bai tap trong lop cua minh" ON public.assignments FOR ALL USING (is_teacher_of_class(classroom_id));

DROP POLICY IF EXISTS "Hoc sinh co the xem bai tap trong lop cua minh" ON public.assignments;
CREATE POLICY "Hoc sinh co the xem bai tap trong lop cua minh" ON public.assignments FOR SELECT USING (is_member_of_class(classroom_id, auth.uid()));

-- Chính sách cho 'submissions'
DROP POLICY IF EXISTS "Hoc sinh co the tao va xem bai nop cua minh" ON public.submissions;
CREATE POLICY "Hoc sinh co the tao va xem bai nop cua minh" ON public.submissions FOR ALL USING (student_id = auth.uid()) WITH CHECK (student_id = auth.uid());

DROP POLICY IF EXISTS "Giao vien co the xem bai nop trong lop cua minh" ON public.submissions;
CREATE POLICY "Giao vien co the xem bai nop trong lop cua minh" ON public.submissions FOR SELECT USING (is_teacher_of_class(classroom_id));

-- Chính sách cho 'submission_reviews'
DROP POLICY IF EXISTS "Nguoi dung co the xem review cho cac bai nop ho co the thay" ON public.submission_reviews;
CREATE POLICY "Nguoi dung co the xem review cho cac bai nop ho co the thay" ON public.submission_reviews FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.submissions WHERE id = submission_id) -- RLS trên submissions sẽ được kiểm tra ngầm
);
```

---

### **4. Triggers Cơ sở dữ liệu**

#### **Trigger để Tạo Hồ sơ cho Người dùng mới**

Trigger này tự động tạo một mục mới trong `public.profiles` khi một người dùng mới đăng ký trong `auth.users`.

```sql
-- Hàm được gọi bởi trigger
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, avatar_url, role)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'full_name',
    NEW.raw_user_meta_data->>'avatar_url',
    COALESCE((NEW.raw_user_meta_data->>'role')::public.user_role_enum, 'user'::public.user_role_enum)
  );
  RETURN NEW;
END;
$$;

-- Trigger gọi hàm
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

#### **Trigger để Cập nhật Dấu thời gian `updated_at` / `last_modified`**

Các trigger này tự động cập nhật trường `updated_at` hoặc `last_modified` khi một hàng được sửa đổi.

```sql
-- Hàm chung để cập nhật cột timestamp
CREATE OR REPLACE FUNCTION public.update_timestamp_column()
RETURNS TRIGGER AS $$
BEGIN
   -- Kiểm tra xem cột `last_modified` hay `updated_at` tồn tại
   IF TG_ARGV[0] = 'last_modified' THEN
       NEW.last_modified = timezone('utc', now()); 
   ELSIF TG_ARGV[0] = 'updated_at' THEN
       NEW.updated_at = timezone('utc', now());
   END IF;
   RETURN NEW;
END;
$$ language 'plpgsql';

-- Áp dụng trigger cho các bảng liên quan
-- profiles (updated_at)
DROP TRIGGER IF EXISTS update_profiles_updated_at ON public.profiles;
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles FOR EACH ROW EXECUTE FUNCTION public.update_timestamp_column('updated_at');

-- subjects (updated_at)
DROP TRIGGER IF EXISTS update_subjects_updated_at ON public.subjects;
CREATE TRIGGER update_subjects_updated_at BEFORE UPDATE ON public.subjects FOR EACH ROW EXECUTE FUNCTION public.update_timestamp_column('updated_at');

-- questions (last_modified)
DROP TRIGGER IF EXISTS update_questions_last_modified ON public.questions;
CREATE TRIGGER update_questions_last_modified BEFORE UPDATE ON public.questions FOR EACH ROW EXECUTE FUNCTION public.update_timestamp_column('last_modified');

-- exams (last_modified)
DROP TRIGGER IF EXISTS update_exams_last_modified ON public.exams;
CREATE TRIGGER update_exams_last_modified BEFORE UPDATE ON public.exams FOR EACH ROW EXECUTE FUNCTION public.update_timestamp_column('last_modified');
```

---

### **5. Hàm Cơ sở dữ liệu (RPCs)**

Phần này chứa các phiên bản RPC cuối cùng, đã được sửa lỗi.

#### **Lấy các KPI hệ thống**

```sql
CREATE OR REPLACE FUNCTION public.get_system_kpis(
    p_from_date date DEFAULT NULL,
    p_to_date date DEFAULT NULL
)
RETURNS TABLE(total_questions BIGINT, total_exams BIGINT, total_attempts BIGINT, completed_attempts BIGINT, active_students BIGINT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        (SELECT count(*) FROM public.questions WHERE (p_from_date IS NULL OR last_modified::date >= p_from_date) AND (p_to_date IS NULL OR last_modified::date <= p_to_date)) AS total_questions,
        (SELECT count(*) FROM public.exams WHERE (p_from_date IS NULL OR last_modified::date >= p_from_date) AND (p_to_date IS NULL OR last_modified::date <= p_to_date)) AS total_exams,
        (SELECT count(*) FROM public.submissions WHERE (p_from_date IS NULL OR submitted_at::date >= p_from_date) AND (p_to_date IS NULL OR submitted_at::date <= p_to_date)) AS total_attempts,
        (SELECT count(*) FROM public.submissions WHERE (session_data->'quizResult'->>'completedAt' IS NOT NULL) AND (p_from_date IS NULL OR submitted_at::date >= p_from_date) AND (p_to_date IS NULL OR submitted_at::date <= p_to_date)) AS completed_attempts,
        (SELECT count(DISTINCT student_id) FROM public.submissions WHERE (p_from_date IS NULL OR submitted_at::date >= p_from_date) AND (p_to_date IS NULL OR submitted_at::date <= p_to_date)) AS active_students;
END;
$$;
```

#### **Phân tích Điểm yếu của Học sinh**

```sql
CREATE OR REPLACE FUNCTION public.analyze_student_weaknesses(
    p_student_id uuid,
    p_from_date date DEFAULT NULL,
    p_to_date date DEFAULT NULL,
    p_subject_code text DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    weakness_data JSONB;
BEGIN
    WITH student_answers AS (
        SELECT
            (q_result.value -> 'questionConfig' ->> 'topic') AS topic_code,
            (q_result.value -> 'questionConfig' ->> 'bloomLevel') AS bloom_level_code,
            (q_result.value ->> 'isCorrect')::boolean AS is_correct
        FROM
            public.submissions s
            CROSS JOIN LATERAL jsonb_array_elements(s.session_data -> 'quizResult' -> 'questionResults') AS q_result(value)
        WHERE
            s.student_id = p_student_id
            AND (s.session_data->'quizResult'->>'completedAt' IS NOT NULL)
            AND (p_from_date IS NULL OR s.submitted_at::date >= p_from_date)
            AND (p_to_date IS NULL OR s.submitted_at::date <= p_to_date)
            AND (p_subject_code IS NULL OR (q_result.value -> 'questionConfig' ->> 'subject') = p_subject_code)
    ),
    topic_stats AS (
        SELECT sa.topic_code, t.name as topic_name, count(*) as total_attempts_on_topic, count(*) FILTER (WHERE sa.is_correct = false) as incorrect_count
        FROM student_answers sa JOIN public.topics t ON sa.topic_code = t.code GROUP BY sa.topic_code, t.name
    ),
    bloom_stats AS (
        SELECT sa.bloom_level_code, bl.name as bloom_name, count(*) as total, count(*) FILTER (WHERE sa.is_correct = true) as correct
        FROM student_answers sa JOIN public.bloom_levels bl ON sa.bloom_level_code = bl.code GROUP BY sa.bloom_level_code, bl.name
    )
    SELECT jsonb_build_object(
        'topWeakTopics', (SELECT jsonb_agg(jsonb_build_object('topicCode', ts.topic_code, 'topicName', ts.topic_name, 'incorrectCount', ts.incorrect_count, 'totalAttemptsOnTopic', ts.total_attempts_on_topic, 'failureRate', ROUND((ts.incorrect_count::numeric / ts.total_attempts_on_topic) * 100, 2)) ORDER BY (ts.incorrect_count::numeric / ts.total_attempts_on_topic) DESC) FROM topic_stats ts WHERE ts.incorrect_count > 0),
        'weakestBloomLevels', (SELECT jsonb_agg(jsonb_build_object('bloomCode', bs.bloom_level_code, 'bloomName', bs.bloom_name, 'successRate', ROUND((bs.correct::numeric / bs.total) * 100, 2)) ORDER BY (bs.correct::numeric / bs.total) ASC) FROM bloom_stats bs)
    ) INTO weakness_data;
    RETURN weakness_data;
END;
$$;
```

---

### **6. Nhập Dữ liệu Ban đầu (Tùy chọn)**

Bạn có thể sử dụng "Table Editor" hoặc "SQL Editor" trong dashboard của Supabase để chèn dữ liệu ban đầu cho các bảng metadata như `subjects`, `grade_levels`, `bloom_levels`, `question_types`, v.v.

Ví dụ để nhập dữ liệu cho một môn học:

```sql
INSERT INTO public.subjects (code, name) VALUES ('MATH', 'Toán học') ON CONFLICT (code) DO NOTHING;
INSERT INTO public.grade_levels (code, name) VALUES ('G9', 'Lớp 9') ON CONFLICT (code) DO NOTHING;
INSERT INTO public.bloom_levels (code, name, description) VALUES ('REMEMBER', 'Ghi nhớ', 'Nhớ lại các sự kiện và khái niệm cơ bản.') ON CONFLICT (code) DO NOTHING;
INSERT INTO public.question_types (code, name, description) VALUES ('MCQ', 'Trắc nghiệm', 'Chọn một câu trả lời từ danh sách các lựa chọn.') ON CONFLICT (code) DO NOTHING;
-- v.v.
```
