# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

import os


def depth_first_search(cwd, upd_fn):
    """
    辅助函数，使用深度优先搜索递归遍历符合条件的文件并进行相关处理
    :param cwd:
    :param upd_fn:
    :return:
    """
    file_names = os.listdir(cwd)
    for name in file_names:
        path = os.path.join(cwd, name)
        if os.path.isdir(path):
            depth_first_search(path, upd_fn)
        else:
            if name.endswith('.py'):
                upd_fn(path)


if __name__ == '__main__':
    
    cp = """# 2020/12/01
# Copyright by Keyu Tian, College of Software, Beihang University.
# This file is a part of my crawler assignment for Computer Network.
# All rights reserved.

"""
    
    def upd(path):
        with open(path, 'r', encoding='utf-8') as fp:
            ctt = fp.read()
        if not ctt.startswith(cp):
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(cp + ctt)
    
    depth_first_search(os.getcwd(), upd)
    

