### 1. Phân tích & Báo cáo (Analysis & Reporting)

*   `analyze_student_weaknesses(p_student_id uuid, p_from_date date, p_to_date date)`: Phân tích và trả về các chủ đề (topic) và cấp độ Bloom yếu nhất của một học sinh dựa trên dữ liệu thành thạo (mastery).
*   `get_classroom_performance_snapshot(p_classroom_id uuid)`: Lấy thông tin tổng quan về hiệu suất của cả lớp học, bao gồm điểm trung bình, các chủ đề có tỷ lệ thành thạo thấp nhất, và những câu hỏi khó nhất.
*   `get_classroom_weakness_analysis(p_classroom_id uuid, p_limit integer)`: Phân tích và xác định các năng lực (LO) và chủ đề (topic) yếu nhất trong một lớp học.
*   `get_content_performance_summary(p_from_date date, p_to_date date, p_limit integer)`: Lấy báo cáo tổng hợp về hiệu suất của nội dung (câu hỏi và năng lực) trên toàn hệ thống, tìm ra những mục khó nhất.
*   `get_student_performance_by_bloom(p_student_id uuid, p_from_date date, p_to_date date)`: Tính toán và trả về tỷ lệ thành công của học sinh theo từng cấp độ nhận thức Bloom.
*   `get_student_performance_report_data(p_student_id uuid, p_from_date timestamptz, p_to_date timestamptz)`: Lấy dữ liệu chi tiết về các bài làm đã nộp của một học sinh để tạo báo cáo.
*   `get_analytics_for_exam(p_exam_code text, p_from_date timestamptz, p_to_date timestamptz)`: Lấy dữ liệu phân tích chi tiết cho một bài kiểm tra cụ thể, bao gồm điểm số và câu trả lời của từng học sinh.
*   `get_system_kpis(p_from_date date, p_to_date date)`: Lấy các chỉ số hiệu suất chính (KPI) của toàn hệ thống như tổng số câu hỏi, số bài kiểm tra, số lượt làm bài, v.v.
*   `get_question_distributions(p_from_date timestamptz, p_to_date timestamptz)`: Thống kê sự phân bổ câu hỏi theo môn học, cấp độ Bloom, và loại câu hỏi.
*   `get_teacher_dashboard_summary(p_teacher_id uuid)`: Lấy dữ liệu tóm tắt cho trang tổng quan của giáo viên, bao gồm số liệu KPI và các hoạt động gần đây.

### 2. Quản lý Dữ liệu (Data Management - CRUD & Upsert)

#### Thao tác hàng loạt (Bulk Operations)
*   `bulk_create_questions_with_los(questions_data jsonb, p_organization_code text)`: Tạo hàng loạt câu hỏi mới cùng với các liên kết đến năng lực học tập (LO).
*   `bulk_upsert_categories_with_subjects(p_categories_data jsonb, p_organization_code text)`: Cập nhật hoặc tạo mới hàng loạt danh mục (category) và các liên kết với môn học (subject).
*   `bulk_upsert_los_with_relations(p_los_data jsonb, p_organization_code text)`: Cập nhật hoặc tạo mới hàng loạt năng lực học tập (LO) cùng các mối quan hệ của chúng (cha-con, chủ đề).
*   `bulk_upsert_subjects_with_courses(p_subjects_data jsonb, p_organization_code text)`: Cập nhật hoặc tạo mới hàng loạt môn học (subject) và các liên kết với khóa học (course).
*   `bulk_upsert_topics_with_categories(p_topics_data jsonb, p_organization_code text)`: Cập nhật hoặc tạo mới hàng loạt chủ đề (topic) và các liên kết với danh mục (category).

#### Thao tác đơn lẻ (Single Item Operations)
*   `create_category_with_subjects(p_code text, p_name text, p_description text, p_organization_code text, p_subject_codes jsonb)`: Tạo một danh mục mới và liên kết nó với các môn học.
*   `create_question_with_los(...)`: Tạo một câu hỏi mới và liên kết nó với các năng lực học tập (có 3 phiên bản với các tham số khác nhau).
*   `create_subject_with_courses(...)`: Tạo một môn học mới và liên kết nó với các khóa học (có 2 phiên bản).
*   `update_category_with_subjects(p_category_code text, p_name text, p_description text, p_subject_codes jsonb)`: Cập nhật một danh mục và các liên kết môn học của nó.
*   `update_question_with_los(p_question_id uuid, p_question_config jsonb, p_text text, p_learning_objective_codes text[])`: Cập nhật một câu hỏi và các liên kết năng lực của nó.
*   `update_subject_with_courses(p_subject_code text, p_name text, p_description text, p_course_codes text[])`: Cập nhật một môn học và các liên kết khóa học của nó.
*   `upsert_approach_with_details(...)`: Cập nhật hoặc tạo mới một phương pháp sư phạm (approach) cùng các chi tiết liên quan (có 3 phiên bản).
*   `upsert_lo_with_relations(...)`: Cập nhật hoặc tạo mới một năng lực học tập (LO) và các liên kết chủ đề của nó.
*   `upsert_resource_with_los(...)`: Cập nhật hoặc tạo mới một tài nguyên học tập và liên kết nó với các năng lực.
*   `upsert_topic_with_relations(...)`: Cập nhật hoặc tạo mới một chủ đề (topic) và các liên kết danh mục của nó (có 2 phiên bản).
*   `update_mastery_after_submission(p_submission_id uuid)`: Cập nhật mức độ thành thạo của học sinh đối với các năng lực liên quan sau khi nộp bài.

### 3. Tìm kiếm, Lọc & Lấy Dữ liệu (Data Retrieval & Filtering)

*   `find_questions_for_blueprint(p_blueprint_data jsonb)`: Tìm và chọn ngẫu nhiên các câu hỏi phù hợp với một ma trận đề thi (blueprint) cho trước.
*   `get_approaches_with_details()`: Lấy danh sách tất cả các phương pháp sư phạm (approach) cùng với các mã ngữ cảnh và độ khó đề xuất.
*   `get_categories_with_subject_codes()`: Lấy danh sách tất cả các danh mục cùng với mảng các mã môn học liên quan.
*   `get_curriculum_for_student_classes(p_student_id uuid)`: Lấy toàn bộ chương trình học (danh sách năng lực) từ tất cả các lớp mà một học sinh tham gia.
*   `get_enriched_questions_by_codes(p_question_codes text[])`: Lấy thông tin chi tiết của một nhóm câu hỏi và làm giàu chúng với siêu dữ liệu từ các năng lực liên quan.
*   `get_filtered_questions(...)`: Lọc và tìm kiếm câu hỏi dựa trên nhiều tiêu chí như từ khóa, môn học, chủ đề, cấp độ Bloom, v.v.
*   `get_los_with_relations()`: Lấy danh sách tất cả các năng lực học tập (LO) cùng với các mã liên quan đã được phi chuẩn hóa (chủ đề, danh mục, môn học).
*   `get_resources_for_los(p_lo_codes text[])`: Lấy danh sách các tài nguyên học tập được liên kết với một danh sách năng lực cho trước.
*   `get_student_next_suggested_los(p_student_id uuid, p_classroom_id uuid, p_limit integer)`: Gợi ý các năng lực học tập tiếp theo cho một học sinh trong một lớp học cụ thể.
*   `get_student_progress_in_class(p_classroom_id uuid, p_student_id uuid)`: Lấy tiến độ học tập của một học sinh trong một lớp (danh sách các bài tập đã nộp và điểm số).
*   `get_subjects_with_course_codes()`: Lấy danh sách tất cả các môn học cùng với mảng các mã khóa học liên quan.
*   `get_teacher_class_list_with_stats(p_teacher_id uuid)`: Lấy danh sách các lớp học của một giáo viên kèm theo thống kê số học sinh và bài tập.
*   `get_topics_with_details()`: Lấy danh sách tất cả các chủ đề (topic) cùng với các mã danh mục và môn học liên quan.
*   `get_organization_members(p_org_code text)`: Lấy danh sách thành viên của một tổ chức.

### 4. Tiện ích & Quản trị (Utility & Admin)

*   `backfill_all_derived_codes()`: Chạy lại quá trình đồng bộ hóa toàn bộ dữ liệu phi chuẩn hóa trên các bảng (dùng cho bảo trì).
*   `debug_my_profile_access()`: Hàm gỡ lỗi để kiểm tra thông tin và quyền truy cập của người dùng đang đăng nhập.
*   `generate_question_code(...)`: Tạo mã định danh duy nhất cho một câu hỏi mới (có 2 phiên bản).
*   `get_my_claim(claim text)`: Lấy một thông tin (claim) cụ thể từ JWT của người dùng.
*   `get_my_organization_code()`: Lấy mã tổ chức của người dùng đang đăng nhập.
*   `get_my_role()`: Lấy vai trò (role) của người dùng đang đăng nhập.
*   `is_admin(p_user_id uuid)`: Kiểm tra xem một người dùng có phải là quản trị viên hay không.
*   `is_member_of_class(p_classroom_id uuid, p_student_id uuid)`: Kiểm tra xem một học sinh có phải là thành viên của lớp học không.
*   `is_org_admin()`: Kiểm tra xem người dùng hiện tại có phải là quản trị viên của tổ chức hay không.
*   `is_teacher_of_class(p_classroom_id uuid)`: Kiểm tra xem người dùng hiện tại có phải là giáo viên của lớp học không.
*   `update_user_role(target_user_id uuid, new_role text)`: Cập nhật vai trò cho một người dùng (chỉ dành cho admin).







----

Chắc chắn rồi. Dưới đây là mã nguồn chi tiết cho từng hàm RPC, được tách ra và phân loại theo chức năng như trong câu trả lời trước của tôi.

***

### 1. Phân tích & Báo cáo (Analysis & Reporting)

#### `analyze_student_weaknesses`
```sql
CREATE OR REPLACE FUNCTION "public"."analyze_student_weaknesses"("p_student_id" "uuid", "p_from_date" "date" DEFAULT NULL::"date", "p_to_date" "date" DEFAULT NULL::"date") RETURNS "jsonb"
    LANGUAGE "plpgsql"
    AS $$
DECLARE
    result jsonb;
BEGIN
    WITH weak_los AS (
        -- Tìm tất cả các năng lực mà học sinh chưa thành thạo
        SELECT 
            sm.learning_objective_code
        FROM public.student_mastery sm
        WHERE sm.student_id = p_student_id
          AND sm.mastery_level IN ('in_progress', 'not_started') -- Mở rộng ra cả các năng lực chưa bắt đầu
          AND (p_from_date IS NULL OR sm.assessed_at::date >= p_from_date)
          AND (p_to_date IS NULL OR sm.assessed_at::date <= p_to_date)
    ),
    topic_weakness AS (
        -- Đếm số lượng năng lực yếu trong mỗi topic
        SELECT
            t.code as topic_code,
            t.name as topic_name,
            count(*) as weak_lo_count
        FROM weak_los wl
        JOIN public.topic_learning_objectives tlo ON wl.learning_objective_code = tlo.learning_objective_code
        JOIN public.topics t ON tlo.topic_code = t.code
        GROUP BY t.code, t.name
        ORDER BY weak_lo_count DESC
        LIMIT 5 -- Lấy 5 topic yếu nhất
    ),
    bloom_weakness AS (
        -- Sử dụng RPC đã được viết lại để lấy hiệu suất theo cấp độ Bloom
        SELECT 
          bloom_code,
          bloom_name,
          success_rate
        FROM public.get_student_performance_by_bloom(p_student_id, p_from_date, p_to_date)
        WHERE success_rate < 70 -- Ngưỡng được coi là yếu
        ORDER BY success_rate ASC
        LIMIT 3 -- Lấy 3 cấp độ yếu nhất
    )
    -- Xây dựng đối tượng JSONB kết quả
    SELECT jsonb_build_object(
        'topWeakTopics', COALESCE((SELECT jsonb_agg(tw) FROM topic_weakness tw), '[]'::jsonb),
        'weakestBloomLevels', COALESCE((SELECT jsonb_agg(bw) FROM bloom_weakness bw), '[]'::jsonb)
    ) INTO result;

    RETURN result;
END;
$$;
```

