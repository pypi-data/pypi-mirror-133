# -*- coding: UTF-8 -*-
"""vega FYI 

    @author: vegaviazhang
    @file:utils_universal.py
    @time:2022/01/05
"""
from datetime import date


def get_datatime_str(strf_str: str = "%Y-%m-%d") -> str:
    return date.today().strftime(strf_str)


if __name__ == '__main__':
    print(get_datatime_str())
