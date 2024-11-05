# 需求一的所有的业务代码
from util.logging_util import init_my_logger
from util.file_util import get_file_name, get_need_process_file_name
from config import project_config as conf
from util.mysql_util import MySqlUtil, get_processed_file_list
from model.json_model import OrdersModel, OrdersDetailModel

# todo 开启日志功能
logger = init_my_logger()
logger.info("~~~~~日志开启成功~~~~~")

# todo 获取需要处理的json文件的绝对路径
json_file_names = get_file_name(conf.json_file_root_path)
logger.info(f"获取到了需要处理的文件的名字{json_file_names}")

# todo 从metadata数据库中获取处理过的json文件的名字
# 创建数据库对象
db_util = MySqlUtil()
# 获取处理过的文件列表
processed_file_list = get_processed_file_list(
    db_util,
    conf.metadata_db_name,
    conf.metadata_file_check_table_name,
    conf.metadata_file_check_create_cols
)

# todo 获取需要处理的json文件名字
need_process_file_list = get_need_process_file_name(json_file_names, processed_file_list)
print("需要处理的文件名:", need_process_file_list)
logger.info(f"需要处理的文件名:{need_process_file_list}")

# todo 在retail数据库中创建 orders和orders_detail数据表 用来存储json文件中的数据
# 检查orders表是否存在 不存在就创建
db_util.check_table_exists_and_create(
    conf.target_db_name,
    conf.target_orders_table_name,
    conf.target_orders_table_create_cols
)
# 检查orders_detail表是否存在 不存在就创建
db_util.check_table_exists_and_create(
    conf.target_db_name,
    conf.target_orders_detail_table_name,
    conf.target_orders_detail_table_create_cols
)

# todo 处理json文件
# key: path json文件的绝对路径
# value: 数量
path_count = {}
# 希望能够让文件中的所有的数据 ==> 插入到数据库中的sql语句
for path in need_process_file_list:
    # 打开一个文件用来存储csv数据
    orders_f = open(f"{conf.csv_file_root_path}/{conf.csv_order_file_name}", "a", encoding="utf8")
    orders_detail_f = open(f"{conf.csv_file_root_path}/{conf.csv_order_detail_file_name}", "a", encoding="utf8")
    # 计数
    count = 0
    # path ==> /Users/xiechen/Desktop/郑州303/day02/代码/01_josn数据/x00
    # line ==> "{age:19,name:'123'}" 订单数据
    for line in open(path, "r", encoding="utf8"):
        # 计数
        count += 1
        # todo 创建模型对象
        # 创建一个orders模型对象
        orders_model = OrdersModel(line)
        # 创建一个orders_detail模型对象
        orders_detail_model = OrdersDetailModel(line)
        # todo A orders表的csv和sql转化
        # to_csv() 把一个订单数据 转化为了 csv字符串
        csv_orders_line = orders_model.to_csv()
        # 把csv_orders_line存储到csv文件里
        orders_f.write(csv_orders_line + "\n")
        # 生成一个插入到orders表的 插入的sql语句
        orders_sql = orders_model.to_sql()
        # 只是执行sql不提交数据
        db_util.execute_without_autocommit(orders_sql)
        # todo B orders_detail表的csv和sql转化
        csv_orders_detail_line = orders_detail_model.to_csv()
        orders_detail_sql = orders_detail_model.to_sql()
        # 把csv存储
        orders_detail_f.write(csv_orders_detail_line)
        # 执行插入的sql语句
        db_util.execute_without_autocommit(orders_detail_sql)

    # 记录
    # path_count ==> {"d://abc//bb/x00":1024}
    path_count[path] = count
    # 关闭文件(把数据真正的存储到文件中)
    orders_f.close()
    orders_detail_f.close()
    # 手动提交数据
    db_util.conn.commit()

# todo 把处理后的json文件名保存到<元数据库>中<file_check>数据表
# 切换到元数据库
db_util.select_db(conf.metadata_db_name)
# 文件名字 文件的订单数量
for json_path, json_count in path_count.items():
    sql = f"insert into file_check(file_name,process_lines) values('{json_path}',{json_count});"
    # 执行sql语句
    db_util.execute(sql)


logger.info("~~~元数据库存储完毕~~~")
