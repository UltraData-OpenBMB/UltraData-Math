import re

from ..base_op import Filter, TEXT_OPERATORS

OP_NAME = "en_short_article_without_punctuation_filter"


@TEXT_OPERATORS.register_module(OP_NAME)
class ShortArticleWithoutPunctuationFilter(Filter):

    def __init__(self, col_name_map):
        """
        删除没有标点符号(英文句号和逗号)的短文章
        文章不包含标点符号，且字符数小于200，则整篇删除
        :param col_name_map:字段映射
        """
        name = OP_NAME
        super().__init__(name, col_name_map)

    def process_single(self, sample):
        content = self.get_content_from_sample(sample)
        if len(content) > 200:
            return sample
        delete = 1
        lines = content.split('\n')
        for line in lines:
            if re.search(r'\.|\,', line):
                delete = 0
                break
        if delete == 1:
            return None
        else:
            return sample
