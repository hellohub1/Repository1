import os


# 获取所有的需要处理的json文件的绝对路径
def get_file_name(path="./"):
    """
    返回指定路径下的所有文件的绝对路径
    :param path: 指定路径
    :return: 列表[所有的文件的绝对路径]
    """
    # 获取所有的指定路径下的文件的名字
    file_names = os.listdir(path)
    # 存储所有的文件的绝对路径
    absolute_path_names = []
    # 获取绝对路径
    for name in file_names:
        # path ==> /Users/xiechen/Desktop/郑州303/day01/代码/01_josn数据
        # name ==> 'x01', 'x00', 'x02'
        absolute_path = f"{path}/{name}"
        absolute_path_names.append(absolute_path)

    return absolute_path_names


def get_need_process_file_name(a_list, b_list):
    """
    获取需要处理的文件的名字
    返回一个列表 存储就是需要处理的文件名
    :param a_list: 全部的文件名的列表
    :param b_list: 处理过的文件名的列表
    :return: 列表 需要处理的文件的名字
    """
    # 需要处理的文件名字
    need_process_list = []

    for i in a_list:
        # i ==> 所有文件名
        if i not in b_list:
            # 如果if语句成立 证明i这个文件没有处理过
            need_process_list.append(i)

    return need_process_list