#### `get_classroom_performance_snapshot`
```sql
CREATE OR REPLACE FUNCTION "public"."get_classroom_performance_snapshot"("p_classroom_id" "uuid") RETURNS "jsonb"
    LANGUAGE "plpgsql" STABLE
    AS $$
DECLARE
    result_json jsonb;
BEGIN
    WITH
    -- Part 1: Analyze performance from the competency profile (student_mastery)
    class_students AS (
        SELECT student_id FROM public.classroom_members WHERE classroom_id = p_classroom_id AND status = 'approved'
    ),
    topic_mastery_stats AS (
        SELECT
            tlo.topic_code,
            -- Đếm tổng số năng lực * số học sinh trong lớp để có mẫu số chính xác
            count(DISTINCT tlo.learning_objective_code) * (SELECT count(*) FROM class_students) as total_possible_mastery_points,
            count(sm.learning_objective_code) FILTER (WHERE sm.mastery_level = 'mastered') AS mastered_los_in_topic_for_class
        FROM public.topic_learning_objectives tlo
        -- Dùng CROSS JOIN để đảm bảo mọi topic đều được tính, ngay cả khi chưa có ai học
        CROSS JOIN class_students cs
        -- LEFT JOIN với mastery để lấy dữ liệu thực tế
        LEFT JOIN public.student_mastery sm ON tlo.learning_objective_code = sm.learning_objective_code AND cs.student_id = sm.student_id
        GROUP BY tlo.topic_code
    ),
    -- Part 2: Analyze performance from individual submissions (for question-specific stats)
    student_question_answers AS (
        SELECT
            s.student_id,
            (q_result.value->>'questionId')::text AS question_config_id,
            (q_result.value->>'isCorrect')::boolean AS is_correct
        FROM public.submissions s
        CROSS JOIN LATERAL jsonb_array_elements(s.session_data->'questionResults') AS q_result(value)
        WHERE s.classroom_id = p_classroom_id
          AND s.submission_type = 'assignment'
          AND s.completed_at IS NOT NULL
    ),
    question_stats AS (
        SELECT
            q.id as question_id,
            q.text AS question_text,
            COUNT(*) AS total_answers,
            COUNT(*) FILTER (WHERE sqa.is_correct) AS correct_answers
        FROM student_question_answers sqa
        -- Đổi JOIN sang question_config->>'id'
        JOIN public.questions q ON (q.question_config->>'id')::text = sqa.question_config_id
        GROUP BY q.id, q.text
    ),
    -- Part 3: General class stats
    student_score_stats AS (
        SELECT
            s.student_id,
            p.full_name,
            AVG((s.session_data ->> 'percentage')::numeric) AS average_score
        FROM public.submissions s
        JOIN public.profiles p ON s.student_id = p.id
        WHERE s.classroom_id = p_classroom_id
          AND s.submission_type = 'assignment'
          AND s.completed_at IS NOT NULL
        GROUP BY s.student_id, p.full_name
    )
    -- Final SELECT to build the JSONB object with COALESCE checks
    SELECT
        jsonb_build_object(
            'classInfo', (
                SELECT jsonb_build_object(
                    'studentCount', (SELECT COUNT(*) FROM class_students),
                    'assignmentCount', (SELECT COUNT(*) FROM public.assignments WHERE classroom_id = p_classroom_id)
                )
            ),
            
            -- SỬA ĐỔI CHÍNH Ở ĐÂY
            'overallPerformance', COALESCE(
                (SELECT jsonb_build_object('averageScore', ROUND(AVG(average_score), 2))
                 FROM student_score_stats),
                '{"averageScore": 0}'::jsonb -- Giá trị mặc định nếu không có submission nào
            ),

            'performanceByTopic', COALESCE(
                (SELECT jsonb_agg(
                    jsonb_build_object(
                        'topicCode', tms.topic_code,
                        'topicName', t.name,
                        -- Xử lý chia cho 0
                        'masteryRate', CASE 
                                          WHEN tms.total_possible_mastery_points > 0 THEN ROUND((tms.mastered_los_in_topic_for_class::numeric * 100) / tms.total_possible_mastery_points, 2)
                                          ELSE 0 
                                       END
                    ) ORDER BY 
                        CASE 
                           WHEN tms.total_possible_mastery_points > 0 THEN ROUND((tms.mastered_los_in_topic_for_class::numeric * 100) / tms.total_possible_mastery_points, 2)
                           ELSE 0
                        END ASC
                )
                FROM topic_mastery_stats tms
                JOIN public.topics t ON tms.topic_code = t.code),
                '[]'::jsonb -- Giá trị mặc định là mảng rỗng
            ),

            'mostDifficultQuestions', COALESCE(
                (SELECT jsonb_agg(
                    jsonb_build_object(
                        'questionId', qs.question_id,
                        'questionText', qs.question_text,
                        'successRate', ROUND((qs.correct_answers::numeric * 100) / qs.total_answers, 2)
                    ) ORDER BY ROUND((qs.correct_answers::numeric * 100) / qs.total_answers, 2) ASC
                )
                FROM (SELECT * FROM question_stats WHERE total_answers > 0 LIMIT 5) AS qs),
                '[]'::jsonb -- Giá trị mặc định là mảng rỗng
            ),

            'topPerformers', COALESCE(
                (SELECT jsonb_agg(
                    jsonb_build_object(
                        'studentId', sss.student_id,
                        'fullName', sss.full_name,
                        'averageScore', ROUND(sss.average_score, 2)
                    ) ORDER BY sss.average_score DESC
                )
                FROM (SELECT * FROM student_score_stats LIMIT 5) AS sss),
                '[]'::jsonb -- Giá trị mặc định là mảng rỗng
            )
        )
    INTO result_json;

    RETURN result_json;
END;
$$;
```

#### `get_classroom_weakness_analysis`
```sql
CREATE OR REPLACE FUNCTION "public"."get_classroom_weakness_analysis"("p_classroom_id" "uuid", "p_limit" integer DEFAULT 5) RETURNS "jsonb"
    LANGUAGE "plpgsql" STABLE SECURITY DEFINER
    AS $$
DECLARE
    result jsonb;
BEGIN
    WITH class_students AS (
        -- Lấy danh sách học sinh đã được duyệt trong lớp
        SELECT student_id FROM public.classroom_members 
        WHERE classroom_id = p_classroom_id AND status = 'approved'
    ),
    lo_performance_in_class AS (
        -- Tính toán hiệu suất của lớp cho mỗi LO
        SELECT
            sm.learning_objective_code,
            lo.name as lo_name,
            count(sm.student_id) AS total_assessed,
            count(sm.student_id) FILTER (WHERE sm.mastery_level = 'mastered') AS mastered_count,
            ROUND(
                (count(sm.student_id) FILTER (WHERE sm.mastery_level = 'mastered') * 100.0) / count(sm.student_id), 2
            ) AS mastery_rate
        FROM public.student_mastery sm
        JOIN class_students cs ON sm.student_id = cs.student_id
        JOIN public.learning_objectives lo ON sm.learning_objective_code = lo.code
        GROUP BY sm.learning_objective_code, lo.name
        HAVING count(sm.student_id) > 0
    ),
    topic_performance_in_class AS (
        -- Tổng hợp hiệu suất theo Topic
        SELECT
            t.code as topic_code,
            t.name as topic_name,
            -- Tính trung bình tỷ lệ thành thạo của tất cả LOs trong topic này
            ROUND(AVG(lp.mastery_rate), 2) as average_mastery_rate,
            -- Đếm số LOs yếu (dưới 70% thành thạo)
            count(lp.learning_objective_code) FILTER (WHERE lp.mastery_rate < 70) as weak_los_count
        FROM lo_performance_in_class lp
        JOIN public.topic_learning_objectives tlo ON lp.learning_objective_code = tlo.learning_objective_code
        JOIN public.topics t ON tlo.topic_code = t.code
        GROUP BY t.code, t.name
    )
    -- Xây dựng kết quả JSONB cuối cùng
    SELECT jsonb_build_object(
        'weakestLearningObjectives', (
            SELECT COALESCE(jsonb_agg(lp.* ORDER BY lp.mastery_rate ASC, lp.total_assessed DESC), '[]'::jsonb)
            FROM (SELECT * FROM lo_performance_in_class LIMIT p_limit) lp
        ),
        'weakestTopics', (
            SELECT COALESCE(jsonb_agg(tp.* ORDER BY tp.average_mastery_rate ASC, tp.weak_los_count DESC), '[]'::jsonb)
            FROM (SELECT * FROM topic_performance_in_class LIMIT p_limit) tp
        )
    ) INTO result;

    RETURN result;
END;
$$;
```

#### `get_content_performance_summary`
```sql
CREATE OR REPLACE FUNCTION "public"."get_content_performance_summary"("p_from_date" "date" DEFAULT NULL::"date", "p_to_date" "date" DEFAULT NULL::"date", "p_limit" integer DEFAULT 10) RETURNS "jsonb"
    LANGUAGE "plpgsql" STABLE SECURITY DEFINER
    AS $$
DECLARE
    result jsonb;
BEGIN
    WITH submission_data_in_range AS (
        -- Lấy các submission trong khoảng thời gian để phân tích câu hỏi
        SELECT
            s.session_data
        FROM public.submissions s
        WHERE s.completed_at IS NOT NULL
          AND (p_from_date IS NULL OR s.submitted_at::date >= p_from_date)
          AND (p_to_date IS NULL OR s.submitted_at::date <= p_to_date)
    ),
    question_answers AS (
        -- Mở rộng mảng questionResults từ tất cả các submission
        SELECT
            (q_result.value->>'questionId')::text AS question_config_id,
            (q_result.value->>'isCorrect')::boolean AS is_correct
        FROM submission_data_in_range
        CROSS JOIN LATERAL jsonb_array_elements(session_data->'questionResults') AS q_result(value)
    ),
    question_performance AS (
        -- Tính toán tỷ lệ thành công cho mỗi câu hỏi
        SELECT
            q.code AS question_code,
            q.text AS question_text,
            count(*) AS total_attempts,
            count(*) FILTER (WHERE qa.is_correct) AS correct_answers,
            ROUND(
                (count(*) FILTER (WHERE qa.is_correct) * 100.0) / count(*), 2
            ) AS success_rate
        FROM question_answers qa
        JOIN public.questions q ON (q.question_config->>'id')::text = qa.question_config_id
        GROUP BY q.code, q.text
        HAVING count(*) > 5 -- Chỉ xem xét các câu hỏi có ít nhất 5 lượt trả lời
    ),
    lo_performance AS (
        -- Tính toán tỷ lệ thành thạo cho mỗi LO trên toàn hệ thống
        SELECT
            sm.learning_objective_code,
            lo.name AS lo_name,
            count(sm.student_id) AS total_students_assessed,
            count(sm.student_id) FILTER (WHERE sm.mastery_level = 'mastered') AS mastered_count,
            ROUND(
                (count(sm.student_id) FILTER (WHERE sm.mastery_level = 'mastered') * 100.0) / count(sm.student_id), 2
            ) AS global_mastery_rate
        FROM public.student_mastery sm
        JOIN public.learning_objectives lo ON sm.learning_objective_code = lo.code
        WHERE (p_from_date IS NULL OR sm.assessed_at::date >= p_from_date)
          AND (p_to_date IS NULL OR sm.assessed_at::date <= p_to_date)
        GROUP BY sm.learning_objective_code, lo.name
        HAVING count(sm.student_id) > 5 -- Chỉ xem xét các LO đã được đánh giá cho ít nhất 5 học sinh
    )
    -- Xây dựng kết quả JSONB cuối cùng
    SELECT jsonb_build_object(
        'mostDifficultQuestions', (
            SELECT COALESCE(jsonb_agg(qp.* ORDER BY qp.success_rate ASC, qp.total_attempts DESC), '[]'::jsonb)
            FROM (SELECT * FROM question_performance LIMIT p_limit) qp
        ),
        'mostDifficultLearningObjectives', (
            SELECT COALESCE(jsonb_agg(lp.* ORDER BY lp.global_mastery_rate ASC, lp.total_students_assessed DESC), '[]'::jsonb)
            FROM (SELECT * FROM lo_performance LIMIT p_limit) lp
        )
    ) INTO result;

    RETURN result;
END;
$$;
```

#### `get_student_performance_by_bloom`
```sql
CREATE OR REPLACE FUNCTION "public"."get_student_performance_by_bloom"("p_student_id" "uuid", "p_from_date" "date" DEFAULT NULL::"date", "p_to_date" "date" DEFAULT NULL::"date") RETURNS TABLE("bloom_code" "text", "bloom_name" "text", "correct_count" bigint, "total_count" bigint, "success_rate" numeric)
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
WITH mastery_with_bloom AS (
  SELECT
    sm.mastery_level,
    -- Unnest the array of suggested bloom level codes into separate rows
    unnest(lo.suggested_bloom_levels) as bloom_code
  FROM
    public.student_mastery sm
  JOIN
    public.learning_objectives lo ON sm.learning_objective_code = lo.code
  WHERE
    sm.student_id = p_student_id
    AND (p_from_date IS NULL OR sm.assessed_at::date >= p_from_date)
    AND (p_to_date IS NULL OR sm.assessed_at::date <= p_to_date)
    -- Ensure we only consider LOs that have suggested bloom levels
    AND array_length(lo.suggested_bloom_levels, 1) > 0
)
SELECT
  mwb.bloom_code,
  bl.name as bloom_name,
  COUNT(*) FILTER (WHERE mwb.mastery_level = 'mastered') AS correct_count,
  COUNT(*) AS total_count,
  -- Handle division by zero case
  CASE
    WHEN COUNT(*) = 0 THEN 0.0
    ELSE ROUND((COUNT(*) FILTER (WHERE mwb.mastery_level = 'mastered') * 100.0 / COUNT(*)), 2)
  END::numeric AS success_rate
FROM
  mastery_with_bloom mwb
JOIN
  public.bloom_levels bl ON mwb.bloom_code = bl.code
GROUP BY
  mwb.bloom_code, bl.name
ORDER BY
  success_rate ASC;
$$;
```

#### `get_student_performance_report_data`
```sql
CREATE OR REPLACE FUNCTION "public"."get_student_performance_report_data"("p_student_id" "uuid", "p_from_date" timestamp with time zone DEFAULT NULL::timestamp with time zone, "p_to_date" timestamp with time zone DEFAULT NULL::timestamp with time zone) RETURNS TABLE("id" "uuid", "assignment_id" "uuid", "exam_code" "text", "test_name" "text", "score" integer, "started_at" timestamp with time zone, "completed_at" timestamp with time zone, "created_at" timestamp with time zone, "answers" "jsonb")
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.assignment_id, -- Added this field to the SELECT statement
        s.context_code AS exam_code,
        COALESCE(a.title, e.name, 'Practice Session') AS test_name,
        (s.session_data ->> 'score')::integer AS score,
        s.started_at,
        s.completed_at,
        s.submitted_at AS created_at,
        s.session_data AS answers
    FROM
        public.submissions s
    LEFT JOIN
        public.assignments a ON s.assignment_id = a.id
    LEFT JOIN
        public.exams e ON s.context_code = e.code
    WHERE
        s.student_id = p_student_id
        AND s.completed_at IS NOT NULL
        AND (p_from_date IS NULL OR s.submitted_at >= p_from_date)
        AND (p_to_date IS NULL OR s.submitted_at <= p_to_date);
END;
$$;
```

