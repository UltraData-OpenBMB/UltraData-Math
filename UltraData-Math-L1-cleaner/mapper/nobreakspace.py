import re

from ..base_op import Mapper, TEXT_OPERATORS

OP_NAME = "nobreakspace"


@TEXT_OPERATORS.register_module(OP_NAME)
class NBSP(Mapper):
    def __init__(self, col_name_map):
        """
        修复不可见字符，控制字符
        :param col_name_map: 字段映射
        """
        name = OP_NAME
        super().__init__(name, col_name_map)
        INVISIBLE_CHARS = [
            # 零宽字符
            "\u200B", "\u200C", "\u200D", "\u2060", "\uFEFF",
            "\u202A", "\u202B", "\u202C", "\u202D", "\u202E",
            "\u2066", "\u2067", "\u2068", "\u2069",
            "\u206A", "\u206B", "\u206C", "\u206D", "\u206E", "\u206F",
            "\u200e", "\u200f"

            # 不可见空格
                      "\u00A0",  # NBSP
            "\u2000", "\u2001", "\u2002", "\u2003", "\u2004",
            "\u2005", "\u2006", "\u2007", "\u2008", "\u2009",
            "\u200A", "\u202F", "\u205F", "\u3000",
        ]

        # 控制字符范围 (去掉常用的 \t=9, \n=10, \r=13)
        CONTROL_CHARS = ''.join(
            chr(c) for c in list(range(0,32)) + list(range(127,160))
            if c not in (9, 10, 13)
        )
        self.ALL_INVISIBLE = re.compile(f"[{''.join(INVISIBLE_CHARS)}{CONTROL_CHARS}]")

    def clean_invisible(self, text: str, replace_map: dict = None) -> str:
        """
        修复文本，清理掉异常字符
        replace_map: 可选映射表，用于替换某些特殊字符为对应的正常字符
        """
        if replace_map is None:
            replace_map = {
                "\u00A0": " ",  # NBSP → 普通空格
                "\u3000": " ",  # 全角空格 → 普通空格
            }

        def _replace(match):
            ch = match.group(0)
            return replace_map.get(ch, "")  # 有映射用映射，否则直接删掉

        return self.ALL_INVISIBLE.sub(_replace, text)


    def process_single(self, sample):
        content = self.get_content_from_sample(sample)
        new_content = self.clean_invisible(content)
        self.update_content(sample, new_content)
        return sample
