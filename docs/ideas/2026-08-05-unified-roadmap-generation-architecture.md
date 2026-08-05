# Unified Roadmap Generation Architecture — Design Session Notes

> **Ngày:** 2026-08-05  
> **Participants:** Human architect + AI assistant  
> **Context:** Phân tích sâu `swift-associate` project artifacts, đánh giá hiện trạng `generate_project_driven_roadmap.py`, và thiết kế kiến trúc pipeline thống nhất cho roadmap generation.  
> **Output:** Kiến trúc Pipeline v3 hoàn chỉnh với 13 gaps identified.

---

## Mục Lục

1. [Phân Tích Hiện Trạng `swift-associate`](#1-phân-tích-hiện-trạng-swift-associate)
2. [Kiến Trúc Đúng: Single Source of Truth](#2-kiến-trúc-đúng-single-source-of-truth)
3. [Hai Cases Đầu Vào](#3-hai-cases-đầu-vào)
4. [JIT Expansion + Judge Gate](#4-jit-expansion--judge-gate)
5. [Cross-Tech SIO Reuse qua CIO Bridge](#5-cross-tech-sio-reuse-qua-cio-bridge)
6. [Pipeline v3 Hoàn Chỉnh](#6-pipeline-v3-hoàn-chỉnh)
7. [13 Gaps Identified](#7-13-gaps-identified)
8. [Data Models](#8-data-models)
9. [Scripts Cần Viết](#9-scripts-cần-viết)
10. [Vấn Đề Mở](#10-vấn-đề-mở)

---

## 1. Phân Tích Hiện Trạng `swift-associate`

### 1.1 Bối Cảnh

Project `swift-associate` có **2 bộ artifacts song song** được tạo bởi 2 pipeline khác nhau:

| Bộ Artifact | Pipeline | Output |
|---|---|---|
| **Standard Knowledge Tree** | `/context-audit` → `/map-taxonomy` → `/build-tree` → `/generate-ulos` → `/generate-cios` → `/generate-sios` | `output/learning-objectives.tsv` — **157 LOs** (40 ULO + 40 CIO + 77 SIO) |
| **Project-Driven Roadmap** | `generate_project_driven_roadmap.py` | `roadmaps/` — 6 phases instruction + roadmap_graph.json + techstack_final.json |

### 1.2 Vấn Đề: Hai Pipeline Không Nói Chuyện Với Nhau

**157 LOs chất lượng** trong `output/learning-objectives.tsv` được sinh bởi pipeline chuẩn, tuân thủ Marr T6, Bloom progression, và đã qua validate. Tuy nhiên:

- `generate_project_driven_roadmap.py` **không đọc** file này
- Nó tự LLM-sinh build guide → tự map concept → tự tạo instruction
- LO codes trong instruction (`ULO-PROCESS_VS_THREAD-1`, `ULO-BEHAVIORAL_PATTERNS-2`) **không tồn tại** ở đâu — hallucinated

### 1.3 Bằng Chứng Cụ Thể

#### a) Project Analysis Nông

`notes.md` (engineering architecture reference) chỉ có **72 dòng**, copy-paste description từ build guide:

```
## 2. LAYER 0: WEBSOCKET TRANSPORT LAYER
Engineering Action: Implement a WebSocket client using URLSessionWebSocketTask...
This layer is responsible for: Implement a WebSocket client using URLSessionWebSocketTask...
```

Không có:
- API signatures (`URLSessionWebSocketTask.receive()`, `send(_:)`)
- Reconnection strategy (exponential backoff, jitter)
- Message format (JSON schema, binary frame)
- Error classification

#### b) Instruction Template Machine

Cả 6 phases (`step-0.md` → `step-5.md`) có **cùng một nội dung generic**:

| Section | Nội dung | Vấn đề |
|---|---|---|
| §2 Khởi tạo file | "Tạo thư mục và file cho Phase X" | Giống hệt mọi phase |
| §3 Thực thi mã nguồn | "Tham chiếu...notes.md" | **Rỗng** — không code snippet |
| §4 Xử lý lỗi | "Xử lý lỗi kết nối..." | Generic cho mọi project |
| §5 Viết test | "Viết unit test..." | Không specific |
| §6 Debug table | 3 dòng generic | Cùng bảng cho WebSocket, CoreData, SwiftUI |

Debug table giống hệt mọi phase:
```
| Import/module not found | File chưa nằm trong đúng thư mục target |
| Runtime crash on async call | Missing await hoặc error handler |
| State không update UI | State mutation trên wrong thread |
```

→ Đây là lỗi debug generic cho **bất kỳ** Swift project, không specific cho WebSocket hay CoreData.

#### c) LO Codes Hallucinated

Instruction trỏ `ULO-PROCESS_VS_THREAD-1`, `SIO-BEHAVIORAL_PATTERNS-2`... — **không tồn tại** trong `learning-objectives.tsv`. LO file có `ULO-RUNTIME_ERRORS-01`, `ULO-ASYNCHRONOUS_PROG_CONCEPT-01`... hoàn toàn khác.

#### d) Vòng Tham Chiếu Rỗng

```
step-0.md §3 → "[REF: notes.md]" → notes.md copy từ build guide → build guide từ LLM guess
```

Không có thông tin kỹ thuật thật ở bất kỳ đâu trong chain.

#### e) Roadmap Graph Quá Thưa

`roadmap_graph.json`: **17 nodes**, **10 edges** — toàn concept trừu tượng:
- `ABSTRACTION_LAYERS`, `BEHAVIORAL_PATTERNS`, `STRUCTURAL_PATTERNS`
- `CAP_THEOREM`, `CLOUD_MODELS_IAAS_PAAS_SAAS`

Thiếu concept cụ thể quan trọng: `DECLARATIVE_UI_PARADIGM`, `STATE_PROPERTY_WRAPPER`, `TWO_WAY_BINDING`, `ASYNCHRONOUS_PROG_CONCEPT`.

#### f) Keyword→Concept Mapping Sai

`mapping-plan.md` có nhiều low-confidence match bị "ép":

| Proposed | → Master Code | Confidence | Vấn đề |
|---|---|---|---|
| `IDENTIFIER_NAMING_RULES` | `PRIMITIVE_TYPE_DECLARATION` | 0.70 | Naming rules ≠ type declaration |
| `FUNCTION_SYNTAX` | `PRIMITIVE_TYPE_DECLARATION` | 0.60 | Function syntax ≠ variable declaration |
| `UI_STACK_LAYOUT` | `LEVEL_LAYOUT` | 0.70 | Game level layout ≠ UI stack |
| `LOOP_CONTROL_FLOW` | `FOR_LOOP` | 0.60 | Control flow ≠ for loop |

Recommendation "Create new concepts" bị bỏ qua — `ULO-LEVEL_LAYOUT-01` vẫn tồn tại với mô tả "Level Layout Design" (game-specific).

### 1.4 Nguyên Nhân Gốc Rễ

`generate_project_driven_roadmap.py` (~1332 dòng) có **3 hàm template** sinh ra "tri thức giả":

**Hàm 1: `_generate_build_guide_llm()` (line 549)**
- Input cho LLM chỉ là JSON metadata (title, description, tech_stack)
- **Không có** source code, README content, dependency analysis
- LLM sinh build guide từ mô tả bề mặt

**Hàm 2: LO generation (lines 890-911)**
- String concatenation: `f"Hiểu nguyên lý phổ quát của {c_name} cho '{title}'."`
- Vi phạm **Quy tắc 8** AGENTS.md: "Cấm Dùng Script thế chuỗi regex cơ học"

**Hàm 3: `generate_instruction_step()` (line 681)**
- 8-section template, §3 chỉ có reference tag trỏ về notes.md
- notes.md cũng rỗng → vòng tham chiếu rỗng

---

## 2. Kiến Trúc Đúng: Single Source of Truth

### 2.1 Flow Chính Xác

```
Master Tree (ULO/CIO trung tính)  +  Project (GitHub repo)
         │                                  │
         │          ┌───────────────────────┘
         │          │
         ▼          ▼
   Phân tích Project → extract keywords/features/patterns
         │
         ▼
   Keywords → align/escalate → Master Tree concepts
         │
         ▼
   Dựa vào CIO (Master) + Project specifics → viết SIO
         │
         ▼
   Bổ sung tree nếu cần (JIT expansion → Judge Gate → merge)
         │
         ▼
   Tạo Roadmap (thứ tự, scheduling, rationale, instruction)
```

### 2.2 Nguyên Tắc Thiết Kế

1. **Master Tree là single source of truth cho ULO/CIO** — đọc, không sinh lại (trừ khi concept mới)
2. **Chỉ SIO là tầng cần sinh mới** — vì nó gắn với project cụ thể
3. **Mọi tầng đều có thể thiếu** — Master Tree đang xây, cần JIT expansion
4. **Cross-tech reuse** — SIO của tech A có thể adapt cho tech B qua CIO bridge
5. **Judge Gate tự động** — LLM-as-Judge cho phép merge nếu pass, không cần human chờ

---

## 3. Hai Cases Đầu Vào

### 3.1 Case 1: Project Mới Tinh (Chưa Có Gì)

Thư mục `projects/<name>/` chưa tồn tại. Không có LOs, không có keywords, không có context.

**Pipeline cần làm:**

```
STEP 0: Scaffold project directory
         (python3 scaffold_tree.py <name>)

STEP 1: Deep Project Analysis
         clone → analyze_repo_structure → extract deps
         → source_context (files, APIs, patterns)

STEP 2: Keyword Extraction
         Từ source → technical keywords
         (imports, types, functions, tests, config, README)

STEP 3: Concept Resolution
         keywords → align/escalate → Master Tree concepts

STEP 4: ULO/CIO Resolution
         Master có? → REUSE
         Không? → GENERATE → quarantine → Judge

STEP 5: SIO Resolution
         Cross-tech có? → ADAPT
         Không? → GENERATE → quarantine → Judge

STEP 6-8: Judge Gate → Staging Merge → Roadmap Assembly
```

### 3.2 Case 2: Đã Có Dự Án Tương Tự

Ví dụ: `swift-associate` (iOS + SwiftUI + Combine + CoreData) đã có 157 LOs. User request `fitness-tracker` (iOS + SwiftUI + HealthKit + CoreData).

**Tái tận dụng 3 tầng:**

```
┌─────────────────────────────────────────────────────────┐
│  TIER 1: MASTER TREE REUSE (luôn có)                   │
│  ULO/CIO: Đọc từ Master Tree — chi phí 0               │
│  Concepts: Match keywords → existing — chi phí 0       │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│  TIER 2: CROSS-PROJECT SIO REUSE                       │
│  Scan projects/*/output/learning-objectives.tsv        │
│                                                         │
│  SIO trùng: Cùng tech prefix + cùng parent CIO         │
│    → Reuse trực tiếp                                    │
│    Ví dụ: SIO-SWIFT-LOCAL_VIEW_STATE-01 (@State)       │
│                                                         │
│  SIO gần trùng: Cùng CIO, khác context                 │
│    → Adapt: giữ structure, thay details                 │
│    Ví dụ: Combine publisher cho Chat → cho Fitness      │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│  TIER 3: NEW SIO GENERATION (chỉ cho features mới)     │
│  Keyword extraction → align/escalate → generate         │
│  Ví dụ: HealthKit-specific SIOs                        │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Scoring Project Similarity

```python
def score_project_similarity(new_project, existing_project) -> float:
    # 1. Tech stack overlap (trọng số cao nhất)
    tech_overlap = len(set(new.tech_stack) & set(existing.tech_stack))
    tech_union = len(set(new.tech_stack) | set(existing.tech_stack))
    tech_score = tech_overlap / tech_union  # Jaccard

    # 2. Domain keyword overlap
    domain_overlap = len(set(new.keywords) & set(existing.keywords))
    domain_score = domain_overlap / max(1, len(new.keywords))

    # 3. Concept code overlap
    concept_overlap = len(set(new.concept_codes) & set(existing.concept_codes))
    concept_score = concept_overlap / max(1, len(new.concept_codes))

    return 0.5 * tech_score + 0.3 * domain_score + 0.2 * concept_score
```

**Decision thresholds:**
- `score >= 0.7` → **High reuse**: Tier 1 + Tier 2 đầy đủ
- `score >= 0.4` → **Partial reuse**: Tier 1 + selective Tier 2
- `score < 0.4` → **Fresh start**: Tương đương Case 1

### 3.4 Ma Trận Chi Phí

| Scenario | Concepts mới | ULO/CIO mới | SIO mới | Judge calls |
|---|---|---|---|---|
| Fresh, unique domain | 15-25 | 15-25 | 30-40 | ~100 |
| Same tech, different domain | 3-8 | 2-5 | 5-10 (adapt) | ~20 |
| Different tech, same domain | 0-2 | 0-1 | 10-15 (cross-tech) | ~15 |
| Same tech, same domain | 0-1 | 0 | 2-3 | ~5 |

---

## 4. JIT Expansion + Judge Gate

### 4.1 Vấn Đề

Master Tree **đang xây, chưa đủ**. Một project có thể đề cập đến concept mới cần ULO/CIO mới. Pipeline không được giả định Master Tree đã "đủ".

### 4.2 Giải Pháp: Mọi Tầng Đều Có Thể Thiếu → JIT Expansion

```
Với mỗi feature/keyword từ project:

┌────────────────────────────┐
│  CONCEPT có trong Master?   │
└─────┬──────────────┬────────┘
 YES  │              │  NO
      ▼              ▼
REUSE concept   PROPOSE new concept
từ Master           │
      │              ▼
      │        ┌──────────────────┐
      │        │ Agent-as-Judge    │
      │        │ • T6 neutrality   │
      │        │ • Noun phrase     │
      │        │ • Not duplicate   │
      │        └───┬──────────┬───┘
      │       PASS │          │ FAIL
      │            ▼          ▼
      │       MERGE vào    Flag cho
      │       Staging      human review
      ▼            ▼
┌────────────────────────────┐
│  ULO có trong Master?       │
└─────┬──────────────┬────────┘
 YES  │              │  NO
      ▼              ▼
REUSE           GENERATE → Judge → MERGE/quarantine
      │
      ▼
┌────────────────────────────┐
│  CIO có trong Master?       │
└─────┬──────────────┬────────┘
 YES  │              │  NO
      ▼              ▼
REUSE           GENERATE → Judge (Marr T6) → MERGE/quarantine
      │
      ▼
┌────────────────────────────┐
│  SIO có sẵn?                │
└─────┬──────────────┬────────┘
 YES  │              │  NO
      ▼              ▼
REUSE/ADAPT     GENERATE → Judge → MERGE/quarantine
```

### 4.3 Staging Architecture (Tận Dụng Roadmap-Aligner)

```
Roadmap Pipeline
     │
     ▼
┌──────────────────────────┐
│ quarantine/              │  ← Per-project isolation
│  proposed_concepts.tsv   │
│  proposed_ulos.tsv       │
│  proposed_cios.tsv       │
│  proposed_sios.tsv       │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Agent-as-Judge           │  ← Batch evaluate
│ PASS items → promote     │
│ FAIL items → rejected/   │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Staging Master TSV       │  ← general-context/mlo-knowlege-tree.tsv
│ (working copy, đã có     │    (cơ chế từ roadmap-aligner)
│  từ roadmap-aligner)     │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ tree_diff.py             │  ← Diff staging vs official
│ → Human approval         │
│ → sync_back_master.py    │  ← Promote to official
└──────────────────────────┘
```

**Tận dụng cơ chế đã có từ `roadmap-aligner`:**
- `init_staging_tree.py` → tạo working copy
- `apply_plan_to_staging.py` → apply approved changes
- `tree_diff.py` → diff staging vs official
- `sync_back_master.py` → promote (cần human approval)

### 4.4 Agent-as-Judge: Modules

**Đã có** (trong `agent_as_judge.py`):

| Evaluator | Checks |
|---|---|
| `evaluate_mapping_plan()` | T6 neutrality, structural validity |
| `evaluate_ulos()` | Bloom distribution, T6 neutrality |
| `evaluate_cios()` | Marr 2-Language Test compliance |

**Cần thêm:**

| Evaluator | Checks | Priority |
|---|---|---|
| `evaluate_concepts()` | T6 neutrality, noun phrase rule, duplicate vs Master, topic parent valid | HIGH |
| `evaluate_sios()` | Parent CIO valid, tech prefix consistent, not duplicate, cross-tech coherence | HIGH |
| `evaluate_prerequisites()` | No cycles, no self-ref, source/target exist, rationale non-empty, hierarchy respect | MEDIUM |
| `evaluate_roadmap_coherence()` | All nodes reachable, no orphans, Bloom progression non-decreasing | LOW |

---

## 5. Cross-Tech SIO Reuse qua CIO Bridge

### 5.1 Nguyên Lý

CIO là tầng trung tính (tech-agnostic), đóng vai "cầu nối" giữa SIOs của các tech khác nhau:

```
           CIO (trung tính, tech-agnostic)
           ┌─────────────────────────────┐
           │ CONSTANTS_VARIABLES          │
           │ "Phân biệt hằng số và biến:  │
           │  scope, lifetime, shadowing" │
           └──────┬────────┬────────┬────┘
                  │        │        │
           ┌──────▼──┐ ┌──▼─────┐ ┌▼──────────┐
           │ JS SIO  │ │ Py SIO │ │ Swift SIO │
           │const/let│ │UPPER_  │ │let/var    │
           │ /var    │ │CASE    │ │           │
           └─────────┘ └────────┘ └───────────┘
           
 Structure giống nhau, chỉ khác tech-specific tokens
```

### 5.2 Thuật Toán

```python
def resolve_sio_cross_tech(
    target_keyword: str,      # "let" trong Swift
    target_tech: str,         # "Swift"
    parent_cio_code: str,     # "CIO-CONSTANTS_VARIABLES-01"
    all_sios: List[Dict],
) -> Dict:
    # 1. Collect sibling SIOs under same CIO
    sibling_sios = [
        s for s in all_sios 
        if s.get("parent_lo_code") == parent_cio_code
        and s.get("lo_type") == "SPECIFIC_IMPL"
    ]
    
    if not sibling_sios:
        return {"action": "GENERATE_NEW"}
    
    # 2. Keyword similarity check
    target_tokens = set(tokenize(target_keyword))
    best_match = None
    best_score = 0.0
    
    for sio in sibling_sios:
        sio_tokens = set(tokenize(
            sio.get("description", "") + " " + sio.get("name", "")
        ))
        overlap = len(target_tokens & sio_tokens)
        score = overlap / max(1, len(target_tokens | sio_tokens))
        
        if score > best_score:
            best_score = score
            best_match = sio
    
    # 3. Decision thresholds
    if best_score >= 0.6:
        return {"action": "ADAPT_FROM_SIBLING", "source_sio": best_match}
    elif best_score >= 0.3:
        return {"action": "TEMPLATE_FROM_SIBLING", "source_sio": best_match}
    else:
        return {"action": "GENERATE_NEW", "nearest_sibling": best_match}
```

### 5.3 CIO Matching

```python
def match_cio_for_project_feature(
    feature_keyword: str,      # "WebSocket reconnection"
    target_bloom: str,        # "APPLY"
    master_cios: List[Dict],
) -> Optional[Dict]:
    feature_tokens = set(tokenize(feature_keyword))
    
    candidates = []
    for cio in master_cios:
        cio_text = cio.get("name", "") + " " + cio.get("description", "")
        cio_tokens = set(tokenize(cio_text))
        overlap = len(feature_tokens & cio_tokens)
        semantic_score = overlap / max(1, len(feature_tokens))
        
        cio_bloom = cio.get("bloom_level", "")
        bloom_score = 1.0 if cio_bloom == target_bloom else 0.5
        
        combined = 0.6 * semantic_score + 0.4 * bloom_score
        candidates.append((cio, combined))
    
    candidates.sort(key=lambda x: x[1], reverse=True)
    
    if candidates and candidates[0][1] >= 0.5:
        return {"matched": True, "cio": candidates[0][0], "score": candidates[0][1]}
    return {"matched": False}
```

### 5.4 Ví Dụ End-to-End

```
Feature keyword: "WebSocket automatic reconnection with exponential backoff"

CIO Matching:
  CIO-ERROR_HANDLING_STRATEGY-01 (hypothetical)
    name: "Error Recovery Strategy"
    desc: "...retry, backoff, circuit breaker, graceful degradation"
    bloom: APPLY
    → semantic_score: 0.70 ("backoff", "retry")
    → bloom_score: 0.5 (APPLY vs target CREATE)
    → combined: 0.62 ✅ MATCH

Cross-Tech SIO Resolution:
  Sibling SIOs under this CIO:

  SIO-JS-ERROR_HANDLING-02:
    "JavaScript: Use fetch with AbortController + retry loop 
     with Math.pow(2, attempt) delay"
    keyword overlap: 0.55 → ADAPT

  → Generate: SIO-SWIFT-ERROR_HANDLING-03:
    "Swift: Implement URLSessionWebSocketTask reconnection with 
     exponential backoff using Task.sleep and pow(2.0, Double(attempt)) delay"
```

### 5.5 Semantic Fidelity Warnings

Cross-tech adapt giữ được structure nhưng **semantics có thể sai lệch**:

| Pattern | JS Behavior | Swift Behavior | Risk |
|---|---|---|---|
| Concurrent async | `Promise.all` rejects fast | `async let` + try tất cả | Error propagation khác |
| Optional chaining | `obj?.prop` → `undefined` | `obj?.prop` → `nil` (Optional type) | Type safety khác |
| Closures | Capture by reference (mutable) | Capture list `[weak self]` needed | Memory leak risk |

**Fix:** Judge check flag "semantic divergence warnings" khi cross-tech adapt. Auto-append caveat.

---

## 6. Pipeline v3 Hoàn Chỉnh

### 6.1 Lưu Đồ Tổng Thể

```
╔══════════════════════════════════════════════════════════════════════╗
║            UNIFIED ROADMAP GENERATION PIPELINE v3                    ║
║                                                                      ║
║  Decisions:                                                          ║
║  D1: Project-scoped staging → merge global                           ║
║  D2: Cross-tech SIO reuse via CIO bridge                             ║
║  D3: LLM infer prerequisites + judge check                           ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  STEP 0: DISCOVERY                                                   ║
║  ├── Scan Master Tree (concepts, ULOs, CIOs, SIOs)                  ║
║  ├── Scan projects/*/output/ (existing SIOs, cross-tech)            ║
║  ├── Score project similarity                                        ║
║  └── → reuse_inventory                                              ║
║                                                                      ║
║  STEP 1: PROJECT ANALYSIS                                            ║
║  ├── Clone → analyze_repo_structure → extract deps                   ║
║  ├── AST-level: type hierarchy, protocol conformances, patterns      ║
║  └── → source_context (files, APIs, patterns, keywords)              ║
║                                                                      ║
║  STEP 2: KEYWORD EXTRACTION                                          ║
║  ├── imports → framework keywords                                    ║
║  ├── class/struct/protocol declarations → domain model               ║
║  ├── function signatures + call graph → business logic               ║
║  ├── test files → behavior contracts, edge cases                     ║
║  ├── config files → platform constraints                             ║
║  ├── doc comments / README → design intent                           ║
║  └── → raw_keywords[] (multi-label: mỗi keyword → top-K concepts)   ║
║                                                                      ║
║  STEP 3: CONCEPT RESOLUTION (per keyword)                            ║
║  ├── Pre-filter: field_codes từ user_goal                            ║
║  ├── Master concept exists? → REUSE                                 ║
║  ├── Project concept exists? → REUSE                                ║
║  └── Neither? → PROPOSE → quarantine                                ║
║                                                                      ║
║  STEP 4: CIO MATCHING (per resolved concept)                         ║
║  ├── Semantic search CIOs in Master (keyword + Bloom)                ║
║  ├── Match found? → REUSE CIO                                       ║
║  └── No match? → GENERATE CIO → quarantine                          ║
║       └── ULO auto-derived from CIO if ULO also missing             ║
║                                                                      ║
║  STEP 5: SIO CROSS-TECH RESOLUTION (per CIO + project keyword)       ║
║  ├── Same-tech SIO exists under CIO? → REUSE                        ║
║  ├── Cross-tech SIO (keyword overlap ≥0.6)? → ADAPT                 │
║  │    └── Replace tech tokens, keep structure                        ║
║  ├── Cross-tech SIO (overlap 0.3-0.6)? → USE AS TEMPLATE            ║
║  └── No sibling (overlap <0.3)? → GENERATE NEW                      ║
║       └── All new/adapted SIOs → quarantine                          ║
║                                                                      ║
║  STEP 6: JUDGE GATE (batch evaluate all quarantine items)            ║
║  ├── evaluate_concepts() — T6, noun phrase, duplicate               ║
║  ├── evaluate_ulos() — Bloom, T6, knowledge dimension                ║
║  ├── evaluate_cios() — Marr 2-Language Test                          ║
║  ├── evaluate_sios() — Parent CIO valid, cross-tech consistency     ║
║  ├── evaluate_prerequisites() — DAG coherence                        ║
║  └── PASS → promote to project-scoped staging                        ║
║       FAIL → rejected/for_human_review.md                            ║
║                                                                      ║
║  STEP 7: STAGING MERGE                                               ║
║  ├── Project staging → Global staging TSV                            ║
║  ├── tree_diff.py → show delta                                       ║
║  └── (defer sync_back_master to human approval)                      ║
║                                                                      ║
║  STEP 8: ROADMAP ASSEMBLY                                            ║
║  ├── all_los = reused + promoted_new                                 ║
║  ├── Prerequisite inference cho nodes mới (3-question protocol)        ║
║  ├── Topo sort on prerequisite DAG                                   ║
║  ├── Schedule per time budget                                        ║
║  └── → roadmap_graph.json + instruction skeleton                    ║
║                                                                      ║
║  STEP 8.5: INSTRUCTION CODE EXTRACTION                               ║
║  ├── For each phase in roadmap:                                      ║
║  │   ├── Identify relevant source files (from Step 1)                ║
║  │   ├── Extract code snippets matching phase's concept codes        ║
║  │   │   ├── Function implementations → §3 hands-on                 ║
║  │   │   ├── Type declarations → §3 pattern reference               ║
║  │   │   ├── Error handling blocks → §6 debug table                 ║
║  │   │   └── Test cases → §5 test scripts                           ║
║  │   ├── Truncate/format snippets (max 30 lines each)               ║
║  │   └── Embed with [REF: ...] tags                                 ║
║  └── Validation: mỗi §3 ≥1 snippet, mỗi §6 ≥2 phase-specific       ║
║                                                                      ║
║  STEP 9: POST-GENERATION VALIDATION                                  ║
║  ├── Structural: LO codes trong instruction tồn tại trong roadmap    ║
║  ├── Pedagogical: Bloom progression non-decreasing per branch        ║
║  ├── Coverage: instruction phases cover ≥80% roadmap LOs            ║
║  ├── Time: total estimated hours ≤ budget × 1.2                      ║
║  └── FAIL → auto-fix loop (max 3) | CRITICAL → abort                ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 6.2 Chi Tiết Từng Step

#### STEP 0: Discovery

```python
def discover_reuse_inventory(
    user_goal: str,
    user_tech_stack: List[str],
    master_tree_path: Path,
    projects_dir: Path,
) -> Dict:
    """Scan Master Tree + existing projects, compute reuse inventory."""
    
    # Load Master Tree
    concepts, los, prereqs = load_master_tree(master_tree_path)
    
    # Scan existing project SIOs
    project_sios = {}
    for project_dir in projects_dir.iterdir():
        lo_file = project_dir / "output" / "learning-objectives.tsv"
        if lo_file.exists():
            sios = [r for r in read_tsv(lo_file) if r.get("lo_type") == "SPECIFIC_IMPL"]
            project_sios[project_dir.name] = {
                "sios": sios,
                "tech_stack": extract_tech_from_sios(sios),
                "concept_codes": extract_concepts_from_sios(sios),
            }
    
    # Score similarity
    scored_projects = []
    for name, data in project_sios.items():
        score = score_project_similarity(
            {"tech_stack": user_tech_stack, "keywords": set(), "concept_codes": set()},
            data
        )
        if score >= 0.4:
            scored_projects.append({"name": name, "score": score, "data": data})
    
    scored_projects.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "master_concepts": concepts,
        "master_los": los,
        "master_prereqs": prereqs,
        "similar_projects": scored_projects,
    }
```

#### STEP 1: Project Analysis (AST-level)

```
analyze_repo_structure.py (đã có) cần extend:
├── Parse Swift files → extract:
│   ├── Type hierarchy (class/struct/enum/protocol declarations)
│   ├── Protocol conformances
│   ├── Property wrappers used (@State, @Binding, @Observable...)
│   ├── Function signatures + call graph
│   └── Error handling patterns (do-catch, Result type, throws)
├── Build dependency graph giữa types
├── Identify architectural patterns:
│   ├── MVVM (View → ViewModel → Model)
│   ├── TCA (Reducer + Store + Effect)
│   ├── Coordinator
│   └── Repository pattern
└── → source_context.json
```

#### STEP 2: Keyword Extraction

```python
def extract_project_keywords(source_context: Dict) -> List[Dict]:
    """Multi-source keyword extraction."""
    keywords = []
    
    # Source 1: Import statements → framework keywords
    for imp in source_context.get("imports", []):
        keywords.append({
            "keyword": imp,
            "source": "import",
            "weight": 1.0,
        })
    
    # Source 2: Type declarations → domain concepts
    for type_decl in source_context.get("types", []):
        keywords.append({
            "keyword": type_decl["name"],
            "source": "type_declaration",
            "weight": 1.5,  # higher weight for domain types
        })
    
    # Source 3: Function signatures → business logic
    for func in source_context.get("functions", []):
        keywords.append({
            "keyword": func["name"],
            "source": "function_signature",
            "weight": 1.2,
        })
    
    # Source 4: Property wrappers → state management patterns
    for pw in source_context.get("property_wrappers", []):
        keywords.append({
            "keyword": pw,
            "source": "property_wrapper",
            "weight": 2.0,  # high weight — strong pattern signal
        })
    
    # Source 5: Test assertions → behavior contracts
    for test in source_context.get("test_assertions", []):
        keywords.append({
            "keyword": test["description"],
            "source": "test_case",
            "weight": 1.3,
        })
    
    # Source 6: Config/entitlements → platform constraints
    for config in source_context.get("config_entries", []):
        keywords.append({
            "keyword": config["key"],
            "source": "config",
            "weight": 0.8,
        })
    
    # Source 7: README sections → design intent
    for section in source_context.get("readme_sections", []):
        keywords.append({
            "keyword": section["title"],
            "source": "readme",
            "weight": 0.9,
        })
    
    return keywords
```

#### STEP 3: Concept Resolution

```python
def resolve_concepts(
    keywords: List[Dict],
    reuse_inventory: Dict,
    top_k: int = 3,  # multi-label
) -> Dict:
    """Resolve keywords to concepts. Multi-label: each keyword → top-K concepts."""
    
    master_concepts = reuse_inventory["master_concepts"]
    
    # Pre-filter by field relevance
    relevant_fields = infer_fields_from_goal(user_goal)
    filtered_concepts = [
        c for c in master_concepts 
        if any(f in relevant_fields for f in c.get("field_codes", "").split(","))
    ]
    
    resolved = []
    proposed = []
    
    for kw in keywords:
        # BM25 + embedding similarity search
        matches = semantic_search(kw["keyword"], filtered_concepts, top_k=top_k)
        
        if matches and matches[0]["score"] >= 0.80:
            # High confidence → REUSE
            resolved.append({
                "keyword": kw["keyword"],
                "concept_codes": [m["code"] for m in matches if m["score"] >= 0.80],
                "source": "master_reuse",
                "confidence": matches[0]["score"],
            })
        else:
            # Low confidence → PROPOSE new concept
            proposed.append({
                "proposed_code": slugify(kw["keyword"]),
                "name": kw["keyword"],
                "source_keyword": kw["keyword"],
                "source_project": project_name,
                "best_existing_match": matches[0] if matches else None,
                "confidence": matches[0]["score"] if matches else 0.0,
            })
    
    # De-duplicate proposed concepts
    proposed = deduplicate_proposals(proposed)
    
    return {"resolved": resolved, "proposed": proposed}
```

#### STEP 4: CIO Matching

```python
def resolve_cios(
    resolved_concepts: List[Dict],
    reuse_inventory: Dict,
) -> Dict:
    """Match or generate CIOs for resolved concepts."""
    
    master_cios = [
        lo for lo in reuse_inventory["master_los"]
        if lo.get("lo_type") == "CONCEPTUAL_IMPL"
    ]
    
    reused = []
    proposed = []
    
    for concept in resolved_concepts:
        for code in concept["concept_codes"]:
            # Search CIOs for this concept
            matching_cios = [
                cio for cio in master_cios
                if code in cio.get("concept_codes", "")
            ]
            
            if matching_cios:
                # REUSE existing CIO
                reused.append({
                    "concept_code": code,
                    "cio_code": matching_cios[0]["code"],
                    "source": "master_reuse",
                })
            else:
                # Cross-project reuse?
                cross_project_cio = search_cross_project_cios(code, reuse_inventory)
                if cross_project_cio:
                    reused.append({
                        "concept_code": code,
                        "cio_code": cross_project_cio["code"],
                        "source": "cross_project_reuse",
                    })
                else:
                    # GENERATE new CIO
                    proposed.append({
                        "concept_code": code,
                        "source_project": project_name,
                    })
    
    return {"reused": reused, "proposed": proposed}
```

#### STEP 5: SIO Cross-Tech Resolution

```python
def resolve_sios(
    cio_mappings: List[Dict],
    project_keywords: List[Dict],
    target_tech: str,
    reuse_inventory: Dict,
) -> Dict:
    """Cross-tech SIO resolution via CIO bridge."""
    
    all_sios = collect_all_sios(reuse_inventory)  # from Master + all projects
    
    reused = []
    adapted = []
    proposed = []
    
    for cio_map in cio_mappings:
        cio_code = cio_map["cio_code"]
        relevant_keywords = get_relevant_keywords(cio_map["concept_code"], project_keywords)
        
        for kw in relevant_keywords:
            result = resolve_sio_cross_tech(
                target_keyword=kw["keyword"],
                target_tech=target_tech,
                parent_cio_code=cio_code,
                all_sios=all_sios,
            )
            
            if result["action"] == "REUSE":
                reused.append(result)
            elif result["action"] in ("ADAPT_FROM_SIBLING", "TEMPLATE_FROM_SIBLING"):
                adapted.append(result)
            else:  # GENERATE_NEW
                proposed.append({
                    "parent_cio_code": cio_code,
                    "tech_prefix": target_tech,
                    "source_keyword": kw["keyword"],
                    "source_project": project_name,
                })
    
    return {"reused": reused, "adapted": adapted, "proposed": proposed}
```

#### STEP 6: Judge Gate

```python
def run_judge_gate(
    quarantine_dir: Path,
    judge_script: Path,
) -> Dict:
    """Batch evaluate all quarantine items."""
    
    results = {"promoted": [], "rejected": []}
    
    # Concepts
    concepts_file = quarantine_dir / "proposed_concepts.tsv"
    if concepts_file.exists():
        verdict = run_command(
            f"python3 {judge_script} --mode concepts --artifact {concepts_file}"
        )
        results["promoted"].extend(verdict.get("approved", []))
        results["rejected"].extend(verdict.get("rejected", []))
    
    # ULOs
    ulos_file = quarantine_dir / "proposed_ulos.tsv"
    if ulos_file.exists():
        verdict = run_command(
            f"python3 {judge_script} --mode ulos --artifact {ulos_file}"
        )
        results["promoted"].extend(verdict.get("approved", []))
        results["rejected"].extend(verdict.get("rejected", []))
    
    # CIOs (Marr T6 test)
    cios_file = quarantine_dir / "proposed_cios.tsv"
    if cios_file.exists():
        verdict = run_command(
            f"python3 {judge_script} --mode cios --artifact {cios_file}"
        )
        results["promoted"].extend(verdict.get("approved", []))
        results["rejected"].extend(verdict.get("rejected", []))
    
    # SIOs
    sios_file = quarantine_dir / "proposed_sios.tsv"
    if sios_file.exists():
        verdict = run_command(
            f"python3 {judge_script} --mode sios --artifact {sios_file}"
        )
        results["promoted"].extend(verdict.get("approved", []))
        results["rejected"].extend(verdict.get("rejected", []))
    
    # Write rejected for human review
    write_rejected_report(results["rejected"], quarantine_dir / "rejected")
    
    return results
```

#### Prerequisite Inference (3-Question Protocol)

```
Khi propose CONCEPT mới (ví dụ: HEALTH_DATA_MODELING):

Q1: Prerequisites của nó là concept nào đã có?
  LLM: "HEALTH_DATA_MODELING cần hiểu DATA_REPRESENTATION 
        và RELATIONAL_VS_NONRELATIONAL trước"
  → Edge: DATA_REPRESENTATION → HEALTH_DATA_MODELING
  → Edge: RELATIONAL_VS_NONRELATIONAL → HEALTH_DATA_MODELING

Q2: Nó là prerequisite của concept nào khác?
  LLM: "HEALTH_DATA_MODELING là prerequisite của 
        BIOMETRIC_SENSOR_API"
  → Edge: HEALTH_DATA_MODELING → BIOMETRIC_SENSOR_API

Q3: ULO/CIO derived từ nó có prerequisite ở tầng tương ứng?
  Rule: CIO parent = ULO cùng concept (auto)
        SIO parent = CIO cùng concept (auto)
        Cross-concept: LLM infer
```

---

## 7. 13 Gaps Identified

| # | Gap | Mức Nghiêm Trọng | Fix |
|---|---|---|---|
| 1 | **Keyword extraction quá surface-level** — chỉ grep tokens, không hiểu code structure | 🔴 Cao | AST-level analysis (type hierarchy, protocols, call graph) |
| 2 | **Context window overflow** — 300-450K tokens tổng data vượt quá model limit | 🔴 Cao | Pre-filter theo field_codes, retrieval strategy trước mỗi LLM call |
| 3 | **Keyword→Concept mapping giả định 1:1** — thực tế 1 keyword map vào 2-3 concepts | 🟡 TB | Multi-label resolution (top-K), de-duplicate |
| 4 | **Instruction code snippet chưa có cơ chế** — §3 rỗng, không có code thật | 🔴 Cao | Sub-pipeline STEP 8.5: extract snippets từ repo, embed vào instruction |
| 5 | **Prerequisite inference chưa detail** — chỉ nói "LLM infer" | 🟡 TB | 3-question protocol (prerequisites, dependents, cross-layer) |
| 6 | **Post-generation validation thiếu** — không verify LO codes trong instruction có tồn tại | 🔴 Cao | STEP 9: structural + pedagogical + technical checks |
| 7 | **Incremental re-planning chưa cover** — chỉ generate from scratch | 🟡 TB | Re-plan mode: existing_roadmap + delta_request → updated_roadmap |
| 8 | **Cross-project learner history** — không track LOs đã master qua nhiều projects | 🟡 TB | Learner profile (completed_lo_codes, mastery_scores, tech_exposure) |
| 9 | **Cross-tech SIO semantic fidelity** — adapt giữ structure nhưng semantics có thể sai | 🟡 TB | Judge flag "semantic divergence warnings", auto-append caveat |
| 10 | **Quarantine data model chưa define** — không có schema cho proposed_*.tsv | 🟡 TB | Schema definition (xem §8) |
| 11 | **Pipeline orchestration thiếu** — scripts standalone, không có workflow | 🟡 TB | Workflow definition YAML |
| 12 | **Scripts cần viết: 6 mới + 3 refactor** — implementation effort lớn | — | Implementation plan (xem §9) |
| 13 | **Feedback loop từ human review** — rejected items là dead-end | 🟡 TB | Bayesian update: approved/rejected → adjust confidence thresholds |

---

## 8. Data Models

### 8.1 Quarantine Schemas

#### proposed_concepts.tsv

```
proposed_code | name | description | suggested_topic_codes |
source_project | source_keyword | confidence_score |
best_existing_match_code | best_existing_match_score |
judge_verdict | judge_reason | status | proposed_at
```

#### proposed_ulos.tsv

```
proposed_code | name | description | concept_codes |
bloom_level | knowledge_dim | assessment_approach |
source_project | source_cio_code | confidence_score |
judge_verdict | judge_reason | status | proposed_at
```

#### proposed_cios.tsv

```
proposed_code | name | description | parent_ulo_code |
concept_codes | bloom_level | marr_t6_pass |
lang1_mapping | lang2_mapping |
source_project | confidence_score |
judge_verdict | judge_reason | status | proposed_at
```

#### proposed_sios.tsv

```
proposed_code | name | description | parent_cio_code |
tech_prefix | concept_codes | bloom_level |
source_type | source_sibling_code | source_sibling_tech |
source_project | confidence_score |
semantic_divergence_warnings |
judge_verdict | judge_reason | status | proposed_at
```

**`source_type` enum:** `NEW` | `ADAPT_FROM_SIBLING` | `TEMPLATE_FROM_SIBLING`

### 8.2 reuse_inventory.json

```json
{
  "master_concepts": {
    "DECLARATIVE_UI_PARADIGM": {"name": "...", "description": "...", "field_codes": "HCC, ASE"},
    "...": "..."
  },
  "master_los": {
    "ULO-DECLARATIVE_UI_PARADIGM-01": {"lo_type": "UNIVERSAL", "...": "..."},
    "CIO-DECLARATIVE_UI_PARADIGM-01": {"lo_type": "CONCEPTUAL_IMPL", "...": "..."},
    "SIO-SWIFT-DECLARATIVE_UI_PARADIGM-01": {"lo_type": "SPECIFIC_IMPL", "...": "..."}
  },
  "master_prereqs": [
    {"source": "FOR_LOOP", "target": "ARRAY_OPERATIONS", "rationale": "..."}
  ],
  "similar_projects": [
    {
      "name": "swift-associate",
      "score": 0.72,
      "tech_stack": ["Swift", "SwiftUI", "Combine", "CoreData"],
      "sio_count": 77,
      "concept_coverage": ["DECLARATIVE_UI_PARADIGM", "LOCAL_VIEW_STATE", "..."]
    }
  ]
}
```

### 8.3 source_context.json

```json
{
  "repo_url": "https://github.com/...",
  "clone_path": ".cache/repos/...",
  "languages": ["Swift"],
  "total_files": 45,
  "architecture_pattern": "MVVM",
  "imports": [
    {"module": "SwiftUI", "files": 12},
    {"module": "Combine", "files": 8},
    {"module": "HealthKit", "files": 3}
  ],
  "types": [
    {"name": "ChatViewModel", "kind": "class", "conforms_to": ["ObservableObject"], "file": "..."},
    {"name": "Message", "kind": "struct", "conforms_to": ["Codable", "Identifiable"], "file": "..."}
  ],
  "property_wrappers": ["@State", "@Binding", "@Published", "@ObservedObject", "@StateObject"],
  "functions": [
    {"name": "connectWebSocket()", "throws": true, "async": true, "class": "ChatTransport"},
    {"name": "handleMessage(_:)", "params": ["Data"], "returns": "ChatEvent", "class": "ChatViewModel"}
  ],
  "error_handling_patterns": [
    {"pattern": "do-catch", "count": 15},
    {"pattern": "Result type", "count": 8},
    {"pattern": "throws propagation", "count": 12}
  ],
  "test_assertions": [
    {"description": "WebSocket reconnection after network loss", "file": "ChatTransportTests.swift"},
    {"description": "Message ordering preserved", "file": "ChatViewModelTests.swift"}
  ],
  "config_entries": [
    {"key": "NSAppTransportSecurity", "file": "Info.plist"},
    {"key": "com.apple.developer.healthkit", "file": "Entitlements.plist"}
  ]
}
```

---

## 9. Scripts Cần Viết

### 9.1 Scripts Mới

| Script | Mô Tả | Effort | Dependencies |
|---|---|---|---|
| `roadmap_discovery.py` | STEP 0: Scan Master Tree + projects, compute reuse inventory | Medium | `load_master_data()` (đã có) |
| `extract_project_keywords.py` | STEP 1-2: AST-level keyword extraction từ repo | High | `analyze_repo_structure.py` (extend) |
| `resolve_concepts.py` | STEP 3: Multi-label concept resolution | Medium | `semantic_search_master.py` (đã có) |
| `match_cios.py` | STEP 4: CIO matching + ULO derivation | Medium | `resolve_concepts.py` output |
| `resolve_sios.py` | STEP 5: Cross-tech SIO resolution via CIO bridge | High | `match_cios.py` output |
| `instruction_code_extractor.py` | STEP 8.5: Extract code snippets từ repo cho instruction | High | `source_context.json` |
| `validate_roadmap.py` | STEP 9: Post-generation validation | Medium | `validate_tree.py` (extend) |

### 9.2 Scripts Cần Refactor/Extend

| Script | Thay Đổi | Effort |
|---|---|---|
| `agent_as_judge.py` | Thêm 3 evaluators: concepts, sios, prerequisites | Medium |
| `generate_project_driven_roadmap.py` | Refactor thành orchestrator gọi pipeline v3 steps | High |
| `apply_plan_to_staging.py` | Extend: accept proposed_*.tsv từ quarantine | Low |

### 9.3 Workflow Definition

```yaml
# .agents/workflows/generate-roadmap.md (mới)
name: generate-roadmap
description: Generate adaptive roadmap from Master Tree + project, with JIT expansion + Judge Gate

steps:
  - id: discovery
    script: roadmap_discovery.py
    input: user_goal, user_tech_stack
    output: reuse_inventory.json
    
  - id: project-analysis
    script: analyze_repo_structure.py (extended)
    input: project_url
    output: source_context.json
    
  - id: keyword-extraction
    script: extract_project_keywords.py
    input: source_context.json
    output: raw_keywords.json
    
  - id: concept-resolution
    script: resolve_concepts.py
    input: raw_keywords.json, reuse_inventory.json
    output: resolved_concepts.json, quarantine/proposed_concepts.tsv
    
  - id: cio-matching
    script: match_cios.py
    input: resolved_concepts.json, reuse_inventory.json
    output: resolved_cios.json, quarantine/proposed_cios.tsv
    
  - id: sio-resolution
    script: resolve_sios.py
    input: resolved_cios.json, raw_keywords.json, reuse_inventory.json
    output: resolved_sios.json, quarantine/proposed_sios.tsv
    
  - id: judge-gate
    script: agent_as_judge.py --mode roadmap-pipeline
    input: quarantine/*.tsv
    output: promoted/, rejected/for_human_review.md
    
  - id: staging-merge
    script: apply_to_staging.py (extended)
    input: promoted/
    output: staging TSV updated
    
  - id: roadmap-assembly
    script: generate_project_driven_roadmap.py (refactored)
    input: reuse_inventory.json, resolved_*.json, promoted/
    output: roadmap_graph.json, instruction/
    
  - id: instruction-code
    script: instruction_code_extractor.py
    input: source_context.json, instruction/
    output: instruction/ (with code snippets)
    
  - id: validation
    script: validate_roadmap.py
    input: roadmap_graph.json, instruction/
    output: validation_report.json
```

---

## 10. Vấn Đề Mở

### 10.1 Merge Conflict (Song Song)

Nếu 2 roadmap pipelines chạy song song cho 2 projects khác nhau, cả 2 đều propose concept mới → staging TSV conflict?

**Giải pháp đề xuất:** Mỗi pipeline merge vào project-scoped staging (`projects/<name>/.work/staging/`). Cuối cùng merge tất cả vào global staging. Conflict resolution: last-write-wins cho cùng code, union cho different codes.

### 10.2 SIO Adapt vs Generate Threshold

Khi nào "adapt" SIO cũ thay vì generate mới?

**Đề xuất:** Keyword overlap ≥0.6 → adapt. 0.3-0.6 → template. <0.3 → generate. Ai quyết cuối cùng? Agent-as-Judge.

### 10.3 Cross-Project SIO Promotion

SIO adapt thành công ở project B → có nên promote ngược vào Master Tree làm SIO chính thức cho tech B?

**Đề xuất:** Có, qua staging → human approval. Để project C sau này reuse trực tiếp từ Master Tree thay vì scan cross-project.

### 10.4 SIO Adapt Semantic Scope

Khi adapt SIO từ tech A sang tech B, có nên giữ `assessment_approach` không?

**Đề xuất:** Giữ nếu cùng category (code-review → code-review). Đổi nếu khác paradigm (debugging-exercise → project, nếu tech B không có debugger tương đương).

### 10.5 Staging Lifecycle

Project-scoped staging tồn tại bao lâu?

**Đề xuất:** Tồn tại cho đến khi global staging merge hoàn tất (human approved sync_back). Sau đó archive vào `.work/archive/`.

### 10.6 Incremental Re-Planning

```
Scenario A: Hoàn thành Phase 0-2, quay lại request tiếp
  → known_set += completed LOs
  → Re-run từ STEP 3 (pruning theo baseline)
  → Phase 0-2 marked COMPLETED trong roadmap

Scenario B: Muốn thay đổi scope mid-way
  → User: "Bỏ phần CoreData, thêm HealthKit"
  → Partial re-plan: remove CoreData LOs, re-run STEP 2-8 cho HealthKit
  → Keep completed phases intact

Scenario C: Learner chậm hơn expected
  → Phase 0 mất 2 tuần thay vì 1
  → Re-schedule remaining phases
  → Option: compress hoặc extend timeline
```

**Đề xuất:** Thêm re-plan mode nhận input: `existing_roadmap + delta_request → updated_roadmap`. Không generate from scratch.

### 10.7 Learner Profile Schema

```json
{
  "learner_id": "uuid",
  "completed_lo_codes": ["ULO-FOR_LOOP-01", "CIO-ARRAY_OPERATIONS-01", "..."],
  "mastery_scores": {
    "ULO-FOR_LOOP-01": 0.95,
    "CIO-ARRAY_OPERATIONS-01": 0.82
  },
  "tech_exposure": {
    "Swift": 3,
    "JavaScript": 1,
    "Python": 2
  },
  "total_hours_learned": 120,
  "projects_completed": ["swift-associate", "python-basics"]
}
```

Lưu ở đâu? Supabase `student_mastery` table (đã có schema trong spec).

### 10.8 Feedback Loop Từ Human Review

```
Human reviews rejected items
  │
  ├── Approved → merge vào staging + log as "positive example"
  │     → Update confidence threshold (bayesian update)
  │
  ├── Rejected → log as "negative example"  
  │     → Future judge: similar proposals auto-reject
  │
  └── Modified → human edits → merge modified version
        → Log as "correction" → fine-tune judge prompt
```

---

## Phụ Lục A: Timeline Thảo Luận

| Thời điểm | Nội dung |
|---|---|
| Đầu phiên | Đọc 2 tài nguyên: `product-first-adaptive-roadmap-architecture.md` + `adaptive-roadmap-generator.md` |
| Khảo sát | `.agents/` directory, roadmap-aligner skill, 3 scripts (`generate_adaptive_roadmap.py`, `generate_project_roadmap.py`, `generate_project_driven_roadmap.py`) |
| Phân tích | `swift-associate` artifacts: mapping-plan, 6 instruction steps, learning-objectives, roadmap_graph, notes, techstack_final |
| Phát hiện | 2 pipeline song song không intersect, instruction template machine, LO codes hallucinated |
| Human chỉnh | "Master Tree là single source of truth, không phải project LOs" — hiểu lại kiến trúc đúng |
| Case 1 | Fresh project — chưa có gì |
| Case 2 | Similar project exists — tái tận dụng |
| Human chỉnh | "Master Tree chưa đủ, mọi tầng đều có thể thiếu, cần JIT expansion + Judge Gate auto-merge" |
| Decision 2 | Cross-tech SIO reuse via CIO bridge (let/const example) |
| Review | 13 gaps identified — keyword extraction, context window, multi-label, code snippets, validation... |
| Cuối | Ghi lại tài liệu này |

## Phụ Lục B: Tài Liệu Tham Chiếu

- `docs/ideas/product-first-adaptive-roadmap-architecture.md` — Spec v4.1 (Pipeline 9 bước Orchable)
- `docs/ideas/adaptive-roadmap-generator.md` — Pipeline 8 giai đoạn (Khoa học nền tảng)
- `docs/ideas/gap-analysis-and-product-first-blueprint.md` — Gap analysis v4.1
- `AGENTS.md` — Quy tắc vận hành Knowledge Tree
- `scripts/generate_project_driven_roadmap.py` — Script hiện tại (~1332 dòng)
- `.agents/skills/taxonomy-mapper/scripts/agent_as_judge.py` — Judge implementation hiện tại
- `.agents/skills/roadmap-aligner/` — Staging architecture (tái tận dụng)
- `projects/swift-associate/` — Case study artifacts