#### `get_analytics_for_exam`
```sql
CREATE OR REPLACE FUNCTION "public"."get_analytics_for_exam"("p_exam_code" "text", "p_from_date" timestamp with time zone DEFAULT NULL::timestamp with time zone, "p_to_date" timestamp with time zone DEFAULT NULL::timestamp with time zone) RETURNS TABLE("id" "uuid", "student_id" "uuid", "exam_code" "text", "score" numeric, "started_at" timestamp with time zone, "completed_at" timestamp with time zone, "answers" "jsonb", "created_at" timestamp with time zone, "student_full_name" "text", "assignment_title" "text")
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.student_id,
        s.context_code as exam_code,
        (s.session_data ->> 'percentage')::numeric as score,
        s.started_at,
        s.completed_at,
        s.session_data as answers,
        s.submitted_at as created_at, -- FIX: Select 'submitted_at' and alias it as 'created_at'
        p.full_name as student_full_name,
        a.title as assignment_title
    FROM
        public.submissions s
    LEFT JOIN
        public.profiles p ON s.student_id = p.id
    LEFT JOIN
        public.assignments a ON s.assignment_id = a.id
    WHERE
        s.context_code = p_exam_code
        AND s.completed_at IS NOT NULL
        AND (p_from_date IS NULL OR s.submitted_at >= p_from_date)
        AND (p_to_date IS NULL OR s.submitted_at <= p_to_date);
END;
$$;
```

#### `get_system_kpis`
```sql
CREATE OR REPLACE FUNCTION "public"."get_system_kpis"("p_from_date" "date" DEFAULT NULL::"date", "p_to_date" "date" DEFAULT NULL::"date") RETURNS TABLE("total_questions" bigint, "total_exams" bigint, "total_attempts" bigint, "completed_attempts" bigint, "active_students" bigint)
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        (SELECT count(*) FROM public.questions WHERE (p_from_date IS NULL OR last_modified::date >= p_from_date) AND (p_to_date IS NULL OR last_modified::date <= p_to_date)) AS total_questions,
        (SELECT count(*) FROM public.exams WHERE (p_from_date IS NULL OR last_modified::date >= p_from_date) AND (p_to_date IS NULL OR last_modified::date <= p_to_date)) AS total_exams,
        (SELECT count(*) FROM public.submissions WHERE (p_from_date IS NULL OR submitted_at::date >= p_from_date) AND (p_to_date IS NULL OR submitted_at::date <= p_to_date)) AS total_attempts,
        (SELECT count(*) FROM public.submissions WHERE completed_at IS NOT NULL AND (p_from_date IS NULL OR submitted_at::date >= p_from_date) AND (p_to_date IS NULL OR submitted_at::date <= p_to_date)) AS completed_attempts,
        (SELECT count(DISTINCT student_id) FROM public.submissions WHERE (p_from_date IS NULL OR submitted_at::date >= p_from_date) AND (p_to_date IS NULL OR submitted_at::date <= p_to_date)) AS active_students;
END;
$$;
```

#### `get_question_distributions`
```sql
CREATE OR REPLACE FUNCTION "public"."get_question_distributions"("p_from_date" timestamp with time zone DEFAULT NULL::timestamp with time zone, "p_to_date" timestamp with time zone DEFAULT NULL::timestamp with time zone) RETURNS "jsonb"
    LANGUAGE "sql"
    AS $$
WITH questions_in_range AS (
    -- First, select the questions within the specified date range
    SELECT code
    FROM public.questions
    WHERE (p_from_date IS NULL OR last_modified >= p_from_date)
      AND (p_to_date IS NULL OR last_modified <= p_to_date)
),
enriched_data AS (
    -- Then, enrich these questions with metadata by traversing the knowledge graph
    SELECT
        qir.code AS question_code,
        s.code AS subject_code,
        lo.suggested_bloom_levels, -- This is now an array
        q.question_type_code
    FROM questions_in_range qir
    JOIN public.questions q ON q.code = qir.code
    LEFT JOIN public.question_learning_objectives qlo ON qir.code = qlo.question_code
    LEFT JOIN public.learning_objectives lo ON qlo.learning_objective_code = lo.code
    LEFT JOIN public.topic_learning_objectives tlo ON lo.code = tlo.learning_objective_code
    LEFT JOIN public.topics t ON tlo.topic_code = t.code
    LEFT JOIN public.category_topics ct ON t.code = ct.topic_code
    LEFT JOIN public.categories c ON ct.category_code = c.code
    LEFT JOIN public.subject_categories sc ON c.code = sc.category_code
    LEFT JOIN public.subjects s ON sc.subject_code = s.code
),
subject_dist AS (
    SELECT ed.subject_code, count(DISTINCT ed.question_code) AS q_count
    FROM enriched_data ed
    WHERE ed.subject_code IS NOT NULL
    GROUP BY ed.subject_code
),
bloom_dist AS (
    -- Unnest the array of bloom levels to count each one
    SELECT unnest(ed.suggested_bloom_levels) as bloom_level_code, count(DISTINCT ed.question_code) as q_count
    FROM enriched_data ed
    WHERE ed.suggested_bloom_levels IS NOT NULL AND array_length(ed.suggested_bloom_levels, 1) > 0
    GROUP BY 1
),
type_dist AS (
    SELECT ed.question_type_code, count(DISTINCT ed.question_code) AS q_count
    FROM enriched_data ed
    WHERE ed.question_type_code IS NOT NULL
    GROUP BY ed.question_type_code
)
SELECT jsonb_build_object(
    'bySubject', (
        SELECT COALESCE(jsonb_agg(
            jsonb_build_object('code', s.code, 'name', s.name, 'value', sd.q_count)
        ), '[]'::jsonb)
        FROM subject_dist sd
        JOIN public.subjects s ON sd.subject_code = s.code
    ),
    'byGradeLevel', '[]'::jsonb, -- Returning empty as grade_level is no longer directly on questions or LOs
    'byBloomLevel', (
        SELECT COALESCE(jsonb_agg(
            jsonb_build_object('code', bl.code, 'name', bl.name, 'value', bd.q_count)
        ), '[]'::jsonb)
        FROM bloom_dist bd
        JOIN public.bloom_levels bl ON bd.bloom_level_code = bl.code
    ),
    'byQuestionType', (
        SELECT COALESCE(jsonb_agg(
            jsonb_build_object('code', qt.code, 'name', qt.name, 'value', td.q_count)
        ), '[]'::jsonb)
        FROM type_dist td
        JOIN public.question_types qt ON td.question_type_code = qt.code
    )
);
$$;
```

#### `get_teacher_dashboard_summary`
```sql
CREATE OR REPLACE FUNCTION "public"."get_teacher_dashboard_summary"("p_teacher_id" "uuid") RETURNS "jsonb"
    LANGUAGE "plpgsql"
    AS $$
DECLARE
    summary_data jsonb;
BEGIN
    WITH teacher_classes AS (
        SELECT id FROM public.classrooms WHERE teacher_id = p_teacher_id
    ),
    pending_requests AS (
        SELECT COUNT(*) as count
        FROM public.classroom_members
        WHERE classroom_id IN (SELECT id FROM teacher_classes) AND status = 'pending'
    ),
    approved_students AS (
        SELECT COUNT(DISTINCT student_id) as count
        FROM public.classroom_members
        WHERE classroom_id IN (SELECT id FROM teacher_classes) AND status = 'approved'
    ),
    recent_activities AS (
        (
            -- Recent Join Requests
            SELECT
                cm.joined_at AS activity_timestamp,
                'join_request' AS type,
                jsonb_build_object(
                    'studentName', p.full_name,
                    'className', c.name,
                    'classId', c.id
                ) AS details
            FROM public.classroom_members cm
            JOIN public.profiles p ON cm.student_id = p.id
            JOIN public.classrooms c ON cm.classroom_id = c.id
            WHERE cm.classroom_id IN (SELECT id FROM teacher_classes) AND cm.status = 'pending'
            ORDER BY cm.joined_at DESC
            LIMIT 5
        )
        UNION ALL
        (
            -- Recent Submissions
            SELECT
                s.submitted_at AS activity_timestamp,
                'submission' AS type,
                jsonb_build_object(
                    'studentName', p.full_name,
                    'assignmentTitle', a.title,
                    'className', c.name,
                    'classId', c.id,
                    'assignmentId', a.id
                ) AS details
            FROM public.submissions s
            JOIN public.profiles p ON s.student_id = p.id
            JOIN public.assignments a ON s.assignment_id = a.id
            JOIN public.classrooms c ON s.classroom_id = c.id
            WHERE s.classroom_id IN (SELECT id FROM teacher_classes) AND s.submission_type = 'assignment'
            ORDER BY s.submitted_at DESC
            LIMIT 5
        )
        ORDER BY activity_timestamp DESC
        LIMIT 10
    )
    SELECT
        jsonb_build_object(
            'kpis', jsonb_build_object(
                'classCount', (SELECT COUNT(*) FROM teacher_classes),
                'studentCount', (SELECT count FROM approved_students),
                'pendingRequestCount', (SELECT count FROM pending_requests)
            ),
            'recentActivities', COALESCE((SELECT jsonb_agg(ra.*) FROM recent_activities ra), '[]'::jsonb)
        )
    INTO summary_data;

    RETURN summary_data;
END;
$$;
```

***

### 2. Quản lý Dữ liệu (Data Management - CRUD & Upsert)

#### Thao tác hàng loạt (Bulk Operations)

#### `bulk_create_questions_with_los`
```sql
CREATE OR REPLACE FUNCTION "public"."bulk_create_questions_with_los"("questions_data" "jsonb", "p_organization_code" "text") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    -- Biến để lưu trữ dữ liệu của một câu hỏi trong vòng lặp
    question_item jsonb;
    -- Biến để lưu trữ mã LO trong vòng lặp con
    lo_code text;
    -- Biến để lưu trữ mã câu hỏi mới được tạo
    new_question_code text;
BEGIN
    -- Bắt đầu vòng lặp qua mảng các câu hỏi được truyền vào
    FOR question_item IN SELECT * FROM jsonb_array_elements(questions_data)
    LOOP
        -- 1. TẠO MÃ CÂU HỎI MỚI (nếu chưa có)
        -- Ưu tiên mã được cung cấp, nếu không thì tạo mã mới
        new_question_code := COALESCE(
            question_item->>'code', 
            public.generate_question_code_from_config(question_item->'questionConfig') -- Giả sử bạn có hàm helper này
        );

        -- 2. INSERT BẢN GHI CÂU HỎI VÀO BẢNG `questions`
        -- Lưu ý: Chúng ta chưa điền các cột phi chuẩn hóa ở bước này.
        -- Trigger sẽ đảm nhiệm việc đó sau khi các liên kết LO được tạo.
        INSERT INTO public.questions (
            code,
            text,
            question_config,
            organization_code,
            -- Điền trực tiếp các giá trị đã được chuẩn hóa từ config
            question_type_code,
            difficulty_code
        )
        VALUES (
            new_question_code,
            -- Trích xuất text từ prompt bên trong question_config
            (question_item->'questionConfig'->>'prompt'), 
            -- Trích xuất object questionConfig dưới dạng jsonb
            question_item->'questionConfig', 
            p_organization_code,
            -- CHUẨN HÓA DỮ LIỆU NGAY KHI INSERT
            UPPER(question_item->'questionConfig'->>'questionType'),
            UPPER(REPLACE(question_item->'questionConfig'->>'difficulty', ' ', '_'))
        );

        -- 3. TẠO CÁC LIÊN KẾT VỚI LEARNING OBJECTIVES
        -- Kiểm tra xem 'learningObjectiveCodes' có tồn tại và là một mảng không
        IF jsonb_typeof(question_item->'learningObjectiveCodes') = 'array' THEN
            -- Lặp qua mảng các mã LO
            FOR lo_code IN SELECT * FROM jsonb_array_elements_text(question_item->'learningObjectiveCodes')
            LOOP
                -- Chèn liên kết vào bảng trung gian.
                -- Trigger trên bảng này sẽ tự động gọi hàm `sync_question_derived_codes`
                -- để cập nhật các cột phi chuẩn hóa trong bảng `questions`.
                INSERT INTO public.question_learning_objectives (question_code, learning_objective_code)
                VALUES (new_question_code, lo_code)
                ON CONFLICT DO NOTHING; -- Bỏ qua nếu liên kết đã tồn tại
            END LOOP;
        END IF;
    END LOOP;
END;
$$;
```

#### `bulk_upsert_categories_with_subjects`
```sql
CREATE OR REPLACE FUNCTION "public"."bulk_upsert_categories_with_subjects"("p_categories_data" "jsonb", "p_organization_code" "text") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    category_item jsonb;
    v_category_code text;
    v_subject_codes text[];
BEGIN
    FOR category_item IN SELECT * FROM jsonb_array_elements(p_categories_data) -- << ĐÃ CHUẨN HÓA
    LOOP
        v_category_code := category_item->>'code';
        
        -- 1. Upsert vào bảng `categories`
        INSERT INTO public.categories (code, name, description, organization_code)
        VALUES (
            v_category_code,
            category_item->>'name',
            category_item->>'description',
            p_organization_code
        )
        ON CONFLICT (code, organization_code) DO UPDATE SET
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            updated_at = now();

        -- 2. Xóa các liên kết môn học cũ
        DELETE FROM public.subject_categories WHERE category_code = v_category_code;

        -- 3. Chèn các liên kết môn học mới
        SELECT array_agg(value) INTO v_subject_codes FROM jsonb_array_elements_text(category_item->'subjectCodes');
        IF v_subject_codes IS NOT NULL AND array_length(v_subject_codes, 1) > 0 THEN
            INSERT INTO public.subject_categories (category_code, subject_code)
            SELECT v_category_code, unnest(v_subject_codes);
        END IF;
    END LOOP;
END;
$$;
```

