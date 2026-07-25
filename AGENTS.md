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
   - Bắt buộc phải **PASS cả 2 script**: `validate_tree.py` (`[PASS] 0 lỗi`) và `audit_coverage.py` (`Coverage Score ≥ 95%`).
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


## Ràng buộc Vận hành (Operational Constraints & Gates)

> Cross-cutting rules áp dụng cho mọi skill và workflow trong Knowledge Tree.

### §1 Context Gate
Trước bất kỳ workflow nào **ghi** artifact dự án (như `/map-taxonomy`, `/build-tree`):
- Đọc PDF/Syllabus trong `projects/<project>/context/`.
- Luôn dùng `.agents/skills/taxonomy-mapper/resources/mlo-knowlege-tree.tsv` làm chân lý. CÓ THỂ đề xuất thêm mã mới vào Master Tree nhưng **tuyệt đối không tự ý ghi** — phải thông qua phê duyệt của Human.
- **BẮT BUỘC Tra cứu Master Tree trước (Search First):** Trước khi đề xuất bất kỳ Concept mới nào trong `/map-taxonomy`, PHẢI tra cứu toàn bộ danh sách Concepts trong Bảng 5 của `mlo-knowlege-tree.tsv`. Chỉ được tạo `[NEW NODE PROPOSAL]` khi kết quả tìm kiếm **hoàn toàn trống**. Tuyệt đối không thêm tiền tố giả mạo (`C_`, `_NEW`, v.v.).

### §2 Mock-Mode Prohibition
⛔ Never run scripts with `--mock` or bypass actual execution.

### §3 Final Artifacts
Output cuối của mỗi project là đúng 6 file TSV đã validate trong `projects/<project>/output/`:
`fields.tsv` · `subjects.tsv` · `categories.tsv` · `topics.tsv` · `concepts.tsv` · `learning-objectives.tsv`

File trung gian (mapping plan, context audit...) lưu trong `projects/<project>/.work/`.

### §4 Approval Gate
Trước khi ghi TSV cuối (chạy `/build-tree`), **BẮT BUỘC** trình `mapping-plan.md` cho người dùng duyệt. Không ghi TSV nếu chưa có phê duyệt rõ ràng.

### §5 Security Boundary
- Đọc master data từ `.agents/skills/taxonomy-mapper/resources/`.
- Đọc project data từ `projects/<project>/context/`.
- Chỉ ghi vào `projects/<project>/output/*.tsv` và `projects/<project>/.work/`. (Sửa `resources/` chỉ khi được User cho phép rõ ràng.)
- Active project được theo dõi trong `status.yaml`.

### §6 Reverse Coverage Gate
Sau khi tạo xong `learning-objectives.tsv`, BẮT BUỘC chạy `/audit-coverage` (hoặc `audit_coverage.py`) để đối chiếu ngược với tài liệu nguồn trong `projects/<project>/context/`.
- Đảm bảo 100% mục syllabus có ít nhất 1 LO đảm nhiệm.
- Xuất báo cáo `coverage_report.md` với các gap phát hiện được.

### §7 Master Tree Integrity Gate
Trước khi `/map-taxonomy` hoặc `/build-tree` đọc từ Master Tree, `/validate-master-tree` (hoặc `validate_master_tree.py`) phải đã PASS kể từ lần cuối tree bị sửa đổi.

### §8 Phê duyệt Đồng bộ DB / Cloud
**CẤM TUYỆT ĐỐI** tự động thực thi `/sync-supabase` hoặc đẩy dữ liệu lên DB/Cloud nếu **chưa nhận được phê duyệt trực tiếp từ người dùng**. Bao gồm cả thao tác "restore" — không chỉ cập nhật mới.

### §9 Cấm Script Bypass Validation (No Metric Gaming)
Khi script hoặc LLM bị lỗi, **BẮT BUỘC BÁO CÁO LỖI GỐC** cho người dùng để thảo luận phương án.
**CẤM TUYỆT ĐỐI** viết script tạm bợ (dummy fallback) chỉ để ép `validate_tree.py` / `audit_coverage.py` báo `[PASS] 0 lỗi`. Script PASS ≠ dữ liệu đạt chất lượng sư phạm.

### §10 Bảo tồn & Minh bạch Dữ liệu
Khi có sai lệch hoặc xung đột giữa dữ liệu mới và backup trước đó, Agent phải:
1. **Dừng ngay** — không ghi đè.
2. **Giải thích nguyên nhân gốc rễ** cho người dùng.
3. **Xin phê duyệt** trước khi ghi đè hoặc phục hồi dữ liệu.




