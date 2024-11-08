"""
零售订单模型
负责构建
- 纯订单相关的数据模型（1比1的class模型）
- 订单和商品相关的数据模型（1比多的class模型）
"""
import json
from util import str_util
from util import time_util
from config import project_config as conf


class OrdersModel:
    """构建订单模型（纯订单，不包含商品信息）"""

    def __init__(self, data: str):
        """
        从传入的字符串数据构建订单model
        此Model只包含订单信息，不包含订单详情（商品售卖）
        """
        # 将一行字符串json转换为字典对象
        data = json.loads(data)

        self.discount_rate = data['discountRate']  # 折扣率
        self.store_shop_no = data['storeShopNo']  # 店铺店号（无用列）
        self.day_order_seq = data['dayOrderSeq']  # 本单为当日第几单
        self.store_district = data['storeDistrict']  # 店铺所在行政区
        self.is_signed = data['isSigned']  # 是否签约店铺（签约第三方支付体系）
        self.store_province = data['storeProvince']  # 店铺所在省份
        self.origin = data['origin']  # 原始信息（无用）
        self.store_gps_longitude = data['storeGPSLongitude']  # 店铺GPS经度
        self.discount = data['discount']  # 折扣金额
        self.store_id = data['storeID']  # 店铺ID
        self.product_count = data['productCount']  # 本单售卖商品数量
        self.operator_name = data['operatorName']  # 操作员姓名
        self.operator = data['operator']  # 操作员ID
        self.store_status = data['storeStatus']  # 店铺状态
        self.store_own_user_tel = data['storeOwnUserTel']  # 店铺店主电话
        self.pay_type = data['payType']  # 支付类型
        self.discount_type = data['discountType']  # 折扣类型
        self.store_name = data['storeName']  # 店铺名称
        self.store_own_user_name = data['storeOwnUserName']  # 店铺店主名称
        self.date_ts = data['dateTS']  # 订单时间
        self.small_change = data['smallChange']  # 找零金额
        self.store_gps_name = data['storeGPSName']  # 店铺GPS名称
        self.erase = data['erase']  # 是否抹零
        self.store_gps_address = data['storeGPSAddress']  # 店铺GPS地址
        self.order_id = data['orderID']  # 订单ID
        self.money_before_whole_discount = data['moneyBeforeWholeDiscount']  # 折扣前金额
        self.store_category = data['storeCategory']  # 店铺类别
        self.receivable = data['receivable']  # 应收金额
        self.face_id = data['faceID']  # 面部识别ID
        self.store_own_user_id = data['storeOwnUserId']  # 店铺店主ID
        self.payment_channel = data['paymentChannel']  # 付款通道
        self.payment_scenarios = data['paymentScenarios']  # 付款情况（无用）
        self.store_address = data['storeAddress']  # 店铺地址
        self.total_no_discount = data['totalNoDiscount']  # 整体价格（无折扣）
        self.payed_total = data['payedTotal']  # 已付款金额
        self.store_gps_latitude = data['storeGPSLatitude']  # 店铺GPS纬度
        self.store_create_date_ts = data['storeCreateDateTS']  # 店铺创建时间
        self.store_city = data['storeCity']  # 店铺所在城市
        self.member_id = data['memberID']  # 会员ID

    def check_and_transform_area(self):
        """
        对指定的字段进行检查 如果为<<空>> 就转化为 "未知xxx"
        :return: None
        """
        if str_util.check_null(self.store_province):
            # 表示省份内容无意义
            self.store_province = "未知省份"

        if str_util.check_null(self.store_city):
            # 表示城市内容无意义
            self.store_city = "未知城市"

        if str_util.check_null(self.store_district):
            # 表示行政区内容无意义
            self.store_district = "未知行政区"

    def to_csv(self, sep=","):
        """
        可以把json订单数据转化为csv字符串
        返回出这个字符串 ==> 111,张三,22
        :param sep: ,
        :return: csv格式的字符串
        """

        # 数据的转化
        self.check_and_transform_area()

        csv_line = \
            f"{self.order_id}{sep}" \
            f"{self.store_id}{sep}" \
            f"{self.store_name}{sep}" \
            f"{self.store_status}{sep}" \
            f"{self.store_own_user_id}{sep}" \
            f"{self.store_own_user_name}{sep}" \
            f"{self.store_own_user_tel}{sep}" \
            f"{self.store_category}{sep}" \
            f"{self.store_address}{sep}" \
            f"{self.store_shop_no}{sep}" \
            f"{self.store_province}{sep}" \
            f"{self.store_city}{sep}" \
            f"{self.store_district}{sep}" \
            f"{self.store_gps_name}{sep}" \
            f"{self.store_gps_address}{sep}" \
            f"{self.store_gps_longitude}{sep}" \
            f"{self.store_gps_latitude}{sep}" \
            f"{self.is_signed}{sep}" \
            f"{self.operator}{sep}" \
            f"{self.operator_name}{sep}" \
            f"{self.face_id}{sep}" \
            f"{self.member_id}{sep}" \
            f"{time_util.ts13_to_date_str(self.store_create_date_ts)}{sep}" \
            f"{self.origin}{sep}" \
            f"{self.day_order_seq}{sep}" \
            f"{self.discount_rate}{sep}" \
            f"{self.discount_type}{sep}" \
            f"{self.discount}{sep}" \
            f"{self.money_before_whole_discount}{sep}" \
            f"{self.receivable}{sep}" \
            f"{self.erase}{sep}" \
            f"{self.small_change}{sep}" \
            f"{self.total_no_discount}{sep}" \
            f"{self.payed_total}{sep}" \
            f"{self.pay_type}{sep}" \
            f"{self.payment_channel}{sep}" \
            f"{self.payment_scenarios}{sep}" \
            f"{self.product_count}{sep}" \
            f"{time_util.ts13_to_date_str(self.date_ts)}"
        return csv_line

    def to_sql(self):
        """把json订单数据 转化为一个插入的sql语句"""
        """
                将模型转换成一条INSERT SQL语句
                :return: 字符串，记录了INSERT INTO的SQL语句
                insert into xxx(11,22,33) values();
        """
        # insert into xxx vlaues (id ); 如果插入的数据主键重复 会报错
        # insert IGNORE into xxx vlaues (id ); 如果插入数据主键重复 就会忽略
        sql = f"INSERT IGNORE INTO {conf.target_orders_table_name}(" \
              f"order_id,store_id,store_name,store_status,store_own_user_id," \
              f"store_own_user_name,store_own_user_tel,store_category," \
              f"store_address,store_shop_no,store_province,store_city," \
              f"store_district,store_gps_name,store_gps_address," \
              f"store_gps_longitude,store_gps_latitude,is_signed," \
              f"operator,operator_name,face_id,member_id,store_create_date_ts," \
              f"origin,day_order_seq,discount_rate,discount_type,discount," \
              f"money_before_whole_discount,receivable,erase,small_change," \
              f"total_no_discount,pay_total,pay_type,payment_channel," \
              f"payment_scenarios,product_count,date_ts" \
              f") VALUES(" \
              f"'{self.order_id}', " \
              f"{self.store_id}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_name)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_status)}, " \
              f"{self.store_own_user_id}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_own_user_name)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_own_user_tel)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_category)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_address)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_shop_no)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_province)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_city)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_district)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_name)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_address)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_longitude)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.store_gps_latitude)}, " \
              f"{self.is_signed}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.operator)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.operator_name)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.face_id)}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.member_id)}, " \
              f"'{time_util.ts13_to_date_str(self.store_create_date_ts)}', " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.origin)}, " \
              f"{self.day_order_seq}, " \
              f"{self.discount_rate}, " \
              f"{self.discount_type}, " \
              f"{self.discount}, " \
              f"{self.money_before_whole_discount}, " \
              f"{self.receivable}, " \
              f"{self.erase}, " \
              f"{self.small_change}, " \
              f"{self.total_no_discount}, " \
              f"{self.payed_total}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.pay_type)}, " \
              f"{self.payment_channel}, " \
              f"{str_util.check_str_null_and_transform_to_sql_null(self.payment_scenarios)}, " \
              f"{self.product_count}, " \
              f"'{time_util.ts13_to_date_str(self.date_ts)}')"

        return sql


