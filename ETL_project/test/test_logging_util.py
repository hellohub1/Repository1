from unittest import TestCase
from util.logging_util import init_my_logger
import logging


class TestLoggingUtil(TestCase):
    def setUp(self) -> None:
        # 可以把一些测试用的数据放到这里
        pass

    def test_init_my_logger(self):
        # 实际调用结果
        result = init_my_logger()
        # 期望的结果 返回是一个日志对象
        my_except = logging.RootLogger

        # 测试
        # 判断期望值和实际结果是否是一个数值
        # self.assertEqual()
        # 判断实际结果,期望值是否是同一个类型
        self.assertIsInstance(result, my_except)