## Workflow Index

| Command                | Owner             | Primary result                                                                                 |
| ---------------------- | ----------------- | ---------------------------------------------------------------------------------------------- |
| `/run-pipeline`        | coordinator       | **Full End-to-End Workflow** with 5 explicit Human-in-the-loop (HITL) review checkpoints       |
| `/init <project>`      | scaffolder        | Scaffold project TSV files (updates status.yaml)                                               |
| `/set-project`         | coordinator       | Update active_project in status.yaml                                                           |
| `/scaffold-keywords <target> --source <path>` | scaffolder | Tạo `.work/kw/`, chunk tài liệu nguồn (PDF/MD/TXT)                              |
| `/extract-terms`       | @keyword-extractor | YAKE + LLM candidate-gen → embedding filter → `candidates_filtered.md`                        |
| `/verify-terms`        | @keyword-extractor | LLM dedup + omission-check loop → `verify-report.md` (**điểm duyệt người**)                   |
| `/finalize-keywords`   | @keyword-extractor | Export `output/keywords.tsv` + inject vào `context-audit.md`                                  |
| `/escalate-concepts`   | @keyword-extractor | Keyword → concept trung tính + match Master Tree → `concept_candidates.tsv` + Gap D detection  |
| `/context-audit`       | @context-analyzer | Read project syllabus/PDFs (+ `context/keywords.tsv` nếu có từ ATE pipeline)                  |
| `/map-taxonomy`        | @taxonomy-mapper  | Cross-reference syllabus with Master TSV -> mapping-plan.md                                    |
| `/build-tree`          | @tree-assembler   | Apply mapping-plan.md to build 5 taxonomy TSVs (fields → concepts)                             |
| `/generate-los`        | @tree-assembler   | Generate `learning-objectives.tsv` via LLM, 1-shot (legacy/fast path)                          |
| `/generate-ulos`       | @tree-assembler   | Phase A: Sinh ULOs từ concepts, Bloom ưu tiên Evaluate/Create — **điểm duyệt**                 |
| `/generate-cios`       | @tree-assembler   | Phase B: Sinh CIOs với Marr 2-Language Test per-CIO — **điểm duyệt**                           |
| `/generate-sios`       | @tree-assembler   | Phase C: Sinh SIOs (tech-specific) + merge → `learning-objectives.tsv`                          |
| `/map-prerequisites`   | @tree-assembler   | Phase E: Sinh `lo_prerequisites.tsv` từ file LO và bối cảnh Curriculum DAG                     |
| `/detect-gaps`         | @tree-validator   | Run `detect_gaps.py` to find 3 gap types: missing LO coverage, shallow CIOs, master candidates |
| `/validate-tree`       | @tree-validator   | Run `validate_tree.py` for structural referential integrity                                    |
| `/audit-coverage`      | @tree-validator   | Run `audit_coverage.py` to cross-reference LO output against source PDF                        |
| `/sync-supabase`       | @tree-assembler   | Run `sync_to_supabase.py` to push TSVs into Supabase Cloud DB                                  |
| `/crawl-roadmap <url>` | @roadmap-aligner  | Scaffold project in `projects/`, run standard pipeline, and propose merge to General Context   |
| `/validate-master-tree`| @tree-validator   | Run `validate_master_tree.py` for Master Tree referential integrity and collision detection   |

## scaffolder

- Goal: Scaffold project directory structure, 6 output TSV headers, and set active project in `status.yaml`.
- Script: `.agents/skills/tree-validator/scripts/scaffold_tree.py`

## @keyword-extractor

- Goal: Vét cạn thuật ngữ chuyên ngành (ATE) từ tài liệu nguồn theo chủ đề mục tiêu. Pipeline lai: YAKE + LLM candidate-gen → embedding filter → LLM dedup + omission-check loop. Output tích hợp vào `/context-audit`. Sau `/finalize-keywords`, lệnh `/escalate-concepts` abstraction keywords lên concept trung tính và match với Master Tree (phát hiện Gap D).
- Skill: `keyword-extractor`

## @context-analyzer

- Goal: Extract syllabus and knowledge domains from `projects/<project>/context/` source files. Nếu `context/keywords.tsv` tồn tại (từ ATE pipeline `/finalize-keywords`), tích hợp section `## ATE Keywords` vào domain breakdown — không cần extract lại từ PDF.
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

- Goal: Run validation scripts (`validate_master_tree.py`, `validate_tree.py`) & reverse coverage audit (`audit_coverage.py`) to ensure 100% referential integrity and 100% syllabus coverage.
- Skill: `tree-validator`