class SingleProductSoldModel:
    """订单内售卖的单类商品信息"""

    # order_id : 订单id
    # product_detail_dict : [{},{},{}]
    # {"name":张三,age:11,tel:110}
    # to_csv ==> "张三,11,110"
    def __init__(self, order_id, product_detail_dict):
        self.order_id = order_id  # 订单ID
        self.name = product_detail_dict["name"]  # 商品名称
        self.count = product_detail_dict["count"]  # 商品售卖数量
        self.unit_id = product_detail_dict["unitID"]  # 单位ID
        self.barcode = product_detail_dict["barcode"]  # 商品的条码
        self.price_per = product_detail_dict["pricePer"]  # 商品卖出的单价
        self.retail_price = product_detail_dict["retailPrice"]  # 商品建议零售价
        self.trade_price = product_detail_dict["tradePrice"]  # 商品建议成本价
        self.category_id = product_detail_dict["categoryID"]  # 商品类别ID

    def to_csv(self, sep=","):
        """把一个上平的信息 生成一条csv数据，分隔符默认逗号"""
        csv_line = \
            f"{self.order_id}{sep}" \
            f"{self.barcode}{sep}" \
            f"{self.name}{sep}" \
            f"{self.count}{sep}" \
            f"{self.price_per}{sep}" \
            f"{self.retail_price}{sep}" \
            f"{self.trade_price}{sep}" \
            f"{self.category_id}{sep}" \
            f"{self.unit_id}"

        return csv_line


