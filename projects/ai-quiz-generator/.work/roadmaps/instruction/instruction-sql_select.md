# 📖 INSTRUCTION: SQL_SELECT

> **Target Tech:** `PYTHON` | **Concept:** `SQL_SELECT`

## 🎯 1. TỔNG QUAN & MỤC TIÊU SƯ PHẠM
- **Concept:** `SQL_SELECT` — 32 SIO(s) cần thực hiện
- **Mức độ nhận thức:** ULO (hiểu) → CIO (thiết kế) → SIO (viết code + pass tests)

## 🛠️ 2. KHỞI TẠO FILE & CẤU TRÚC THƯ MỤC
- Tạo module/file cho concept `SQL_SELECT` theo cấu trúc dự án hiện tại.

## 💻 3. THỰC THI MÃ NGUỒN
### SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_PIPELINE — SQL SELECT Statement - Build Pipeline
**Mô tả:** Người học có khả năng build data pipeline cho sql select statement: Airflow/Dagster/Prefect DAG, task dependencies, retries, SLA, data quality gates.

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


### SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_MODEL — SQL SELECT Statement - Build Model
**Mô tả:** Người học có khả năng train ML model cho sql select statement: feature store, experiment tracking (MLflow), model registry, serving (FastAPI/BentoML).

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

**Snippet 2** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
```

**Snippet 3** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
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


### SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-QUERY_DATA — SQL SELECT Statement - Query Data
**Mô tả:** Người học có khả năng query sql select statement: SQLAlchemy/DuckDB/Polars, parameterized queries, connection pooling, pagination.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-TRANSFORM_DATA — SQL SELECT Statement - Transform Data
**Mô tả:** Người học có khả năng transform sql select statement: Pandas/Polars/Spark, type casting, pivot, window functions, UDF, vectorized ops.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_PIPELINE — SQL SELECT Statement - Build Pipeline
**Mô tả:** Người học có khả năng build data pipeline cho sql select statement: Airflow/Dagster/Prefect DAG, task dependencies, retries, SLA, data quality gates.

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


### SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_MODEL — SQL SELECT Statement - Build Model
**Mô tả:** Người học có khả năng train ML model cho sql select statement: feature store, experiment tracking (MLflow), model registry, serving (FastAPI/BentoML).

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

**Snippet 2** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
```

**Snippet 3** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
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


### SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-QUERY_DATA — SQL SELECT Statement - Query Data
**Mô tả:** Người học có khả năng query sql select statement: SQLAlchemy/DuckDB/Polars, parameterized queries, connection pooling, pagination.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-TRANSFORM_DATA — SQL SELECT Statement - Transform Data
**Mô tả:** Người học có khả năng transform sql select statement: Pandas/Polars/Spark, type casting, pivot, window functions, UDF, vectorized ops.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_PIPELINE — SQL SELECT Statement - Build Pipeline
**Mô tả:** Người học có khả năng build data pipeline cho sql select statement: Airflow/Dagster/Prefect DAG, task dependencies, retries, SLA, data quality gates.

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


### SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_MODEL — SQL SELECT Statement - Build Model
**Mô tả:** Người học có khả năng train ML model cho sql select statement: feature store, experiment tracking (MLflow), model registry, serving (FastAPI/BentoML).

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

**Snippet 2** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
```

**Snippet 3** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
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


### SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-PROFILE_DATA — SQL SELECT Statement - Profile Data
**Mô tả:** Người học có khả năng profile sql select statement: ydata-profiling, Great Expectations, schema validation, anomaly detection, data lineage.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-OPTIMIZE_QUERY — SQL SELECT Statement - Optimize Query
**Mô tả:** Người học có khả năng optimize query cho sql select statement: EXPLAIN ANALYZE, index design, partition pruning, materialized view, caching.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_PIPELINE — SQL SELECT Statement - Build Pipeline
**Mô tả:** Người học có khả năng build data pipeline cho sql select statement: Airflow/Dagster/Prefect DAG, task dependencies, retries, SLA, data quality gates.

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


### SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_MODEL — SQL SELECT Statement - Build Model
**Mô tả:** Người học có khả năng train ML model cho sql select statement: feature store, experiment tracking (MLflow), model registry, serving (FastAPI/BentoML).

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

**Snippet 2** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
```

**Snippet 3** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
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


### SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-PROFILE_DATA — SQL SELECT Statement - Profile Data
**Mô tả:** Người học có khả năng profile sql select statement: ydata-profiling, Great Expectations, schema validation, anomaly detection, data lineage.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-OPTIMIZE_QUERY — SQL SELECT Statement - Optimize Query
**Mô tả:** Người học có khả năng optimize query cho sql select statement: EXPLAIN ANALYZE, index design, partition pruning, materialized view, caching.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_PIPELINE — SQL SELECT Statement - Build Pipeline
**Mô tả:** Người học có khả năng build data pipeline cho sql select statement: Airflow/Dagster/Prefect DAG, task dependencies, retries, SLA, data quality gates.

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


### SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_MODEL — SQL SELECT Statement - Build Model
**Mô tả:** Người học có khả năng train ML model cho sql select statement: feature store, experiment tracking (MLflow), model registry, serving (FastAPI/BentoML).

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

**Snippet 2** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
```

**Snippet 3** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
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


### SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-QUERY_DATA — SQL SELECT Statement - Query Data
**Mô tả:** Người học có khả năng query sql select statement: SQLAlchemy/DuckDB/Polars, parameterized queries, connection pooling, pagination.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-TRANSFORM_DATA — SQL SELECT Statement - Transform Data
**Mô tả:** Người học có khả năng transform sql select statement: Pandas/Polars/Spark, type casting, pivot, window functions, UDF, vectorized ops.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_PIPELINE — SQL SELECT Statement - Build Pipeline
**Mô tả:** Người học có khả năng build data pipeline cho sql select statement: Airflow/Dagster/Prefect DAG, task dependencies, retries, SLA, data quality gates.

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


### SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_MODEL — SQL SELECT Statement - Build Model
**Mô tả:** Người học có khả năng train ML model cho sql select statement: feature store, experiment tracking (MLflow), model registry, serving (FastAPI/BentoML).

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

**Snippet 2** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
```

**Snippet 3** — `QuizGenerator` (class, /tmp/ai-quiz-generator/quiz_generator.py):
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


### SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-QUERY_DATA — SQL SELECT Statement - Query Data
**Mô tả:** Người học có khả năng query sql select statement: SQLAlchemy/DuckDB/Polars, parameterized queries, connection pooling, pagination.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-TRANSFORM_DATA — SQL SELECT Statement - Transform Data
**Mô tả:** Người học có khả năng transform sql select statement: Pandas/Polars/Spark, type casting, pivot, window functions, UDF, vectorized ops.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-PROFILE_DATA — SQL SELECT Statement - Profile Data
**Mô tả:** Người học có khả năng profile sql select statement: ydata-profiling, Great Expectations, schema validation, anomaly detection, data lineage.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-OPTIMIZE_QUERY — SQL SELECT Statement - Optimize Query
**Mô tả:** Người học có khả năng optimize query cho sql select statement: EXPLAIN ANALYZE, index design, partition pruning, materialized view, caching.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-PROFILE_DATA — SQL SELECT Statement - Profile Data
**Mô tả:** Người học có khả năng profile sql select statement: ydata-profiling, Great Expectations, schema validation, anomaly detection, data lineage.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-OPTIMIZE_QUERY — SQL SELECT Statement - Optimize Query
**Mô tả:** Người học có khả năng optimize query cho sql select statement: EXPLAIN ANALYZE, index design, partition pruning, materialized view, caching.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-PROFILE_DATA — SQL SELECT Statement - Profile Data
**Mô tả:** Người học có khả năng profile sql select statement: ydata-profiling, Great Expectations, schema validation, anomaly detection, data lineage.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-OPTIMIZE_QUERY — SQL SELECT Statement - Optimize Query
**Mô tả:** Người học có khả năng optimize query cho sql select statement: EXPLAIN ANALYZE, index design, partition pruning, materialized view, caching.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


### SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-PROFILE_DATA — SQL SELECT Statement - Profile Data
**Mô tả:** Người học có khả năng profile sql select statement: ydata-profiling, Great Expectations, schema validation, anomaly detection, data lineage.

**Snippet 1** — `Config` (class, /tmp/ai-quiz-generator/config.py):
```
"""Configuration for the AI Quiz Generator."""
import os

class Config:
    API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("QUIZ_MODEL", "gpt-4o-mini")
    DEFAULT_QUESTIONS = 5
    SUPPORTED_TOPICS = ["python", "machine learning", "data structures", "algorithms"]
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

**Snippet 3** — `_parse_response` (function, /tmp/ai-quiz-generator/quiz_generator.py):
```
        ])

    def _parse_response(self, response: str) -> List[Question]:
        data = json.loads(response)
        return [Question(**item) for item in data]
