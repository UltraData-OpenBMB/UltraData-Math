# -*- coding:utf-8 -*-
import re
from copy import deepcopy

from lxml.html import Element, tostring, fromstring

from ultradata_math_parser.config import Forum_XPATH, Unique_ID
from ultradata_math_parser.utils import load_html, text_len
from ultradata_math_parser.parsers.base_parser import BaseParser
from ultradata_math_parser.parsers.title_parser import TitleParser


class UnifiedParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.need_comment = True
        self.enable_forum_assembly = True
        self.forum_assembly_min_gain = 1.1

    def extract(self, html="", **kwargs) -> dict:
        base_url = kwargs.get("base_url", "")
        self.process_math = kwargs.get("process_math", self.process_math)
        self.preserve_math_containers = kwargs.get("preserve_math_containers", self.preserve_math_containers)
        self.include_tables = kwargs.get("include_tables", self.include_tables)
        self.include_images = kwargs.get("include_images", self.include_images)
        self.enable_forum_assembly = kwargs.get("enable_forum_assembly", self.enable_forum_assembly)
        self.fallback_min_length = kwargs.get("fallback_min_length", self.fallback_min_length)

        html = html.replace("&nbsp;", " ").replace("&#160;", " ")
        tree = load_html(html)
        if tree is None:
            raise ValueError

        title = TitleParser().process(tree)

        raw_tree = deepcopy(tree)

        # base_url
        base_href = tree.xpath("//base/@href")
        if base_href and "http" in base_href[0]:
            base_url = base_href[0]

        self.generate_unique_id(tree)

        # 标签转换
        format_tree = self.convert_tags(tree, base_url=base_url)
        format_tree = self._remove_tables_from_tree(format_tree)
        format_tree = self._remove_images_from_tree(format_tree)

        normal_tree = self.clean_tags(format_tree)
        normal_tree = self._remove_tables_from_tree(normal_tree)
        normal_tree = self._remove_images_from_tree(normal_tree)

        fallback_tree = deepcopy(normal_tree)

        # 主体提取
        subtree, xp_num, drop_list = self.xp_1_5(normal_tree)
        if xp_num == "others":
            subtree, drop_list = self.prune_unwanted_sections(normal_tree)

        body_html = self.get_content_html(subtree, xp_num, base_url)

        # 论坛帖子拼装
        forum_assembled = False
        if self.enable_forum_assembly:
            if xp_num != "others":
                normal_tree, _ = self.prune_unwanted_sections(normal_tree)

            original_length = self._text_length_from_html(body_html)
            assembled_html = self._try_forum_assembly(normal_tree, body_html)
            assembled_length = self._text_length_from_html(assembled_html)

            if assembled_length >= original_length * self.forum_assembly_min_gain:
                body_html = assembled_html
                forum_assembled = True

        # 条件兜底
        current_length = self._text_length_from_html(body_html)
        fallback_strategy = "primary"

        if current_length < self.fallback_min_length:
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
            "forum_assembled": forum_assembled,
        }

    def _try_forum_assembly(self, normal_tree, body_html):
        if not body_html:
            return body_html

        try:
            body_html_tree = fromstring(body_html)
        except Exception:
            return body_html

        try:
            body_tree = body_html_tree.body
        except:
            body_tree = Element("body")
            body_tree.extend(body_html_tree)

        main_ids = body_tree.xpath(f".//@{Unique_ID}")

        for main_id in main_ids:
            main_tree = normal_tree.xpath(f".//*[@{Unique_ID}={main_id}]")
            if main_tree:
                try:
                    self.remove_node(main_tree[0])
                except:
                    pass

        if not main_ids:
            main_ids = [-1]

        for c_xpath in Forum_XPATH:
            while True:
                matches = normal_tree.xpath(c_xpath)
                if not matches:
                    break

                x = matches[0]
                self.remove_node(x)

                if "'post-'" in c_xpath or "'post_'" in c_xpath:
                    elem_id = x.attrib.get("id", "").lower()
                    if not (re.search(r'post-\d+', elem_id) or re.search(r'post_\d+', elem_id)):
                        continue

                if "header" in x.attrib.get("class", "").lower() or "header" in x.attrib.get("id", "").lower():
                    continue

                try:
                    node_id = int(x.attrib.get(Unique_ID, "0"))
                    last_main_id = int(main_ids[-1]) if main_ids else -1

                    if node_id > last_main_id:
                        body_tree.append(x)
                    else:
                        prefix_div = Element("div")
                        suffix_div = Element("div")
                        need_prefix = False
                        need_suffix = False

                        while x.xpath(f".//*[number(@{Unique_ID}) > {last_main_id}]"):
                            tmp_x = x.xpath(f".//*[number(@{Unique_ID}) > {last_main_id}]")[0]
                            self.remove_node(tmp_x)
                            suffix_div.append(tmp_x)
                            need_suffix = True

                        while x.xpath(f".//*[number(@{Unique_ID}) < {last_main_id}]"):
                            tmp_x = x.xpath(f".//*[number(@{Unique_ID}) < {last_main_id}]")[0]
                            self.remove_node(tmp_x)
                            prefix_div.append(tmp_x)
                            need_prefix = True

                        if need_prefix:
                            body_tree.insert(0, prefix_div)
                        if need_suffix:
                            body_tree.append(suffix_div)
                except Exception:
                    pass

        result_html = re.sub(
            f' {Unique_ID}="\d+"',
            "",
            tostring(body_tree, encoding=str),
        )

        return result_html
