"""
基础算子类定义

提供 Mapper、Filter 等基础算子的抽象基类。
"""

import re
from typing import Any, Dict, List, Optional


class Registry:
    """简单的算子注册器"""
    
    def __init__(self, name: str):
        self.name = name
        self._modules: Dict[str, type] = {}
    
    def register_module(self, name: str):
        def decorator(cls):
            self._modules[name] = cls
            return cls
        return decorator
    
    def get(self, name: str) -> Optional[type]:
        return self._modules.get(name)
    
    def list_modules(self) -> List[str]:
        return list(self._modules.keys())


TEXT_OPERATORS = Registry("Operators")


def get_content_from_sample(sample: Dict[str, Any], col_name_map: Dict[str, str]) -> str:
    """
    从样本中获取文本内容
    
    Args:
        sample: 数据样本字典
        col_name_map: 字段映射配置，如 {"content": "contents[0]"}
    
    Returns:
        文本内容字符串
    """
    content_key = col_name_map.get("content", "content")
    
    # 处理数组索引格式，如 "contents[0]"
    if "[" in content_key and "]" in content_key:
        base_key = content_key.split("[")[0]
        index = int(content_key.split("[")[1].split("]")[0])
        return sample.get(base_key, [""])[index]
    
    return sample.get(content_key, sample.get("content", sample.get("text", "")))


def update_sample_content(sample: Dict[str, Any], new_content: str, col_name_map: Dict[str, str]) -> Dict[str, Any]:
    """
    更新样本中的文本内容
    
    Args:
        sample: 数据样本字典
        new_content: 新的文本内容
        col_name_map: 字段映射配置
    
    Returns:
        更新后的样本字典
    """
    content_key = col_name_map.get("content", "content")
    
    if "[" in content_key and "]" in content_key:
        base_key = content_key.split("[")[0]
        index = int(content_key.split("[")[1].split("]")[0])
        if base_key in sample and isinstance(sample[base_key], list):
            sample[base_key][index] = new_content
    else:
        sample[content_key] = new_content
    
    return sample


class BaseOp:
    """算子基类"""
    
    def __init__(self, name: str, col_name_map: Dict[str, str], *args, **kwargs):
        self.name = name
        self.col_name_map = col_name_map or {}

    def process_batched(self, samples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量处理"""
        new_samples = []
        for sample in samples:
            new_sample = self.process_single(sample)
            if new_sample is not None:
                new_samples.append(new_sample)
        return new_samples

    def process_single(self, sample: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        处理单个样本
        
        Args:
            sample: 输入样本
        
        Returns:
            处理后的样本，如果需要过滤则返回 None
        """
        raise NotImplementedError

    def get_content_from_sample(self, sample: Dict[str, Any]) -> str:
        """从样本中获取文本内容"""
        return get_content_from_sample(sample, self.col_name_map)

    def update_content(self, sample: Dict[str, Any], new_content: str) -> Dict[str, Any]:
        """更新样本中的文本内容"""
        return update_sample_content(sample, new_content, self.col_name_map)


class Mapper(BaseOp):
    """
    映射算子基类
    
    对数据进行清洗，修复错误的数据，不改变数据条数。
    """

    def __init__(self, name: str, col_name_map: Dict[str, str], *args, **kwargs):
        super().__init__(name, col_name_map, *args, **kwargs)


class Filter(BaseOp):
    """
    过滤算子基类
    
    当数据不符合要求时整条丢弃，如果符合要求则不对数据做任何改动。
    """

    def __init__(self, name: str, col_name_map: Dict[str, str], *args, **kwargs):
        super().__init__(name, col_name_map, *args, **kwargs)

    def is_bad_sample(self, sample: Dict[str, Any], *args, **kwargs) -> bool:
        """
        判断样本是否为坏样本
        
        Args:
            sample: 输入样本
        
        Returns:
            True 表示坏样本需要过滤，False 表示保留
        """
        raise NotImplementedError

    def process_single(self, sample: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        处理单个样本
        
        Returns:
            如果样本是坏样本返回 None，否则返回原样本
        """
        raise NotImplementedError


class BadLineFilter(Filter):
    """基于行级正则匹配的过滤器"""
    
    def __init__(self, name: str, col_name_map: Dict[str, str], *args, **kwargs):
        super().__init__(name, col_name_map, *args, **kwargs)
        self.badline_regex: List[str] = []

    def process_single(self, sample: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        content = self.get_content_from_sample(sample)
        for line in content.split("\n"):
            for bad_line_reg in self.badline_regex:
                if re.search(bad_line_reg, line) is not None:
                    return None
        return sample


class RemoveWordsMapper(Mapper):
    """基于正则匹配的文本清洗器"""
    
    def __init__(self, name: str, col_name_map: Dict[str, str]):
        self.words_to_remove_regex: List[str] = []  # 被正则命中部分会被删除
        self.line_to_remove_regex: List[str] = []   # 单行中出现正则命中内容则整行被删除
        self.lower_line_before_remove: bool = False # 匹配正则之前是否转小写
        self.words_to_new_words: Dict[str, str] = {}  # 将正则命中的文本替换成指定的字符串
        
        super().__init__(name, col_name_map)

    def repair_line(self, line: str) -> str:
        """修复单行文本"""
        for re_str in self.line_to_remove_regex:
            _line = line.lower() if self.lower_line_before_remove else line
            if re.findall(re_str, _line):
                return ""
        
        for re_str in self.words_to_remove_regex:
            line = re.sub(re_str, '', line)
        
        for old_words_reg, new_words in self.words_to_new_words.items():
            line = re.sub(old_words_reg, new_words, line)
        
        return line

    def clean(self, content: str) -> str:
        """清洗文本内容"""
        new_lines = []
        for line in content.split("\n"):
            new_line = self.repair_line(line)
            if new_line:
                new_lines.append(new_line)
        return "\n".join(new_lines)

    def process_single(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        content = self.get_content_from_sample(sample)
        new_content = self.clean(content)
        self.update_content(sample, new_content)
        return sample


__all__ = [
    "Registry",
    "TEXT_OPERATORS", 
    "BaseOp",
    "Mapper",
    "Filter",
    "BadLineFilter",
    "RemoveWordsMapper",
    "get_content_from_sample",
    "update_sample_content",
]