```


### SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-OPTIMIZE_QUERY — SQL SELECT Statement - Optimize Query
**Mô tả:** Người học có khả năng optimize query cho sql select statement: EXPLAIN ANALYZE, index design, partition pruning, materialized view, caching.

> ⚠️ Không có code snippet thực từ repository cho SIO này. Tham khảo tài liệu chính thức của framework/API tương ứng.


## 🚨 4. XỬ LÝ LỖI & PHÒNG NGỪA NGOẠI LỆ
- Luôn bọc I/O trong error handling (do-catch / Result type / try-catch).
- Xử lý edge cases: dữ liệu rỗng, null/nil, timeout, mất kết nối.

## 🧪 5. VIẾT KỊCH BẢN KIỂM THỬ TỰ ĐỘNG
- Viết unit test cho từng SIO của concept `SQL_SELECT`.
- Test happy path + error path + edge cases.

## 🔍 6. BẮT LỖI PHỔ BIẾN & HƯỚNG DẪN DEBUG
**SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_PIPELINE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_MODEL:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-QUERY_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Network timeout / connection lost | Thiếu retry/backoff, timeout quá ngắn | Thêm exponential backoff + timeout handling |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-TRANSFORM_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_PIPELINE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_MODEL:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-QUERY_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Network timeout / connection lost | Thiếu retry/backoff, timeout quá ngắn | Thêm exponential backoff + timeout handling |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-TRANSFORM_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_PIPELINE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_MODEL:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-PROFILE_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-OPTIMIZE_QUERY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_PIPELINE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_MODEL:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-PROFILE_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-OPTIMIZE_QUERY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_PIPELINE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_MODEL:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-QUERY_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Network timeout / connection lost | Thiếu retry/backoff, timeout quá ngắn | Thêm exponential backoff + timeout handling |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-TRANSFORM_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_PIPELINE:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |
| Race condition / data race | Shared mutable state truy cập đồng thời | Dùng actor / serial queue / lock |

**SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_MODEL:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-QUERY_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Network timeout / connection lost | Thiếu retry/backoff, timeout quá ngắn | Thêm exponential backoff + timeout handling |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-TRANSFORM_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-PROFILE_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-OPTIMIZE_QUERY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-PROFILE_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-OPTIMIZE_QUERY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-PROFILE_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-OPTIMIZE_QUERY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

**SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-PROFILE_DATA:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |
| Decode/parse lỗi | Schema mismatch giữa client và server | Kiểm tra Codable/JSON schema, thêm error mapping |

**SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-OPTIMIZE_QUERY:**
| Lỗi Thường Gặp | Nguyên Nhân | Cách Sửa |
| :--- | :--- | :--- |
| State không cập nhật UI | Mutation state trên background thread / thiếu @MainActor | Dispatch về main thread hoặc dùng @MainActor |

## 📋 7. CHECKLIST NHIỆM VỤ NGUYÊN TỬ
- [ ] **TASK_1** — `SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_PIPELINE`: SQL SELECT Statement - Build Pipeline (prereq: CIO-SQL_SELECT-01-RECALL_DEFINITIONS)
- [ ] **TASK_2** — `SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_MODEL`: SQL SELECT Statement - Build Model (prereq: CIO-SQL_SELECT-01-RECALL_DEFINITIONS)
- [ ] **TASK_3** — `SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-QUERY_DATA`: SQL SELECT Statement - Query Data (prereq: CIO-SQL_SELECT-01-RECALL_DEFINITIONS)
- [ ] **TASK_4** — `SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-TRANSFORM_DATA`: SQL SELECT Statement - Transform Data (prereq: CIO-SQL_SELECT-01-RECALL_DEFINITIONS)
- [ ] **TASK_5** — `SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_PIPELINE`: SQL SELECT Statement - Build Pipeline (prereq: CIO-SQL_SELECT-01-RECALL_DEFINITIONS)
- [ ] **TASK_6** — `SIO-PYTHON-SQL_SELECT-IDENTIFY_COMPONENTS-BUILD_MODEL`: SQL SELECT Statement - Build Model (prereq: CIO-SQL_SELECT-01-RECALL_DEFINITIONS)
- [ ] **TASK_7** — `SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-QUERY_DATA`: SQL SELECT Statement - Query Data (prereq: CIO-SQL_SELECT-01-RECALL_DEFINITIONS)
- [ ] **TASK_8** — `SIO-PYTHON-SQL_SELECT-RECALL_DEFINITIONS-TRANSFORM_DATA`: SQL SELECT Statement - Transform Data (prereq: CIO-SQL_SELECT-01-RECALL_DEFINITIONS)
- [ ] **TASK_9** — `SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_PIPELINE`: SQL SELECT Statement - Build Pipeline (prereq: CIO-SQL_SELECT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_10** — `SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_MODEL`: SQL SELECT Statement - Build Model (prereq: CIO-SQL_SELECT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_11** — `SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-PROFILE_DATA`: SQL SELECT Statement - Profile Data (prereq: CIO-SQL_SELECT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_12** — `SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-OPTIMIZE_QUERY`: SQL SELECT Statement - Optimize Query (prereq: CIO-SQL_SELECT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_13** — `SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_PIPELINE`: SQL SELECT Statement - Build Pipeline (prereq: CIO-SQL_SELECT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_14** — `SIO-PYTHON-SQL_SELECT-EXPLAIN_MECHANISM-BUILD_MODEL`: SQL SELECT Statement - Build Model (prereq: CIO-SQL_SELECT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_15** — `SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-PROFILE_DATA`: SQL SELECT Statement - Profile Data (prereq: CIO-SQL_SELECT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_16** — `SIO-PYTHON-SQL_SELECT-INTERPRET_PARAMETERS-OPTIMIZE_QUERY`: SQL SELECT Statement - Optimize Query (prereq: CIO-SQL_SELECT-02-INTERPRET_PARAMETERS)
- [ ] **TASK_17** — `SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_PIPELINE`: SQL SELECT Statement - Build Pipeline (prereq: CIO-SQL_SELECT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_18** — `SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_MODEL`: SQL SELECT Statement - Build Model (prereq: CIO-SQL_SELECT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_19** — `SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-QUERY_DATA`: SQL SELECT Statement - Query Data (prereq: CIO-SQL_SELECT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_20** — `SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-TRANSFORM_DATA`: SQL SELECT Statement - Transform Data (prereq: CIO-SQL_SELECT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_21** — `SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_PIPELINE`: SQL SELECT Statement - Build Pipeline (prereq: CIO-SQL_SELECT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_22** — `SIO-PYTHON-SQL_SELECT-IMPLEMENT_PATTERN-BUILD_MODEL`: SQL SELECT Statement - Build Model (prereq: CIO-SQL_SELECT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_23** — `SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-QUERY_DATA`: SQL SELECT Statement - Query Data (prereq: CIO-SQL_SELECT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_24** — `SIO-PYTHON-SQL_SELECT-ADAPT_TO_CONTEXT-TRANSFORM_DATA`: SQL SELECT Statement - Transform Data (prereq: CIO-SQL_SELECT-03-ADAPT_TO_CONTEXT)
- [ ] **TASK_25** — `SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-PROFILE_DATA`: SQL SELECT Statement - Profile Data (prereq: CIO-SQL_SELECT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_26** — `SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-OPTIMIZE_QUERY`: SQL SELECT Statement - Optimize Query (prereq: CIO-SQL_SELECT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_27** — `SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-PROFILE_DATA`: SQL SELECT Statement - Profile Data (prereq: CIO-SQL_SELECT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_28** — `SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-OPTIMIZE_QUERY`: SQL SELECT Statement - Optimize Query (prereq: CIO-SQL_SELECT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_29** — `SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-PROFILE_DATA`: SQL SELECT Statement - Profile Data (prereq: CIO-SQL_SELECT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_30** — `SIO-PYTHON-SQL_SELECT-DECOMPOSE_TRADEOFFS-OPTIMIZE_QUERY`: SQL SELECT Statement - Optimize Query (prereq: CIO-SQL_SELECT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_31** — `SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-PROFILE_DATA`: SQL SELECT Statement - Profile Data (prereq: CIO-SQL_SELECT-04-COMPARE_ALTERNATIVES)
- [ ] **TASK_32** — `SIO-PYTHON-SQL_SELECT-COMPARE_ALTERNATIVES-OPTIMIZE_QUERY`: SQL SELECT Statement - Optimize Query (prereq: CIO-SQL_SELECT-04-COMPARE_ALTERNATIVES)

## 🏁 8. DEFINITION OF DONE
- [ ] Code module hoạt động hoàn chỉnh.
- [ ] Unit tests pass.
- [ ] Git commit với message rõ ràng.
