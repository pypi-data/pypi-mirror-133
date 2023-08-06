# -*- coding: UTF-8 -*-
"""vega FYI 
    1.去除带有音标的符号
        来自transformers - transformers\tokenization_bert.py
        eg:[zhòngyīn]->[zhongyin]
    2.把空白符换成空格并删除控制符
        来自transformers - transformers\tokenization_bert.py

    @author: vegaviazhang
    @file:chinese_character_handler.py
    @time:2021/12/29
"""
import unicodedata


def _run_strip_accents(text):
    """vega FYI 去除带有音标的符号
        来自transformers - transformers\tokenization_bert.py
        eg:[zhòngyīn]->[zhongyin]
    """
    text = unicodedata.normalize("NFD", text)
    # print('unicodedata.normalize("NFD", text)', text)  # unicodedata.normalize("NFD", text) zhòngyīn
    output = []
    for char in text:
        cat = unicodedata.category(char)
        if cat == "Mn":
            continue
        output.append(char)
    return "".join(output)


def _is_control(char):
    """Checks whether `char` is a control character."""
    # These are technically control characters but we count them as whitespace
    # characters.
    if char == "\t" or char == "\n" or char == "\r":
        return False
    cat = unicodedata.category(char)
    if cat.startswith("C"):
        return True
    return False


def _is_whitespace(char):
    """Checks whether `char` is a whitespace character."""
    # \t, \n, and \r are technically contorl characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def _clean_text(text) -> str:
    """Performs invalid character removal and whitespace cleanup on text."""
    output = []
    for char in text:
        cp = ord(char)
        if cp == 0 or cp == 0xFFFD or _is_control(char):
            continue
        if _is_whitespace(char):
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)


def text_preprocess(raw_text):
    """vega FYI
        1.去除带有音标的符号
        2.替换无效字符换成空格，删除控制符
    """
    text = _run_strip_accents(raw_text)
    clean_str = _clean_text(text)
    return clean_str


if __name__ == '__main__':
    origin_text = "zhòngyīn@#Today is Sunday, \t I'm in here!!!"
    print(text_preprocess(origin_text))
