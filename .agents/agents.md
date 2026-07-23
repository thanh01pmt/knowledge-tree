# Knowledge Tree Team

## Core Architectural & Quality Rules (Must-Follow)

1. **Quy chuẩn Trung tính 100% & Phép thử Marr cho CIO (Technology-Agnostic & Marr's Tri-Level Test [T6])**:
   - **Fields, Subjects, Categories, Topics, Concepts, ULOs, CIOs**: **100% TRUNG TÍNH (Mã, Tên, Mô tả)**. Cấm tuyệt đối tên công nghệ hay ngôn ngữ lập trình cụ thể (như TypeScript, React, Vue, Docker, Python, Swift, v.v.).
   - **Phép thử Marr 2-Ngôn-ngữ cho CIO (Representation-Independent)**: Tầng Algorithmic (CIO) BẮT BUỘC phải độc lập với biểu diễn cú pháp. Trước khi duyệt một CIO, **BẮT BUỘC map thử mô tả CIO sang $\ge 2$ ngôn ngữ/công cụ khác nhau**. Nếu mô tả chỉ khớp tự nhiên với 1 ngôn ngữ (ví dụ ép thứ tự từ khóa token-order của Python/Swift), CIO đó đã bị giáng cấp xuống Implementational trá hình $\rightarrow$ BẮT BUỘC viết lại thành thủ tục trung tính hoặc giáng xuống SIO.
   - **SIOs (`lo_type: SPECIFIC_IMPL`)**: **TẦNG DUY NHẤT CHỨA CÔNG NGHỆ CỤ THỂ**.
2. **Quy tắc Đặt mã SIO & Đối chiếu Mẫu Đa Công nghệ (SIO Cross-Referencing Rules)**:
   - **Định dạng mã SIO**: `SIO-<TECH_PREFIX>-<FEATURE_SLUG>` (dạng `UPPER_SNAKE_CASE`).
   - **Đối chiếu Mẫu SIO Đa Công nghệ**: Do tầng Concept/ULO/CIO là 100% Trung tính và dùng chung, khi xây dựng SIO cho một công nghệ mới (ví dụ: Swift), Agent **CẦN TRA CỨU & ĐỐI CHIẾU** các SIO đã có ở các cây công nghệ khác (như JS, Python) nằm cùng mã CIO/Concept để nhân bản mẫu mã và đổi tên/nội dung tương đương cho công nghệ mới.
3. **Mô hình Quan hệ N:N (Many-to-Many Relationships)**:
   - Quan hệ **Concept $\leftrightarrow$ ULO $\leftrightarrow$ CIO $\leftrightarrow$ SIO** là N:N. Phân tách danh sách mã bằng dấu phẩy trong `concept_codes` và `parent_lo_code`.
4. **Tiền tố Câu Mô tả LO Chuẩn hóa**:
   - 100% câu mô tả trong `learning-objectives.tsv` BẮT BUỘC bắt đầu bằng: **`"Người học có khả năng ..."`**.
5. **Quy mô & Độ phủ Tri thức Cạn kiệt ($\ge 80 - 160$ LOs)**:
   - Trích xuất cạn kệt 100% nội dung `context/*.json` và `context/*.pdf` với quy mô trung bình **$\ge 80 - 160$ LOs**.
   - Bắt buộc phải **PASS cả 2 script**: `validate_tree.py` (`[PASS] 0 lỗi`) và `audit_coverage.py` (`Coverage Score ≥ 90%`).
6. **Phân định 2 Trục Bloom & Khuyến khích Bloom Cấp cao ở ULO (Anderson & Krathwohl [T1])**:
   - Phân định rõ 2 trục độc lập: **Cognitive Process** (động từ Bloom: Remember $\rightarrow$ Create) và **Knowledge Dimension** (`FACTUAL`, `CONCEPTUAL`, `PROCEDURAL`, `METACOGNITIVE`).
   - Khi nội dung cho phép, chủ động chọn động từ cấp **Evaluate / Create** cho tầng ULO để tránh "lực hút tự nhiên" (natural pull) kéo tất cả LOs về Understand/Apply.
7. **Ràng buộc Coverage Đánh giá Trực tiếp cho CIO/ULO (Skemp [T4], Perkins & Salomon [T8])**:
   - Tách biệt "biết cách làm" (SIO - Instrumental) và "hiểu tại sao" (ULO/CIO - Relational). Không giả định suy luận ngây thơ 100% SIO $\rightarrow$ CIO/ULO.
   - Mỗi ULO/CIO BẮT BUỘC phải có $\ge N$ câu hỏi/hoạt động đánh giá trực tiếp để đảm bảo tính hợp lệ suy luận (Inferential Validity) và tránh rủi ro Far Transfer thấp.
8. **Cấm Dùng Script thế chuỗi regex cơ học (No Dumb Find-and-Replace)**:
   - Mọi câu từ mô tả ULO/CIO/Concept phải được viết tự nhiên, mạch lạc, không find-and-replace thô ráp.
9. **Sạch sẽ Thư mục Root**:
   - Không để lại script Python rác tại thư mục gốc workspace. All automation scripts belong inside `.agents/skills/`.


## Workflow Index

| Command                | Owner             | Primary result                                                                                 |
| ---------------------- | ----------------- | ---------------------------------------------------------------------------------------------- |
| `/init <project>`      | scaffolder        | Scaffold project TSV files (updates status.yaml)                                               |
| `/set-project`         | coordinator       | Update active_project in status.yaml                                                           |
| `/context-audit`       | @context-analyzer | Read project syllabus/PDFs                                                                     |
| `/map-taxonomy`        | @taxonomy-mapper  | Cross-reference syllabus with Master TSV -> mapping-plan.md                                    |
| `/build-tree`          | @tree-assembler   | Apply mapping-plan.md to build 5 taxonomy TSVs (fields → concepts)                             |
| `/generate-los`        | @tree-assembler   | Generate `learning-objectives.tsv` via LLM, grounded in project concept codes                  |
| `/detect-gaps`         | @tree-validator   | Run `detect_gaps.py` to find 3 gap types: missing LO coverage, shallow CIOs, master candidates |
| `/validate-tree`       | @tree-validator   | Run `validate_tree.py` for structural referential integrity                                    |
| `/audit-coverage`      | @tree-validator   | Run `audit_coverage.py` to cross-reference LO output against source PDF                        |
| `/sync-supabase`       | @tree-assembler   | Run `sync_to_supabase.py` to push TSVs into Supabase Cloud DB                                  |
| `/crawl-roadmap <url>` | @roadmap-aligner  | Scaffold project in `projects/`, run standard pipeline, and propose merge to General Context   |

## scaffolder

- Goal: Scaffold project directory structure, 6 output TSV headers, and set active project in `status.yaml`.
- Script: `.agents/skills/tree-validator/scripts/scaffold_tree.py`

## @context-analyzer

- Goal: Extract syllabus and knowledge domains from `projects/<project>/context/` source files.
- Skill: `project-context-loader`

## @taxonomy-mapper

- Goal: Map the extracted domains to exact codes in `KnowledgeTree v2.2.tsv`.
- Handover: `.work/mapping-plan.md`
- Skill: `taxonomy-mapper`

## @roadmap-aligner

- Goal: Crawl external roadmaps (roadmap.sh) via Crawl4AI server & align missing topics with Master TSV.
- Handover: `.work/roadmap_alignment_report.md`
- Skill: `roadmap-aligner`

## @tree-assembler

- Goal: (1) Build 5 taxonomy TSVs from approved mapping-plan. (2) Generate learning-objectives.tsv via /generate-los after build-tree. (3) Sync to Supabase via /sync-supabase.
- Skill: `tree-assembler`, `learning-objective-generator`, `supabase-sync`

## @tree-validator

- Goal: Run validation script (`validate_tree.py`) & reverse coverage audit (`audit_coverage.py`) to ensure 100% referential integrity and 100% syllabus coverage.
- Skill: `tree-validator`
