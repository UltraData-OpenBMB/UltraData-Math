# -*- coding: utf-8 -*-
import json
import logging
from typing import Optional, Type
from urllib.parse import urlparse
import tldextract

from ultradata_math_parser.parsers.article_parser import ArticleParser
from ultradata_math_parser.parsers.forum_parser import ForumParser
from ultradata_math_parser.parsers.custom_parser import CustomParser
from ultradata_math_parser.parsers.unified_parser import UnifiedParser
from ultradata_math_parser.utils import text_len, run_w3m_dump, W3MError
from ultradata_math_parser.config import URL_PATTERNS_TO_HTML_TYPE, BUILTIN_SITE_RULES


class GeneralParser:
    def __init__(self, config_path="", w3m_path: str = "w3m"):
        self.logger = logging.getLogger(__name__)
        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.rule = json.loads(f.read())
            except:
                pass
        else:
            self.rule = {}
        self.w3m_path = w3m_path or "w3m"
        self.tld_extractor = tldextract.TLDExtract()

    def extract(self, html="", w3m_path: Optional[str] = None, **kwargs) -> dict:
        base_url = kwargs.get("base_url", "")
        netloc = urlparse(base_url).netloc if base_url else ""
        html_type = kwargs.pop("html_type", None)

        current_w3m_path = w3m_path or self.w3m_path

        # 检查 URL 是否匹配内置规则
        if base_url and self._quick_check_builtin_rules(base_url):
            try:
                extracted = self.tld_extractor(base_url)
                domain = f"{extracted.domain}.{extracted.suffix}"
                self.logger.debug("TLD Extract result for %s: domain=%s, suffix=%s -> key=%s", base_url, extracted.domain, extracted.suffix, domain)

                if domain in BUILTIN_SITE_RULES:
                    try:
                        builtin_rule = BUILTIN_SITE_RULES[domain]
                        new_kwargs = dict()
                        new_kwargs["rule"] = builtin_rule
                        new_kwargs.update(kwargs)
                        self.logger.debug("Using builtin rule for domain: %s", domain)
                        return self._run_extractor(CustomParser, html, new_kwargs, w3m_path=current_w3m_path)
                    except Exception as exc:
                        self.logger.debug("Builtin rule extractor failed for %s: %s", domain, exc)
            except Exception as e:
                self.logger.debug("Error extracting domain or checking builtin rules: %s", e)

        # 检查 URL 类型模式
        if not html_type and base_url:
            for pattern, type in URL_PATTERNS_TO_HTML_TYPE.items():
                if pattern in base_url:
                    html_type = type
                    break

        # 使用用户配置的规则
        if netloc in self.rule:
            try:
                new_kwargs = dict()
                new_kwargs["rule"] = self.rule[netloc]
                new_kwargs.update(kwargs)
                return self._run_extractor(CustomParser, html, new_kwargs, w3m_path=current_w3m_path)
            except Exception as exc:
                self.logger.debug("Custom extractor failed for %s: %s", netloc, exc)

        # 根据 html_type 选择提取模式
        if html_type == "forum":
            return self._run_extractor(ForumParser, html, kwargs, w3m_path=current_w3m_path)
        if html_type == "article":
            return self._run_extractor(ArticleParser, html, kwargs, w3m_path=current_w3m_path)
        if html_type == "unified":
            return self._run_extractor(UnifiedParser, html, kwargs, w3m_path=current_w3m_path)

        # 默认使用统一模式
        return self._run_extractor(UnifiedParser, html, kwargs, w3m_path=current_w3m_path)

    def _quick_check_builtin_rules(self, url: str) -> bool:
        if not url:
            return False
        url_lower = url.lower()
        for domain in BUILTIN_SITE_RULES:
            if domain in url_lower:
                return True
        return False

    def _run_extractor(self, extractor_cls: Type, html: str, kwargs: dict, w3m_path: str):
        result = extractor_cls().extract(html=html, **dict(kwargs))
        return self._apply_w3m(result, w3m_path=w3m_path)

    def _apply_w3m(self, result: Optional[dict], w3m_path: str) -> Optional[dict]:
        if not result:
            return result
        html_fragment = result.get("html")
        if not html_fragment:
            raise RuntimeError("Extraction result does not contain 'html' for w3m")
        text = run_w3m_dump(html_fragment, w3m_path)
        enriched = dict(result)
        enriched["text"] = text
        enriched["w3m_text"] = text
        enriched["text_length"] = text_len(text)
        return enriched
