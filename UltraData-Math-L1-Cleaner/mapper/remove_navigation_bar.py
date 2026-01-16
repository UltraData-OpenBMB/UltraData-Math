
from ..base_op import RemoveWordsMapper, TEXT_OPERATORS

OP_NAME = "remove_en_navigation_bar_mapper"


@TEXT_OPERATORS.register_module(OP_NAME)
class RemoveNavigationBar(RemoveWordsMapper):
    def __init__(self, col_name_map):
        """
        删除网页中的导航栏
        删除网页中的导航栏
        :param col_name_map:字段映射
        """
        name = OP_NAME

        super().__init__(name, col_name_map)

        self.words_to_remove_regex = [
            r'^Home » Site Map$',
            r'^Site Map$',
            r'^Computer Games Homepage\|Editor\'s Picks Articles\|Top Ten Articles\|Computer Games Site Map\s{0,3}$',

        ]
