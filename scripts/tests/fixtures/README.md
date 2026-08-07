# Golden Fixtures — smart-bulb-controller pipeline run 2026-08-07

Xuất xứ: `/tmp/pipeline-bulb9/` — full pipeline run trên `/tmp/smart-bulb-controller`
(Swift app + ESP32 firmware), commit `79ac59e`.

## bulb9/ — pipeline artifacts (input/output của từng step)
| File | Step | Nội dung |
|---|---|---|
| `keywords.json` | 1-2 | 38 keywords + source + platform lineage |
| `resolved_concepts.json` | 3 | keyword → concept (embedding + override) |
| `escalated_concepts.json` | 3.5 | LLM abstraction (2 concepts sau skip-resolved fix) |
| `matched_cios.json` | 4 | concept → CIO Master Tree (đã lọc 12-verb template) |
| `resolved_sios.json` | 5 | GENERATE-first |
| `prerequisites.json` | 4.5 | 73 edges concept-level |
| `jit_los.json` | 5.5 | 36 LOs (12 concepts × 3 tiers), 3 ULO needs_review |
| `roadmap_final.json` | 8.7 | 12 milestones, 3 phases, semantic gate PASS |

## smart-bulb-repo/ — ground-truth code (3 file cần thiết)
- `ContentView.swift`, `HTTPBulbService.swift` — Swift app (platform=app)
- `smart_bulb.ino` — ESP32 firmware (platform=esp32, chứa `for` ×4)

## Ground truths đã biết (cho assertions)
- 12 concepts, 3 phases, 36 LOs; SIO platform prefix: SIO-SWIFT-*/SIO-ESP32-*
- Keywords thật: SwiftUI, URLSession, @State, try!, Task, Foundation, for, WiFi.h, WebServer.h, PubSubClient.h, Adafruit_NeoPixel.h, JSONSerialization
- KHÔNG tồn tại trong code: forEach, http protocol, authentication