#### `bulk_upsert_los_with_relations`
```sql
CREATE OR REPLACE FUNCTION "public"."bulk_upsert_los_with_relations"("p_los_data" "jsonb", "p_organization_code" "text") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    lo_item jsonb;
    v_lo_code text;
    v_topic_codes text[];
BEGIN
    -- LƯỢT 1: UPSERT THÔNG TIN CỐT LÕI CỦA TẤT CẢ CÁC LOs
    -- Mục đích: Đảm bảo tất cả các 'code' đều tồn tại trong bảng trước khi tạo mối quan hệ.
    -- parent_lo_code và các liên kết topics sẽ được cập nhật ở Lượt 2.
    FOR lo_item IN SELECT * FROM jsonb_array_elements(p_los_data)
    LOOP
        v_lo_code := lo_item->>'code';

        INSERT INTO public.learning_objectives (
            code, name, description, lo_type, organization_code, context_tags, keywords, suggested_bloom_levels
        )
        VALUES (
            v_lo_code,
            COALESCE(lo_item->>'name', ''),
            lo_item->>'description',
            COALESCE(lo_item->>'loType', 'SPECIFIC_IMPL'),
            p_organization_code,
            COALESCE((SELECT array_agg(value) FROM jsonb_array_elements_text(lo_item->'contextTags')), '{}'::text[]),
            COALESCE((SELECT array_agg(value) FROM jsonb_array_elements_text(lo_item->'keywords')), '{}'::text[]),
            COALESCE((SELECT array_agg(value) FROM jsonb_array_elements_text(lo_item->'suggestedBloomLevels')), '{}'::text[])
        )
        ON CONFLICT (code, organization_code) DO UPDATE SET
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            lo_type = EXCLUDED.lo_type,
            context_tags = EXCLUDED.context_tags,
            keywords = EXCLUDED.keywords,
            suggested_bloom_levels = EXCLUDED.suggested_bloom_levels,
            updated_at = now();
    END LOOP;

    -- LƯỢT 2: CẬP NHẬT CÁC MỐI QUAN HỆ (parent_lo_code và topicCodes)
    -- Mục đích: Bây giờ tất cả các LOs đã tồn tại, việc tạo liên kết khóa ngoại sẽ luôn thành công.
    FOR lo_item IN SELECT * FROM jsonb_array_elements(p_los_data)
    LOOP
        v_lo_code := lo_item->>'code';

        -- Cập nhật parent_lo_code
        UPDATE public.learning_objectives
        SET parent_lo_code = lo_item->>'parentLoCode'
        WHERE code = v_lo_code AND organization_code = p_organization_code;

        -- Xóa và thêm lại các liên kết topic
        DELETE FROM public.topic_learning_objectives WHERE learning_objective_code = v_lo_code;

        SELECT array_agg(value) INTO v_topic_codes FROM jsonb_array_elements_text(lo_item->'topicCodes');
        IF v_topic_codes IS NOT NULL AND array_length(v_topic_codes, 1) > 0 THEN
            INSERT INTO public.topic_learning_objectives (topic_code, learning_objective_code)
            SELECT unnest(v_topic_codes), v_lo_code;
        END IF;
    END LOOP;

END;
$$;
```

#### `bulk_upsert_subjects_with_courses`
```sql
CREATE OR REPLACE FUNCTION "public"."bulk_upsert_subjects_with_courses"("p_subjects_data" "jsonb", "p_organization_code" "text") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    subject_item jsonb;
    v_subject_code text;
    v_course_codes text[];
BEGIN
    -- Lặp qua từng đối tượng subject trong mảng JSON đầu vào
    FOR subject_item IN SELECT * FROM jsonb_array_elements(p_subjects_data) -- << ĐÃ CHUẨN HÓA
    LOOP
        v_subject_code := subject_item->>'code';
        
        -- 1. Upsert vào bảng chính `subjects`
        INSERT INTO public.subjects (code, name, description, organization_code)
        VALUES (
            v_subject_code,
            subject_item->>'name',
            subject_item->>'description',
            p_organization_code
        )
        ON CONFLICT (code, organization_code) DO UPDATE SET
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            updated_at = now();

        -- 2. Xóa các liên kết khóa học cũ
        DELETE FROM public.course_subjects WHERE subject_code = v_subject_code;

        -- 3. Chèn các liên kết khóa học mới
        SELECT array_agg(value) INTO v_course_codes FROM jsonb_array_elements_text(subject_item->'courseCodes');
        IF v_course_codes IS NOT NULL AND array_length(v_course_codes, 1) > 0 THEN
            INSERT INTO public.course_subjects (subject_code, course_code)
            SELECT v_subject_code, unnest(v_course_codes);
        END IF;
    END LOOP;
END;
$$;
```

#### `bulk_upsert_topics_with_categories`
```sql
CREATE OR REPLACE FUNCTION "public"."bulk_upsert_topics_with_categories"("p_topics_data" "jsonb", "p_organization_code" "text") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    topic_record jsonb;
BEGIN
    -- Loop through each topic object in the input JSON array
    FOR topic_record IN SELECT * FROM jsonb_array_elements(p_topics_data)
    LOOP
        -- Call the single-item upsert function for each record
        -- This reuses the existing logic and ensures consistency
        PERFORM public.upsert_topic_with_relations(
            p_code := topic_record->>'code',
            p_name := topic_record->>'name',
            p_description := topic_record->>'description',
            p_organization_code := p_organization_code,
            p_category_codes := ARRAY(SELECT jsonb_array_elements_text(topic_record->'categoryCodes'))
        );
    END LOOP;
END;
$$;
```

#### Thao tác đơn lẻ (Single Item Operations)

#### `create_category_with_subjects`
```sql
CREATE OR REPLACE FUNCTION "public"."create_category_with_subjects"("p_code" "text", "p_name" "text", "p_description" "text", "p_organization_code" "text", "p_subject_codes" "jsonb") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    subject_code_item text;
BEGIN
    -- Bước 1: Thêm category mới vào bảng chính
    INSERT INTO public.categories(code, name, description, organization_code)
    VALUES (p_code, p_name, p_description, p_organization_code);

    -- Bước 2: Lặp qua mảng JSON và thêm các liên kết
    FOR subject_code_item IN SELECT * FROM jsonb_array_elements_text(p_subject_codes)
    LOOP
        INSERT INTO public.subject_categories (category_code, subject_code)
        VALUES (p_code, subject_code_item);
    END LOOP;
END;
$$;
```

#### `create_question_with_los` (3 phiên bản)
```sql
-- Version 1
CREATE OR REPLACE FUNCTION "public"."create_question_with_los"("p_question_config" "jsonb", "p_organization_code" "text", "p_learning_objective_codes" "text"[]) RETURNS SETOF "public"."questions"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    new_question_code TEXT;
    new_question_id UUID;
BEGIN
    -- STEP 1: GENERATE NEW, SIMPLIFIED QUESTION CODE
    new_question_code := public.generate_question_code(
        p_question_config->>'questionType'
    );

    -- STEP 2: INSERT NEW QUESTION
    INSERT INTO public.questions (
        code, text, question_config, organization_code, question_type_code, difficulty_code
    )
    VALUES (
        new_question_code,
        p_question_config->>'prompt',
        p_question_config,
        p_organization_code,
        UPPER(REPLACE(p_question_config->>'questionType', '-', '_')),
        UPPER(REPLACE(p_question_config->>'difficulty', ' ', '_'))
    )
    RETURNING id INTO new_question_id;

    -- STEP 3: CREATE ASSOCIATIONS (This will trigger the sync)
    IF array_length(p_learning_objective_codes, 1) > 0 THEN
        INSERT INTO public.question_learning_objectives (question_code, learning_objective_code)
        SELECT new_question_code, unnest(p_learning_objective_codes);
    ELSE
        -- If no LOs, we still need to trigger a sync to ensure fields are at least empty arrays
        PERFORM public.sync_question_derived_codes(new_question_code);
    END IF;

    -- STEP 4: RETURN THE FINALIZED QUESTION
    RETURN QUERY SELECT * FROM public.questions WHERE id = new_question_id;
END;
$$;

-- Version 2
CREATE OR REPLACE FUNCTION "public"."create_question_with_los"("p_code" "text", "p_question_config" "jsonb", "p_text" "text", "p_organization_code" "text", "p_learning_objective_codes" "text"[]) RETURNS SETOF "public"."questions"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$DECLARE
    new_question_id UUID;
    lo_code TEXT;
    v_subject_codes TEXT[];
    v_category_codes TEXT[];
    v_topic_codes TEXT[];
    v_bloom_level_codes TEXT[];
BEGIN
    -- Step 1: Aggregate metadata from the provided Learning Objective codes
    WITH lo_metadata AS (
        SELECT
            -- Use array_agg to collect all codes from the related LOs
            array_agg(DISTINCT s.code) FILTER (WHERE s.code IS NOT NULL) as subject_codes,
            array_agg(DISTINCT c.code) FILTER (WHERE c.code IS NOT NULL) as category_codes,
            array_agg(DISTINCT t.code) FILTER (WHERE t.code IS NOT NULL) as topic_codes,
            array_agg(DISTINCT bl.code) FILTER (WHERE bl.code IS NOT NULL) as bloom_level_codes
        FROM
            unnest(p_learning_objective_codes) AS input_lo_code
        JOIN
            public.learning_objectives lo ON lo.code = input_lo_code
        -- Traverse the graph upwards to find all related metadata
        LEFT JOIN public.topic_learning_objectives tlo ON lo.code = tlo.learning_objective_code
        LEFT JOIN public.topics t ON tlo.topic_code = t.code
        LEFT JOIN public.category_topics ct ON t.code = ct.topic_code
        LEFT JOIN public.categories c ON ct.category_code = c.code
        LEFT JOIN public.subject_categories sc ON c.code = sc.category_code
        LEFT JOIN public.subjects s ON sc.subject_code = s.code
        LEFT JOIN public.bloom_levels bl ON bl.name = ANY(lo.bloom_levels_guideline)
    )
    SELECT
        COALESCE(subject_codes, '{}'),
        COALESCE(category_codes, '{}'),
        COALESCE(topic_codes, '{}'),
        COALESCE(bloom_level_codes, '{}')
    INTO
        v_subject_codes,
        v_category_codes,
        v_topic_codes,
        v_bloom_level_codes
    FROM lo_metadata;

    -- Step 2: Insert the new question with both direct and aggregated denormalized data
    INSERT INTO public.questions (
        code,
        question_config,
        text,
        organization_code,
        question_type_code,
        difficulty_code,
        -- Insert the aggregated metadata
        subject_codes,
        category_codes,
        topic_codes,
        bloom_level_codes
    )
    VALUES (
        p_code,
        p_question_config,
        p_text,
        p_organization_code,
        UPPER(p_question_config->>'questionType'),
        COALESCE(UPPER(REPLACE(p_question_config->>'difficulty', ' ', '_')), 'MEDIUM'),
        -- Use the variables populated in Step 1
        v_subject_codes,
        v_category_codes,
        v_topic_codes,
        v_bloom_level_codes
    )
    RETURNING id INTO new_question_id;

    -- Step 3: Associate the new question with its learning objectives in the junction table
    IF array_length(p_learning_objective_codes, 1) > 0 THEN
        FOREACH lo_code IN ARRAY p_learning_objective_codes
        LOOP
            INSERT INTO public.question_learning_objectives (question_code, learning_objective_code)
            VALUES (p_code, lo_code);
        END LOOP;
    END IF;

    -- Step 4: Return the newly created question record
    RETURN QUERY SELECT * FROM public.questions WHERE id = new_question_id;
END;$$;

-- Version 3
CREATE OR REPLACE FUNCTION "public"."create_question_with_los"("p_question_config" "jsonb", "p_organization_code" "text", "p_learning_objective_codes" "text"[], "p_topic_codes" "text"[] DEFAULT '{}'::"text"[], "p_category_codes" "text"[] DEFAULT '{}'::"text"[], "p_subject_codes" "text"[] DEFAULT '{}'::"text"[], "p_course_codes" "text"[] DEFAULT '{}'::"text"[]) RETURNS SETOF "public"."questions"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    new_question_code TEXT;
    new_question_id UUID;
    v_subject_code TEXT;
    v_topic_code TEXT;
    v_bloom_code TEXT; -- Vẫn giữ lại để tương thích logic code cũ
BEGIN
    -- STEP 1: DETERMINE METADATA FOR CODE GENERATION
    IF array_length(p_learning_objective_codes, 1) > 0 THEN
        -- **COMPETENCY-FIRST LOGIC:** Infer metadata from provided LOs
        WITH aggregated_metadata AS (
            SELECT
                array_agg(DISTINCT s.code) FILTER (WHERE s.code IS NOT NULL) as all_subject_codes,
                array_agg(DISTINCT t.code) FILTER (WHERE t.code IS NOT NULL) as all_topic_codes,
                array_agg(DISTINCT bl.code) FILTER (WHERE bl.name = ANY(lo.suggested_bloom_levels)) as all_bloom_codes
            FROM unnest(p_learning_objective_codes) as input_lo_code
            JOIN public.learning_objectives lo ON lo.code = input_lo_code
            LEFT JOIN public.topic_learning_objectives tlo ON lo.code = tlo.learning_objective_code
            LEFT JOIN public.topics t ON tlo.topic_code = t.code
            LEFT JOIN public.category_topics ct ON t.code = ct.topic_code
            LEFT JOIN public.categories c ON ct.category_code = c.code
            LEFT JOIN public.subject_categories sc ON c.code = sc.category_code
            LEFT JOIN public.subjects s ON sc.subject_code = s.code
            LEFT JOIN public.bloom_levels bl ON bl.name = ANY(lo.suggested_bloom_levels)
        )
        SELECT
            all_subject_codes[1],
            all_topic_codes[1],
            all_bloom_codes[1]
        INTO v_subject_code, v_topic_code, v_bloom_code
        FROM aggregated_metadata;
    ELSE
        -- **HIERARCHY-FIRST (FALLBACK) LOGIC:** Use directly provided codes
        v_subject_code := p_subject_codes[1];
        v_topic_code := p_topic_codes[1];
        v_bloom_code := NULL; -- Bloom level is not passed directly for now
    END IF;

    -- STEP 2: GENERATE NEW, SIMPLIFIED QUESTION CODE
    new_question_code := public.generate_question_code(
        p_question_config->>'questionType'
    );

    -- STEP 3: INSERT NEW QUESTION
    INSERT INTO public.questions (
        code, text, question_config, organization_code, question_type_code, difficulty_code
    )
    VALUES (
        new_question_code,
        p_question_config->>'prompt',
        p_question_config,
        p_organization_code,
        UPPER(REPLACE(p_question_config->>'questionType', '-', '_')),
        UPPER(REPLACE(p_question_config->>'difficulty', ' ', '_'))
    )
    RETURNING id INTO new_question_id;

    -- STEP 4: CREATE ASSOCIATIONS OR DIRECTLY UPDATE METADATA
    IF array_length(p_learning_objective_codes, 1) > 0 THEN
        -- **COMPETENCY-FIRST PATH:** Insert links, which will trigger sync_question_derived_codes
        INSERT INTO public.question_learning_objectives (question_code, learning_objective_code)
        SELECT new_question_code, unnest(p_learning_objective_codes);
    ELSE
        -- **HIERARCHY-FIRST PATH:** No LOs, so manually update the denormalized columns.
        -- The trigger will not run, so we must do it here.
        UPDATE public.questions
        SET 
            topic_codes = COALESCE(p_topic_codes, '{}'),
            category_codes = COALESCE(p_category_codes, '{}'),
            subject_codes = COALESCE(p_subject_codes, '{}'),
            course_codes = COALESCE(p_course_codes, '{}'),
            learning_objective_codes = '{}' -- Ensure it's an empty array
        WHERE id = new_question_id;
    END IF;

    -- STEP 5: RETURN THE FINALIZED QUESTION
    RETURN QUERY SELECT * FROM public.questions WHERE id = new_question_id;
END;
$$;
```

