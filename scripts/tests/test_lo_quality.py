"""test_lo_quality.py - Unit tests for scripts/lo_quality.py using pure Python assertions.
"""

import sys
import os

# Add scripts directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import lo_quality


def test_export_counts():
    print("Testing export counts...")
    assert len(lo_quality.TEMPLATE_CIO_VERBS) == 12, f"Expected 12 verbs, got {len(lo_quality.TEMPLATE_CIO_VERBS)}"
    assert len(lo_quality.TEMPLATE_DESC_SIGNALS) >= 20, f"Expected >=20 signals, got {len(lo_quality.TEMPLATE_DESC_SIGNALS)}"
    assert len(lo_quality.GENERIC_KEYWORDS) == 15, f"Expected 15 keywords, got {len(lo_quality.GENERIC_KEYWORDS)}"


def test_template_cio_verbs():
    print("Testing template CIO verbs...")
    for verb in lo_quality.TEMPLATE_CIO_VERBS:
        code = f"CIO-CONCEPT-01-{verb}"
        assert lo_quality.is_template_cio_code(code) is True, f"Failed for verb {verb} with code {code}"

    # Test non-template code
    assert lo_quality.is_template_cio_code("CIO-FOR_LOOP-01-CUSTOM_VERB") is False
    assert lo_quality.is_template_cio_code("") is False


def test_is_template_description():
    print("Testing is_template_description...")
    # ULO signals
    assert lo_quality.is_template_description("người học có khả năng hiểu nguyên lý phổ quát", layer="ULO") is True
    assert lo_quality.is_template_description("hiểu: hiểu cách hoạt động", layer="ULO") is True

    # CIO signals
    assert lo_quality.is_template_description("đánh giá ngưỡng hiệu năng", layer="CIO") is True
    assert lo_quality.is_template_description("mô hình tham chiếu hệ thống", layer="CIO") is True

    # Check layer specificity: ULO-specific signal in CIO layer should not trigger layer='CIO' check
    assert lo_quality.is_template_description("nguyên lý phổ quát", layer="CIO") is False

    # Layer='' checks all signals
    assert lo_quality.is_template_description("nguyên lý phổ quát", layer="") is True
    assert lo_quality.is_template_description("đánh giá ngưỡng hiệu năng", layer="") is True

    # Clean non-template description
    assert lo_quality.is_template_description("Giải thích cách sử dụng vòng lặp for trong Swift", layer="") is False


def test_generic_keywords():
    print("Testing generic keywords...")
    assert "loop" in lo_quality.GENERIC_KEYWORDS
    assert "state" in lo_quality.GENERIC_KEYWORDS
    assert "server" in lo_quality.GENERIC_KEYWORDS

    assert lo_quality.is_generic_keyword("loop") is True
    assert lo_quality.is_generic_keyword("SERVER") is True
    assert lo_quality.is_generic_keyword("swift") is False


def test_clean_llm_description():
    print("Testing clean_llm_description...")
    # Test duplicate "hiểu" prefix
    desc_dup = "hiểu For Loop: Hiểu cách hoạt động của vòng lặp"
    cleaned_dup = lo_quality.clean_llm_description(desc_dup, "For Loop")
    assert cleaned_dup == "Hiểu cách hoạt động của vòng lặp", f"Got: '{cleaned_dup}'"

    # Test markdown fence
    desc_fence = "```markdown\nHiểu nguyên lý bộ nhớ Stack\n```"
    cleaned_fence = lo_quality.clean_llm_description(desc_fence, "Stack")
    assert cleaned_fence == "Hiểu nguyên lý bộ nhớ Stack", f"Got: '{cleaned_fence}'"

    # Test clean description kept intact
    desc_clean = "Giải thích cách quản lý bộ nhớ ARC trong Swift"
    cleaned_clean = lo_quality.clean_llm_description(desc_clean, "ARC")
    assert cleaned_clean == desc_clean, f"Got: '{cleaned_clean}'"


def test_build_lo_desc():
    print("Testing build_lo_desc...")
    # Empty source_desc -> needs_review=True
    desc_ulo, review_ulo = lo_quality.build_lo_desc("ULO", "C01", "For Loop", "")
    assert review_ulo is True
    assert desc_ulo == "Người học có khả năng hiểu For Loop trong ngữ cảnh dự án."

    desc_cio, review_cio = lo_quality.build_lo_desc("CIO", "C01", "For Loop", "")
    assert review_cio is True
    assert desc_cio == "Người học có khả năng vận dụng For Loop ở mức mô hình trong dự án."

    desc_sio, review_sio = lo_quality.build_lo_desc("SIO", "C01", "For Loop", "", keyword="for", platform="Swift")
    assert review_sio is True
    assert desc_sio == "Người học có khả năng triển khai For Loop dùng 'for' trong Swift."

    # Non-empty valid source_desc -> needs_review=False
    valid_source = "Cung cấp cú pháp lặp qua các phần tử mảng."
    desc_valid, review_valid = lo_quality.build_lo_desc("ULO", "C01", "For Loop", valid_source)
    assert review_valid is False
    assert desc_valid == "Người học có khả năng hiểu For Loop: Cung cấp cú pháp lặp qua các phần tử mảng."

    # Forbidden strings check: build_lo_desc output must NEVER contain forbidden strings
    forbidden_source = "Hiểu nguyên lý phổ quát và cách vận dụng nó trong vai trò của nó trong thiết kế"
    desc_forbidden, review_forbidden = lo_quality.build_lo_desc("ULO", "C01", "For Loop", forbidden_source)
    assert review_forbidden is True
    for forbidden in lo_quality.FORBIDDEN_STRINGS:
        assert forbidden not in desc_forbidden, f"Forbidden string '{forbidden}' found in build_lo_desc output: '{desc_forbidden}'"


def main():
    test_export_counts()
    test_template_cio_verbs()
    test_is_template_description()
    test_generic_keywords()
    test_clean_llm_description()
    test_build_lo_desc()
    print("ALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
