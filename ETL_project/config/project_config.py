# 写我们的整个项目的所有的配置信息
import time

# ###### json_server相关的配置信息 #####
log_file_root_path = "D:/Python/Pycharm/project/ETL_project/logs"  # 日志路径
log_name = f'py_etl_{time.strftime("%Y_%m_%d_%H", time.localtime(time.time()))}.log'  # 日志文件名
json_file_root_path = "D:/Python/Pycharm/project/ETL_project/01_josn数据"  # json文件所在的路径
# ############# mysql数据库配置选项 ##################
host = "localhost"
port = 3306
user = 'root'
passwd = '123456'
charset = "utf8"
autocommit = False
# #############--metadata-mysql数据库配置选项--##################
metadata_host = "localhost"
metadata_port = 3306
metadata_user = 'root'
metadata_passwd = '123456'
metadata_charset = "utf8"
metadata_autocommit = False

# #############--元数据库配置选项--##################
metadata_db_name = "metadata"
metadata_file_check_table_name = "file_check"
metadata_file_check_create_cols = """
            id INT PRIMARY KEY AUTO_INCREMENT, 
            file_name VARCHAR(255) UNIQUE NOT NULL COMMENT '被处理的文件名称', 
            process_lines INT COMMENT '本文件中有多少条数据被处理', 
            process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '处理时间'
             """
# ############--orders表和orders_detail表相关配置信息--############
# 数据库名
target_db_name = "retail"
# JSON数据采集后，写入MySQL，存储订单相关的表，表名是：
target_orders_table_name = "orders"
# orders表的建表语句的列信息
target_orders_table_create_cols = \
    f"order_id VARCHAR(255) PRIMARY KEY, " \
    f"store_id INT COMMENT '店铺ID', " \
    f"store_name VARCHAR(30) COMMENT '店铺名称', " \
    f"store_status VARCHAR(10) COMMENT '店铺状态(open,close)', " \
    f"store_own_user_id INT COMMENT '店主id', " \
    f"store_own_user_name VARCHAR(50) COMMENT '店主名称', " \
    f"store_own_user_tel VARCHAR(15) COMMENT '店主手机号', " \
    f"store_category VARCHAR(10) COMMENT '店铺类型(normal,test)', " \
    f"store_address VARCHAR(255) COMMENT '店铺地址', " \
    f"store_shop_no VARCHAR(255) COMMENT '店铺第三方支付id号', " \
    f"store_province VARCHAR(10) COMMENT '店铺所在省', " \
    f"store_city VARCHAR(10) COMMENT '店铺所在市', " \
    f"store_district VARCHAR(10) COMMENT '店铺所在行政区', " \
    f"store_gps_name VARCHAR(255) COMMENT '店铺gps名称', " \
    f"store_gps_address VARCHAR(255) COMMENT '店铺gps地址', " \
    f"store_gps_longitude VARCHAR(255) COMMENT '店铺gps经度', " \
    f"store_gps_latitude VARCHAR(255) COMMENT '店铺gps纬度', " \
    f"is_signed TINYINT COMMENT '是否第三方支付签约(0,1)', " \
    f"operator VARCHAR(10) COMMENT '操作员', " \
    f"operator_name VARCHAR(50) COMMENT '操作员名称', " \
    f"face_id VARCHAR(255) COMMENT '顾客面部识别ID', " \
    f"member_id VARCHAR(255) COMMENT '顾客会员ID', " \
    f"store_create_date_ts TIMESTAMP COMMENT '店铺创建时间', " \
    f"origin VARCHAR(255) COMMENT '原始信息(无用)', " \
    f"day_order_seq INT COMMENT '本订单是当日第几单', " \
    f"discount_rate DECIMAL(10, 5) COMMENT '折扣率', " \
    f"discount_type TINYINT COMMENT '折扣类型', " \
    f"discount DECIMAL(10, 5) COMMENT '折扣金额', " \
    f"money_before_whole_discount DECIMAL(10, 5) COMMENT '折扣前总金额', " \
    f"receivable DECIMAL(10, 5) COMMENT '应收金额', " \
    f"erase DECIMAL(10, 5) COMMENT '抹零金额', " \
    f"small_change DECIMAL(10, 5) COMMENT '找零金额', " \
    f"total_no_discount DECIMAL(10, 5) COMMENT '总价格(无折扣)', " \
    f"pay_total DECIMAL(10, 5) COMMENT '付款金额', " \
    f"pay_type VARCHAR(10) COMMENT '付款类型', " \
    f"payment_channel TINYINT COMMENT '付款通道', " \
    f"payment_scenarios VARCHAR(15) COMMENT '付款描述(无用)', " \
    f"product_count INT COMMENT '本单卖出多少商品', " \
    f"date_ts TIMESTAMP COMMENT '订单时间', " \
    f"INDEX (receivable), INDEX (date_ts)"