#### `create_subject_with_courses` (2 phiên bản)
```sql
-- Version 1
CREATE OR REPLACE FUNCTION "public"."create_subject_with_courses"("p_code" "text", "p_name" "text", "p_organization_code" "text", "p_course_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
DECLARE
    new_subject_id UUID;
BEGIN
    -- Insert into the main subjects table
    INSERT INTO public.subjects (code, name, organization_code)
    VALUES (p_code, p_name, p_organization_code)
    RETURNING id INTO new_subject_id;

    -- Insert relationships into the junction table if any course codes are provided
    IF array_length(p_course_codes, 1) > 0 THEN
        INSERT INTO public.course_subjects (subject_code, course_code)
        SELECT p_code, unnest(p_course_codes);
    END IF;
END;
$$;

-- Version 2
CREATE OR REPLACE FUNCTION "public"."create_subject_with_courses"("p_code" "text", "p_name" "text", "p_description" "text", "p_organization_code" "text", "p_course_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    new_subject_id uuid;
BEGIN
    -- 1. Insert a new subject and get its ID
    INSERT INTO public.subjects (code, name, description, organization_code)
    VALUES (p_code, p_name, p_description, p_organization_code)
    RETURNING id INTO new_subject_id;

    -- 2. If course codes are provided, link them in the junction table
    IF array_length(p_course_codes, 1) > 0 THEN
        INSERT INTO public.course_subjects (course_code, subject_code)
        SELECT unnest(p_course_codes), p_code;
    END IF;
END;
$$;
```

#### `update_category_with_subjects`
```sql
CREATE OR REPLACE FUNCTION "public"."update_category_with_subjects"("p_category_code" "text", "p_name" "text", "p_description" "text", "p_subject_codes" "jsonb") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    subject_code_item text;
BEGIN
    -- Bước 1: Cập nhật thông tin trong bảng chính 'categories'
    -- Lưu ý: Chúng ta không cập nhật subject_code denormalized ở đây nữa vì nó không tồn tại trong schema bạn cung cấp
    UPDATE public.categories
    SET
        name = p_name,
        description = p_description,
        updated_at = now()
    WHERE code = p_category_code;

    -- Bước 2: Xóa tất cả các liên kết môn học cũ của danh mục này
    DELETE FROM public.subject_categories
    WHERE category_code = p_category_code;

    -- Bước 3: Thêm lại các liên kết môn học mới nếu có
    IF jsonb_array_length(p_subject_codes) > 0 THEN
        FOR subject_code_item IN SELECT * FROM jsonb_array_elements_text(p_subject_codes)
        LOOP
            INSERT INTO public.subject_categories (category_code, subject_code)
            VALUES (p_category_code, subject_code_item);
        END LOOP;
    END IF;
END;
$$;
```

#### `update_question_with_los`
```sql
CREATE OR REPLACE FUNCTION "public"."update_question_with_los"("p_question_id" "uuid", "p_question_config" "jsonb", "p_text" "text", "p_learning_objective_codes" "text"[]) RETURNS SETOF "public"."questions"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$DECLARE
    v_question_code TEXT;
    lo_code TEXT;
    v_subject_codes TEXT[];
    v_category_codes TEXT[];
    v_topic_codes TEXT[];
    v_bloom_level_codes TEXT[];
BEGIN
    -- Step 1: Get the question code we are updating
    SELECT code INTO v_question_code FROM public.questions WHERE id = p_question_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Question with ID % not found', p_question_id;
    END IF;

    -- Step 2: Aggregate metadata from the NEW list of Learning Objective codes
    WITH lo_metadata AS (
        SELECT
            array_agg(DISTINCT s.code) FILTER (WHERE s.code IS NOT NULL) as subject_codes,
            array_agg(DISTINCT c.code) FILTER (WHERE c.code IS NOT NULL) as category_codes,
            array_agg(DISTINCT t.code) FILTER (WHERE t.code IS NOT NULL) as topic_codes,
            array_agg(DISTINCT bl.code) FILTER (WHERE bl.code IS NOT NULL) as bloom_level_codes
        FROM
            unnest(p_learning_objective_codes) AS input_lo_code
        JOIN
            public.learning_objectives lo ON lo.code = input_lo_code
        LEFT JOIN public.topic_learning_objectives tlo ON lo.code = tlo.learning_objective_code
        LEFT JOIN public.topics t ON tlo.topic_code = t.code
        LEFT JOIN public.category_topics ct ON t.code = ct.topic_code
        LEFT JOIN public.categories c ON ct.category_code = c.code
        LEFT JOIN public.subject_categories sc ON c.code = sc.category_code
        LEFT JOIN public.subjects s ON sc.subject_code = s.code
        LEFT JOIN public.bloom_levels bl ON bl.name = ANY(lo.bloom_levels_guideline)
    )
    SELECT
        COALESCE(subject_codes, '{}'),
        COALESCE(category_codes, '{}'),
        COALESCE(topic_codes, '{}'),
        COALESCE(bloom_level_codes, '{}')
    INTO
        v_subject_codes,
        v_category_codes,
        v_topic_codes,
        v_bloom_level_codes
    FROM lo_metadata;

    -- Step 3: Update the question details including the new aggregated metadata
    UPDATE public.questions
    SET
        question_config = p_question_config,
        text = p_text,
        last_modified = now(),
        question_type_code = UPPER(p_question_config->>'questionType'),
        difficulty_code = COALESCE(UPPER(REPLACE(p_question_config->>'difficulty', ' ', '_')), 'MEDIUM'),
        subject_codes = v_subject_codes,
        category_codes = v_category_codes,
        topic_codes = v_topic_codes,
        bloom_level_codes = v_bloom_level_codes
    WHERE id = p_question_id;

    -- Step 4: Manage its LO associations
    -- 4a. Delete all existing associations
    DELETE FROM public.question_learning_objectives
    WHERE question_code = v_question_code;

    -- 4b. Insert the new set of associations
    IF array_length(p_learning_objective_codes, 1) > 0 THEN
        FOREACH lo_code IN ARRAY p_learning_objective_codes
        LOOP
            INSERT INTO public.question_learning_objectives (question_code, learning_objective_code)
            VALUES (v_question_code, lo_code);
        END LOOP;
    END IF;

    -- Step 5: Return the updated question record
    RETURN QUERY SELECT * FROM public.questions WHERE id = p_question_id;
END;$$;
```

#### `update_subject_with_courses`
```sql
CREATE OR REPLACE FUNCTION "public"."update_subject_with_courses"("p_subject_code" "text", "p_name" "text", "p_description" "text", "p_course_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Bước 1: Cập nhật thông tin trong bảng chính 'subjects'
    UPDATE public.subjects
    SET
        name = p_name,
        description = p_description,
        updated_at = now()
    WHERE code = p_subject_code;

    -- Bước 2: Xóa tất cả các liên kết khóa học cũ của môn học này
    DELETE FROM public.course_subjects
    WHERE subject_code = p_subject_code;

    -- Bước 3: Thêm lại các liên kết khóa học mới nếu có
    IF array_length(p_course_codes, 1) > 0 THEN
        INSERT INTO public.course_subjects (subject_code, course_code)
        SELECT p_subject_code, unnest(p_course_codes);
    END IF;
END;
$$;
```

#### `upsert_approach_with_details` (3 phiên bản)
```sql
-- Version 1
CREATE OR REPLACE FUNCTION "public"."upsert_approach_with_details"("p_code" "text", "p_name" "text", "p_verb_en" "text", "p_verb_vi" "text", "p_suggest_bloom_level_code" "text", "p_knowledge_dimension_code" "text", "p_example_en" "text", "p_example_vi" "text", "p_question_type_codes" "text"[], "p_difficulty_codes" "text"[], "p_context_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Step 1: Upsert the main approach record.
    -- If the code exists, it updates the record. If not, it inserts a new one.
    INSERT INTO public.approaches (
        code, name, verb_en, verb_vi, suggest_bloom_level_code, knowledge_dimension_code, example_en, example_vi
    ) VALUES (
        p_code, p_name, p_verb_en, p_verb_vi, p_suggest_bloom_level_code, p_knowledge_dimension_code, p_example_en, p_example_vi
    )
    ON CONFLICT (code) DO UPDATE SET
        name = p_name,
        verb_en = p_verb_en,
        verb_vi = p_verb_vi,
        suggest_bloom_level_code = p_suggest_bloom_level_code,
        knowledge_dimension_code = p_knowledge_dimension_code,
        example_en = p_example_en,
        example_vi = p_example_vi;

    -- Step 2: Clear out old associations in junction tables for this approach.
    -- ON DELETE CASCADE on the foreign keys in junction tables also handles this if you delete and re-insert the main approach,
    -- but this is a safer way to handle updates without deleting the main record.
    DELETE FROM public.approach_question_types WHERE approach_code = p_code;
    DELETE FROM public.approach_difficulties WHERE approach_code = p_code;
    DELETE FROM public.approach_contexts WHERE approach_code = p_code;

    -- Step 3: Insert new associations into the junction tables.
    -- Insert question types if the array is not empty
    IF array_length(p_question_type_codes, 1) > 0 THEN
        INSERT INTO public.approach_question_types (approach_code, question_type_code)
        SELECT p_code, unnest(p_question_type_codes);
    END IF;

    -- Insert difficulties if the array is not empty
    IF array_length(p_difficulty_codes, 1) > 0 THEN
        INSERT INTO public.approach_difficulties (approach_code, difficulty_code)
        SELECT p_code, unnest(p_difficulty_codes);
    END IF;

    -- Insert contexts if the array is not empty
    IF array_length(p_context_codes, 1) > 0 THEN
        INSERT INTO public.approach_contexts (approach_code, context_code)
        SELECT p_code, unnest(p_context_codes);
    END IF;

END;
$$;

-- Version 2
CREATE OR REPLACE FUNCTION "public"."upsert_approach_with_details"("p_code" "text", "p_name" "text", "p_verb_en" "text", "p_verb_vi" "text", "p_knowledge_dimension_code" "text", "p_bloom_level_code" "text", "p_question_type_code" "text", "p_example_en" "text", "p_example_vi" "text", "p_context_codes" "text"[], "p_difficulty_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    -- Step 1: Upsert the main record in the 'approaches' table
    INSERT INTO public.approaches (
        code, name, verb_en, verb_vi, knowledge_dimension_code, bloom_level_code, question_type_code, example_en, example_vi
    )
    VALUES (
        p_code, p_name, p_verb_en, p_verb_vi, p_knowledge_dimension_code, p_bloom_level_code, p_question_type_code, p_example_en, p_example_vi
    )
    ON CONFLICT (code) DO UPDATE SET
        name = EXCLUDED.name,
        verb_en = EXCLUDED.verb_en,
        verb_vi = EXCLUDED.verb_vi,
        knowledge_dimension_code = EXCLUDED.knowledge_dimension_code,
        bloom_level_code = EXCLUDED.bloom_level_code,
        question_type_code = EXCLUDED.question_type_code,
        example_en = EXCLUDED.example_en,
        example_vi = EXCLUDED.example_vi;

    -- Step 2: Delete old relationships for this approach in junction tables
    DELETE FROM public.approach_contexts WHERE approach_code = p_code;
    DELETE FROM public.approach_difficulties WHERE approach_code = p_code;

    -- Step 3: Insert new relationships into junction tables if the arrays are not empty
    IF array_length(p_context_codes, 1) > 0 THEN
        INSERT INTO public.approach_contexts (approach_code, context_code)
        SELECT p_code, unnest(p_context_codes);
    END IF;

    IF array_length(p_difficulty_codes, 1) > 0 THEN
        INSERT INTO public.approach_difficulties (approach_code, difficulty_code)
        SELECT p_code, unnest(p_difficulty_codes);
    END IF;

END;
$$;

-- Version 3 (upsert_approach_with_details_v2)
CREATE OR REPLACE FUNCTION "public"."upsert_approach_with_details_v2"("p_code" "text", "p_name" "text", "p_verb_en" "text", "p_verb_vi" "text", "p_suggest_bloom_level_code" "text", "p_knowledge_dimension_code" "text", "p_question_type_code" "text", "p_example_en" "text", "p_example_vi" "text", "p_difficulty_codes" "text"[], "p_context_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Step 1: Upsert the main approach record.
    INSERT INTO public.approaches (
        code, name, verb_en, verb_vi, suggest_bloom_level_code, knowledge_dimension_code, question_type_code, example_en, example_vi
    ) VALUES (
        p_code, p_name, p_verb_en, p_verb_vi, p_suggest_bloom_level_code, p_knowledge_dimension_code, p_question_type_code, p_example_en, p_example_vi
    )
    ON CONFLICT (code) DO UPDATE SET
        name = p_name,
        verb_en = p_verb_en,
        verb_vi = p_verb_vi,
        suggest_bloom_level_code = p_suggest_bloom_level_code,
        knowledge_dimension_code = p_knowledge_dimension_code,
        question_type_code = p_question_type_code,
        example_en = p_example_en,
        example_vi = p_example_vi;

    -- Step 2: Clear out old associations in junction tables for this approach.
    DELETE FROM public.approach_difficulties WHERE approach_code = p_code;
    DELETE FROM public.approach_contexts WHERE approach_code = p_code;

    -- Step 3: Insert new associations into the junction tables.
    -- Insert difficulties if the array is not null and has elements
    IF p_difficulty_codes IS NOT NULL AND array_length(p_difficulty_codes, 1) > 0 THEN
        INSERT INTO public.approach_difficulties (approach_code, difficulty_code)
        SELECT p_code, unnest(p_difficulty_codes);
    END IF;

    -- Insert contexts if the array is not null and has elements
    IF p_context_codes IS NOT NULL AND array_length(p_context_codes, 1) > 0 THEN
        INSERT INTO public.approach_contexts (approach_code, context_code)
        SELECT p_code, unnest(p_context_codes);
    END IF;

END;
$$;
```

