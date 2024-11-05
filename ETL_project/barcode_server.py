from util.logging_util import init_my_logger
from util.mysql_util import MySqlUtil
from config import project_config as conf
import sys
from model.barcorde_model import BarcodeModel

# todo 步骤1:开启日志
logger = init_my_logger()
logger.info("开启日志")
# todo 步骤2:链接数据库(3个数据库)
source_db_util = MySqlUtil(
    conf.source_host,
    conf.source_port,
    conf.source_user,
    conf.source_passwd,
    conf.source_charset,
    conf.source_autocommit
)
retail_db_util = MySqlUtil(
    conf.retail_host,
    conf.retail_port,
    conf.retail_user,
    conf.retail_passwd,
    conf.retail_charset,
    conf.retail_autocommit
)
metadata_db_util = MySqlUtil(
    conf.metadata_host,
    conf.metadata_port,
    conf.metadata_user,
    conf.metadata_passwd,
    conf.metadata_charset,
    conf.metadata_autocommit
)
# 选择数据库
source_db_util.select_db(conf.source_db_name)
retail_db_util.select_db(conf.retail_db_name)
metadata_db_util.select_db(conf.metadata_db_name)
# todo 步骤3:检查<后台数据库source>中是否有数据表 如果没有需要社交
if not source_db_util.check_table_exists(conf.source_db_name, conf.source_barcode_data_table_name):
    # 如果if语句成立证明 数据表不存在
    logger.warning("数据表都没有 玩什么呀 社交去吧")
    # 退出整个程序
    sys.exit(1)
# todo 步骤4:<后台数据库source>中是有数据表, <数仓retail>数据库中创建数据表
# 如果能执行到这里 证明后台数据库source中有数据表的
retail_db_util.check_table_exists_and_create(
    conf.retail_db_name,
    conf.retail_barcode_table_name,
    conf.retail_barcode_table_create_cols
)
# todo 步骤5:从<元数据库metadata>中获取<最后一次的更新时间>(创建元数据库的数据表)
# 存储最后一次更新时间
last_update_time = None
# 确定元数据库中有数据表
if not metadata_db_util.check_table_exists(conf.metadata_db_name, conf.metadata_barcode_table_name):
    # 如果if语句成立 证明元数据库中数据表不存在
    # 创建元数据库中的数据表
    metadata_db_util.check_table_exists_and_create(
        conf.metadata_db_name,
        conf.metadata_barcode_table_name,
        conf.metadata_barcode_table_create_cols
    )
else:
    # 证明元数据库中数据表存在
    # ret ==> ( (2017-07-10,),)  有数据
    # ret ==> () 没有数据  ==> max ==> ((None,))
    ret = metadata_db_util.query(f"select time_record from {conf.metadata_barcode_table_name} "
                                 f"order by time_record desc limit 1;")

    if len(ret) > 0:
        # 如果if语句成立 证明是有数据的
        # ret == > ( (2017-07-10,),)
        # ret[0][0] ==> 最后一次更新具体的时间
        # 转化成 字符串 "2017-07-10"
        last_update_time = str(ret[0][0])
# todo 步骤6:通过<最后一次的更新时间>从<后台数据库source>获取新增的数据
if last_update_time:
    # 如果if语句成立 证明last_update_time不为None的
    # sql = "select * from xxx where updateAt>='2017-07-10' ;"
    sql = f"select * from {conf.source_barcode_data_table_name} where updateAt>='{last_update_time}' order by updateAt;"
else:
    # 证明last_update_time为None的
    sql = f"select * from {conf.source_barcode_data_table_name} order by updateAt;"
# 执行查询sql语句
# source_data ==> ((),()) 新增数据
source_data = source_db_util.query(sql)
# todo 步骤7:把<新增数据>转化为<模型对象>
# 模型对象列表(存储所有的数据模型对象) 数据模型对象==>一个商品的信息
model_list = []
for i in source_data:
    # i是元组，存储了一个商品的信息
    code = i[0]
    name = i[1]
    spec = i[2]
    trademark = i[3]
    addr = i[4]
    units = i[5]
    factory_name = i[6]
    trade_price = i[7]
    retail_price = i[8]
    update_at = str(i[9])  # i[9]是读取的updateAt时间，类型是datetime，转换成字符串
    wholeunit = i[10]
    wholenum = i[11]
    img = i[12]
    src = i[13]
    # 构建BarcodeModel
    # model是一个数据模型对象
    model = BarcodeModel(
        code=code,
        name=name,
        spec=spec,
        trademark=trademark,
        addr=addr,
        units=units,
        factory_name=factory_name,
        trade_price=trade_price,
        retail_price=retail_price,
        update_at=update_at,
        wholeunit=wholeunit,
        wholenum=wholenum,
        img=img,
        src=src
    )
    # 把模型对象添加到列表中
    model_list.append(model)
# todo 步骤8:通过<模型对象>生成sql和csv (数据的插入--数仓retail中--和保存)
# 打开一个文件用来保存csv数据
csv_f = open("D:/Python/Pycharm/project/ETL_project/02_csv文件/barcode.csv", "a", encoding="utf8")
# 计数
count = 0
for model in model_list:
    # 计数
    count += 1
    # model ==> 一个商品信息的对象
    # todo sql插入
    sql = model.to_sql()
    retail_db_util.execute_without_autocommit(sql)
    # todo csv的保存
    csv_line = model.to_csv()
    csv_f.write(csv_line + "\n")
    # 每100条数据 提交一回 保存一回
    if count % 100 == 0:
        # 提交
        retail_db_util.conn.commit()
        # close(): 保存并退出文件
        # flush(): 保存但不退出文件
        csv_f.flush()
# 最后进行一次文件关闭 和 数据提交
retail_db_util.conn.commit()
csv_f.close()
# todo 步骤9:把<数仓retail>里的最后的更新时间 存储到<元数据库metadata>中
# ret ==> ((2017-10-10,),)
# 从retail数仓中获取最后的更新时间last_update_time
ret = retail_db_util.query(f"select max(update_at) from {conf.retail_barcode_table_name};")
last_update_time = str(ret[0][0])
# # 把这个更新时间存储到元数据库metadata中
metadata_db_util.execute(f"insert into {conf.metadata_barcode_table_name}(time_record,gather_line_count) "
                         f"values('{last_update_time}',{count})")
# # 关闭连接
metadata_db_util.close_conn()
retail_db_util.close_conn()
source_db_util.close_conn()

