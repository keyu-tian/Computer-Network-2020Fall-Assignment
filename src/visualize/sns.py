# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from data_cleaning.convert import dist_key, speed_key, road_name_and_num_key, road_dir_key, road_num_key, road_name_key, trend_key


def render(figure_name: str):
    """
    使用 Matplotlib 框架展示所绘制的图
    :param figure_name: 图的题名
    :return: 无返回
    """
    # ax = plt.gca()
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['font.family'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    if figure_name is not None:
        plt.title(figure_name, pad=33, fontdict={'size': 24})
    plt.show()


def vis_bins(df: pd.DataFrame, val_key, figname: str, rev=False):
    """
    可视化箱线图（类似条形图；但通过了额外的黑线段对数据的离散程度进行了描述）
    :param df: 数据帧
    :param val_key: 被考虑的数值键
    :param figname: 图的标题
    :param rev: 色系是否翻转（是则为蓝绿，否则为红橙）
    :return: 无返回
    """
    sns.set(
        palette=sns.color_palette(f'Spectral{"_r" if rev else ""}', n_colors=len(set(df[road_name_and_num_key]))),
        # palette=sns.cubehelix_palette(n_colors=len(candidates), start=0.6, rot=.2, light=.77),
        # palette=sns.cubehelix_palette(n_colors=len(candidates), start=.2, rot=-.3, light=.77),
        # palette=sns.hls_palette(len(candidates), h=0.01, l=0.4, s=0.8),
        style='ticks',
    )
    sns.set_context(context='talk', font_scale=1.5)
    sns.barplot(
        x=road_dir_key, y=val_key, hue=road_num_key,
        # hue_order=candidates,
        data=df,
    )
    sns.despine()
    
    # plt.xlabel(, labelpad=20)
    # plt.ylabel(val_key, labelpad=20)
    
    render(figure_name=figname)


def vis_correlations(df: pd.DataFrame, figname: str):
    """
    可视化相关性图（自动拟合回归曲线；阴影部分为置信区间）
    :param df: 数据帧
    :param figname: 图的标题
    :return: 无返回
    """
    sns.set(
        # palette='Blues_r',
        style='darkgrid'
    )
    
    sns.lmplot(
        x=dist_key, y=speed_key,
        col=road_name_key, col_wrap=2,
        data=df,
    )

    sns.despine(right=True, top=True)

    render(figure_name=None)


def vis_heat_map(heat_map_ndarray: np.ndarray, figname: str, cmap='Blues', normalize=False):
    """
    可视化热力图，用于非常直观地绘制二、三、四、五环的拥堵状况
    :param heat_map_ndarray: 热力图的多维数组
    :param figname: 图的标题
    :param cmap: 色系
    :param normalize: 是否需要自动归一化
    :return: 无返回
    """
    if normalize:
        mi, ma = heat_map_ndarray.min(), heat_map_ndarray.max()
        heat_map_ndarray = (heat_map_ndarray - mi) / (ma - mi)

    sns.set(style='white')
    sns.set_context(context='talk', font_scale=1)
    g = sns.heatmap(
        heat_map_ndarray,
        # vmax=1,
        # vmin=0,
        annot=False,
        fmt='d',
        cmap=cmap,
        linewidths=0.1,
    )
    g.set(xticklabels=[], yticklabels=[])
    plt.xticks(rotation=40, fontsize=18)
    # plt.xlabel('date', fontdict={'size': 20}, labelpad=10)
    # plt.ylabel('province', fontdict={'size': 20}, labelpad=13)
    render(figname)