#### `upsert_lo_with_relations`
```sql
CREATE OR REPLACE FUNCTION "public"."upsert_lo_with_relations"("p_code" "text", "p_name" "text", "p_description" "text", "p_lo_type" "text", "p_parent_lo_code" "text", "p_context_tags" "text"[], "p_keywords" "text"[], "p_organization_code" "text", "p_topic_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    v_lo_exists boolean;
BEGIN
    -- Check if LO exists
    SELECT EXISTS (SELECT 1 FROM public.learning_objectives WHERE code = p_code AND organization_code = p_organization_code) INTO v_lo_exists;

    IF v_lo_exists THEN
        -- Update existing LO
        UPDATE public.learning_objectives
        SET 
            name = p_name,
            description = p_description,
            lo_type = p_lo_type,
            parent_lo_code = p_parent_lo_code,
            context_tags = p_context_tags,
            keywords = p_keywords,
            updated_at = now()
        WHERE code = p_code AND organization_code = p_organization_code;
    ELSE
        -- Insert new LO
        INSERT INTO public.learning_objectives (code, name, description, lo_type, parent_lo_code, context_tags, keywords, organization_code)
        VALUES (p_code, p_name, p_description, p_lo_type, p_parent_lo_code, p_context_tags, p_keywords, p_organization_code);
    END IF;

    -- Manage relationships in the junction table
    -- 1. Delete old relationships for this LO
    DELETE FROM public.topic_learning_objectives WHERE learning_objective_code = p_code;

    -- 2. Insert new relationships if any are provided
    IF array_length(p_topic_codes, 1) > 0 THEN
        INSERT INTO public.topic_learning_objectives (topic_code, learning_objective_code)
        SELECT unnest(p_topic_codes), p_code;
    END IF;

END;
$$;
```

#### `upsert_resource_with_los`
```sql
CREATE OR REPLACE FUNCTION "public"."upsert_resource_with_los"("p_code" "text", "p_title" "text", "p_description" "text", "p_resource_type" "text", "p_url" "text", "p_storage_path" "text", "p_file_metadata" "jsonb", "p_organization_code" "text", "p_created_by" "uuid", "p_lo_codes" "text"[]) RETURNS SETOF "public"."learning_resources"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    v_resource_id UUID;
BEGIN
    -- 1. Upsert vào bảng chính `learning_resources`
    INSERT INTO public.learning_resources (code, title, description, resource_type, url, storage_path, file_metadata, organization_code, created_by)
    VALUES (p_code, p_title, p_description, p_resource_type, p_url, p_storage_path, p_file_metadata, p_organization_code, p_created_by)
    ON CONFLICT (code) DO UPDATE SET
        title = EXCLUDED.title,
        description = EXCLUDED.description,
        updated_at = now()
    RETURNING id INTO v_resource_id;

    -- 2. Xóa các liên kết LO cũ
    DELETE FROM public.learning_objective_resources WHERE resource_code = p_code;

    -- 3. Chèn các liên kết LO mới
    IF array_length(p_lo_codes, 1) > 0 THEN
        INSERT INTO public.learning_objective_resources (resource_code, learning_objective_code)
        SELECT p_code, unnest(p_lo_codes);
    END IF;

    -- 4. Trả về bản ghi tài nguyên vừa được upsert
    RETURN QUERY SELECT * FROM public.learning_resources WHERE id = v_resource_id;
END;
$$;
```

#### `upsert_topic_with_relations` (2 phiên bản)
```sql
-- Version 1
CREATE OR REPLACE FUNCTION "public"."upsert_topic_with_relations"("p_code" "text", "p_name" "text", "p_description" "text", "p_organization_code" "text", "p_category_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    v_topic_id uuid;
BEGIN
    -- Step 1: Upsert the topic in the main 'topics' table.
    -- It finds a topic by code and organization_code. If it exists, it updates the name and description.
    -- If it doesn't exist, it creates a new one.
    INSERT INTO public.topics (code, name, description, organization_code)
    VALUES (p_code, p_name, p_description, p_organization_code)
    ON CONFLICT (code, organization_code)
    DO UPDATE SET
        name = EXCLUDED.name,
        description = EXCLUDED.description,
        updated_at = now()
    RETURNING id INTO v_topic_id;

    -- If the topic was just inserted, v_topic_id will be set.
    -- If it was updated, we need to fetch the id.
    IF v_topic_id IS NULL THEN
        SELECT id INTO v_topic_id FROM public.topics 
        WHERE code = p_code AND organization_code = p_organization_code;
    END IF;

    -- Step 2: Manage the many-to-many relationship in 'category_topics'.
    -- This is a common and efficient pattern for syncing junction table records.

    -- First, delete any existing relationships for this topic that are NOT in the new list.
    DELETE FROM public.category_topics
    WHERE topic_code = p_code
      AND category_code NOT IN (SELECT unnest(p_category_codes));

    -- Second, insert new relationships that don't already exist.
    -- The ON CONFLICT clause prevents errors if a relationship already exists,
    -- effectively making this an "upsert" operation for the relationships.
    INSERT INTO public.category_topics (category_code, topic_code)
    SELECT category_code, p_code
    FROM unnest(p_category_codes) AS t(category_code)
    ON CONFLICT (category_code, topic_code) DO NOTHING;

END;
$$;

-- Version 2
CREATE OR REPLACE FUNCTION "public"."upsert_topic_with_relations"("p_code" "text", "p_name" "text", "p_description" "text", "p_organization_code" "text", "p_course_code" "text", "p_category_codes" "text"[]) RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    v_topic_exists boolean;
BEGIN
    -- Check if topic exists
    SELECT EXISTS (SELECT 1 FROM public.topics WHERE code = p_code AND organization_code = p_organization_code) INTO v_topic_exists;

    IF v_topic_exists THEN
        -- Update existing topic
        UPDATE public.topics
        SET 
            name = p_name,
            description = p_description,
            course_code = p_course_code,
            updated_at = now()
        WHERE code = p_code AND organization_code = p_organization_code;
    ELSE
        -- Insert new topic
        INSERT INTO public.topics (code, name, description, organization_code, course_code)
        VALUES (p_code, p_name, p_description, p_organization_code, p_course_code);
    END IF;

    -- Manage relationships in the junction table
    -- 1. Delete old relationships for this topic
    DELETE FROM public.category_topics WHERE topic_code = p_code;

    -- 2. Insert new relationships if any are provided
    IF array_length(p_category_codes, 1) > 0 THEN
        INSERT INTO public.category_topics (category_code, topic_code)
        SELECT unnest(p_category_codes), p_code;
    END IF;

END;
$$;
```

#### `update_mastery_after_submission`
```sql
CREATE OR REPLACE FUNCTION "public"."update_mastery_after_submission"("p_submission_id" "uuid") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    submission_record RECORD;
    question_result JSONB;
    lo_record RECORD;
    question_config JSONB;
    question_record RECORD;
BEGIN
    -- 1. Get the entire submission record into the RECORD variable
    SELECT * INTO submission_record
    FROM public.submissions
    WHERE id = p_submission_id;

    -- Exit if no submission is found
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Submission with ID % not found', p_submission_id;
        RETURN;
    END IF;

    -- 2. Iterate through each question result in the submission's session_data
    FOR question_result IN SELECT * FROM jsonb_array_elements(submission_record.session_data->'questionResults')
    LOOP
        -- 3. For each question result, find the original question's config and code
        SELECT q.code, q.question_config INTO question_record
        FROM public.questions q
        WHERE (q.question_config->>'id')::text = (question_result->>'questionId')::text;
        
        -- If the question exists, find all its associated Learning Objectives
        IF FOUND THEN
            FOR lo_record IN
                SELECT qlo.learning_objective_code
                FROM public.question_learning_objectives qlo
                WHERE qlo.question_code = question_record.code
            LOOP
                -- 4. Determine the new mastery level based on correctness
                DECLARE
                    new_mastery_level TEXT;
                    new_mastery_score NUMERIC;
                BEGIN
                    IF (question_result->>'isCorrect')::boolean THEN
                        new_mastery_level := 'mastered';
                        new_mastery_score := 100;
                    ELSE
                        new_mastery_level := 'in_progress';
                        new_mastery_score := 0; -- Or some other logic for partial credit/decay
                    END IF;

                    -- 5. UPSERT the student_mastery record
                    INSERT INTO public.student_mastery (
                        student_id,
                        learning_objective_code,
                        mastery_level,
                        mastery_score,
                        assessed_at,
                        evidence_submission_id
                    )
                    VALUES (
                        submission_record.student_id,
                        lo_record.learning_objective_code,
                        new_mastery_level,
                        new_mastery_score,
                        submission_record.submitted_at,
                        p_submission_id
                    )
                    ON CONFLICT (student_id, learning_objective_code)
                    DO UPDATE SET
                        mastery_level = EXCLUDED.mastery_level,
                        mastery_score = EXCLUDED.mastery_score,
                        assessed_at = EXCLUDED.assessed_at,
                        evidence_submission_id = EXCLUDED.evidence_submission_id,
                        updated_at = now();
                END;
            END LOOP;
        END IF;
    END LOOP;
END;
$$;
```

***

### 3. Tìm kiếm, Lọc & Lấy Dữ liệu (Data Retrieval & Filtering)

#### `find_questions_for_blueprint`
```sql
CREATE OR REPLACE FUNCTION "public"."find_questions_for_blueprint"("p_blueprint_data" "jsonb") RETURNS SETOF "public"."blueprint_question_group"
    LANGUAGE "plpgsql"
    AS $$
DECLARE
    crit jsonb;
    selected_question_codes text[] := '{}';
    found_questions_for_crit record;
    -- Variables to hold filter arrays from the criterion
    v_lo_code text;
    v_question_count int;
    v_bloom_levels text[];
    v_context_codes text[];
    v_knowledge_dimension_codes text[];
BEGIN
    -- Loop through each criterion in the blueprint JSON array
    FOR crit IN SELECT * FROM jsonb_array_elements(p_blueprint_data)
    LOOP
        -- Extract criteria for easier use
        v_lo_code := (crit->>'learningObjectiveCode')::text;
        v_question_count := (crit->>'questionCount')::int;
        
        -- Extract optional filter arrays from the JSONB criterion
        SELECT array_agg(value) INTO v_bloom_levels FROM jsonb_array_elements_text(crit->'allowedBloomLevels');
        SELECT array_agg(value) INTO v_context_codes FROM jsonb_array_elements_text(crit->'allowedContexts');
        SELECT array_agg(value) INTO v_knowledge_dimension_codes FROM jsonb_array_elements_text(crit->'allowedKnowledgeDimensions');

        -- Find the best matching questions for this single criterion
        SELECT
            (crit->>'criterionId')::text AS criterion_id,
            COALESCE(
                (
                    SELECT jsonb_agg(q)
                    FROM (
                        SELECT q.*
                        FROM public.questions q
                        -- This JOIN is essential to link questions to their LOs
                        JOIN public.question_learning_objectives qlo ON q.code = qlo.question_code
                        WHERE
                            -- 1. Must match the specific Learning Objective
                            qlo.learning_objective_code = v_lo_code
                            
                            -- 2. Exclude questions already selected for other criteria
                            AND NOT (q.code = ANY(selected_question_codes))
                            
                            -- 3. Filter by Bloom Levels (if specified in blueprint)
                            AND (
                                v_bloom_levels IS NULL OR array_length(v_bloom_levels, 1) IS NULL
                                OR
                                q.bloom_level_codes && v_bloom_levels
                            )
                            
                            -- 4. Filter by Contexts (if specified in blueprint)
                            -- NOTE: This requires a `context_codes` TEXT[] column on the `questions` table.
                            AND (
                                v_context_codes IS NULL OR array_length(v_context_codes, 1) IS NULL
                                OR
                                q.context_codes && v_context_codes
                            )

                            -- 5. Filter by Knowledge Dimensions (if specified in blueprint)
                            -- NOTE: This requires a `knowledge_dimension_codes` TEXT[] column on the `questions` table.
                            AND (
                                v_knowledge_dimension_codes IS NULL OR array_length(v_knowledge_dimension_codes, 1) IS NULL
                                OR
                                q.knowledge_dimension_codes && v_knowledge_dimension_codes
                            )
                        ORDER BY
                            random() -- Randomize the selection
                        LIMIT v_question_count
                    ) q
                ),
                '[]'::jsonb
            ) AS questions
        INTO found_questions_for_crit;

        -- Add the found question codes to our main list to avoid duplicates
        IF jsonb_array_length(found_questions_for_crit.questions) > 0 THEN
             selected_question_codes := selected_question_codes || ARRAY(
                SELECT value->>'code'
                FROM jsonb_array_elements(found_questions_for_crit.questions)
             );
        END IF;

        -- Return the current group of questions for this criterion
        RETURN NEXT found_questions_for_crit;
    END LOOP;
END;
$$;
```