class OrdersDetailModel:
    """订单详情数据模型"""

    def __init__(self, data):
        # data python中的字典
        data = json.loads(data)
        # 获取订单id
        self.order_id = data["orderID"]
        # 列表存储 单个模型对象的
        self.products_detail = []

        # 把这个订单的所有的商品转化为 单个商品模型对象 存储到product_detail列表中
        # products_list == [{},{},{}]
        products_list = data["product"]

        for i in products_list:
            # i ==> {} 一个商品信息
            # model就是一个商品对象==> (炸弹对象)
            model = SingleProductSoldModel(self.order_id, i)
            # 添交到列表中
            self.products_detail.append(model)

    def to_sql(self):
        """
                生成插入MySQL的INSERT SQL语句
                可以完成一次性插入多条数据
                sql = "insert into xxx(11,22,33) values"
        """
        sql = f"INSERT IGNORE INTO {conf.target_orders_detail_table_name}(" \
              f"order_id,barcode,name,count,price_per,retail_price,trade_price,category_id,unit_id) VALUES"
        # 当前这个SQL字符串是半成品，类似于：`INSERT IGNORE INTO table(id, name) VALUES`
        for model in self.products_detail:
            # model：SingleProductSoldModel的一个对象
            # sql = "insert into xxx(11,22,33) values('火箭id',null,null,2), ('炸弹id',null,null,3), "
            sql += "("
            sql += f"'{model.order_id}', " \
                   f"{str_util.check_str_null_and_transform_to_sql_null(model.barcode)}, " \
                   f"{str_util.check_str_null_and_transform_to_sql_null(model.name)}, " \
                   f"{model.count}, " \
                   f"{model.price_per}, " \
                   f"{model.retail_price}, " \
                   f"{model.trade_price}, " \
                   f"{model.category_id}, " \
                   f"{model.unit_id}"
            sql += "), "

        # 去除SQL结尾的逗号
        # sql = "insert into xxx(11,22,33) values('火箭id',null,null,2), ('炸弹id',null,null,3)
        sql = sql[:-2]  # 为什么是-2，因为逗号后面还有一个空格

        return sql

    def to_csv(self):
        """可以把一个订单中的所有的商品的信息 都转化为csv字符串"""
        # 空字符串
        csv_line = ""
        # model ==> 商品对象
        for model in self.products_detail:
            # csv_line ==>  "张三,11,110"
            # csv_list ==>  "老王,22,220"
            # csv_list ==>  "张三,11,110\n老王,22,220\n"
            csv_line += model.to_csv()
            csv_line += "\n"
        return csv_line
