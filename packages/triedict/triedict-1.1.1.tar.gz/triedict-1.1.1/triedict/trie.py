# -*- coding: UTF-8 -*-
"""vega FYI 最大前向匹配的实现及实现

    @author: vegaviazhang
    @file:triedict.py
    @time:2021/10/04
"""
from typing import Union, List, Tuple, Set, Optional, Dict
from .projects.utils.chinese_character_handler import text_preprocess
from .projects.utils.utils_chinese import is_contain_english, check_english_word
from .projects.utils.utils_universal import get_datatime_str


class TrieDict:
    def __init__(
            self,
            stop_chars: Union[str, List, Tuple, Set] = None,
            corpus_no_english_word=True,
            case_ignored=True
    ):
        """vega FYI
            self.stop_chars               忽略掉的字符
            self.case_ignored:            是否忽略英文字母大小写
            self.trie:                    关键字典树
            self.item_tuple_flag:         传入的text是否携带其他备注信息
            self.corpus_no_english_word   传入的词典中是否携带英文单词
        """
        if stop_chars is None:
            stop_chars = ''
        self.stop_chars = stop_chars
        self.case_ignored = case_ignored
        self.trie = {}
        self.item_tuple_flag = False
        self.corpus_no_english_word = corpus_no_english_word

    def init_or_insert_dict(
            self,
            items: Union[List, Tuple, Set],
            text_preprocess_flag: bool = False,
            log_info: bool = True,
    ) -> None:
        """vega FYI 初始化字典树或者扩充字典树
            text_preprocess_flag: 处理中文重音符、不可见字符等
        """
        for item in items:
            self.item_tuple_flag = isinstance(item, Tuple) or isinstance(item, List)
            if self.item_tuple_flag:
                raw_text, text_info = item
            else:
                raw_text = item
            raw_text = raw_text.strip()
            if text_preprocess_flag:
                raw_text = text_preprocess(raw_text)
            if not raw_text:
                continue
            curr_trie = self.trie
            raw_text = raw_text.lower() if self.case_ignored else raw_text
            if self.corpus_no_english_word and is_contain_english(raw_text):
                self.corpus_no_english_word = False
            for sub_char in raw_text:
                if sub_char not in self.stop_chars:
                    curr_trie = curr_trie.setdefault(sub_char, {})
            if self.item_tuple_flag:
                curr_trie["whole_word"] = [raw_text, text_info]  # noqa
            else:
                curr_trie["whole_word"] = raw_text
        if log_info:
            print(f"[info] \033[33m本次[{get_datatime_str()}]实例化的字典树匹配信息如下:\033[0m\n"
                  f"[info] \t\tstop_chars [过滤掉的字符集]: {self.stop_chars}\n"
                  f"[info] \t\titem_tuple_flag [term中是否带备注信息]: {self.item_tuple_flag}\n"
                  f"[info] \t\tcorpus_no_english_word[词典中是否带有英文词]: {self.corpus_no_english_word}\n"
                  f"[info] \t\tcase_ignored [是否忽略字母大小写]: {self.case_ignored}")

    def get_match(self, text: str) -> Tuple[Union[None, str], int]:
        """vega FYI 从头开始匹配，匹配到一个就返回，相当于 re.match
            从text的开始往后匹配,返回匹配到的内容和序号
        """
        curr_trie, longest_match, offset = self.trie, None, 0
        if not text:
            return longest_match, offset
        text = text.lower() if self.case_ignored else text
        for idx, sub_char in enumerate(text):
            if sub_char not in self.stop_chars:
                if sub_char not in curr_trie:
                    return longest_match, offset
                curr_trie = curr_trie[sub_char]
                if "whole_word" in curr_trie:
                    longest_match, offset = curr_trie["whole_word"], idx + 1
        return longest_match, offset

    def check_exist(self, text: str) -> Tuple[bool, Optional[str]]:
        """vega FYI 判断text是否在字典树中
            从text的idx 0往后匹配,如果没有匹配到，
            接着从1开始匹配，如果匹配到了，
            假设长度为3，继续从索引3开始匹配
        """
        word_exist_bool, first_match_word = False, None
        text = text.lower() if self.case_ignored else text
        text_len = len(text)
        start_offset = 0
        while start_offset <= text_len - 1:
            sub_text = text[start_offset:]
            temp_word, curr_trie = "", self.trie
            for sub_char in sub_text:
                if sub_char not in self.stop_chars:
                    if sub_char not in curr_trie:
                        break
                    curr_trie = curr_trie[sub_char]
                    if "whole_word" in curr_trie:
                        temp_word = curr_trie["whole_word"]
            if temp_word:
                word_exist_bool = True
                first_match_word = temp_word
                break
            else:
                start_offset += 1
        return word_exist_bool, first_match_word

    def get_match_words(
            self,
            text: str,
            return_offset: bool = True,
            all_chinese_character: bool = None,
            log_info: bool = False
    ) -> List[Dict]:
        """vega FYI
            核心逻辑：从text的idx 0往后匹配,如果没有匹配到，
                接着从1开始匹配，如果匹配到了，
                假设长度为3，继续从索引3开始匹配

            注：start_offset:int, end_offset:int: 含左不含右
        """
        # [info] 判断text是否含有英文，如果含有英文要对匹配出的单词进行检测
        english_flag = True
        contain_english = is_contain_english(text)
        if self.corpus_no_english_word or all_chinese_character is None and not contain_english:
            english_flag = False
        if log_info:
            print(f"[info] \033[33m含有英文词汇情况: \033[0m\n"
                  f"[info] 字典树中是否含有英文词汇: {not self.corpus_no_english_word}\n"
                  f"[info] 待匹配文本中是否含有英文词汇: {contain_english}\n"
                  f"[info] 是否需要对匹配出的word进行核验: {english_flag}")

        # [info] 返回匹配到的索引  + 部分有term_info，部分没有term_info
        match_words_list = []
        text = text.lower() if self.case_ignored else text
        text_len = len(text)
        start_offset = 0
        while start_offset <= text_len - 1:
            sub_text = text[start_offset:]
            temp_word, curr_trie = "", self.trie
            for sub_char in sub_text:
                if sub_char not in self.stop_chars:
                    if sub_char not in curr_trie:
                        break
                    curr_trie = curr_trie[sub_char]
                    if "whole_word" in curr_trie:
                        temp_word = curr_trie["whole_word"]
            if temp_word and english_flag:
                if not self.item_tuple_flag:
                    temp_word = check_english_word(text, temp_word, start_offset, start_offset + len(temp_word))
                else:
                    temp_word, term_info = temp_word[0], temp_word[1]
                    temp_word = check_english_word(text, temp_word, start_offset, start_offset + len(temp_word))
                    if temp_word:
                        temp_word = (temp_word, term_info)
            if temp_word:
                word_start_offset = start_offset
                if self.item_tuple_flag:
                    word_length = len(temp_word[0])
                    word_end_offset = word_start_offset + word_length
                    item_match_info = {
                        "id": len(match_words_list) + 1,
                        "term": temp_word[0],
                        "start_offset": word_start_offset,
                        "end_offset": word_end_offset,
                        "term_info": temp_word[1],
                        "term_len": word_length
                    }
                else:
                    word_length = len(temp_word)
                    word_end_offset = word_start_offset + word_length
                    item_match_info = {
                        "id": len(match_words_list) + 1,
                        "term": temp_word,
                        "start_offset": word_start_offset,
                        "end_offset": word_end_offset,
                        "term_len": word_length
                    }
                match_words_list.append(item_match_info)
                start_offset += word_length
            else:
                start_offset += 1
        return match_words_list
