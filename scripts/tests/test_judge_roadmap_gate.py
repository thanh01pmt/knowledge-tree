"""test_judge_roadmap_gate.py - Unit tests for agent_as_judge.py evaluate_roadmap logic.
"""

import sys
import os

# Add scripts directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import agent_as_judge


def make_clean_roadmap():
    return {
        "phases": [
            {
                "phase_id": 1,
                "milestones": [
                    {
                        "concept_code": "CONCEPT_A",
                        "learning_objectives": [
                            {
                                "code": "ULO-CONCEPT_A-01",
                                "lo_type": "UNIVERSAL",
                                "description": "Giải thích cú pháp và cách dùng vòng lặp for trong Swift",
                                "bloom_level": "understand",
                                "keyword": "",
                                "platform": ""
                            },
                            {
                                "code": "CIO-CONCEPT_A-01",
                                "lo_type": "CONCEPTUAL_IMPL",
                                "description": "Áp dụng thuật toán lặp để duyệt mảng dữ liệu",
                                "bloom_level": "apply",
                                "keyword": "",
                                "platform": ""
                            },
                            {
                                "code": "SIO-SWIFT-CONCEPT_A-01",
                                "lo_type": "SPECIFIC_IMPL",
                                "description": "Xây dựng ứng dụng Swift dùng vòng lặp for",
                                "bloom_level": "create",
                                "keyword": "for-in",
                                "platform": "app"
                            }
                        ]
                    }
                ]
            },
            {
                "phase_id": 2,
                "milestones": [
                    {
                        "concept_code": "CONCEPT_B",
                        "learning_objectives": [
                            {
                                "code": "ULO-CONCEPT_B-01",
                                "lo_type": "UNIVERSAL",
                                "description": "Nắm vững khái niệm hàm và phương thức",
                                "bloom_level": "understand",
                                "keyword": "",
                                "platform": ""
                            },
                            {
                                "code": "CIO-CONCEPT_B-01",
                                "lo_type": "CONCEPTUAL_IMPL",
                                "description": "Thiết kế hàm có tham số và giá trị trả về",
                                "bloom_level": "apply",
                                "keyword": "",
                                "platform": ""
                            },
                            {
                                "code": "SIO-SWIFT-CONCEPT_B-01",
                                "lo_type": "SPECIFIC_IMPL",
                                "description": "Viết hàm xử lý sự kiện trong Swift",
                                "bloom_level": "create",
                                "keyword": "func",
                                "platform": "app"
                            }
                        ]
                    }
                ]
            },
            {
                "phase_id": 3,
                "milestones": [
                    {
                        "concept_code": "CONCEPT_C",
                        "learning_objectives": [
                            {
                                "code": "ULO-CONCEPT_C-01",
                                "lo_type": "UNIVERSAL",
                                "description": "Giải thích khái niệm mảng và từ điển trong lập trình",
                                "bloom_level": "understand",
                                "keyword": "",
                                "platform": ""
                            },
                            {
                                "code": "CIO-CONCEPT_C-01",
                                "lo_type": "CONCEPTUAL_IMPL",
                                "description": "Thao tác trên mảng và dictionary",
                                "bloom_level": "apply",
                                "keyword": "",
                                "platform": ""
                            },
                            {
                                "code": "SIO-SWIFT-CONCEPT_C-01",
                                "lo_type": "SPECIFIC_IMPL",
                                "description": "Khởi tạo và làm việc với Array trong Swift",
                                "bloom_level": "create",
                                "keyword": "Array",
                                "platform": "app"
                            }
                        ]
                    }
                ]
            }
        ]
    }


def test_clean_roadmap_pass():
    print("Testing Case 1: Clean roadmap returns PASS...")
    roadmap = make_clean_roadmap()
    res = agent_as_judge.evaluate_roadmap(roadmap)
    assert res["status"] == "PASS", f"Expected PASS, got {res['status']}: {res}"
    assert len(res["issues"]) == 0, f"Expected 0 issues, got {res['issues']}"
    assert len(res["warnings"]) == 0, f"Expected 0 warnings, got {res['warnings']}"
    print("  ✓ Case 1 passed")


def test_needs_review_warn():
    print("Testing Case 2: LO with needs_review=True returns WARN...")
    roadmap = make_clean_roadmap()
    lo = roadmap["phases"][0]["milestones"][0]["learning_objectives"][0]
    lo["needs_review"] = True
    res = agent_as_judge.evaluate_roadmap(roadmap)
    assert res["status"] == "WARN", f"Expected WARN, got {res['status']}: {res}"
    assert len(res["issues"]) == 0, f"Expected 0 issues, got {res['issues']}"
    assert any("ULO-CONCEPT_A-01" in w for w in res["warnings"]), f"Expected ULO-CONCEPT_A-01 in warnings, got {res['warnings']}"
    print("  ✓ Case 2 passed")


def test_template_description_fail():
    print("Testing Case 3: ULO description with template signal returns FAIL...")
    roadmap = make_clean_roadmap()
    lo = roadmap["phases"][0]["milestones"][0]["learning_objectives"][0]
    lo["description"] = "hiểu nguyên lý phổ quát của X"
    res = agent_as_judge.evaluate_roadmap(roadmap)
    assert res["status"] == "FAIL", f"Expected FAIL, got {res['status']}: {res}"
    assert any("ULO-CONCEPT_A-01" in issue for issue in res["issues"]), f"Expected ULO-CONCEPT_A-01 in issues, got {res['issues']}"
    print("  ✓ Case 3 passed")


def test_concept_leak_keyword_fail():
    print("Testing Case 4: SIO keyword 'http protocol' returns FAIL...")
    roadmap = make_clean_roadmap()
    sio = roadmap["phases"][0]["milestones"][0]["learning_objectives"][2]
    sio["keyword"] = "http protocol"
    res = agent_as_judge.evaluate_roadmap(roadmap)
    assert res["status"] == "FAIL", f"Expected FAIL, got {res['status']}: {res}"
    assert any("http protocol" in issue for issue in res["issues"]), f"Expected 'http protocol' in issues, got {res['issues']}"
    print("  ✓ Case 4 passed")


def main():
    test_clean_roadmap_pass()
    test_needs_review_warn()
    test_template_description_fail()
    test_concept_leak_keyword_fail()
    print("ALL ROADMAP JUDGE GATE TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
