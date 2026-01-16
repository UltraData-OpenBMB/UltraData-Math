
from ..base_op import RemoveWordsMapper, TEXT_OPERATORS

OP_NAME = "remove_en_page_small_button_mapper"


@TEXT_OPERATORS.register_module(OP_NAME)
class RemovePageSmallButton(RemoveWordsMapper):
    def __init__(self, col_name_map):
        """
        删除网页中小按钮
        删除网页中小按钮(点击 打印 滑动 滚动 关闭 保存 复制 剪切 放大 广告弹窗)
        :param col_name_map:字段映射
        """
        name = OP_NAME

        super().__init__(name, col_name_map)

        self.words_to_remove_regex = [

            # 点击这里
            r'^(C|c)lick\s{0,3}(H|h)ere$',
            r'^CLICK\s{0,3}(HERE|here|Here)$',
            r'^Click\s{0,3}HERE$',

            # 打印按钮
            r'^(P|p)rint\s{0,3}this\s{0,3}article$',
            r'^(P|p)rint\s{0,3}this\s{0,3}page$',
            # 滑动按钮 滚动按钮
            r'SWIPE\s{0,3}LEFT$',
            r'^Allow\s{0,3}map\s{0,3}scroll$',
            r'^SWIPE\s{0,3}LEFT\s{0,3}OR\s{0,3}RIGHTLooking\s{0,3}Ahead$',

            # 关闭按钮
            r'\"Close\s{0,3}\(esc\)\"',
            r'^Comments\s{0,3}are\s{0,3}closed\.$',

            # 保存按钮
            r'^Preferences\s{0,3}saved$',
            r'^Save\/Compare$',

            # 复制剪切
            r'^Co\s{0,3}to\s{0,3}clipboard$',

            # 点击放大
            r'^Click to (E|e)nlarge\.?$',
            r'^Click to (E|e)xpand\.?$',

            # 广告弹窗
            r'^Advertisement \- Continue Reading Below$',

            # 返回按钮
            r'^(R|r)eturn\s{0,3}to\s{0,3}News\s{0,3}and\s{0,3}Events$',
            r'\s{0,3}(R|r)eturn\s{0,3}to\s{0,3}top$',
            r'\s{0,3}returned\s{0,3}the\s{0,3}following\s{0,3}results\.$',
            r'^Return\s{0,3}to\s{0,3}video\s{0,3}Video\s{0,3}settings$',
            r'^(G|g)oing\s{0,3}back$',
            r'^(G|g)o\s{0,3}back$',
            r'^(B|b)ack\s{0,3}to\s{0,3}Top$',

            # 添加按钮
            r'\s{0,3}(A|a)dd\s{0,3}to\s{0,3}this\s{0,3}section$',

        ]
