# 这是一个日志工具
import logging
from config import project_config as conf


class LoggingUtil:
    # init是用来初始化实例对象的
    def __init__(self, level=20):
        # 实例属性
        self.logger = logging.getLogger()
        # 设置默认日志级别
        self.logger.setLevel(level)


def init_my_logger():
    """
    通过这个方法 可以直接获取一个设置好日志级别的日志对象
    :return: 日志对象
    """

    # 1. 获取了一个设置好日志级别的日志对象
    logger = LoggingUtil().logger

    # logger.handlers 如果 给logger设置过了 handler日志的输出方式 : True
    # logger.handlers 如果没有设置 : False
    if logger.handlers:
        # 如果if语句成立 证明 logger日志已经设置过handler
        # 那就没有必要再设置一回了
        return logger

    # 2. handler
    file_handler = logging.FileHandler(
        # /Users/xiechen/Desktop/郑州303/day01/代码/logs/py_etl_2023_05_09_04.log
        filename=f"{conf.log_file_root_path}/{conf.log_name}",
        mode="a",
        encoding="utf8"
    )
    # 3. 格式对象
    fmt = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(filename)s[%(lineno)d]: %(message)s"
    )
    # 4. 添加格式
    file_handler.setFormatter(fmt)
    # 5. 添加handler
    logger.addHandler(file_handler)

    return logger


if __name__ == '__main__':
    a = init_my_logger()
    # logging.RootLogger ==> 日志对象类型
    print(type(a))