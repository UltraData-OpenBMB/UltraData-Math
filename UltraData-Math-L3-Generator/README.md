# UltraData-Math-L3-Generator

<div align="center">

[🇨🇳 中文 README](README_ZH.md)

</div>

L3 Synthetic Data Layer: a multi-format mathematical data synthesis tool powered by LLMs.

## 📂 Directory Structure

```
UltraData-Math-L3-Generator/
├── run_synthesis.py                 # OpenAI API invocation script
├── qa_synthesis.py                  # Q&A pair synthesis prompt
├── conversation_synthesis.py        # Multi-turn conversation synthesis prompt
├── multistyle_rewrite.py           # Multi-style rewriting prompt
├── knowledge_textbook.py           # Knowledge extraction + textbook exercise prompt
└── README.md
```

## 🔧 Install Dependencies

```bash
pip install openai
```

## 🚀 Quick Start

### Environment Setup

```bash
# Set API Key
export OPENAI_API_KEY="your-api-key"

# Optional: Set a custom API endpoint (OpenAI-compatible APIs)
export OPENAI_BASE_URL="https://your-api-endpoint/v1"
```

### Basic Usage

```bash
python run_synthesis.py \
    --input data.jsonl \
    --output output.jsonl \
    --task qa \
    --level high_school \
    --model gpt-4o \
    --workers 10
```

## 📋 Task Types

### 1. Q&A Pair Synthesis (`qa`)

Generate question-answer pairs from mathematical content, categorized by educational difficulty level.

**Parameter `--level`:**
| Value | Description |
|:---|:---|
| `grade_school` | Grade school |
| `middle_school` | Middle school |
| `high_school` | High school (default) |
| `college` | College |

```bash
python run_synthesis.py -i data.jsonl -o output.jsonl -t qa --level high_school
```

### 2. Multi-turn Conversation Synthesis (`conversation`)

Convert mathematical content into multi-turn dialogue format.

**Parameter `--style`:**
| Value | Description |
|:---|:---|
| `two_professors` | Conversation between two professors |
| `teacher_student` | Teacher-student dialogue (default) |
| `two_students` | Conversation between two students |
| `interview` | Interview style |
| `problem_solving` | Problem-solving style |
| `layman_expert` | Layman and expert |
| `debate` | Debate style |

```bash
python run_synthesis.py -i data.jsonl -o output.jsonl -t conversation --style teacher_student
```

### 3. Multi-style Rewriting (`rewrite`)

Rewrite mathematical content in various styles.

**Parameter `--style`:**
| Value | Description |
|:---|:---|
| `wikipedia` | Wikipedia style |
| `textbook` | Textbook style (default) |
| `blog` | Blog style |
| `popular_science` | Popular science style |
| `academic_paper` | Academic paper style |
| `learning_note` | Learning notes style |
| `lecture_note` | Lecture notes style |

```bash
python run_synthesis.py -i data.jsonl -o output.jsonl -t rewrite --style textbook
```

### 4. Knowledge Point Extraction (`knowledge`)

Extract definitions, theorems, properties, and other knowledge points from mathematical content.

```bash
python run_synthesis.py -i data.jsonl -o knowledge_output.jsonl -t knowledge
```

### 5. Textbook Exercise Generation (`textbook`)

Generate textbook-style exercises at varying difficulty levels based on knowledge points.

**Parameter `--difficulty`:**
| Value | Description |
|:---|:---|
| `easy` | Easy (default) |
| `medium` | Medium |
| `hard` | Hard |

```bash
python run_synthesis.py -i knowledge.jsonl -o output.jsonl -t textbook --difficulty medium
```

**Note:** The input file must contain a `knowledge_point` field (customizable via `--knowledge-field`).

## ⚙️ Parameters

| Parameter | Description | Default |
|:---|:---|:---|
| `-i, --input` | Input JSONL file path | Required |
| `-o, --output` | Output JSONL file path | Required |
| `-t, --task` | Task type: `qa`, `conversation`, `rewrite`, `knowledge`, `textbook` | Required |
| `--level` | Q&A difficulty level | `high_school` |
| `--style` | Conversation/rewrite style | - |
| `--difficulty` | Textbook exercise difficulty | `easy` |
| `--text-field` | Input text field name | `text` |
| `--knowledge-field` | Knowledge point field name | `knowledge_point` |
| `--api-key` | OpenAI API Key | Environment variable |
| `--base-url` | API Base URL | Environment variable |
| `--model` | Model name | `gpt-4o` |
| `--temperature` | Sampling temperature | `0.7` |
| `--max-tokens` | Maximum generated tokens | `4096` |
| `-w, --workers` | Number of concurrent workers | `10` |
| `--max-retries` | Maximum retry attempts | `3` |
| `--limit` | Limit number of samples to process | - |
| `-q, --quiet` | Quiet mode | `False` |

## 📊 Input/Output Format

**Input:** JSONL format, one JSON object per line (see `example_data.jsonl`):

```jsonl
{"text": "The quadratic formula states that for any quadratic equation..."}
{"text": "The Pythagorean theorem is a fundamental relation..."}
```

**Output:** Adds a `synthesis_result` field to the original data:

```json
{
  "text": "Original mathematical content",
  "synthesis_result": {
    "raw": "Full response",
    "problem": "Generated problem",
    "solution": "Detailed solution"
  }
}
```

## 🔌 Compatible with Other APIs

Supports any OpenAI-compatible API (e.g., Qwen, DeepSeek, vLLM, etc.):

```bash
# Using Alibaba Cloud Qwen API
export OPENAI_API_KEY="your-dashscope-api-key"
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

python run_synthesis.py -i data.jsonl -o output.jsonl -t qa --model qwen-plus
```

## 📜 License

This project is licensed under [Apache 2.0](../LICENSE).
