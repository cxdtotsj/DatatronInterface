import json
import operator


class AssertJudgment:

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
        '''判断 dict1 是否在 dict2 中 '''
        # except_list = [(k,v) for k,v in except_dict.items()]
        # receive_list = [(k,v) for k,v in receive_dict.items()]
        except_list = except_dict
        receive_list = receive_dict
        for each in except_list:
            if each in receive_list:
                continue
            else:
                return False
        return True

if __name__ == "__main__":
    assert_result = AssertJudgment()
    exc = [('name', 'Auto园区名称1539077601'), ('area', 100), ('building_num', 19), ('loc', {'province': '上海市', 'city': '上海市', 'county': '静安区', 'addr': '恒丰路329号'}), ('coord', {'longitude': 121, 'latitude': 31, 'altitude': 0}), ('extra', {'build_corp': '建筑单位名称', 'build_start_at': '2018-10-09', 'construct_corp': '规划单位名称', 'construct_end_at': '2018-10-09', 'design_corp': '设计单位名称', 'design_end_at': '2018-10-09', 'plan_corp': '施工单位名称', 'plan_end_at': '2018-10-09', 'supervise_corp': '监理单位名称', 'supervise_end_at': '2018-10-09'})]
    rec = [('id', '111383146515149355'), ('corpId', '109777231634510875'), ('name', 'Auto园区名称1539077601'), ('loc', {'province': '上海市', 'city': '上海市', 'county': '静安区', 'addr': '恒丰路329号'}), ('coord', {'longitude': 121, 'latitude': 31, 'altitude': 0}), ('buildingNum', '19'), ('buildingCount', '0'), ('area', 100), ('extra', {'buildCorp': '建筑单位名称', 'buildStartAt': '2018-10-09', 'planCorp': '施工单位名称', 'planEndAt': '2018-10-09', 'designCorp': '设计单位名称', 'designEndAt': '2018-10-09', 'constructCorp': '规划单位名称', 'constructEndAt': '2018-10-09', 'superviseCorp': '监理单位名称', 'superviseEndAt': '2018-10-09'}), ('status', 1), ('modifyBy', ''), ('createAt', '1539077528'), ('updateAt', '1539077528')]
    a = assert_result.is_dict_in(exc,rec)
    print(a)

