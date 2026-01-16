import re

from ..base_op import Mapper, TEXT_OPERATORS

OP_NAME = "clean_invisible_chars"


@TEXT_OPERATORS.register_module(OP_NAME)
class CleanInvisibleChars(Mapper):
    def __init__(self, col_name_map):
        """
        乱码字符替换为空
        :param col_name_map: 字段映射
        """
        name = OP_NAME
        super().__init__(name, col_name_map)
        self.pattern = re.compile(r'[\uE000-\uF8FF]')
    def fix_underscores(self, line):
        line = self.pattern.sub('', line)
        return line

    def process_single(self, sample):
        content = self.get_content_from_sample(sample)
        new_content = self.fix_underscores(content)
        self.update_content(sample, new_content)
        return sample
