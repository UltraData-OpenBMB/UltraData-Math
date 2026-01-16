# -*- coding:utf-8 -*-
import re

from ultradata_math_parser.utils import *
from ultradata_math_parser.parsers.base_parser import BaseParser
from ultradata_math_parser.parsers.title_parser import TitleParser


class CustomParser(BaseParser):
    def __init__(self) -> None:
        super().__init__()

    def use_clean_rule(self, tree, clean_rules):
        for clean_rule in clean_rules:
            for x in tree.xpath(clean_rule):
                self.remove_node(x)
        return tree

    def use_extract_rule(self, tree, extract_rule):
        if "/text()" in extract_rule["value"]:
            return "".join(tree.xpath(extract_rule["value"])).strip()
        return tree.xpath(extract_rule["value"])[0]

    def extract(self, html="", base_url="", rule={}, **kwargs) -> dict:
        self.include_images = kwargs.get("include_images", False)
        tree = load_html(html)
        if tree is None:
            raise ValueError

        # base_url
        base_href = tree.xpath("//base/@href")

        if base_href and "http" in base_href[0]:
            base_url = base_href[0]

        if "clean" in rule:
            tree = self.use_clean_rule(tree, rule["clean"])

        # 获取title
        if "title" not in rule:
            title = TitleParser().process(tree)
        else:
            title = self.use_extract_rule(tree, rule["title"])

        # 文章区域
        try:
            body_tree = self.use_extract_rule(tree, rule["content"])
        except:
            raise ValueError
        if not self.include_images:
            self._remove_images_from_tree(body_tree)
        body_html = tostring(body_tree, encoding=str)
        body_html = self._strip_images_from_html(body_html)

        text_length = self._text_length_from_html(body_html)

        return {
            "xp_num": "custom",
            "drop_list": False,
            "html": body_html,
            "title": title,
            "base_url": base_url,
            "text_length": text_length,
        }
