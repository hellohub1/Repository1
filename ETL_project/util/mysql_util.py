import pymysql
from config import project_config as conf
from util.logging_util import init_my_logger

# 日志对象
logger = init_my_logger()


class MySqlUtil:
    def __init__(self,
                 host=conf.host,
                 port=conf.port,
                 user=conf.user,
                 passwd=conf.passwd,
                 charset=conf.charset,
                 autocommit=conf.autocommit
                 ):
        # 创建链接
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            charset=charset,
            # 数据库中增删改操作不会自动提交
            autocommit=autocommit
        )

        logger.info(f"创建链接{host}:{port}//{user}, 成功!!!")

    def close_conn(self):
        """关闭连接"""
        # self.conn.open : True代表没有关闭数据库
        # self.conn.open : False代表数据库关闭
        if self.conn.open:
            # 如果if语句成立证明 数据库没有关闭
            self.conn.close()

        logger.info("~~关闭了链接~~")

    def select_db(self, db):
        """
        切换数据库
        :param db: 要选择的数据
        :return:None
        """
        self.conn.select_db(db)

        logger.info(f"切换了数据库{db}")

    def query(self, sql):
        """
        执行查询的sql语句 返回查询结果
        :sql: 查询的sql语句
        :return: 查询结果 ((),(),())
        """
        # 创建游标
        cur = self.conn.cursor()
        # 执行sql
        cur.execute(sql)
        # 获取数据
        # data ==> ((),(),())
        data = cur.fetchall()
        # 关闭游标
        cur.close()
        # 我们现在的日志级别20
        logger.debug(f"执行了查询的sql{sql}")
        # 把查询出来的数据返回
        return data

    def execute(self, sql):
        """
        执行增删改这些sql  create table 并且可以自动提交(不管数据设置自动提交与否 execute都会自动提交)
        :sql: 增删改的sql
        :return: None
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        # 判断这个数据库是否设置了自动提交
        # get_autocommit()可以获取是否自动提交
        # self.conn.get_autocommit(): 如果设置了自动提交 True
        # self.conn.get_autocommit(): 如果没有设置自动提交 False
        if not self.conn.get_autocommit():
            # 如果if成立 证明数据库没有设置自动提交
            # 手动提交
            self.conn.commit()

        cur.close()

        logger.info(f"执行了execute方法 sql为{sql}")

    def execute_without_autocommit(self, sql):
        """
        执行增删改这些sql  create table
        不会自动提交(前提 数据库本身就没有设置自动提交)
        :sql: 增删改的sql
        :return: None
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()

        logger.info(f"执行了execute_without_autocommit方法 sql为{sql}")

    def check_table_exists(self, db_name, table_name):
        """
        用来检查某个数据库中是否存在某个数据表
        如果存在返回True
        如果不存在返回False
        :db_name:数据库名
        :table_name: 数据表名
        :return: True/False
        """
        # 切换数据库
        self.select_db(db_name)
        # 查询所有的数据表
        # 数据表table_name ==> a
        # ret ==> ((a,),(b,),(c,))
        # (a,) in ((a,),(b,),(c,))
        ret = self.query("show tables;")
        # 如果数据表存在 my_ret为 True
        # 如果数据表不存在 my_ret为 False
        my_ret = (table_name,) in ret

        return my_ret

    def check_table_exists_and_create(self, db_name, table_name, create_cols):
        """
        检查数据表是否存在 如果不存在直接创建这个数据表
        :db_name: 数据库名
        :table_name: 数据表名
        :create_cols: 数据表的字段(字段名 字段类型 约束)
        :return: None
        """
        if not self.check_table_exists(db_name, table_name):
            # 如果if语句成立 证明表不存在 那么创建数据表
            sql = f"create table {table_name}({create_cols});"
            self.execute(sql)
            logger.info(f"在{db_name}创建了数据表{table_name}")
        else:
            # 数据表存在
            logger.warning(f"在{db_name}已经存在了数据表{table_name},故没有进行数据表的创建")


def get_processed_file_list(db_util, db_name, table_name, create_cols):
    """
    从metadata元数据库中获取处理过的文件的名字
    :param db_util: 数据库对象
    :param db_name: 数据库名
    :param table_name: 数据表名
    :param create_cols: 创建数据表的字段
    :return: 列表 ["文件名","文件名"]
    """
    # 创建数据表file_check
    db_util.check_table_exists_and_create(
        db_name,
        table_name,
        create_cols
    )
    # 查询file_check中有哪些文件名
    # 返回值的类型是
    # (('/Users/xiechen/Desktop/郑州303/day02/01_josn数据/x00',),(b,),(c,))
    processed_file_name = db_util.query(f"select file_name from {table_name};")
    # 存储都是处理过的文件的名字了
    processed_file_list = []
    for i in processed_file_name:
        # i ==> (b,)
        # i ==> ('/Users/xiechen/Desktop/郑州303/day02/01_josn数据/x00',)
        # i[0] ==> b  '/Users/xiechen/Desktop/郑州303/day02/01_josn数据/x00'
        processed_file_list.append(i[0])
    # 返回列表
    return processed_file_list


if __name__ == '__main__':
    db_util = MySqlUtil()
    db_util.check_table_exists_and_create(
        "zhengzhou",
        "student",
        """
            id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(30) NOT NULL
        """
    )
