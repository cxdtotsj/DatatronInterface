import json
import operator


class OperationAssert:

    def is_contain(self, receive_data, except_data):
        '''
        判断一个字符串是否在另一个字符串中
        receive_data:返回的结果
        except_data:预期的结果(excel中的预期结果)
        '''

        self.flag = None
        if receive_data in except_data:
            self.flag = True
        else:
            self.flag = False
        return self.flag

    def is_equal_dict(self, receive_dict, except_dict):
        '''
        判断两个字典是否相等
        '''
        if isinstance(receive_dict, str):
            receive_dict = json.loads(receive_dict)
        if isinstance(except_dict, str):
            except_dict = json.loads(except_dict)
        return operator.eq(receive_dict, except_dict)

    def is_equal_json_keys(self, receive_dict, except_dict):
        '''
        判断两个字典中的keys是否相等
        '''
        if isinstance(receive_dict, str):
            receive_dict = json.loads(receive_dict)
        if isinstance(except_dict, str):
            except_dict = json.loads(except_dict)
        receive_keys = list(receive_dict.keys())
        except_keys = list(except_dict.keys())
        return operator.eq(receive_keys, except_keys)

    def is_equal_value_len(self, receive_num, except_num, sql_num):
        '''
        判断返回值的长度是否和预期值的相等
        :param receive_value: 实际返回的字段数量
        :param except_value: 入参时设定的数量
        :param sql_value: 数据库中已存在的数量
        '''
        if sql_num >= except_num:
            assert receive_num == except_num, "实际值和预期值应该相等"
        elif 1 <= sql_num < except_num:
            assert receive_num == sql_num, "实际值应等于数据库查到的值"
        else:
            assert receive_num == 0, "实际值应该为0"

    def is_dict_in(self,except_dict,receive_dict):
        '''
        判断 except_dict 是否在 receive_dict 中
        '''
        except_list = [(k,v) for k,v in except_dict.items()]
        receive_list = [(k,v) for k,v in receive_dict.items()]
        for each in except_list:
            assert each in receive_list,"新增后返回的结果不正确"

    def is_equal_value(self,except_value,receive_list,receive_key):
        '''
        判断 receive_list 中的某个字段的值都为 except_value
        '''
        value_list = list(map(lambda x:x[receive_key],receive_list))
        for each in value_list:
            assert each == except_value,"存在其他的返回值"






if __name__ == "__main__":
    assert_result = OperationAssert()
    