#### `get_approaches_with_details`
```sql
CREATE OR REPLACE FUNCTION "public"."get_approaches_with_details"() RETURNS TABLE("id" "uuid", "code" "text", "name" "text", "verb_en" "text", "verb_vi" "text", "knowledge_dimension_code" "text", "bloom_level_code" "text", "question_type_code" "text", "example_en" "text", "example_vi" "text", "suggest_context_codes" "text"[], "suggest_difficulty_codes" "text"[])
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
SELECT
    a.id,
    a.code,
    a.name,
    a.verb_en,
    a.verb_vi,
    a.knowledge_dimension_code,
    a.bloom_level_code,
    a.question_type_code,
    a.example_en,
    a.example_vi,
    -- Aggregate suggested context codes into an array
    COALESCE(
        (SELECT array_agg(ac.context_code) FROM public.approach_contexts ac WHERE ac.approach_code = a.code),
        '{}'::text[]
    ) as suggest_context_codes,
    -- Aggregate suggested difficulty codes into an array
    COALESCE(
        (SELECT array_agg(ad.difficulty_code) FROM public.approach_difficulties ad WHERE ad.approach_code = a.code),
        '{}'::text[]
    ) as suggest_difficulty_codes
FROM
    public.approaches a
ORDER BY
    a.name;
$$;
```

#### `get_categories_with_subject_codes`
```sql
CREATE OR REPLACE FUNCTION "public"."get_categories_with_subject_codes"() RETURNS TABLE("id" "uuid", "code" "text", "name" "text", "description" "text", "organization_code" "text", "created_at" timestamp with time zone, "updated_at" timestamp with time zone, "subject_codes" "text"[])
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
SELECT
    c.id,
    c.code,
    c.name,
    c.description,
    c.organization_code,
    c.created_at,
    c.updated_at,
    -- Aggregate subject codes into an array for each category
    COALESCE(
        array_agg(sc.subject_code) FILTER (WHERE sc.subject_code IS NOT NULL),
        '{}'::text[]
    ) as subject_codes
FROM
    public.categories c
LEFT JOIN
    public.subject_categories sc ON c.code = sc.category_code
GROUP BY
    c.id
ORDER BY
    c.name;
$$;
```

#### `get_curriculum_for_student_classes`
```sql
CREATE OR REPLACE FUNCTION "public"."get_curriculum_for_student_classes"("p_student_id" "uuid") RETURNS TABLE("id" "uuid", "code" "text", "name" "text", "description" "text", "lo_type" "text", "parent_lo_code" "text", "keywords" "text"[], "context_tags" "text"[], "suggested_bloom_levels" "text"[], "subject_code" "text", "category_code" "text", "topic_code" "text", "subject" "text", "category" "text", "topic" "text")
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
SELECT DISTINCT
    lo.id,
    lo.code,
    lo.name,
    lo.description,
    lo.lo_type,
    lo.parent_lo_code,
    lo.keywords,
    lo.context_tags,
    lo.suggested_bloom_levels,
    -- Lấy phần tử đầu tiên từ các mảng phi chuẩn hóa
    lo.subject_codes[1] AS subject_code,
    lo.category_codes[1] AS category_code,
    lo.topic_codes[1] AS topic_code,
    -- JOIN để lấy tên tương ứng với mã đầu tiên
    s.name AS subject,
    c.name AS category,
    t.name AS topic
FROM 
    public.classroom_members cm
JOIN 
    public.classroom_curriculum cc ON cm.classroom_id = cc.classroom_id
JOIN 
    public.learning_objectives lo ON cc.learning_objective_code = lo.code
LEFT JOIN
    public.subjects s ON s.code = lo.subject_codes[1]
LEFT JOIN
    public.categories c ON c.code = lo.category_codes[1]
LEFT JOIN
    public.topics t ON t.code = lo.topic_codes[1]
WHERE 
    cm.student_id = p_student_id
    AND cm.status = 'approved';
$$;
```

#### `get_enriched_questions_by_codes`
```sql
CREATE OR REPLACE FUNCTION "public"."get_enriched_questions_by_codes"("p_question_codes" "text"[]) RETURNS TABLE("id" "uuid", "code" "text", "text" "text", "question_config" "jsonb", "last_modified" timestamp with time zone, "question_type_code" "text", "final_difficulty_code" "text", "subject_codes" "text"[], "category_codes" "text"[], "topic_codes" "text"[], "bloom_level_codes" "text"[], "learning_objective_codes" "text"[])
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
SELECT
    q.id,
    q.code,
    q.text,
    q.question_config,
    q.last_modified,
    q.question_type_code,
    q.final_difficulty_code,
    -- Gộp tất cả các mảng từ các LOs liên quan thành một mảng duy nhất, loại bỏ trùng lặp
    COALESCE(array_agg(DISTINCT s_code) FILTER (WHERE s_code IS NOT NULL), '{}'::text[]) as subject_codes,
    COALESCE(array_agg(DISTINCT c_code) FILTER (WHERE c_code IS NOT NULL), '{}'::text[]) as category_codes,
    COALESCE(array_agg(DISTINCT t_code) FILTER (WHERE t_code IS NOT NULL), '{}'::text[]) as topic_codes,
    COALESCE(array_agg(DISTINCT b_code) FILTER (WHERE b_code IS NOT NULL), '{}'::text[]) as bloom_level_codes,
    COALESCE(array_agg(DISTINCT qlo.learning_objective_code) FILTER (WHERE qlo.learning_objective_code IS NOT NULL), '{}'::text[]) as learning_objective_codes
FROM
    public.questions q
LEFT JOIN
    public.question_learning_objectives qlo ON q.code = qlo.question_code
LEFT JOIN
    public.learning_objectives lo ON qlo.learning_objective_code = lo.code
LEFT JOIN
    LATERAL unnest(lo.subject_codes) s_code ON true
LEFT JOIN
    LATERAL unnest(lo.category_codes) c_code ON true
LEFT JOIN
    LATERAL unnest(lo.topic_codes) t_code ON true
LEFT JOIN
    LATERAL unnest(lo.suggested_bloom_levels) b_code ON true
WHERE
    q.code = ANY(p_question_codes)
GROUP BY
    q.id;
$$;
```

#### `get_filtered_questions`
```sql
CREATE OR REPLACE FUNCTION "public"."get_filtered_questions"("p_search_term" "text" DEFAULT NULL::"text", "p_subject_code" "text" DEFAULT NULL::"text", "p_category_code" "text" DEFAULT NULL::"text", "p_topic_code" "text" DEFAULT NULL::"text", "p_bloom_level_code" "text" DEFAULT NULL::"text", "p_question_type_code" "text" DEFAULT NULL::"text", "p_context_code" "text" DEFAULT NULL::"text", "p_difficulty" "text" DEFAULT NULL::"text") RETURNS TABLE("id" "uuid", "code" "text", "text" "text", "last_modified" timestamp with time zone, "organization_code" "text", "question_config" "jsonb", "learning_objective_codes" "text"[])
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
SELECT
    q.id,
    q.code,
    q.text,
    q.last_modified,
    q.organization_code,
    q.question_config,
    -- Tổng hợp các mã LO liên quan để trả về cho client
    COALESCE(array_agg(DISTINCT qlo.learning_objective_code) FILTER (WHERE qlo.learning_objective_code IS NOT NULL), '{}'::text[]) as learning_objective_codes
FROM
    public.questions q
LEFT JOIN
    public.question_learning_objectives qlo ON q.code = qlo.question_code
WHERE
    -- Các bộ lọc trực tiếp trên bảng questions (không thay đổi)
    (p_search_term IS NULL OR q.text ILIKE '%' || p_search_term || '%')
    AND (p_question_type_code IS NULL OR q.question_type_code = p_question_type_code)
    AND (p_difficulty IS NULL OR q.final_difficulty_code = p_difficulty)

    -- SỬA ĐỔI Ở ĐÂY: Loại bỏ q.context_code và thay bằng logic lọc qua LOs
    AND (p_context_code IS NULL OR EXISTS (
        SELECT 1
        FROM public.question_learning_objectives qlo_sub
        JOIN public.learning_objectives lo ON qlo_sub.learning_objective_code = lo.code
        WHERE qlo_sub.question_code = q.code AND p_context_code = ANY(lo.context_tags)
    ))

    -- Các bộ lọc gián tiếp qua Đồ thị Tri thức (không thay đổi)
    AND (p_bloom_level_code IS NULL OR EXISTS (
        SELECT 1
        FROM public.question_learning_objectives qlo_sub
        JOIN public.learning_objectives lo ON qlo_sub.learning_objective_code = lo.code
        WHERE qlo_sub.question_code = q.code AND p_bloom_level_code = ANY(lo.suggested_bloom_levels)
    ))
    AND (p_topic_code IS NULL OR EXISTS (
        SELECT 1
        FROM public.question_learning_objectives qlo_sub
        JOIN public.learning_objectives lo ON qlo_sub.learning_objective_code = lo.code
        WHERE qlo_sub.question_code = q.code AND p_topic_code = ANY(lo.topic_codes)
    ))
    AND (p_category_code IS NULL OR EXISTS (
        SELECT 1
        FROM public.question_learning_objectives qlo_sub
        JOIN public.learning_objectives lo ON qlo_sub.learning_objective_code = lo.code
        WHERE qlo_sub.question_code = q.code AND p_category_code = ANY(lo.category_codes)
    ))
    AND (p_subject_code IS NULL OR EXISTS (
        SELECT 1
        FROM public.question_learning_objectives qlo_sub
        JOIN public.learning_objectives lo ON qlo_sub.learning_objective_code = lo.code
        WHERE qlo_sub.question_code = q.code AND p_subject_code = ANY(lo.subject_codes)
    ))
GROUP BY
    q.id
ORDER BY
    q.last_modified DESC;
$$;
```

#### `get_los_with_relations`
```sql
CREATE OR REPLACE FUNCTION "public"."get_los_with_relations"() RETURNS TABLE("id" "uuid", "code" "text", "name" "text", "description" "text", "keywords" "text"[], "organization_code" "text", "lo_type" "text", "parent_lo_code" "text", "context_tags" "text"[], "suggested_bloom_levels" "text"[], "updated_at" timestamp with time zone, "topic_codes" "text"[], "category_codes" "text"[], "subject_codes" "text"[], "course_codes" "text"[])
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
  -- Hàm bây giờ trở nên đơn giản hơn rất nhiều
  -- vì nó chỉ cần đọc các cột đã được trigger tính toán sẵn.
  SELECT
    lo.id,
    lo.code,
    lo.name,
    lo.description,
    lo.keywords,
    lo.organization_code,
    lo.lo_type,
    lo.parent_lo_code,
    lo.context_tags,
    lo.suggested_bloom_levels,
    lo.updated_at,
    -- Chỉ cần chọn các cột mảng đã tồn tại
    lo.topic_codes,
    lo.category_codes,
    lo.subject_codes,
    lo.course_codes
  FROM
    public.learning_objectives lo
  ORDER BY
    lo.code;
$$;
```

#### `get_resources_for_los`
```sql
CREATE OR REPLACE FUNCTION "public"."get_resources_for_los"("p_lo_codes" "text"[]) RETURNS SETOF "public"."learning_resources"
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
    SELECT DISTINCT lr.*
    FROM public.learning_resources lr
    JOIN public.learning_objective_resources lor ON lr.code = lor.resource_code
    WHERE lor.learning_objective_code = ANY(p_lo_codes);
$$;
```

