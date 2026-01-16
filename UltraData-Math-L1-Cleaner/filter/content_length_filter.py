from ..base_op import Filter, TEXT_OPERATORS

OP_NAME = "content_length_filter"


@TEXT_OPERATORS.register_module(OP_NAME)
class ContentLengthFilter(Filter):
    def __init__(self, col_name_map, content_lang="zh", max_content_len=100 * 10000, min_content_len=80):
        """
        文本长度过滤算子
        删除文本长度异常的文章，默认删除：文本长度小于80或文本长度大于100w
        :param col_name_map:字段映射
        :param content_lang:文本语言，中文会按照字符串长度计算文本长度，英文会按照单词数计算文本长度
        :param max_content_len:最大长度，通常取100万
        :param min_content_len:最小长度，通常取80或100
        """
        name = OP_NAME
        super().__init__(name, col_name_map)
        self.max_content_len = max_content_len
        self.min_content_len = min_content_len
        self.content_lang = content_lang

    def cal_nwords(self, content):
        if self.content_lang == "zh":
            return len(content)
        if self.content_lang == "en":
            return len([x for x in content.split(" ") if x])
        else:
            return len(content)

    def process_single(self, sample):
        content = self.get_content_from_sample(sample)
        n_words = len(content)  # cal n_words
        if n_words > self.max_content_len or n_words < self.min_content_len:
            return None
        return sample


__all__ = ["ContentLengthFilter"]
