# -*- coding: UTF-8 -*-
"""vega FYI 

    @author: vegaviazhang
    @file:utils_chinese.py
    @time:2022/01/04
"""
from typing import Union, Tuple

chinese_single_char = "，。~！@#￥%……&*（）——{}|“：”‘’？》《、"
english_char_set = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                    "u", "v", "w", "x", "y", "z"}


def is_contain_chinese(text: str) -> bool:
    """vega FYI
    检查整个字符串是否只包含包含中文，或者中文符号
    需要检查的字符串
    """
    for ch in text:
        if u'\u4e00' <= ch <= u'\u9fff' or ch in chinese_single_char:
            return True
    return False


def is_contain_english(text: str) -> bool:
    """vega FYI
    检查整个字符串是否包含英文
    需要检查的字符串
    """
    if set(text.lower()) & english_char_set:
        return True
    return False


def check_english_word(text: str, word: Union[str, Tuple], start_offset: int, end_offset: int) -> str:
    """vega FYI
        核心逻辑：判断前一个字符或者后一个字符是否为英文即可
    """
    start_char_is_non_alpha = (start_offset == 0) or not is_contain_english(text[start_offset - 1])
    end_char_is_non_alpha = (end_offset == len(text)) or not is_contain_english(text[end_offset])
    if start_char_is_non_alpha and end_char_is_non_alpha:
        return word
    else:
        return ""


if __name__ == '__main__':
    # print(is_contain_chinese("，。"))
    print(is_contain_english("，。"))
    print(is_contain_english("今天成立了l。"))  # True
