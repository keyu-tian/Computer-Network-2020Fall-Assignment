# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

import datetime
import json
import os


def time_str(in_fname=False) -> str:
    """
    获取统一格式的时间字符串
    :param in_fname: 是否需要考虑文件名合法
    :return: 时间字符串
    """
    return (
        datetime.datetime.now().strftime('%m-%d %H-%M-%S') if in_fname
        else datetime.datetime.now().strftime('[%m-%d %H:%M:%S]')
    )


def dump_json(json_like_data, save_path: str, fname_prefix: str):
    """
    集中以 json 格式存储文件
    :param json_like_data: json 格式的数据
    :param save_path: 存储路径
    :param fname_prefix: 文件名前缀（后缀为.json 自动补充）
    :return: 无返回
    """
    with open(os.path.join(save_path, f'{fname_prefix}.json'), 'w', encoding='utf-8') as fp:
        json.dump(json_like_data, fp, ensure_ascii=False, indent=2)
