# UltraData-Math-L1-Cleaner

<div align="center">

[🌏 English README](README.md)

</div>

L1 数据清洗层：格式修复 + 内容过滤算子集合。

## 📂 目录结构

```
UltraData-Math-L1-Cleaner/
├── __init__.py
├── README.md
├── base_op.py                           # 基础算子类定义
├── mapper/                              # 格式修复类算子
│   ├── __init__.py
│   ├── nobreakspace.py                  # 修复不可见字符
│   ├── clean_invisible_chars.py         # 清理乱码字符
│   ├── removebreakline.py               # 清洗连续换行
│   ├── remove_navigation_bar.py         # 删除导航栏
│   ├── remove_page_button.py            # 删除翻页按钮
│   └── remove_page_small_button.py      # 删除小按钮
└── filter/                              # 内容过滤类算子
    ├── __init__.py
    ├── short_article_without_punctuation_filter.py  # 短文无标点过滤
    └── content_length_filter.py         # 文本长度过滤
```

## 🔧 算子说明

### Mapper 算子（格式修复）

对数据进行清洗，修复错误的数据，不改变数据条数。

| 算子名称 | 功能描述 |
|:---|:---|
| `nobreakspace` | 清理零宽字符、不可见空格、控制字符 |
| `clean_invisible_chars` | 清理 Unicode 私有区乱码字符 |
| `remove_break_line` | 清洗 3 个及以上的连续换行符 |
| `remove_en_navigation_bar_mapper` | 删除导航栏文本 |
| `remove_en_page_button_mapper` | 删除翻页按钮文本 |
| `remove_en_page_small_button_mapper` | 删除各类小按钮文本 |

### Filter 算子（内容过滤）

当数据不符合要求时整条丢弃，符合要求则不对数据做任何改动。

| 算子名称 | 功能描述 |
|:---|:---|
| `en_short_article_without_punctuation_filter` | 过滤无标点且 <200 字符的短文 |
| `content_length_filter` | 文本长度过滤（默认 80~100万字符） |

## 📋 使用示例

```python
from mapper import NBSP, CleanInvisibleChars, RemoveBreakLine
from filter import ContentLengthFilter, ShortArticleWithoutPunctuationFilter

# 创建算子实例
col_name_map = {"content": "text"}  # 字段映射

# Mapper 示例
nbsp_cleaner = NBSP(col_name_map)
sample = {"text": "Hello\u00A0World"}  # 包含 NBSP 字符
cleaned_sample = nbsp_cleaner.process_single(sample)

# Filter 示例
length_filter = ContentLengthFilter(
    col_name_map, 
    content_lang="en",
    min_content_len=100,
    max_content_len=50000
)
result = length_filter.process_single(sample)  # 返回 None 表示被过滤

# 批量处理
samples = [{"text": "sample1"}, {"text": "sample2"}]
processed = length_filter.process_batched(samples)
```

### 完整清洗流程示例

```python
# 定义清洗流程
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

## 📜 许可证

本项目基于 [Apache 2.0](../LICENSE) 许可证发布。
