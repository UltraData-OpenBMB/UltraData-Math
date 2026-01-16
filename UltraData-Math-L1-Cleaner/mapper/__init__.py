# Mapper 算子
# 格式修复类，对数据进行清洗和文本修复

from .nobreakspace import NBSP
from .clean_invisible_chars import CleanInvisibleChars
from .removebreakline import RemoveBreakLine
from .remove_navigation_bar import RemoveNavigationBar
from .remove_page_button import RemovePageButton
from .remove_page_small_button import RemovePageSmallButton

__all__ = [
    "NBSP",
    "CleanInvisibleChars",
    "RemoveBreakLine",
    "RemoveNavigationBar",
    "RemovePageButton",
    "RemovePageSmallButton",
]
