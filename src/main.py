# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

import json
import os
import time

from crawler.impl import RingsRoadCrawler
from utils.file_utils import time_str


def main():
    """
    构造爬虫；爬取并初步处理数据；处理、可视化最终数据并以 json 格式存储数据
    """
    DATA_PATH = os.path.abspath('../data')
    if not os.path.exists(DATA_PATH):
        DATA_PATH = os.path.abspath('./data')
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    
    # 构造爬虫，预备
    crawler = RingsRoadCrawler(timeout=20)
    crawler.register_developer_ak('0wem7DQG7HjCVpzKk5y8y3kGnhPmMFRk')
    all_params = crawler.crawling_prologue()
    
    # 10min 定时
    secs_10min = 600
    cnt = 0
    while True:
        cnt += 1
        print(f'{time_str()} 第{cnt}次爬取开始')
        # 爬取、初步处理数据
        raw_results, final_results = crawler.crawling_process(all_params)
    
        # 处理、以 json 格式存储数据、可视化
        save_path = os.path.join(DATA_PATH, time_str(in_fname=True))
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        crawler.crawling_epilogue(save_path, raw_results, final_results)
        print(f'{time_str()} 第{cnt}次爬取结束，等待十分钟后下次爬取 ...')
        time.sleep(secs_10min)
    
    # with open(r'C:\Users\16333\Desktop\PyCharm\crawler\data\12-11 17-47-09\最终数据.json', 'r', encoding='utf-8') as fp:
    #     final_results = json.load(fp)
    # crawler.visualize_final_results(final_results)


if __name__ == '__main__':
    main()
