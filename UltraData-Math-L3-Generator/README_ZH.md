# UltraData-Math-L3-Generator

<div align="center">

[🌏 English README](README.md)

</div>

L3 合成数据层：基于 LLM 的多格式数学数据合成工具。

## 📂 目录结构

```
UltraData-Math-L3-Generator/
├── run_synthesis.py                 # OpenAI API 调用脚本
├── qa_synthesis.py                  # Q&A 问答对合成 Prompt
├── conversation_synthesis.py        # 多轮对话合成 Prompt
├── multistyle_rewrite.py           # 多风格改写 Prompt
├── knowledge_textbook.py           # 知识点提取 + 教材练习 Prompt
└── README.md
```

## 🔧 安装依赖

```bash
pip install openai
```

## 🚀 快速开始

### 环境配置

```bash
# 设置 API Key
export OPENAI_API_KEY="your-api-key"

# 可选：设置自定义 API 地址（兼容 OpenAI 格式的 API）
export OPENAI_BASE_URL="https://your-api-endpoint/v1"
```

### 基本用法

```bash
python run_synthesis.py \
    --input data.jsonl \
    --output output.jsonl \
    --task qa \
    --level high_school \
    --model gpt-4o \
    --workers 10
```

## 📋 任务类型

### 1. Q&A 问答对合成 (`qa`)

根据数学内容生成问答对，按教育难度分级。

**参数 `--level`：**
| 值 | 说明 |
|:---|:---|
| `grade_school` | 小学 |
| `middle_school` | 初中 |
| `high_school` | 高中（默认） |
| `college` | 大学 |

```bash
python run_synthesis.py -i data.jsonl -o output.jsonl -t qa --level high_school
```

### 2. 多轮对话合成 (`conversation`)

将数学内容转换为多轮对话格式。

**参数 `--style`：**
| 值 | 说明 |
|:---|:---|
| `two_professors` | 两位教授对话 |
| `teacher_student` | 师生对话（默认） |
| `two_students` | 两位学生对话 |
| `interview` | 面试风格 |
| `problem_solving` | 问题解决 |
| `layman_expert` | 外行与专家 |
| `debate` | 辩论风格 |

```bash
python run_synthesis.py -i data.jsonl -o output.jsonl -t conversation --style teacher_student
```

### 3. 多风格改写 (`rewrite`)

将数学内容改写为不同风格。

**参数 `--style`：**
| 值 | 说明 |
|:---|:---|
| `wikipedia` | 维基百科风格 |
| `textbook` | 教科书风格（默认） |
| `blog` | 博客风格 |
| `popular_science` | 科普风格 |
| `academic_paper` | 学术论文风格 |
| `learning_note` | 学习笔记风格 |
| `lecture_note` | 讲义风格 |

```bash
python run_synthesis.py -i data.jsonl -o output.jsonl -t rewrite --style textbook
```

### 4. 知识点提取 (`knowledge`)

从数学内容中提取定义、定理、性质等知识点。

```bash
python run_synthesis.py -i data.jsonl -o knowledge_output.jsonl -t knowledge
```

### 5. 教材练习生成 (`textbook`)

基于知识点生成不同难度的教材式练习。

**参数 `--difficulty`：**
| 值 | 说明 |
|:---|:---|
| `easy` | 简单（默认） |
| `medium` | 中等 |
| `hard` | 困难 |

```bash
python run_synthesis.py -i knowledge.jsonl -o output.jsonl -t textbook --difficulty medium
```

**注意：** 输入文件需包含 `knowledge_point` 字段（可通过 `--knowledge-field` 自定义）。

## ⚙️ 参数说明

| 参数 | 说明 | 默认值 |
|:---|:---|:---|
| `-i, --input` | 输入 JSONL 文件路径 | 必填 |
| `-o, --output` | 输出 JSONL 文件路径 | 必填 |
| `-t, --task` | 任务类型：`qa`, `conversation`, `rewrite`, `knowledge`, `textbook` | 必填 |
| `--level` | Q&A 难度级别 | `high_school` |
| `--style` | 对话/改写风格 | - |
| `--difficulty` | 教材练习难度 | `easy` |
| `--text-field` | 输入文本字段名 | `text` |
| `--knowledge-field` | 知识点字段名 | `knowledge_point` |
| `--api-key` | OpenAI API Key | 环境变量 |
| `--base-url` | API Base URL | 环境变量 |
| `--model` | 模型名称 | `gpt-4o` |
| `--temperature` | 采样温度 | `0.7` |
| `--max-tokens` | 最大生成 token 数 | `4096` |
| `-w, --workers` | 并发数 | `10` |
| `--max-retries` | 最大重试次数 | `3` |
| `--limit` | 限制处理样本数量 | - |
| `-q, --quiet` | 静默模式 | `False` |

## 📊 输入输出格式

**输入：** JSONL 格式，每行一个 JSON 对象（参见 `example_data.jsonl`）：

```jsonl
{"text": "The quadratic formula states that for any quadratic equation..."}
{"text": "The Pythagorean theorem is a fundamental relation..."}
```

**输出：** 在原数据基础上添加 `synthesis_result` 字段：

```json
{
  "text": "原始数学内容",
  "synthesis_result": {
    "raw": "完整响应",
    "problem": "生成的问题",
    "solution": "详细解答"
  }
}
```

## 🔌 兼容其他 API

支持任何 OpenAI 兼容的 API（如 Qwen、DeepSeek、vLLM 等）：

```bash
# 使用阿里云 Qwen API
export OPENAI_API_KEY="your-dashscope-api-key"
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

python run_synthesis.py -i data.jsonl -o output.jsonl -t qa --model qwen-plus
```

## 📜 许可证

本项目基于 [Apache 2.0](../LICENSE) 许可证发布。
