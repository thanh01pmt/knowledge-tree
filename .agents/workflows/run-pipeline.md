---
description: Thực thi toàn bộ quy trình Knowledge Tree End-to-End với 7 điểm kiểm duyệt của con người (HITL - Human-in-the-loop).
---

# Workflow: Run Full Pipeline (HITL)

> Trình tự chuẩn mực (Golden Path) để xây dựng một project Knowledge Tree hoàn chỉnh từ con số 0. Workflow này kết nối tất cả các tool và quy định rõ **7 Điểm Dừng (Checkpoints)** cần người dùng phê duyệt trước khi đi tiếp.

**Command:** `/run-pipeline`
**Owner:** `coordinator`

## 🏁 Giai đoạn 1: Context & Terminology (Vét cạn ngữ cảnh)

1. **Khởi tạo & Cào dữ liệu:**
   - Hoặc `/init <project>` (nếu dùng PDF).
   - Hoặc `/crawl-roadmap <url>` (nếu dùng roadmap.sh $\rightarrow$ xuất `roadmap_dag_context.json`).

2. **Khởi động ATE Pipeline (Tùy chọn nhưng Khuyến nghị):**
   ```bash
   /scaffold-keywords "<topic>" --source projects/<project>/context/
   /extract-terms
   /verify-terms
   ```

> 🛑 **HITL Checkpoint 1: Xác minh Thuật ngữ**
>
> - **File:** `.work/kw/verify-report.md`
> - **Hành động:** Người dùng rà soát xem có thuật ngữ rác nào lọt vào không, hoặc có thuật ngữ quan trọng nào bị bỏ sót (omission) không. Phê duyệt để Agent tiếp tục.

3. **Chốt Keywords & Nâng cấp (Escalate) lên Concept:**
   ```bash
   /finalize-keywords
   /escalate-concepts
   ```

> 🛑 **HITL Checkpoint 2: Duyệt Concept Mới (Gap D)**
>
> - **File:** `projects/<project>/output/concept_candidates.tsv` (hoặc `concept_escalation.md`)
> - **Hành động:** Người dùng kiểm tra các concept mới (`is_new_concept=True`). Phê duyệt để Agent dùng làm "hint" cho bước tiếp theo.

---

## 🏗️ Giai đoạn 2: Taxonomy & Xây Cây Phân Loại

4. **Validate Master Tree (Gate §7):**

   ```bash
   /validate-master-tree
   ```

   _(BẮT BUỘC phải PASS trước khi đọc Master Tree — đảm bảo toàn vẹn tham chiếu và không có collision.)_

5. **Context Audit (Phân tích Ngữ cảnh):**
   ```bash
   /context-audit
   ```
   _(Đọc syllabus/PDF trong `context/`, tích hợp `keywords.tsv` nếu có từ ATE pipeline, xuất `.work/context-audit.md`.)_

> 🛑 **HITL Checkpoint 3: Xác nhận Context Audit**
>
> - **File:** `projects/<project>/.work/context-audit.md`
> - **Hành động:** Người dùng rà soát bản phân tích domain và syllabus. Xác nhận đã vét cạn nội dung nguồn. Phê duyệt để Agent tiếp tục map taxonomy.

6. **Map Taxonomy (Dựa trên ATE Hints):**
   ```bash
   /map-taxonomy
   ```

> 🛑 **HITL Checkpoint 4: Phê duyệt Cấu trúc N:N**
>
> - **File:** `projects/<project>/.work/mapping-plan.md`
> - **Hành động:** Người dùng rà soát các đề xuất `[NEW NODE PROPOSAL]`, xác nhận các node `[VERIFY]` (độ tin cậy 0.70-0.80) và kiến trúc mượn node (N:N Reuse). Phê duyệt để Build.

7. **Lắp ráp Cây (Build Tree):**
   ```bash
   /build-tree
   ```
   _(Tạo ra 5 TSV: fields, subjects, categories, topics, concepts)._

---

## 🧠 Giai đoạn 3: Hierarchical Learning Objectives & Curriculum DAG

8. **Sinh Universal LOs (Phase A):**
   ```bash
   /generate-ulos
   ```

> 🛑 **HITL Checkpoint 5: Phê duyệt ULO (Tính Độc Lập)**
>
> - **File:** `projects/<project>/.work/hlo/ulos_preview.md`
> - **Hành động:** Đảm bảo ULO ưu tiên Bloom Cấp cao (Evaluate/Create) và tuyệt đối không dính dáng đến công nghệ cụ thể. Phê duyệt.

9. **Sinh Conceptual LOs (Phase B - Phép thử Marr):**
   ```bash
   /generate-cios
   ```

> 🛑 **HITL Checkpoint 6: Nghiệm thu Phép thử Marr**
>
> - **File:** `projects/<project>/.work/hlo/cios_preview.md`
> - **Hành động:** Đọc cột `Marr Test Note`. Nếu LLM không thể chỉ ra CIO áp dụng cho ≥ 2 ngôn ngữ khác nhau $\rightarrow$ Yêu cầu LLM viết lại. Đây là chốt chặn khắt khe nhất. Phê duyệt.

10. **Sinh Specific LOs & Nối Dây Tiền đề (Phase C, D, E):**

```bash
/generate-sios
# (Tạo SIO và merge ra file learning-objectives.tsv hoàn chỉnh)

/map-prerequisites
# (Đọc DAG bối cảnh và sinh ra lo_prerequisites.tsv)
```

---

## 🚀 Giai đoạn 4: Đánh giá & Phát hành

11. **Kiểm thử (Validation & Audit):**

```bash
/validate-tree
/audit-coverage
/detect-gaps
```

_(Phải PASS 100% không có lỗi tham chiếu)._

> 🛑 **HITL Checkpoint 7: Phê duyệt Đồng bộ Cloud (§8)**
>
> - **Hành động:** CẤM TUYỆT ĐỐI tự động đẩy dữ liệu lên DB/Cloud. Người dùng PHẢI phê duyệt trực tiếp trước khi Agent thực thi `/sync-supabase`. Bao gồm cả thao tác "restore" — không chỉ cập nhật mới.

12. **Đồng bộ Lên Cloud (Supabase):**
    ```bash
    /sync-supabase
    ```
    _(Đồng bộ 7 bảng theo đúng thứ tự Top-down, không bẻ gãy khóa ngoại)._

> **Hoàn tất Pipeline!** 🎉