#### `get_student_next_suggested_los`
```sql
CREATE OR REPLACE FUNCTION "public"."get_student_next_suggested_los"("p_student_id" "uuid", "p_classroom_id" "uuid", "p_limit" integer DEFAULT 5) RETURNS TABLE("lo_code" "text", "lo_name" "text", "lo_description" "text", "reason" "text")
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
WITH classroom_curriculum_los AS (
    -- 1. Lấy tất cả các LOs trong chương trình học của lớp
    SELECT learning_objective_code FROM public.classroom_curriculum
    WHERE classroom_id = p_classroom_id
),
student_mastered_los AS (
    -- 2. Lấy tất cả các LOs mà học sinh đã thành thạo
    SELECT learning_objective_code FROM public.student_mastery
    WHERE student_id = p_student_id AND mastery_level = 'mastered'
),
student_inprogress_los AS (
    -- Lấy các LOs học sinh đang yếu
    SELECT learning_objective_code FROM public.student_mastery
    WHERE student_id = p_student_id AND mastery_level = 'in_progress'
),
remaining_los AS (
    -- 3. Tìm các LOs trong chương trình học mà học sinh chưa thành thạo
    SELECT learning_objective_code FROM classroom_curriculum_los
    EXCEPT
    SELECT learning_objective_code FROM student_mastered_los
),
suggestions AS (
    -- 4. Xây dựng danh sách đề xuất với lý do và thứ tự ưu tiên
    SELECT
        rl.learning_objective_code,
        -- Ưu tiên 1: Các LOs đang 'in_progress' (cần củng cố)
        1 AS priority,
        'This is an area you are currently working on and need to solidify.' AS reason
    FROM remaining_los rl
    WHERE rl.learning_objective_code IN (SELECT learning_objective_code FROM student_inprogress_los)
    
    UNION ALL
    
    SELECT
        rl.learning_objective_code,
        -- Ưu tiên 2: Các LOs chưa bắt đầu
        2 AS priority,
        'This is the next topic in your learning path.' AS reason
    FROM remaining_los rl
    WHERE rl.learning_objective_code NOT IN (SELECT learning_objective_code FROM student_inprogress_los)
)
SELECT
    s.learning_objective_code AS lo_code,
    lo.name AS lo_name,
    lo.description AS lo_description,
    s.reason
FROM suggestions s
JOIN public.learning_objectives lo ON s.learning_objective_code = lo.code
ORDER BY
    s.priority ASC,
    lo.code ASC -- Sắp xếp thứ cấp theo mã để đảm bảo thứ tự ổn định
LIMIT p_limit;
$$;
```

#### `get_student_progress_in_class`
```sql
CREATE OR REPLACE FUNCTION "public"."get_student_progress_in_class"("p_classroom_id" "uuid", "p_student_id" "uuid") RETURNS TABLE("submission_id" "uuid", "assignment_id" "uuid", "assignment_title" "text", "submitted_at" timestamp with time zone, "score" integer, "max_score" integer, "percentage" numeric, "session_data" "jsonb")
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id AS submission_id,
        a.id AS assignment_id,
        a.title AS assignment_title,
        s.submitted_at,
        (s.session_data ->> 'score')::integer AS score,
        (s.session_data ->> 'maxScore')::integer AS max_score,
        (s.session_data ->> 'percentage')::numeric AS percentage,
        s.session_data
    FROM
        public.submissions s
    JOIN
        public.assignments a ON s.assignment_id = a.id
    WHERE
        s.classroom_id = p_classroom_id
        AND s.student_id = p_student_id
        AND s.submission_type = 'assignment'
        AND s.completed_at IS NOT NULL
    ORDER BY
        s.submitted_at DESC;
END;
$$;
```

#### `get_subjects_with_course_codes`
```sql
CREATE OR REPLACE FUNCTION "public"."get_subjects_with_course_codes"() RETURNS TABLE("id" "uuid", "code" "text", "name" "text", "description" "text", "organization_code" "text", "created_at" timestamp with time zone, "updated_at" timestamp with time zone, "course_codes" "text"[])
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
SELECT
    s.id,
    s.code,
    s.name,
    s.description,
    s.organization_code,
    s.created_at,
    s.updated_at,
    -- Aggregate course codes into an array for each subject
    COALESCE(
        array_agg(cs.course_code) FILTER (WHERE cs.course_code IS NOT NULL),
        '{}'::text[]
    ) as course_codes
FROM
    public.subjects s
LEFT JOIN
    public.course_subjects cs ON s.code = cs.subject_code
GROUP BY
    s.id
ORDER BY
    s.name;
$$;
```

#### `get_teacher_class_list_with_stats`
```sql
CREATE OR REPLACE FUNCTION "public"."get_teacher_class_list_with_stats"("p_teacher_id" "uuid") RETURNS TABLE("id" "uuid", "teacher_id" "uuid", "name" "text", "class_code" "text", "created_at" timestamp with time zone, "updated_at" timestamp with time zone, "student_count" bigint, "assignment_count" bigint)
    LANGUAGE "sql"
    AS $$
    SELECT c.id, c.teacher_id, c.name, c.class_code, c.created_at, c.updated_at,
        (SELECT COUNT(*) FROM public.classroom_members cm WHERE cm.classroom_id = c.id AND cm.status = 'approved') AS student_count,
        (SELECT COUNT(*) FROM public.assignments a WHERE a.classroom_id = c.id) AS assignment_count
    FROM public.classrooms c
    WHERE c.teacher_id = p_teacher_id
    ORDER BY c.created_at DESC;
$$;
```

#### `get_topics_with_details`
```sql
CREATE OR REPLACE FUNCTION "public"."get_topics_with_details"() RETURNS TABLE("id" "uuid", "code" "text", "name" "text", "description" "text", "organization_code" "text", "course_code" "text", "created_at" timestamp with time zone, "updated_at" timestamp with time zone, "category_codes" "text"[], "subject_codes" "text"[])
    LANGUAGE "sql" STABLE SECURITY DEFINER
    AS $$
SELECT
    t.id,
    t.code,
    t.name,
    t.description,
    t.organization_code,
    t.course_code,
    t.created_at,
    t.updated_at,
    COALESCE(array_agg(DISTINCT ct.category_code) FILTER (WHERE ct.category_code IS NOT NULL), '{}'::text[]) as category_codes,
    -- Join through to subject_categories to find all related subjects
    COALESCE(array_agg(DISTINCT sc.subject_code) FILTER (WHERE sc.subject_code IS NOT NULL), '{}'::text[]) as subject_codes
FROM 
    public.topics t
LEFT JOIN 
    public.category_topics ct ON t.code = ct.topic_code
LEFT JOIN
    public.subject_categories sc ON ct.category_code = sc.category_code
GROUP BY
    t.id;
$$;
```

#### `get_organization_members` (2 phiên bản)
```sql
-- Version 1
CREATE OR REPLACE FUNCTION "public"."get_organization_members"("p_org_code" "text") RETURNS TABLE("id" "uuid", "full_name" "text", "avatar_url" "text", "role" "text", "updated_at" timestamp with time zone, "organization_code" "text", "email" "text", "personal_settings" "jsonb")
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO 'public', 'auth'
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id::uuid,
        p.full_name::text,
        p.avatar_url::text,
        p.role::text,
        p.updated_at::timestamp with time zone,
        p.organization_code::text,
        u.email::text,
        p.personal_settings::jsonb
    FROM
        public.profiles p
    JOIN
        auth.users u ON p.id = u.id
    WHERE
        p.organization_code = p_org_code;
END;
$$;

-- Version 2
CREATE OR REPLACE FUNCTION "public"."get_organization_members"("p_org_id" "uuid") RETURNS TABLE("id" "uuid", "full_name" "text", "avatar_url" "text", "role" "text", "email" "text", "updated_at" timestamp with time zone)
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
BEGIN
    -- Security Check: Only super admins or an org_admin of the requested organization can proceed.
    IF NOT (
        public.is_admin(auth.uid()) OR 
        (public.is_org_admin() AND public.get_my_organization_id() = p_org_id)
    ) THEN
        RAISE EXCEPTION 'Access Denied: You do not have permission to view members of this organization.';
    END IF;

    RETURN QUERY
    SELECT
        p.id,
        p.full_name,
        p.avatar_url,
        p.role,
        u.email,
        p.updated_at
    FROM
        public.profiles p
    JOIN
        auth.users u ON p.id = u.id
    WHERE
        p.organization_id = p_org_id
    ORDER BY
        p.full_name;
END;
$$;
```

***

### 4. Tiện ích & Quản trị (Utility & Admin)

#### `backfill_all_derived_codes`
```sql
CREATE OR REPLACE FUNCTION "public"."backfill_all_derived_codes"() RETURNS "void"
    LANGUAGE "plpgsql"
    AS $$
DECLARE
    all_subject_codes TEXT[];
BEGIN
    -- Start the cascade from the top-level (subjects)
    SELECT array_agg(code) INTO all_subject_codes FROM public.subjects;
    IF all_subject_codes IS NOT NULL THEN
        PERFORM public.sync_subject_derived_codes(all_subject_codes);
    END IF;
END;
$$;
```

#### `debug_my_profile_access`
```sql
CREATE OR REPLACE FUNCTION "public"."debug_my_profile_access"() RETURNS "jsonb"
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO ''
    AS $$
DECLARE
  result jsonb;
  v_uid uuid := auth.uid();
  v_role text;
  v_profile_exists boolean;
BEGIN
  -- This query runs safely under SECURITY DEFINER, bypassing the RLS policies on this table
  SELECT
    p.role,
    (p.id IS NOT NULL)
  INTO
    v_role,
    v_profile_exists
  FROM public.profiles p
  WHERE p.id = v_uid;

  -- Build the final JSONB object with the retrieved data
  SELECT jsonb_build_object(
    'auth_uid', v_uid,
    'profile_exists_for_uid', COALESCE(v_profile_exists, false),
    'role_from_db', v_role
  ) INTO result;
  
  RETURN result;
END;
$$;
```

#### `generate_question_code` (2 phiên bản)
```sql
-- Version 1
CREATE OR REPLACE FUNCTION "public"."generate_question_code"("p_qtype_code" "text") RETURNS "text"
    LANGUAGE "plpgsql"
    AS $$
DECLARE
    random_part text := substr(md5(random()::text), 1, 8);
BEGIN
    RETURN UPPER(
        COALESCE(p_qtype_code, 'QUESTION') || '-' ||
        random_part
    );
END;
$$;

-- Version 2
CREATE OR REPLACE FUNCTION "public"."generate_question_code"("p_subject_code" "text", "p_topic_code" "text", "p_bloom_code" "text", "p_qtype_code" "text") RETURNS "text"
    LANGUAGE "plpgsql"
    AS $$
DECLARE
    -- Lấy 4 ký tự ngẫu nhiên để đảm bảo mã là duy nhất
    random_part text := substr(md5(random()::text), 1, 4);
BEGIN
    RETURN UPPER(
        COALESCE(p_subject_code, 'NOSUB') || '-' ||
        COALESCE(p_topic_code, 'NOTOP') || '-' ||
        COALESCE(p_bloom_code, 'NOBLM') || '-' ||
        COALESCE(p_qtype_code, 'NOTYPE') || '-' ||
        random_part
    );
END;
$$;
```

#### `get_my_claim`
```sql
CREATE OR REPLACE FUNCTION "public"."get_my_claim"("claim" "text") RETURNS "jsonb"
    LANGUAGE "sql" STABLE
    AS $$
  SELECT COALESCE(
    current_setting('request.jwt.claims', true)::jsonb -> 'raw_user_meta_data' -> claim,
    (SELECT raw_user_meta_data -> claim FROM auth.users WHERE id = auth.uid())
  );
$$;
```

#### `get_my_organization_code`
```sql
CREATE OR REPLACE FUNCTION "public"."get_my_organization_code"() RETURNS "text"
    LANGUAGE "sql" STABLE SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
  SELECT organization_code FROM public.profiles WHERE id = auth.uid();
$$;
```

#### `get_my_role`
```sql
CREATE OR REPLACE FUNCTION "public"."get_my_role"() RETURNS "text"
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO ''
    AS $$
BEGIN
  -- get_my_claim('role') returns a JSONB string like '"admin"'.
  -- We use trim to remove the quotes and get the raw text 'admin'.
  RETURN trim(both '"' from (public.get_my_claim('role'))::text);
END;
$$;
```

#### `is_admin`
```sql
CREATE OR REPLACE FUNCTION "public"."is_admin"("p_user_id" "uuid") RETURNS boolean
    LANGUAGE "sql" STABLE SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.profiles
    WHERE public.profiles.id = p_user_id AND public.profiles.role = 'admin'
  );
$$;
```

#### `is_member_of_class`
```sql
CREATE OR REPLACE FUNCTION "public"."is_member_of_class"("p_classroom_id" "uuid", "p_student_id" "uuid") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM public.classroom_members
    WHERE classroom_id = p_classroom_id AND student_id = p_student_id
  );
END;
$$;
```

#### `is_org_admin`
```sql
CREATE OR REPLACE FUNCTION "public"."is_org_admin"() RETURNS boolean
    LANGUAGE "sql" STABLE SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
  SELECT EXISTS (
    SELECT 1
    FROM public.profiles
    WHERE id = auth.uid() AND role = 'org_admin'
  );
$$;
```

#### `is_teacher_of_class`
```sql
CREATE OR REPLACE FUNCTION "public"."is_teacher_of_class"("p_classroom_id" "uuid") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
  -- This query runs as the function definer, bypassing RLS on the 'classrooms' table for this specific check.
  RETURN EXISTS (
    SELECT 1 FROM public.classrooms
    WHERE id = p_classroom_id AND teacher_id = auth.uid()
  );
END;
$$;
```

#### `update_user_role`
```sql
CREATE OR REPLACE FUNCTION "public"."update_user_role"("target_user_id" "uuid", "new_role" "text") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$BEGIN
  IF NOT public.is_admin() THEN
    RAISE EXCEPTION 'Access denied: Admin privileges required';
  END IF;
  
  IF target_user_id = auth.uid() AND new_role != 'admin' THEN
    RAISE EXCEPTION 'Cannot remove admin role from your own account';
  END IF;
  
  UPDATE public.profiles SET role = new_role WHERE id = target_user_id;
  RETURN FOUND;
END;$$;
```