# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

from abc import ABCMeta, abstractmethod
from typing import Any, Tuple, List


class AbsCrawler(metaclass=ABCMeta):
    """
    爬虫抽象类，需要实现符合规范的爬虫方法
    """
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    
    def __init__(self):
        self.app_key = ''
    
    def register_developer_ak(self, app_key: str):
        """
        注册百度地图开放平台开发者的应用密钥
        :param app_key: 应用密钥字符串
        :return: 无返回
        """
        self.app_key = app_key
    
    @abstractmethod
    def crawling_prologue(self, *args, **kwargs) -> Any:
        """
        爬取前准备工作，包括链接自动生成、请求参数自动组合
        :param args: 任意可能的变长参数
        :param kwargs: 任意可能的键值对参数
        :return: 任意可能的返回
        """
        pass
    
    @abstractmethod
    def crawling_process(self, *args, **kwargs) -> Tuple[List, List]:
        """
        爬取过程，包括进行自动爬取、数据初步处理
        :param args: 任意可能的变长参数
        :param kwargs: 任意可能的键值对参数
        :return: 返回一个二元组，代表爬取原始数据和初步处理过的数据
        """
        pass
    
    @abstractmethod
    def crawling_epilogue(self, *args, **kwargs):
        """
        爬取后续，包括数据的进一步处理、运算、可视化分析，以及最终 json 格式的存储
        :param args: 任意可能的变长参数
        :param kwargs: 任意可能的键值对参数
        :return: 不需要返回
        """
        pass
