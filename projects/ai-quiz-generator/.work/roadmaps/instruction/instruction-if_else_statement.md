# 📖 INSTRUCTION: IF_ELSE_STATEMENT

> **Target Tech:** `PYTHON` | **Concept:** `IF_ELSE_STATEMENT`

## 🎯 1. TỔNG QUAN & MỤC TIÊU SƯ PHẠM
- **Concept:** `IF_ELSE_STATEMENT` — 36 SIO(s) cần thực hiện
- **Mức độ nhận thức:** ULO (hiểu) → CIO (thiết kế) → SIO (viết code + pass tests)

## 🛠️ 2. KHỞI TẠO FILE & CẤU TRÚC THƯ MỤC
- Tạo module/file cho concept `IF_ELSE_STATEMENT` theo cấu trúc dự án hiện tại.

## 💻 3. THỰC THI MÃ NGUỒN
### SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY — If-Else Statement - Implement Library
**Mô tả:** Người học có khả năng build reusable Python library cho if-else statement: API design, type hints, tests, docs, packaging (pyproject.toml).

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK — If-Else Statement - Build Framework
**Mô tả:** Người học có khả năng build framework component cho if-else statement: plugin system, DI container, async runtime, middleware.

**Snippet 1** — `_build_prompt` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
```

**Snippet 2** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
```
from typing import List
from question_bank import Question

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
        # Simplified: in production this calls the LLM API
        return json.dumps([
            {
                "question": f"What is the main concept of {prompt.split('about ')[1].split('.')[0]}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": "This is the correct answer."
            }
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```

**Snippet 3** — `generate_questions` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
```


### SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN — If-Else Statement - Use Pattern
**Mô tả:** Người học có khả năng áp dụng design pattern cho if-else statement: strategy, decorator, context manager, async context manager, protocol.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE — If-Else Statement - Refactor Code
**Mô tả:** Người học có khả năng refactor code sử dụng if-else statement: extract method, introduce parameter object, replace conditional with polymorphism.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY — If-Else Statement - Implement Library
**Mô tả:** Người học có khả năng build reusable Python library cho if-else statement: API design, type hints, tests, docs, packaging (pyproject.toml).

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK — If-Else Statement - Build Framework
**Mô tả:** Người học có khả năng build framework component cho if-else statement: plugin system, DI container, async runtime, middleware.

**Snippet 1** — `_build_prompt` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
```

**Snippet 2** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
```
from typing import List
from question_bank import Question

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
        # Simplified: in production this calls the LLM API
        return json.dumps([
            {
                "question": f"What is the main concept of {prompt.split('about ')[1].split('.')[0]}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": "This is the correct answer."
            }
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```

**Snippet 3** — `generate_questions` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
```


### SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN — If-Else Statement - Use Pattern
**Mô tả:** Người học có khả năng áp dụng design pattern cho if-else statement: strategy, decorator, context manager, async context manager, protocol.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE — If-Else Statement - Refactor Code
**Mô tả:** Người học có khả năng refactor code sử dụng if-else statement: extract method, introduce parameter object, replace conditional with polymorphism.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-IMPLEMENT_LIBRARY — If-Else Statement - Implement Library
**Mô tả:** Người học có khả năng build reusable Python library cho if-else statement: API design, type hints, tests, docs, packaging (pyproject.toml).

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-BUILD_FRAMEWORK — If-Else Statement - Build Framework
**Mô tả:** Người học có khả năng build framework component cho if-else statement: plugin system, DI container, async runtime, middleware.

**Snippet 1** — `_build_prompt` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
```

**Snippet 2** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
```
from typing import List
from question_bank import Question

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
        # Simplified: in production this calls the LLM API
        return json.dumps([
            {
                "question": f"What is the main concept of {prompt.split('about ')[1].split('.')[0]}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": "This is the correct answer."
            }
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```

**Snippet 3** — `generate_questions` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
```


### SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-STATIC_ANALYSIS — If-Else Statement - Static Analysis
**Mô tả:** Người học có khả năng static analysis code liên quan if-else statement: mypy, pyright, ruff, bandit, semgrep, custom AST visitor.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-PERFORMANCE_PROFILE — If-Else Statement - Performance Profile
**Mô tả:** Người học có khả năng profile if-else statement: cProfile, pyinstrument, scalene, memray, line_profiler, identify bottlenecks.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-IMPLEMENT_LIBRARY — If-Else Statement - Implement Library
**Mô tả:** Người học có khả năng build reusable Python library cho if-else statement: API design, type hints, tests, docs, packaging (pyproject.toml).

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-BUILD_FRAMEWORK — If-Else Statement - Build Framework
**Mô tả:** Người học có khả năng build framework component cho if-else statement: plugin system, DI container, async runtime, middleware.

**Snippet 1** — `_build_prompt` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
```

**Snippet 2** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
```
from typing import List
from question_bank import Question

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
        # Simplified: in production this calls the LLM API
        return json.dumps([
            {
                "question": f"What is the main concept of {prompt.split('about ')[1].split('.')[0]}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": "This is the correct answer."
            }
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```

**Snippet 3** — `generate_questions` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
```


### SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-STATIC_ANALYSIS — If-Else Statement - Static Analysis
**Mô tả:** Người học có khả năng static analysis code liên quan if-else statement: mypy, pyright, ruff, bandit, semgrep, custom AST visitor.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-PERFORMANCE_PROFILE — If-Else Statement - Performance Profile
**Mô tả:** Người học có khả năng profile if-else statement: cProfile, pyinstrument, scalene, memray, line_profiler, identify bottlenecks.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-IMPLEMENT_LIBRARY — If-Else Statement - Implement Library
**Mô tả:** Người học có khả năng build reusable Python library cho if-else statement: API design, type hints, tests, docs, packaging (pyproject.toml).

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-BUILD_FRAMEWORK — If-Else Statement - Build Framework
**Mô tả:** Người học có khả năng build framework component cho if-else statement: plugin system, DI container, async runtime, middleware.

**Snippet 1** — `_build_prompt` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
```

**Snippet 2** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
```
from typing import List
from question_bank import Question

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
        # Simplified: in production this calls the LLM API
        return json.dumps([
            {
                "question": f"What is the main concept of {prompt.split('about ')[1].split('.')[0]}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": "This is the correct answer."
            }
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```

**Snippet 3** — `generate_questions` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
```


### SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-USE_PATTERN — If-Else Statement - Use Pattern
**Mô tả:** Người học có khả năng áp dụng design pattern cho if-else statement: strategy, decorator, context manager, async context manager, protocol.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-REFACTOR_CODE — If-Else Statement - Refactor Code
**Mô tả:** Người học có khả năng refactor code sử dụng if-else statement: extract method, introduce parameter object, replace conditional with polymorphism.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-IMPLEMENT_LIBRARY — If-Else Statement - Implement Library
**Mô tả:** Người học có khả năng build reusable Python library cho if-else statement: API design, type hints, tests, docs, packaging (pyproject.toml).

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-BUILD_FRAMEWORK — If-Else Statement - Build Framework
**Mô tả:** Người học có khả năng build framework component cho if-else statement: plugin system, DI container, async runtime, middleware.

**Snippet 1** — `_build_prompt` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
```

**Snippet 2** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
```
from typing import List
from question_bank import Question

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
        # Simplified: in production this calls the LLM API
        return json.dumps([
            {
                "question": f"What is the main concept of {prompt.split('about ')[1].split('.')[0]}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": "This is the correct answer."
            }
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```

**Snippet 3** — `generate_questions` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
```


### SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-USE_PATTERN — If-Else Statement - Use Pattern
**Mô tả:** Người học có khả năng áp dụng design pattern cho if-else statement: strategy, decorator, context manager, async context manager, protocol.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-REFACTOR_CODE — If-Else Statement - Refactor Code
**Mô tả:** Người học có khả năng refactor code sử dụng if-else statement: extract method, introduce parameter object, replace conditional with polymorphism.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-STATIC_ANALYSIS — If-Else Statement - Static Analysis
**Mô tả:** Người học có khả năng static analysis code liên quan if-else statement: mypy, pyright, ruff, bandit, semgrep, custom AST visitor.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-PERFORMANCE_PROFILE — If-Else Statement - Performance Profile
**Mô tả:** Người học có khả năng profile if-else statement: cProfile, pyinstrument, scalene, memray, line_profiler, identify bottlenecks.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-STATIC_ANALYSIS — If-Else Statement - Static Analysis
**Mô tả:** Người học có khả năng static analysis code liên quan if-else statement: mypy, pyright, ruff, bandit, semgrep, custom AST visitor.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-PERFORMANCE_PROFILE — If-Else Statement - Performance Profile
**Mô tả:** Người học có khả năng profile if-else statement: cProfile, pyinstrument, scalene, memray, line_profiler, identify bottlenecks.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-STATIC_ANALYSIS — If-Else Statement - Static Analysis
**Mô tả:** Người học có khả năng static analysis code liên quan if-else statement: mypy, pyright, ruff, bandit, semgrep, custom AST visitor.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-PERFORMANCE_PROFILE — If-Else Statement - Performance Profile
**Mô tả:** Người học có khả năng profile if-else statement: cProfile, pyinstrument, scalene, memray, line_profiler, identify bottlenecks.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-STATIC_ANALYSIS — If-Else Statement - Static Analysis
**Mô tả:** Người học có khả năng static analysis code liên quan if-else statement: mypy, pyright, ruff, bandit, semgrep, custom AST visitor.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-PERFORMANCE_PROFILE — If-Else Statement - Performance Profile
**Mô tả:** Người học có khả năng profile if-else statement: cProfile, pyinstrument, scalene, memray, line_profiler, identify bottlenecks.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY — If-Else Statement - Implement Library
**Mô tả:** Người học có khả năng build reusable Python library cho if-else statement: API design, type hints, tests, docs, packaging (pyproject.toml).

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK — If-Else Statement - Build Framework
**Mô tả:** Người học có khả năng build framework component cho if-else statement: plugin system, DI container, async runtime, middleware.

**Snippet 1** — `_build_prompt` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
```

**Snippet 2** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
```
from typing import List
from question_bank import Question

class QuizGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
        return (
            f"Create {num} multiple-choice questions about {topic}. "
            "Return JSON array with fields: question, options (4), correct_index, explanation."
        )

    def _call_llm(self, prompt: str) -> str:
        # Simplified: in production this calls the LLM API
        return json.dumps([
            {
                "question": f"What is the main concept of {prompt.split('about ')[1].split('.')[0]}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_index": 0,
                "explanation": "This is the correct answer."
            }
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```

**Snippet 3** — `generate_questions` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        self.model = os.getenv("QUIZ_MODEL", "gpt-4o-mini")

    def generate_questions(self, topic: str, num: int = 5) -> List[Question]:
        """Generate multiple-choice questions for a topic using LLM."""
        prompt = self._build_prompt(topic, num)
        response = self._call_llm(prompt)
        return self._parse_response(response)

    def _build_prompt(self, topic: str, num: int) -> str:
```


### SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN — If-Else Statement - Use Pattern
**Mô tả:** Người học có khả năng áp dụng design pattern cho if-else statement: strategy, decorator, context manager, async context manager, protocol.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE — If-Else Statement - Refactor Code
**Mô tả:** Người học có khả năng refactor code sử dụng if-else statement: extract method, introduce parameter object, replace conditional with polymorphism.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


## 🚨 4. XỬ LÝ LỖI & PHÒNG NGỪA NGOẠI LỆ
- Luôn bọc I/O trong error handling (do-catch / Result type / try-catch).
- Xử lý edge cases: dữ liệu rỗng, null/nil, timeout, mất kết nối.

## 🧪 5. VIẾT KỊCH BẢN KIỂM THỬ TỰ ĐỘNG
- Viết unit test cho từng SIO của concept `IF_ELSE_STATEMENT`.
- Test happy path + error path + edge cases.

## 🔍 6. BẮT LỖI PHỔ BIẾN & HƯỚNG DẪN DEBUG
**SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-IMPLEMENT_LIBRARY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-BUILD_FRAMEWORK:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-STATIC_ANALYSIS:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-PERFORMANCE_PROFILE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-IMPLEMENT_LIBRARY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-BUILD_FRAMEWORK:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-STATIC_ANALYSIS:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-PERFORMANCE_PROFILE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-IMPLEMENT_LIBRARY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-BUILD_FRAMEWORK:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-USE_PATTERN:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-REFACTOR_CODE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-IMPLEMENT_LIBRARY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-BUILD_FRAMEWORK:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-USE_PATTERN:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-REFACTOR_CODE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-STATIC_ANALYSIS:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-PERFORMANCE_PROFILE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-STATIC_ANALYSIS:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-PERFORMANCE_PROFILE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-STATIC_ANALYSIS:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-PERFORMANCE_PROFILE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-STATIC_ANALYSIS:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-PERFORMANCE_PROFILE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

## 📋 7. CHECKLIST NHIỆM VỤ NGUYÊN TỬ
- [ ] **TASK_1** — `SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY`: If-Else Statement - Implement Library (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_2** — `SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK`: If-Else Statement - Build Framework (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_3** — `SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN`: If-Else Statement - Use Pattern (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_4** — `SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE`: If-Else Statement - Refactor Code (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_5** — `SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY`: If-Else Statement - Implement Library (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_6** — `SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK`: If-Else Statement - Build Framework (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_7** — `SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN`: If-Else Statement - Use Pattern (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_8** — `SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE`: If-Else Statement - Refactor Code (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_9** — `SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-IMPLEMENT_LIBRARY`: If-Else Statement - Implement Library (prereq: CIO-IF_ELSE_STATEMENT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_10** — `SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-BUILD_FRAMEWORK`: If-Else Statement - Build Framework (prereq: CIO-IF_ELSE_STATEMENT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_11** — `SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-STATIC_ANALYSIS`: If-Else Statement - Static Analysis (prereq: CIO-IF_ELSE_STATEMENT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_12** — `SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-PERFORMANCE_PROFILE`: If-Else Statement - Performance Profile (prereq: CIO-IF_ELSE_STATEMENT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_13** — `SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-IMPLEMENT_LIBRARY`: If-Else Statement - Implement Library (prereq: CIO-IF_ELSE_STATEMENT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_14** — `SIO-PYTHON-IF_ELSE_STATEMENT-EXPLAIN_MECHANISM-BUILD_FRAMEWORK`: If-Else Statement - Build Framework (prereq: CIO-IF_ELSE_STATEMENT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_15** — `SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-STATIC_ANALYSIS`: If-Else Statement - Static Analysis (prereq: CIO-IF_ELSE_STATEMENT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_16** — `SIO-PYTHON-IF_ELSE_STATEMENT-INTERPRET_PARAMETERS-PERFORMANCE_PROFILE`: If-Else Statement - Performance Profile (prereq: CIO-IF_ELSE_STATEMENT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_17** — `SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-IMPLEMENT_LIBRARY`: If-Else Statement - Implement Library (prereq: CIO-IF_ELSE_STATEMENT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_18** — `SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-BUILD_FRAMEWORK`: If-Else Statement - Build Framework (prereq: CIO-IF_ELSE_STATEMENT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_19** — `SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-USE_PATTERN`: If-Else Statement - Use Pattern (prereq: CIO-IF_ELSE_STATEMENT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_20** — `SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-REFACTOR_CODE`: If-Else Statement - Refactor Code (prereq: CIO-IF_ELSE_STATEMENT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_21** — `SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-IMPLEMENT_LIBRARY`: If-Else Statement - Implement Library (prereq: CIO-IF_ELSE_STATEMENT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_22** — `SIO-PYTHON-IF_ELSE_STATEMENT-IMPLEMENT_PATTERN-BUILD_FRAMEWORK`: If-Else Statement - Build Framework (prereq: CIO-IF_ELSE_STATEMENT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_23** — `SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-USE_PATTERN`: If-Else Statement - Use Pattern (prereq: CIO-IF_ELSE_STATEMENT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_24** — `SIO-PYTHON-IF_ELSE_STATEMENT-ADAPT_TO_CONTEXT-REFACTOR_CODE`: If-Else Statement - Refactor Code (prereq: CIO-IF_ELSE_STATEMENT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_25** — `SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-STATIC_ANALYSIS`: If-Else Statement - Static Analysis (prereq: CIO-IF_ELSE_STATEMENT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_26** — `SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-PERFORMANCE_PROFILE`: If-Else Statement - Performance Profile (prereq: CIO-IF_ELSE_STATEMENT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_27** — `SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-STATIC_ANALYSIS`: If-Else Statement - Static Analysis (prereq: CIO-IF_ELSE_STATEMENT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_28** — `SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-PERFORMANCE_PROFILE`: If-Else Statement - Performance Profile (prereq: CIO-IF_ELSE_STATEMENT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_29** — `SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-STATIC_ANALYSIS`: If-Else Statement - Static Analysis (prereq: CIO-IF_ELSE_STATEMENT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_30** — `SIO-PYTHON-IF_ELSE_STATEMENT-DECOMPOSE_TRADEOFFS-PERFORMANCE_PROFILE`: If-Else Statement - Performance Profile (prereq: CIO-IF_ELSE_STATEMENT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_31** — `SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-STATIC_ANALYSIS`: If-Else Statement - Static Analysis (prereq: CIO-IF_ELSE_STATEMENT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_32** — `SIO-PYTHON-IF_ELSE_STATEMENT-COMPARE_ALTERNATIVES-PERFORMANCE_PROFILE`: If-Else Statement - Performance Profile (prereq: CIO-IF_ELSE_STATEMENT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_33** — `SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-IMPLEMENT_LIBRARY`: If-Else Statement - Implement Library (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_34** — `SIO-PYTHON-IF_ELSE_STATEMENT-IDENTIFY_COMPONENTS-BUILD_FRAMEWORK`: If-Else Statement - Build Framework (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_35** — `SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-USE_PATTERN`: If-Else Statement - Use Pattern (prereq: CIO-IF_ELSE_STATEMENT-01)
- [ ] **TASK_36** — `SIO-PYTHON-IF_ELSE_STATEMENT-RECALL_DEFINITIONS-REFACTOR_CODE`: If-Else Statement - Refactor Code (prereq: CIO-IF_ELSE_STATEMENT-01)

## 🏁 8. DEFINITION OF DONE
- [ ] Code module hoạt động hoàn chỉnh.
- [ ] Unit tests pass.
- [ ] Git commit với message rõ ràng.
