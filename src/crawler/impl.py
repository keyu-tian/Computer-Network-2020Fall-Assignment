# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

import itertools as itt
import json
from collections import defaultdict
from typing import List, Dict, Tuple

import requests
from tqdm import tqdm

from crawler.interface import AbsCrawler
from data_cleaning.convert import to_data_frame_dict, to_heat_map_ndarray, to_data_frame, dist_key, speed_key
from utils.file_utils import dump_json
from visualize.sns import vis_heat_map, vis_correlations, vis_bins


class RingsRoadCrawler(AbsCrawler):
    """
    环路的拥堵路况爬虫实现类，实现了对北京市二、三、四、五环各自的路段（东、南、西、北段）的集成爬取。
    """
    
    def __init__(self, timeout=20):
        """
        初始化爬虫
        :param timeout: 爬取的最长等待时间
        """
        super(RingsRoadCrawler, self).__init__()
        self.timeout = timeout
        
        self.ring_nums = list(range(2, 6))
        self.num_to_ch = {2: '二', 3: '三', 4: '四', 5: '五'}
        self.ch_to_num = {v: k for k, v in self.num_to_ch.items()}
        self.directions = ['东', '南', '西', '北']
        ring_names = itt.product(
            self.num_to_ch.values(),
            self.directions
        )
        self.ring_names = list(
            map(
                lambda tup: ''.join(tup[::-1]) + '环',
                ring_names
            )
        )
    
    def generate_road_name_lists(self) -> List[List[str]]:
        """
        自动排列组合生成路段名（二、三、四、五环各自的东、南、西、北段）
        :return: 路段名列表
        """
        tails = {
            2: defaultdict(list),
            3: {'东': ['南', '北'], '南': ['东', '西'], '西': ['南', '北'], '北': ['东', '西']},
            4: {'东': ['南', '北'], '南': ['东', '西'], '西': ['南', '北'], '北': ['东', '西']},
            5: defaultdict(list),
        }
        road_name_lists = []
        for num in self.ring_nums:
            ch_num = self.num_to_ch[num]
            for d in self.directions:
                suffixes = tails[num][d]
                if len(suffixes):
                    road_name_lists.append([f'{d}{ch_num}环{s}{"" if num == 2 else "路"}' for s in suffixes])
                else:
                    road_name_lists.append([f'{d}{ch_num}环{"" if num == 2 else "路"}'])
        return road_name_lists
    
    def crawling_prologue(self) -> List[List[Dict]]:
        """
        爬取前的预处理，自动生成待爬取的请求并返回请求列表
        :return: 请求参数列表（每个列表中有一个或多个爬取请求参数）
        """
        all_params = []
        for road_name_list in self.generate_road_name_lists():
            paras = [
                {
                    'ak': self.app_key,
                    'road_name': road_name,
                    'city': '110000',
                } for road_name in road_name_list
            ]
            all_params.append(paras)
        
        return all_params
    
    def data_cleaning(self, json_result: dict, congestion_elements: list):
        """
        进行数据清洗（初步处理）
        :param json_result: 爬取的原始数据
        :param congestion_elements: 存放处理过的清洁数据的容器
        :return: 无返回
        """
        results: List[Dict] = json_result.get('road_traffic', [])
        if len(results) == 0:
            return []  # 过滤失效数据
        
        for result in results:
            congestion_sections = result.get('congestion_sections', [])
            for sec in congestion_sections:
                congestion_elements.append({
                    '拥堵路段长度': sec['congestion_distance'],  # 拥堵路段长度, int
                    '平均拥堵时速': sec['speed'],  # 平均通行速度, float
                    '拥堵状态': {
                        0: '未知',
                        1: '稍缓',
                        2: '缓行',
                        3: '拥堵',
                        4: '严重拥堵',
                    }[sec['status']],
                    '拥堵趋势': sec['congestion_trend'],  # 发展态势中文描述: 持平; 缓解; 加重
                    '情况描述': sec['section_desc'],  # 具体区域中文描述
                })
    
    def crawling_process(self, all_params) -> Tuple[List, List]:
        """
        爬取过程，按照提供的参数列表逐个爬取（自动聚合列表中的多个参数）
        :param all_params: 提供的参数列表（每个列表中有一个或多个爬取请求参数）
        :return: 返回一个二元组，代表爬取原始数据和初步处理过的数据
        """
        raw_results = []
        final_results = []
        n = len(all_params)
        for i in tqdm(range(n)):
            params = all_params[i]
            ring_name = self.ring_names[i]
            congestion_elements = []
            
            for param in params:
                html_result = requests.get(
                    'http://api.map.baidu.com/traffic/v1/road',
                    params=param, headers=AbsCrawler.request_headers,
                    timeout=self.timeout
                )
                json_result = json.loads(html_result.text)
                raw_results.append(json_result)
                self.data_cleaning(json_result, congestion_elements)
            
            final_results.append({'环路名称': ring_name, '环路拥堵状态': congestion_elements})
        
        return raw_results, final_results
    
    def crawling_epilogue(self, save_path, raw_results, final_results):
        """
        爬取后续，包括数据的进一步处理、运算、可视化分析，以及最终 json 格式的存储
        :param save_path: 存储最终 json 数据的路径
        :param raw_results: 爬取原始数据
        :param final_results: 初步处理过的数据
        :return: 不需要返回
        """
        dump_json(raw_results, save_path=save_path, fname_prefix='原始数据')
        dump_json(final_results, save_path=save_path, fname_prefix='最终数据')
        
        self.visualize_final_results(final_results)
    
    def visualize_final_results(self, final_results):
        """
        可视化分析最终数据
        :param final_results: 最终数据
        :return: 无返回
        """
        df_dict = to_data_frame_dict(final_results)
        dist_heat_map, speed_heat_map = to_heat_map_ndarray(df_dict)
        df = to_data_frame(df_dict)
        
        vis_bins(df, dist_key, '拥堵距离统计', rev=False)
        vis_bins(df, speed_key, '拥堵时速统计', rev=True)
        vis_correlations(df, '拥堵距离与拥堵时速相关性一览')
        vis_heat_map(dist_heat_map, '各环拥堵距离(km)一览', cmap='Reds')
        vis_heat_map(speed_heat_map, '各环拥堵时速(km/h)一览', cmap='Blues')
