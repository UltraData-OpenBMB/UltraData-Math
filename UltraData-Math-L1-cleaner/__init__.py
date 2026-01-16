# UltraData-Math-L1-Cleaner
# L1 数据清洗层：格式修复 + 内容过滤

"""
该模块包含用于数据清洗的算子：

Mapper 算子 (mapper/):
  格式修复类，对数据进行清洗和文本修复
  - nobreakspace: 修复不可见字符和控制字符
  - clean_invisible_chars: 清理乱码字符
  - removebreakline: 清洗连续换行符
  - remove_navigation_bar: 删除导航栏
  - remove_page_button: 删除翻页按钮
  - remove_page_small_button: 删除小按钮

Filter 算子 (filter/):
  内容过滤类，过滤不符合要求的数据
  - short_article_without_punctuation_filter: 过滤无标点短文章
  - content_length_filter: 文本长度过滤

基础类:
  - base_op: 基础算子类定义 (Mapper, Filter, RemoveWordsMapper 等)
"""

__version__ = "1.0.0"
