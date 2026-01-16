
from ..base_op import RemoveWordsMapper, TEXT_OPERATORS

OP_NAME = "remove_en_page_button_mapper"


@TEXT_OPERATORS.register_module(OP_NAME)
class RemovePageButton(RemoveWordsMapper):
    def __init__(self, col_name_map):
        """
        删除页面上的翻页按钮
        删除页面上的翻页按钮
        :param col_name_map:字段映射
        """
        name = OP_NAME

        super().__init__(name, col_name_map)

        self.words_to_remove_regex = [

            # 页码
            r'^(P|p)ages:\s{0,3}\d{1,6}\.\s{1,10}',  # pages:123.
            r'^(P|p)age:?\s{0,3}\d{1,5}$',  # Page: 148 或 Page 148
            r'^(P|p)ages:?\s{0,3}\d{1,5}$',  # Pages: 148 或 Pages 148
            r'^(P|p)age\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # 单行page 1 of 3
            r'^(P|p)age\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}\s{0,3}\.?\s{0,3}',  # 开头page 1 of 3
            r'\s{0,3}\(\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}\)$',  # (page 1 of 3)
            r'\s{0,3}\•\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # 带 -符号的 结尾page 1 of 3
            r'\s{0,3}\-\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # 带 •符号的 结尾page 1 of 3
            r'\s{0,3}\/\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # 带 /符号的 结尾page 1 of 3
            r'(?<=\.)\s{0,5}\d{1,3}\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # . 句尾 1 page 1 of 3
            r'(?<=\?)\s{0,5}\d{1,3}\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # ? 句尾 1 page 1 of 3
            r'(?<=\,)\s{0,5}\d{1,3}\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # , 句尾 1 page 1 of 3
            r'(?<=\…)\s{0,5}\d{1,3}\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # …句尾 1 page 1 of 3
            # r'\s{0,5}\d{1,3}\s{0,3}Page\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,3}$',  # page 1 of 3

            # 翻页
            r'^Go\s{0,3}DownPages\d{1,5}$',
            r'^Go\s{0,3}UpPages\d{1,5}$',
            r'^\(previous entry\)$',
            r'^\(next entry\)$',
            r'^«\s{0,5}Previous\s{0,3}page$',  # « Previous page
            r'\s{0,3}\<\s{0,3}Previous\s{0,3}\d{1,8}$',  # < Previous 10
            r'^Previous\s{0,3}Article$',  # Previous Article
            r'^Previous\d{1,5}\…\s{0,5}',  # Previous1…
            r'^prev\s{0,3}\|\s{0,3}next\§\s{0,5}',
            r'^(P|p)age\◀\d{1,10}\▶$',  # page◀12345▶
            r'^PagePrevious\d{1,20}Next$',  # PagePrevious1234Next
            r'Pages:\s{0,3}\d{1,2}\s{0,3}\.{2,6}\s{0,3}\d{1,20}',  # Pages:1...789101112
            r'^Pages:\s{0,3}\[\d{1,8}Go\s{0,3}Down\s{0,3}',
            r'^Page\s{0,3}\d{1,5}Next\s{0,3}Page$',  # Page 2 NEXT Page
            r'^(P|p)ages:\s{0,3}\d{1,3}NEXT\s{0,3}»$',  # Page: 2 NEXT »
            r'\s{0,3}\«\s{0,3}Previous\s{0,3}\d{1,20}\s{0,3}',  # « Previous123
            r'^Pages\:\s{0,3}\(\d\)\s{0,3}\<\d{1,20}\>\s{0,3}',  # Pages: (4) <123>
            r'(P|p)ages?:(\s{0,3}\d{1,3}){4,20}',  # page: 1 2 3 4 5
            r'Page\s{0,3}\d{1,5}\s{0,3}of\s{0,3}\d{1,5}\s{0,3}Next\s{0,3}Prev',  # Page 1 of 2Next  Prev
            r'^(P|p)ages?:\s{0,3}((P|p)age\s{0,3}\d{1,3},\s{0,3}){4,20}(P|p)age\s{0,3}\d{1,3}\s{0,3},?$',
            # page:page 1, page 2, page 3, page 4, page 5
            r'^((P|p)age\s{0,5}\d{1,3}\s{0,10}){4,20}$',  # page 1 page 2 page 3 page 4 ...
            r'^Post\s{0,3}Reply\d{1,8}\s{0,3}postsPage\s{0,3}\d{1,3}\s{0,3}of\s{0,3}\d{1,8}Jump\s{0,3}to\s{0,3}page:$',
            r'^«\s{0,3}Previous\d{1,20}\…\d{1,20}Next\s{0,3}»\s{0,3}$',  # «Previous123456…20212223Next»
            r'^(P|p)age\s{0,3}\d{1,5}\s{0,3}of\s{0,3}\d{1,5}«\s{0,3}(F|f)irst«\.{2,6}\d{1,20}\.{2,6}\d{1,5}\.{2,6}»(L|l)ast\s{0,3}»\s{0,3}$',
            # Page 4 of 10« First«...23456...10...»Last »

        ]
