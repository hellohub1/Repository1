from util.logging_util import init_my_logger
from util.mysql_util import MySqlUtil
from config import project_config as conf
from util.file_util import get_file_name
from model.backend_model import BackendLogsModel
# todo 1.开启日志
logger = init_my_logger()
logger.info("日志开启了~~~")
# todo 2.创建数据链接 <metadata> 和 <retail>
metadata_db_util = MySqlUtil(
    host = conf.metadata_host,
    port = conf.metadata_port,
    user = conf.metadata_user,
    passwd = conf.metadata_passwd,
    charset = conf.metadata_charset,
    autocommit = conf.metadata_autocommit
)
retail_db_util = MySqlUtil(
    host = conf.retail_host,
    port = conf.retail_port,
    user = conf.retail_user,
    passwd = conf.retail_passwd,
    charset = conf.retail_charset,
    autocommit = conf.retail_autocommit
)
# 切换数据库
metadata_db_util.select_db(conf.metadata_db_name)
retail_db_util.select_db(conf.retail_db_name)
# todo 3. 创建数据库<metadata>以及<retail>中的数据表
# 创建两个数据库中的两个表
metadata_db_util.check_table_exists_and_create(
    conf.metadata_db_name,
    conf.metadata_backend_table_name,
    conf.metadata_backend_table_create_cols
)

retail_db_util.check_table_exists_and_create(
    conf.retail_db_name,
    conf.retail_backend_table_name,
    conf.retail_backend_table_create_cols
)
# todo 4.获取指定路径所有的文件名字
all_file_list = get_file_name("//logs/log_data")
logger.info(f"获取所有的文件名{all_file_list}")
# todo 5. 从元数据路<metadata>中获取备份过得文件名
processed_file_name = []
ret = metadata_db_util.query(f"select file_name from {conf.metadata_backend_table_name}")
for i in ret:
    # i ==> () 文件
    # i[0] ==> () 文件名
    processed_file_name.append(i[0])
logger.info(f"获取处理过的文件名列表{processed_file_name}")

# todo 6. 进一步对比获取的文件名 进而获取需要的文件名
# 未处理的文件名列表
without_fil_name = []
for path in all_file_list:
    if path not in processed_file_name:
        without_fil_name.append(path)
# for file_name in without_fil_name:
#     print(file_name)
# todo 7. 通过数据模型将需要处理的文件中的数据 转化为 数据模型对象
# key:用来存储文件名
# value:文件中数据数量
path_count_dict = {}

for path in without_fil_name:
    # 计数
    count = 0
    # 打开一个文件存储生成的csv
    csv_file = open("D:/Python/Pycharm/project/ETL_project/02_csv文件/logs_csv", "a", encoding="utf-8")
    # path ==> 文件的绝对路径
    for line in open(path, "r", encoding="utf8"):
        # 计数
        count += 1
        # 模型对象
        barcode_model = BackendLogsModel(line)
        # todo sql插入
        retail_db_util.execute_without_autocommit(barcode_model.to_sql())
        # todo csv保存
        csv_file.write(barcode_model.to_csv())

    path_count_dict[path] = count
    # 提交数据
    retail_db_util.conn.commit()
    # 保存并退出
    csv_file.close()
# todo 8. 将处理的过的文件名存放到<metadata>数据库中
for path,count in path_count_dict.items():
    metadata_db_util.execute(
        f"insert into {conf.metadata_backend_table_name}("
        f"file_name, process_lines)"
        f" values('{path}','{count}'); "
    )
# # 关闭连接
metadata_db_util.close_conn()
retail_db_util.close_conn()

