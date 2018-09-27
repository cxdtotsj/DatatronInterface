
from util.operation_excel import OperationExcel
import data.define_col

class GetExcelValue:

    def __init__(self):
        self.opera_excel = OperationExcel()

    # 获取要执行的case个数
    def get_case_num(self):
        return self.opera_excel.get_lines()

    # 获取GRPCURL命令
    def get_gcurl(self,row):
        col = int(data.define_col.get_gcurl())
        gcurl = self.opera_excel.get_cell_value(row,col)
        return gcurl

    # 获取Proto路径
    def get_proto_path(self,row):
        col = int(data.define_col.get_proto_path())
        proto_path = self.opera_excel.get_cell_value(row,col)
        return proto_path


    # 获取请求参数
    def get_request_data(self,row):
        col = int(data.define_col.get_request_data())
        url = self.opera_excel.get_cell_value(row,col)
        return url

    # 获取请求方法
    def get_proto_method(self,row):
        col = int(data.define_col.get_proto_method())
        url = self.opera_excel.get_cell_value(row,col)
        return url

    # 获取是否运行
    def get_is_run(self,row):
        col = int(data.define_col.get_run())
        is_run = self.opera_excel.get_cell_value(row,col)
        return is_run

    # 获取预期结果
    def get_expect_data(self,row):
        col = int(data.define_col.get_expect())
        except_data = self.opera_excel.get_cell_value(row, col)
        return except_data

    # 写入实际结果
    def write_result(self,row,value):
        col = int(data.define_col.get_result())
        self.opera_excel.write_value(row, col, value)

    # 写入报错信息
    def write_error_msg(self,row,value):
        col = int(data.define_col.get_error_msg())
        self.opera_excel.write_value(row, col, value)

    # 判断是否有case依赖
    def get_is_depend(self, row):
        col = int(data.define_col.get_case_depend())
        depend_case_id = self.opera_excel.get_cell_value(row, col)
        if depend_case_id == "":
            return None
        else:
            return depend_case_id

    # 获取依赖数据的key
    def get_depend_key(self, row):
        col = int(data.define_col.get_data_depend())
        depent_key = self.opera_excel.get_cell_value(row, col)
        if depent_key == "":
            return None
        else:
            return depent_key

    # 获取数据依赖字段
    def get_depend_field(self, row):
        col = int(data.define_col.get_case_depend())
        depend_field = self.opera_excel.get_cell_value(row, col)
        if depend_field == "":
            return None
        else:
            return depend_field


# if __name__ == '__main__':
#     # excel_value = GetExcelValue()
#     # #url = excel_value.get_request_url(1)
#     # #is_run = excel_value.get_is_run(1)
#     # #depend_key = excel_value.get_is_depend(1)
#     # excel_value.write_result(1,8,"fail")
#     # #print(depend_key)