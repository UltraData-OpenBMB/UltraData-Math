# UltraData-Math-L0-Parser

<div align="center">

[🌏 English README](README.md)

</div>

UltraData-Math 项目 L0 层（原始数据层）的 HTML 解析器。

---

## 项目描述

本解析器是基于 [magic-html](https://github.com/opendatalab/magic-html) 开发的增强版通用 HTML 数据提取器，针对数学内容进行了专门优化。

它支持**多种提取模式**（Article、Forum、Unified），并原生支持保留数学公式、图片等富文本结构，旨在提供更精准、更完整的高质量网页内容提取能力。无论您处理的是复杂的论坛帖子还是标准的新闻文章，这个库都能适配合适的提取策略。

## 特点

- **多种提取模式**：支持 Article（文章）、Forum（论坛）、Unified（统一）三种提取模式。
- **统一提取模式**：`UnifiedParser` 统一提取器融合文章和论坛逻辑。
- **多层回退策略**：当主体提取内容不足时，自动触发回退策略，确保内容完整性。
- **内置站点规则**：支持预配置的网站适配规则，加入后可使用指定的解析方案进行精准提取。
- **格式转换**：支持将 HTML 转换为纯文本（依赖 w3m）。
- **Latex公式支持**：支持将网页中的数学公式提取并转换为标准 Latex 格式。

## 安装

```shell
# 从源码安装
git clone https://github.com/UltraData-OpenBMB/UltraData-Math.git
cd UltraData-Math/UltraData-Math-L0-Parser
pip install .
```

## 使用

### 基础用法

默认情况下，提取器使用统一提取模式（Unified）提取内容。默认会保留图片和公式。

```python
from ultradata_math_parser import GeneralParser

# 初始化提取器 (可选指定 w3m 路径)
parser = GeneralParser(w3m_path="/usr/bin/w3m")

url = "http://example.com/"
html = "<html>...</html>"

# 提取内容
# 默认配置：include_images=False, include_tables=True, process_math=True
data = parser.extract(html, base_url=url)

print(f"标题: {data.get('title')}")
print(f"正文内容: {data.get('text')}")
print(f"回退策略: {data.get('fallback_strategy')}")
```

### 切换提取模式

通过 `html_type` 参数指定提取模式：

```python
from ultradata_math_parser import GeneralParser

parser = GeneralParser()

# Article 模式
data = parser.extract(html, base_url=url, html_type="article")

# Forum 模式（适合论坛类页面）
data = parser.extract(html, base_url=url, html_type="forum")

# Unified 模式（默认）
data = parser.extract(html, base_url=url, html_type="unified")
```

### 自定义站点规则

支持通过配置文件为特定网站指定提取规则：

```python
from ultradata_math_parser import GeneralParser

# 通过配置文件加载自定义规则
parser = GeneralParser(config_path="./my_rules.json")

# 规则配置示例 (my_rules.json):
# {
#     "example.com": {
#         "clean": ["//script", "//style", "//div[@class='ad']"],
#         "title": {
#             "mode": "xpath",
#             "value": "//h1[@class='title']//text()"
#         },
#         "content": {
#             "mode": "xpath",
#             "value": "//div[@class='article-content']"
#         }
#     }
# }

data = parser.extract(html, base_url="http://example.com/article")
```

### 配置参数说明

虽然默认配置适用于大多数场景，但您可以通过参数调整提取行为：

#### 初始化参数

| 参数 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `config_path` | `""` | 自定义规则配置文件路径 |
| `w3m_path` | `"w3m"` | w3m 可执行文件路径 |

#### 提取参数

| 参数 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `base_url` | `""` | 页面 URL，用于解析相对链接 |
| `html_type` | `None` | 提取模式：`"unified"`（默认）、`"article"`、`"forum"` |
| `include_images` | `False` | 是否保留图片标签 `<img>` |
| `include_tables` | `True` | 是否保留表格 `<table>` |
| `process_math` | `True` | 是否将公式转换为 Latex 格式 |
| `preserve_math_containers` | `True` | 是否保留公式的原始容器标签 |
| `w3m_path` | 继承初始化 | 动态覆盖 w3m 路径 |

例如，如果您需要保留图片：

```python
data = parser.extract(html, base_url=url, include_images=True)
```

## 输出字段说明

提取结果包含以下主要字段：

### 基础字段

- `text`: 提取后的纯文本内容（由 w3m 转换）。
- `html`: 提取出的正文 HTML 片段（包含保留的标签）。
- `title`: 提取的标题。
- `text_length`: 正文文本长度。
- `base_url`: 解析后的基础 URL。

### 统一模式特有字段

- `forum_assembled`: 是否使用了论坛帖子拼装。
- `fallback_strategy`: 使用的回退策略（`primary`、`wild_text`、`readability`）。

## 架构说明

```
ultradata_math_parser/
├── __init__.py           # GeneralParser 入口
├── config.py             # 配置常量、XPath规则、内置站点规则
├── utils.py              # 工具函数
├── readability_plus.py   # 增强版 readability 算法
└── parsers/
    ├── base_parser.py     # 基础提取器（回退策略、公式处理等）
    ├── article_parser.py  # 文章提取器
    ├── forum_parser.py    # 论坛提取器（帖子拼装）
    ├── unified_parser.py  # 统一提取器（融合文章+论坛）
    ├── custom_parser.py   # 自定义规则提取器
    └── title_parser.py    # 标题提取器
```

## 许可

本项目代码采用[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html)授权。

## 鸣谢

- [magic-html](https://github.com/opendatalab/magic-html)
- [trafilatura](https://github.com/adbar/trafilatura)
- [w3m](https://github.com/tats/w3m)
- [readability-lxml](https://github.com/buriy/python-readability)
