# Keyword → Concept Escalation — Quy trình chuẩn & bài học từ Smart Bulb

> **Ngày:** 2026-08-07  
> **Trạng thái:** ✅ Ý tưởng ghi nhận (bởi Human) — phát hiện từ dự án Smart Bulb  
> **Liên kết:** [`2026-08-07-vertical-slicing-roadmap.md`](./2026-08-07-vertical-slicing-roadmap.md) · [`2026-08-06-action-roadmap.md`](./2026-08-06-action-roadmap.md)

---

## 1. Quy trình chuẩn (đã xác nhận)

```
Extract (code) → Keyword (tech-specific) → Đánh giá escalate → Concept trung tính
                                                              ├─ match Master Tree (REUSE)
                                                              └─ tạo concept mới (Gap D)
```

**Nguyên tắc:**
- **Extract luôn ra keyword** — không lọc bớt ở bước extract
- **Keyword phải được ĐÁNH GIÁ** để escalate lên concept
- Escalate = abstraction: keyword cụ thể → concept trung tính (technology-agnostic)
- Concept mới chỉ tạo khi **không match** Master Tree (Gap D)

---

## 2. Vấn đề phát hiện từ Smart Bulb (2026-08-07)

### 2.1 Lỗi: tên thư viện cụ thể bị đẩy thành concept

Khi chạy pipeline cho smart bulb (SwiftUI + ESP32 firmware), extractor bắt được:

```
WiFi.h, ArduinoJson.h, PubSubClient.h, Adafruit_NeoPixel.h
```

→ resolve_concepts tạo concept code từ tên file: `WIFI_H`, `ARDUINOJSON_H`...

**SAI** vì:
- `WIFI_H`, `ARDUINOJSON_H` là **tên header file / thư viện cụ thể** (Implementational)
- Vi phạm nguyên tắc trung tính (AGENTS.md §1): concepts 100% trung tính, không tên công nghệ
- Thư viện cụ thể thuộc tầng **SIO** (tầng duy nhất chứa công nghệ)

### 2.2 Phân loại đúng

| Sai (concept) | Đúng (concept trung tính) | Đúng (SIO — tech-specific) |
|---------------|---------------------------|----------------------------|
| WIFI_H | Wireless Networking | WiFi.h, WiFi.begin |
| ARDUINOJSON_H | JSON Serialization | ArduinoJson, deserializeJson |
| PUBSUBCLIENT_H | MQTT Messaging | PubSubClient, mqttClient |
| ADAFRUIT_NEOPIXEL_H | LED Control | Adafruit_NeoPixel, setPixelColor |
| SWIFTUI | Declarative UI | SwiftUI, @State |

### 2.3 Master Tree đã có concept trung tính cover

```
JSON_SERIALIZATION          ← cover ArduinoJson.h ✅
IOT_PROTOCOLS_MQTT_CONCEPT  ← cover PubSubClient.h ✅
```

Nhưng **embedding match tệ**:
- `ArduinoJson.h` → match `MECHATRONICS_SYSTEMS_DIAGNOSTICS` (0.25) thay vì `JSON_SERIALIZATION`
- `PubSubClient.h` → match `PACKAGE_MANAGEMENT` (0.40) thay vì `IOT_PROTOCOLS_MQTT_CONCEPT`

→ Embedding không hiểu tên thư viện cụ thể → cần **LLM abstraction** (không chỉ embedding).

---

## 3. Giải pháp: tận dụng workflow /escalate-concepts đã có

Repo **đã có sẵn** workflow `/escalate-concepts` + script `llm_escalate_concepts.py`:

```
Phase 1 — Abstraction (LLM):
  Group keywords theo concept trung tính (technology-agnostic)
  Ràng buộc: concept name/description KHÔNG chứa tên công nghệ cụ thể
  Mapping N:N: 1 keyword → nhiều concept; nhiều keywords → 1 concept

Phase 2 — Master Tree Matching (embedding cosine):
  Embed proposed concept + Master Tree concepts
  Cosine >= 0.80 (conservative) → matched_master_code

Phase 3 — Gap Detection:
  Concept không match → is_new_concept = True → Gap D candidate
```

**Vấn đề:** pipeline v3 (`resolve_concepts.py`) **không gọi** bước escalate này — nó tự embedding match trực tiếp keyword → concept, dẫn đến lỗi trên.

---

## 4. Thay đổi đề xuất

### 4.1 Pipeline v3: thêm bước escalate giữa STEP 3 và STEP 4

```
STEP 3    resolve_concepts.py      — keyword → concept (embedding, hiện tại)
STEP 3.5  llm_escalate_concepts.py — LLM abstraction: keyword → concept trung tính
                                     → match Master Tree (0.80) → Gap D candidates
STEP 4    match_cios.py            — concept → CIO (dùng concept đã escalate)
```

### 4.2 resolve_concepts: không tạo concept code từ tên file

- Keyword là tên thư viện (`WiFi.h`) → **không** tạo `WIFI_H`
- Đẩy qua LLM abstraction → concept trung tính (`Wireless Networking`)
- Thư viện cụ thể → ghi vào SIO layer (tech-specific)

### 4.3 JIT nội bộ (đã có, giữ nguyên)

- Concepts thiếu Master Tree → JIT sinh ULO/CIO/SIO **nội bộ**
- Roadmap chạy được ngay
- **Cuối dự án mới đề xuất sync ngược** Master Tree (không tự ghi — AGENTS.md §1)

---

## 5. Tác động

| Thành phần | Thay đổi |
|-----------|----------|
| `resolve_concepts.py` | Không tạo concept từ tên file; đẩy keyword qua escalate |
| `generate_roadmap_v3.py` | Thêm STEP 3.5 (escalate) giữa STEP 3 và STEP 4 |
| `llm_escalate_concepts.py` | Tái sử dụng (đã có) — wire vào pipeline |
| JIT (`generate_jit_los.py`) | Giữ nguyên — chỉ JIT cho concept trung tính thật |

---

## 6. Trạng thái

- [x] Phát hiện vấn đề (2026-08-07, từ Smart Bulb)
- [x] Xác nhận quy trình chuẩn: extract → keyword → escalate → concept
- [x] Xác nhận Master Tree đã có concept trung tính cover (JSON_SERIALIZATION, IOT_PROTOCOLS_MQTT_CONCEPT)
- [x] Xác nhận workflow /escalate-concepts đã có sẵn
- [ ] Wire STEP 3.5 vào pipeline v3
- [ ] Fix resolve_concepts: không tạo concept từ tên file
- [ ] Test lại Smart Bulb: ArduinoJson.h → JSON_SERIALIZATION (không phải MECHATRONICS)
