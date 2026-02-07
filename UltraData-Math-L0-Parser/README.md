# UltraData-Math-L0-Parser

<div align="center">

[🇨🇳 中文 README](README_ZH.md)

</div>

HTML parser for the L0 (Raw Data) layer of the UltraData-Math project.

---

## Description

This parser is an enhanced general-purpose HTML data extractor developed on top of [magic-html](https://github.com/opendatalab/magic-html), specifically optimized for mathematical content.

It supports **multiple extraction modes** (Article, Forum, Unified) and natively preserves rich-text structures such as mathematical formulas and images, aiming to deliver more accurate and complete high-quality web content extraction. Whether you are dealing with complex forum threads or standard news articles, this library adapts the appropriate extraction strategy.

## Features

- **Multiple Extraction Modes**: Supports three extraction modes — Article, Forum, and Unified.
- **Unified Extraction Mode**: `UnifiedParser` merges article and forum extraction logic.
- **Multi-level Fallback Strategy**: Automatically triggers fallback strategies when the primary extraction yields insufficient content, ensuring content integrity.
- **Built-in Site Rules**: Supports pre-configured website adaptation rules for precise extraction using specified parsing schemes.
- **Format Conversion**: Converts HTML to plain text (powered by w3m).
- **LaTeX Formula Support**: Extracts and converts mathematical formulas from web pages into standard LaTeX format.

## Installation

```shell
# Install from source
git clone https://github.com/UltraData-OpenBMB/UltraData-Math.git
cd UltraData-Math/UltraData-Math-L0-Parser
pip install .
```

## Usage

### Basic Usage

By default, the extractor uses the Unified extraction mode. Images are excluded and formulas are preserved by default.

```python
from ultradata_math_parser import GeneralParser

# Initialize the extractor (optionally specify w3m path)
parser = GeneralParser(w3m_path="/usr/bin/w3m")

url = "http://example.com/"
html = "<html>...</html>"

# Extract content
# Default: include_images=False, include_tables=True, process_math=True
data = parser.extract(html, base_url=url)

print(f"Title: {data.get('title')}")
print(f"Content: {data.get('text')}")
print(f"Fallback Strategy: {data.get('fallback_strategy')}")
```

### Switching Extraction Modes

Specify the extraction mode via the `html_type` parameter:

```python
from ultradata_math_parser import GeneralParser

parser = GeneralParser()

# Article mode
data = parser.extract(html, base_url=url, html_type="article")

# Forum mode (suitable for forum-like pages)
data = parser.extract(html, base_url=url, html_type="forum")

# Unified mode (default)
data = parser.extract(html, base_url=url, html_type="unified")
```

### Custom Site Rules

Configure extraction rules for specific websites via a configuration file:

```python
from ultradata_math_parser import GeneralParser

# Load custom rules from a config file
parser = GeneralParser(config_path="./my_rules.json")

# Example rule configuration (my_rules.json):
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

### Configuration Parameters

While the default configuration works well for most scenarios, you can adjust the extraction behavior through parameters:

#### Initialization Parameters

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `config_path` | `""` | Path to a custom rules configuration file |
| `w3m_path` | `"w3m"` | Path to the w3m executable |

#### Extraction Parameters

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `base_url` | `""` | Page URL, used for resolving relative links |
| `html_type` | `None` | Extraction mode: `"unified"` (default), `"article"`, `"forum"` |
| `include_images` | `False` | Whether to preserve `<img>` tags |
| `include_tables` | `True` | Whether to preserve `<table>` elements |
| `process_math` | `True` | Whether to convert formulas to LaTeX format |
| `preserve_math_containers` | `True` | Whether to preserve original formula container tags |
| `w3m_path` | Inherited | Dynamically override the w3m path |

For example, to include images in the output:

```python
data = parser.extract(html, base_url=url, include_images=True)
```

## Output Fields

The extraction result contains the following fields:

### Basic Fields

- `text`: Extracted plain text content (converted by w3m).
- `html`: Extracted HTML fragment of the main content (with preserved tags).
- `title`: Extracted title.
- `text_length`: Length of the main text content.
- `base_url`: Resolved base URL.

### Unified Mode Specific Fields

- `forum_assembled`: Whether forum post assembly was used.
- `fallback_strategy`: The fallback strategy used (`primary`, `wild_text`, `readability`).

## Architecture

```
ultradata_math_parser/
├── __init__.py           # GeneralParser entry point
├── config.py             # Configuration constants, XPath rules, built-in site rules
├── utils.py              # Utility functions
├── readability_plus.py   # Enhanced readability algorithm
└── parsers/
    ├── base_parser.py     # Base extractor (fallback strategies, formula processing, etc.)
    ├── article_parser.py  # Article extractor
    ├── forum_parser.py    # Forum extractor (post assembly)
    ├── unified_parser.py  # Unified extractor (merges article + forum)
    ├── custom_parser.py   # Custom rules extractor
    └── title_parser.py    # Title extractor
```

## License

This project is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.html).

## Acknowledgements

- [magic-html](https://github.com/opendatalab/magic-html)
- [trafilatura](https://github.com/adbar/trafilatura)
- [w3m](https://github.com/tats/w3m)
- [readability-lxml](https://github.com/buriy/python-readability)
