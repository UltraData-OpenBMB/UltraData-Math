# -*- coding:utf-8 -*-

from copy import deepcopy

from ultradata_math_parser.utils import *
from ultradata_math_parser.parsers.base_parser import BaseParser
from ultradata_math_parser.parsers.title_parser import TitleParser


class ArticleParser(BaseParser):
    def __init__(self) -> None:
        super().__init__()

    def extract(self, html="", **kwargs) -> dict:
        base_url = kwargs.get("base_url", "")
        self.process_math = kwargs.get("process_math", self.process_math)
        self.preserve_math_containers = kwargs.get("preserve_math_containers", self.preserve_math_containers)
        self.include_tables = kwargs.get("include_tables", self.include_tables)
        self.include_images = kwargs.get("include_images", self.include_images)
        html = html.replace("&nbsp;", " ").replace("&#160;", " ")
        tree = load_html(html)
        if tree is None:
            raise ValueError

        title = TitleParser().process(tree)

        # base_url
        base_href = tree.xpath("//base/@href")

        if base_href and "http" in base_href[0]:
            base_url = base_href[0]

        if "://blog.csdn.net/" in base_url:
            for dtree in tree.xpath('//div[@id="content_views"]//ul[@class="pre-numbering"]'):
                self.remove_node(dtree)

        raw_tree = deepcopy(tree)
        working_tree = deepcopy(tree)

        # 标签转换, 增加数学标签处理
        format_tree = self.convert_tags(working_tree, base_url=base_url)
        format_tree = self._remove_tables_from_tree(format_tree)
        format_tree = self._remove_images_from_tree(format_tree)

        # 删除script style等标签及其内容
        normal_tree = self.clean_tags(format_tree)
        normal_tree = self._remove_tables_from_tree(normal_tree)
        normal_tree = self._remove_images_from_tree(normal_tree)
        fallback_tree = deepcopy(normal_tree)

        subtree, xp_num, drop_list = self.xp_1_5(normal_tree)
        if xp_num == "others":
            subtree, drop_list = self.prune_unwanted_sections(normal_tree)
        body_html = self.get_content_html(subtree, xp_num, base_url)

        body_html, fallback_strategy = self.apply_fallbacks(
            primary_html=body_html,
            base_url=base_url,
            normal_tree=fallback_tree,
            raw_tree=raw_tree,
        )

        body_html = self._strip_tables_from_html(body_html)
        body_html = self._strip_images_from_html(body_html)

        text_length = self._text_length_from_html(body_html)

        return {
            "xp_num": xp_num,
            "drop_list": drop_list,
            "html": body_html,
            "title": title,
            "base_url": base_url,
            "fallback_strategy": fallback_strategy,
            "text_length": text_length,
        }