# JSON数据采集后，写入MySQL，存储订单详情（带商品信息的）相关的表，表名是：
target_orders_detail_table_name = "orders_detail"
# orders_detail表的建表语句的列信息
target_orders_detail_table_create_cols = \
    f"order_id VARCHAR(255) COMMENT '订单ID', " \
    f"barcode VARCHAR(255) COMMENT '商品条码', " \
    f"name VARCHAR(255) COMMENT '商品名称', " \
    f"count INT COMMENT '本单此商品卖出数量', " \
    f"price_per DECIMAL(10, 5) COMMENT '实际售卖单价', " \
    f"retail_price DECIMAL(10, 5) COMMENT '零售建议价', " \
    f"trade_price DECIMAL(10, 5) COMMENT '贸易价格(进货价)', " \
    f"category_id INT COMMENT '商品类别ID', " \
    f"unit_id INT COMMENT '商品单位ID(包、袋、箱、等)', " \
    f"PRIMARY KEY (order_id, barcode)"
# #########csv相关配置############
# csv文件路径
csv_file_root_path = "D:/Python/Pycharm/project/ETL_project/02_csv文件"
# order订单数据文件名
csv_order_file_name = f"orders_{time.strftime('%Y_%m_%d_%H', time.localtime(time.time()))}.csv"
# order_product订单商品文件名
csv_order_detail_file_name = f"orders_detail_{time.strftime('%Y_%m_%d_%H', time.localtime(time.time()))}.csv"





# ######################## 需求二的配置信息 #######################################
# #############--retail--mysql数据库配置选项--##################
retail_host = "localhost"
retail_port = 3306
retail_user = 'root'
retail_passwd = '123456'
retail_charset = "utf8"
retail_autocommit = False
# #############--source_data--mysql数据库配置选项--##################
source_host = "localhost"
source_port = 3306
source_user = 'root'
source_passwd = '123456'
source_charset = "utf8"
source_autocommit = False
# ############### 元数据库的配置信息
# <元数据库数据库名>
# metadata_db_name = "metadata"
# <元数据库数据库表名>(数据最后更新时间)
metadata_barcode_table_name = "barcode_monitor"
# <元数据库数据库表名>的创建字段
metadata_barcode_table_create_cols = "id INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID', " \
                                     "time_record TIMESTAMP NOT NULL COMMENT '本次采集记录的最大时间', " \
                                     "gather_line_count INT NULL COMMENT '本次采集条数'"

# <数仓数据库名>
retail_db_name = "retail"
# <数仓数据表名>
retail_barcode_table_name = "barcode"
# <数仓数据表名>的创建字段
retail_barcode_table_create_cols = """
    `code` varchar(50) PRIMARY KEY COMMENT '商品条码',
    `name` varchar(200) DEFAULT '' COMMENT '商品名称',
    `spec` varchar(200) DEFAULT '' COMMENT '商品规格',
    `trademark` varchar(100) DEFAULT '' COMMENT '商品商标',
    `addr` varchar(200) DEFAULT '' COMMENT '商品产地',
    `units` varchar(50) DEFAULT '' COMMENT '商品单位(个、杯、箱、等)',
    `factory_name` varchar(200) DEFAULT '' COMMENT '生产厂家',
    `trade_price` DECIMAL(50, 5) DEFAULT 0.0 COMMENT '贸易价格(指导进价)',
    `retail_price` DECIMAL(50, 5) DEFAULT 0.0 COMMENT '零售价格(建议卖价)',
    `update_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `wholeunit` varchar(50) DEFAULT NULL COMMENT '大包装单位',
    `wholenum` int(11) DEFAULT NULL COMMENT '大包装内装数量',
    `img` varchar(500) DEFAULT NULL COMMENT '商品图片',
    `src` varchar(20) DEFAULT NULL COMMENT '源信息', 
    INDEX (update_at)
"""

# <后台数据库>数据库名
source_db_name = "source_data"
# <后台数据库>数据表名
source_barcode_data_table_name = "sys_barcode"
# <csv文件>文件名
barcode_orders_output_csv_file_name = f'barcode-{time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))}.csv'


# ################--需求3的相关配置--############################
# <<存放备份log的数据表名字>>
retail_backend_table_name = "backend_logs"
# <<表创建字段>>
retail_backend_table_create_cols = \
    f"id int PRIMARY KEY AUTO_INCREMENT COMMENT '自增ID', " \
    f"log_time TIMESTAMP(6) COMMENT '日志时间,精确到6位毫秒值', " \
    f"log_level VARCHAR(10) COMMENT '日志级别', " \
    f"log_module VARCHAR(50) COMMENT '输出日志的功能模块名', " \
    f"response_time INT COMMENT '接口响应时间毫秒', " \
    f"province VARCHAR(30) COMMENT '访问者省份', " \
    f"city VARCHAR(30) COMMENT '访问者城市', " \
    f"log_text VARCHAR(255) COMMENT '日志正文', " \
    f"INDEX(log_time)"
# <<元数据库metadata>>中存放已经处理过的日志文件的<<数据表名>>
metadata_backend_table_name = "backend_logs_monitor"
# <<表的字段>>
metadata_backend_table_create_cols = "id INT PRIMARY KEY AUTO_INCREMENT, " \
                                     "file_name VARCHAR(255) NOT NULL COMMENT '处理文件名称', " \
                                     "process_lines INT NULL COMMENT '文件处理行数', " \
                                     "process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '文件处理时间'"

# <<备份日志的csv文件名>>
backend_logs_csv_file_name = f"backend_logs_{time.strftime('%Y-%m-%d-%H%M%S', time.localtime(time.time()))}.csv"
backend_logs_csv_file_root_path = "D:/Python/Pycharm/project/ETL_project/02_csv文件/"

