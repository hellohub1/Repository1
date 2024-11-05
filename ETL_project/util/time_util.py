import time


# 10位时间戳的转化
# time_01 = time.time()
# time_02 = time.localtime(time_01)
# time_03 = time.strftime("%Y-%m-%d %H:%M:%S", time_02)
# 时间戳 10位 以秒为单位
# 时间戳 13位 以毫秒为单位

def ts13_to_date_str(data):
    """
    把13位的时间戳(data)转化为具体的时间  2020-09-01 03:10:23
    :param data: 13位的时间戳
    :return: 字符串 "2020-09-01 03:10:23"
    """
    # 13位转化为10位
    data = data / 1000
    time_01 = time.localtime(data)
    time_02 = time.strftime("%Y-%m-%d %H:%M:%S", time_01)

    return time_02


if __name__ == '__main__':
    data = 1540619466000
    print(ts13_to_date_str(data))
