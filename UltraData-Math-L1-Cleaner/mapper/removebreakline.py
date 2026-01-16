import re

from ..base_op import Mapper, TEXT_OPERATORS

OP_NAME = "remove_break_line"


@TEXT_OPERATORS.register_module(OP_NAME)
class RemoveBreakLine(Mapper):
    def __init__(self, col_name_map):
        """
        清洗连续换行符
        :param col_name_map: 字段映射
        """
        name = OP_NAME
        super().__init__(name, col_name_map)
        self.regex = r"([ \t]*\n){3,}"

    def clean_line(self, content):
        content = re.sub(self.regex, "\n\n", content)
        return content

    def process_single(self, sample):
        content = self.get_content_from_sample(sample)
        new_content = self.clean_line(content)
        self.update_content(sample, new_content)
        return sample
