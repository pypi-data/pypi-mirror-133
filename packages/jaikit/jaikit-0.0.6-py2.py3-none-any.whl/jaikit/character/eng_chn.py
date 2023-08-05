from jaikit.character.unicode import WIKI_UNICODE_INFO
from itertools import chain
from typing import Set, Optional


# 包含汉字的区段
CHN_PART = WIKI_UNICODE_INFO.loc[WIKI_UNICODE_INFO["文字"].str.contains("汉字", na=False)]
CHINESE_ORDS: Set[int] = {
    _
    for _ in chain(
        *(range(item["start"], item["end"] + 1) for idx, item in CHN_PART.iterrows())
    )
}
REMOVE_CHINESE_MAP = {_: "" for _ in CHINESE_ORDS}


def contains_chinese(text: str) -> bool:
    """基于Unicode字符集的汉字所涉及范围，判断一个字符串是否含有汉字"""
    return any((ord(character) in CHINESE_ORDS for character in text))


def remove_chinese(text: str) -> str:
    """基于Unicode码表汉字区段，从字符串中删除所有汉字"""
    return text.translate(REMOVE_CHINESE_MAP)


def chinese_eng_boundary(text: str) -> Optional[int]:
    """对于含中英内容的字符串，返回第一个汉字的位置索引"""
    for idx, character in enumerate(text):
        if ord(character) in CHINESE_ORDS:
            return idx
    return None
