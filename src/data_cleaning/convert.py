# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

from collections import defaultdict
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd

road_name_key = '环路名'        # 二环，三环
road_dir_key = '环路方位'       # 东，南，西，北
road_num_key = '环路编号'       # 二，三，四，五
road_name_and_num_key = '环路段'   # 东二环，西三环
dist_key = '拥堵路段长度'
dist_sum_key = '环路拥堵总长'
speed_key = '平均拥堵时速'
status_key = '拥堵程度'
trend_key = '拥堵趋势'


def to_data_frame_dict(final_results: List[Dict]) -> dict:
    """
    将最终结果（json解析后的对象格式）转换为 Pandas 框架需要的二维数据帧格式。
    过程中会进行数据清洗，自动过滤并处理不存在拥堵的情况。
    :param final_results: 最终结果（json解析后的对象格式）
    :return: Pandas 框架需要的二维数据帧字典
    """
    df_dict = defaultdict(list)
    
    dist_sums = defaultdict(int)
    
    def insert_ring_road_data(json_element: dict):
        ring_name, congestion_elements = json_element.values()
        subroad_name = ring_name
        road_name = ring_name[1:]
        
        def apply_insertion(road_name, subroad_name, dist, speed, status, trend):
            df_dict[road_name_key].append(road_name)
            df_dict[road_dir_key].append(subroad_name[0])
            df_dict[road_num_key].append(subroad_name[1])
            df_dict[road_name_and_num_key].append(subroad_name)
            df_dict[dist_key].append(dist)
            df_dict[speed_key].append(speed)
            df_dict[status_key].append(status)
            df_dict[trend_key].append(trend)
        
        for con in congestion_elements:
            dist, speed, status, trend = (
                con['拥堵路段长度'], con['平均拥堵时速'],
                con['拥堵状态'], con['拥堵趋势']
            )
            dist_sums[road_name] += dist
            apply_insertion(road_name, subroad_name, dist, speed, status, trend)
        
        # 进行数据清洗，自动过滤并处理不存在拥堵的情况
        if len(congestion_elements) == 0:
            dist, speed = 0, 0
            status, trend = '畅通', '无拥堵'
            dist_sums[road_name] += dist
            apply_insertion(road_name, subroad_name, dist, speed, status, trend)
    
    for res in final_results:
        insert_ring_road_data(res)
    
    for road_name in df_dict[road_name_key]:
        df_dict[dist_sum_key].append(dist_sums[road_name])
    
    return df_dict


def to_data_frame(df_dict: dict):
    """
    将字典型数据转换为 Pandas 框架的数据帧
    """
    return pd.DataFrame(data=df_dict, index=None)


def to_heat_map_ndarray(df_dict: dict, core_w=2) -> Tuple[np.ndarray, np.ndarray]:
    """
    将字典型数据转换为适用于热力图的 Numpy 框架多维数组
    """
    subroad_name_key = '环路段'
    dist_key = '拥堵路段长度'
    speed_key = '平均拥堵时速'
    
    dists, speeds = defaultdict(list), defaultdict(list)
    for subroad_name, dist, speed in zip(df_dict[subroad_name_key], df_dict[dist_key], df_dict[speed_key]):
        dists[subroad_name].append(dist)
        speeds[subroad_name].append(speed)
    
    dist_core = np.zeros((2 * core_w, 2 * core_w))
    speed_core = dist_core.copy()
    
    def avg(li):
        return sum(li) / len(li) if len(li) else 0
    
    for num in range(2, 6):
        ch = {
            2: '二', 3: '三', 4: '四', 5: '五',
        }[num]
        dist_core = np.pad(dist_core, core_w, constant_values=[
            [sum(dists[f'北{ch}环']) / 1000, sum(dists[f'南{ch}环']) / 1000],
            [sum(dists[f'西{ch}环']) / 1000, sum(dists[f'东{ch}环']) / 1000]
        ])
        speed_core = np.pad(speed_core, core_w, constant_values=[
            [avg(speeds[f'北{ch}环']), avg(speeds[f'南{ch}环'])],
            [avg(speeds[f'西{ch}环']), avg(speeds[f'东{ch}环'])]
        ])
    
    return dist_core, speed_core
