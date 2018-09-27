

class DefineCol:

    g_order = '0'
    proto_path = '1'
    id = '2'
    interface_name = '3'
    request_data = '4'
    proto_method = '5'
    run = '6'
    case_depend = '7'
    data_depend = '8'
    field_depend = '9'
    expect = '10'
    result = '11'
    error_msg = '12'


# 获取GRPCURL命令
def get_gcurl():
    return DefineCol.g_order

# 获取Proto文件路径
def get_proto_path():
    return DefineCol.proto_path

# 获取caseid
def get_id():
    return DefineCol.id

# 获取请求参数
def get_request_data():
    return DefineCol.request_data

# 获取Proto方法
def get_proto_method():
    return DefineCol.proto_method

# 获取是否运行
def get_run():
    return DefineCol.run

# 获取依赖id
def get_case_depend():
    return DefineCol.case_depend

# 获取依赖数据
def get_data_depend():
    return DefineCol.data_depend

# 获取依赖数据所属字段
def get_field_depend():
    return DefineCol.field_depend

# 获取预期结果
def get_expect():
    return DefineCol.expect

# 写入实际结果
def get_result():
    return DefineCol.result

# 写入错误信息
def get_error_msg():
    return DefineCol.error_msg
