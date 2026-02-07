# UltraData-Math-L1-Cleaner

<div align="center">

[🇨🇳 中文 README](README_ZH.md)

</div>

L1 Data Cleaning Layer: a collection of format repair and content filtering operators.

## 📂 Directory Structure

```
UltraData-Math-L1-Cleaner/
├── __init__.py
├── README.md
├── base_op.py                           # Base operator class definition
├── mapper/                              # Format repair operators
│   ├── __init__.py
│   ├── nobreakspace.py                  # Fix invisible characters
│   ├── clean_invisible_chars.py         # Clean garbled characters
│   ├── removebreakline.py               # Remove consecutive line breaks
│   ├── remove_navigation_bar.py         # Remove navigation bars
│   ├── remove_page_button.py            # Remove pagination buttons
│   └── remove_page_small_button.py      # Remove small buttons
└── filter/                              # Content filtering operators
    ├── __init__.py
    ├── short_article_without_punctuation_filter.py  # Short text without punctuation filter
    └── content_length_filter.py         # Content length filter
```

## 🔧 Operators

### Mapper Operators (Format Repair)

Clean and repair malformed data without changing the number of records.

| Operator | Description |
|:---|:---|
| `nobreakspace` | Remove zero-width characters, invisible spaces, and control characters |
| `clean_invisible_chars` | Remove garbled characters from Unicode private use areas |
| `remove_break_line` | Collapse 3 or more consecutive line breaks |
| `remove_en_navigation_bar_mapper` | Remove navigation bar text |
| `remove_en_page_button_mapper` | Remove pagination button text |
| `remove_en_page_small_button_mapper` | Remove miscellaneous small button text |

### Filter Operators (Content Filtering)

Discard entire records that do not meet the criteria; qualifying records are left unchanged.

| Operator | Description |
|:---|:---|
| `en_short_article_without_punctuation_filter` | Filter out short texts (<200 chars) without punctuation |
| `content_length_filter` | Content length filter (default range: 80 to 1,000,000 characters) |

## 📋 Usage Examples

```python
from mapper import NBSP, CleanInvisibleChars, RemoveBreakLine
from filter import ContentLengthFilter, ShortArticleWithoutPunctuationFilter

# Create operator instances
col_name_map = {"content": "text"}  # Field mapping

# Mapper example
nbsp_cleaner = NBSP(col_name_map)
sample = {"text": "Hello\u00A0World"}  # Contains NBSP character
cleaned_sample = nbsp_cleaner.process_single(sample)

# Filter example
length_filter = ContentLengthFilter(
    col_name_map, 
    content_lang="en",
    min_content_len=100,
    max_content_len=50000
)
result = length_filter.process_single(sample)  # Returns None if filtered out

# Batch processing
samples = [{"text": "sample1"}, {"text": "sample2"}]
processed = length_filter.process_batched(samples)
```

### Full Cleaning Pipeline Example

```python
# Define the cleaning pipeline
pipeline_config = [
    {'name': 'nobreakspace'},
    {'name': 'clean_invisible_chars'},
    {'name': 'en_short_article_without_punctuation_filter'},
    {'name': 'remove_en_navigation_bar_mapper'},
    {'name': 'remove_en_page_button_mapper'},
    {'name': 'remove_en_page_small_button_mapper'},
    {'name': 'remove_break_line'},
    {'name': 'content_length_filter', 'min_content_len': 80}
]
```

## 📜 License

This project is licensed under [Apache 2.0](../LICENSE).
