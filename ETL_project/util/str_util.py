def check_null(data):
    """
    检查data(字符串类型)是否是<<空>>
    如果是<<空>> 就返回 : True
    如果不是<<空>> 就返回 : False

    数据源有很多: None null NULL "" undefined  ==> <<空>>
    :param data: 具体数据
    :return: True/False
    """
    # None  "None"
    data = str(data)
    # None  ==> none
    data = data.lower()
    # 判断data是否为空
    if data == "none" or data == "null" or data == "" or data == "undefined":
        return True
    else:
        return False


def check_str_null_and_transform_to_sql_null(data):
    """
    把<<空>> 转化数据库 <<空>> null
    :param data: 数据 None null NULL "" undefined  ==> <<空>>
    :return: 数据库的<<空>>null
    """
    # 判断数据是否为空
    if check_null(data):
        # 如果if成立 证明data为空
        return "null"
    else:
        return f"'{data}'"

def clean_str(data:str):
    """
    进行字符串的一个清洗 可口可乐/ ==> 可口可乐
    :param data: 具体的数据
    :return: 清洗过得数据
    """
    if check_null(data):
        return data

    data = data.replace("'", "")
    data = data.replace('"', "")
    data = data.replace("\\", "")
    data = data.replace(";", "")
    data = data.replace(",", "")
    data = data.replace("@", "")
    return data
def check_number_null_and_transform_to_sql_null(data):
    """
    把数字类型的数据 检查一下是否为空 如果为空直接返回null
    如果不为空 返回data(数字类型)
    :param data:  数字类型的数据
    :return: null/数字
    """
    if check_null(data):
        return "null"
    else:
        return data

if __name__ == '__main__':
    name = None
    age = 18
    sql = (f"insert into XXX " 
           f"values(" 
           f"{check_str_null_and_transform_to_sql_null(name)}," 
           f"{check_number_null_and_transform_to_sql_null(age)}"
           f")")

    print(sql)
