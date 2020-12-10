# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

from abc import ABCMeta, abstractmethod

import numpy


class AbsCrawler(metaclass=ABCMeta):
    app_key = ''
    
    def __init__(self):
        pass
    
    @classmethod
    def register_developer_ak(cls, app_key: str):
        cls.app_key = app_key

    @abstractmethod
    def crawling_prologue(self):
        pass

    @abstractmethod
    def crawling_process(self):
        pass

    @abstractmethod
    def crawling_epilogue(self):
        pass
