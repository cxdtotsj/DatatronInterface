from util.operation_db import OperationDB
from util.operation_json import OperetionJson
from base.baseMethod import BaseMethod
from base.getURL import API
import random
import datetime
import time


class SQLData:

    def __init__(self):
        self.opera_db = OperationDB()
        self.opera_json = OperetionJson()
        self.run_method = BaseMethod()
        self.get_url = API()

    # 自动插入一条 无需报名的活动，并返回出 id
    def insert_event_no(self):
        num = random.randint(1, 100)
        event_title = "这是活动--名称{}".format(num)
        event_intro = "这是活动--说明{}".format(num)
        event_content = "这是活动--内容{}".format(num)
        created_time = int(time.time())
        noAllow_sql = '''insert into zyt_event (event_title,event_intro,event_content,apply_need,end_time,event_rank,event_status,created_time,created_user)
                            value ("{}","{}","{}",0,{},0,1,{},"xdchen")'''.format(event_title, event_intro, event_content, created_time, created_time)
        no_eventID = self.opera_db.insert_data(noAllow_sql)
        return no_eventID

    # 需要报名的活动，并返回出 id
    def insert_event_yes(self):
        num = random.randint(1, 100)
        event_title = "这是报名活动--名称{}".format(num)
        event_intro = "这是报名活动--说明{}".format(num)
        event_content = "这是报名活动--内容{}".format(num)
        created_time = int(time.time())
        end_time = int(time.time() + 1000)
        yesAllow_sql = '''insert into zyt_event (event_title,event_intro,event_content,apply_need,allowed_num,end_time,event_rank,event_status,created_time,created_user)
                            value ("{}","{}","{}",1,5,{},0,1,{},"xdchen")'''.format(event_title, event_intro, event_content, end_time, created_time)
        yse_eventID = self.opera_db.insert_data(yesAllow_sql)
        return yse_eventID

    # 获取数据库或者返回值返出的数据，把value放入列表
    def array_get_dictValue(self, array, key):
        value_list = []
        for i in array:
            value_list.append(i[key])
        return value_list

    # 筑英台下单操作，并返回order_id
    def zyt_pay_order(
            self,
            user_id,
            token,
            good_id,
            good_type,
            amount,
            returnurl):
        '''
        :param user_id:
        :param token:
        :param good_id: 商品id: 课程id(商品类型:课程),问题id(商品类型:提问、查看问题答案)
        :param good_type: 商品类型: 1-课程，2-提问，3-查看问题答案
        :param amount: 支付价格(单位元)
        :param returnurl: 支付成功后的跳转url
        :return:
        '''
        api = "/api/v1/pay/pay"
        return_url = self.get_url.http_api_url(returnurl)
        data = {"user_id": user_id,
                "token": token,
                "paymethod": 1,
                "paychannel": "web",
                "good_id": good_id,
                "good_type": good_type,
                "amount": amount,
                "returnurl": return_url}
        self.run_method.post(api, data)
        sql = '''select order_id from zyt_order where user_id = '{}' and good_id = {} and good_type = {}'''.format(
            user_id, good_id, good_type)
        order_id = self.opera_db.get_fetchone(sql)["order_id"]
        return order_id

    # 插入一个线上课程
    def insert_course(self, classes_type):
        num = random.randint(1, 100)
        class_title = "这是课程类型{}--名称{}".format(classes_type, num)
        classes_img = "/1536548798927572876?imageView2/2/w/100/h/100/q/100"
        classes_description = "这是课程--介绍{}".format(num)
        professor = "f350756baf4211e8b6e30017fa004b58"
        created_time = int(time.time())
        sql = '''insert into zyt_classes (classes_type,classes_title,classes_img,is_professor,professor,
                    professor_position,professor_intro,classes_description,classes_cate_id,classes_organizers,
                      classes_address,classes_status,created_time,update_time,created_user) value
                      ({},"{}","{}",1,"{}","","","{}",1,"","",1,{},{},"xdchen")'''.format(
            classes_type, class_title, classes_img, professor, classes_description, created_time, created_time)
        course_id = self.opera_db.insert_data(sql)
        return course_id

    # 插入线上课时
    def insert_course_hour(self, classes_id):
        num = random.randint(1, 100)
        classes_hour_name = "这是课时名称{}".format(num)
        sql = '''insert into zyt_classes_hour (classes_id,classes_hour_name,classes_url) value ({},"{}","")'''.format(
            classes_id, classes_hour_name)
        hour_id = self.opera_db.insert_data(sql)
        return hour_id

    # 新增一个问题，并购买
    def get_ask(self, user_id, token, e_id):
        api = "/api/v1/qa/qsubmit"
        random_mun = random.randint(1, 100)
        qa_headers = {"content-type": "application/json"}
        data = {"user_id": user_id,
                "token": token,
                "eid": e_id,
                "title": "固定问题题目 -- %s" % random_mun,
                "description": "固定问题描述 -- %s" % random_mun,
                "img": ["/1536116758846885506?imageView2/2/w/212/h/136/q/100"]}
        qid = self.run_method.post(api, data, headers=qa_headers).json()[
            "data"]["last_id"]
        # 购买问题
        self.zyt_pay_order(
            user_id, token, qid, 2, 0, "#/expert/payment")
        return qid

    # 专家回答一个问题
    def get_answer(self, e_id, e_token, qid):
        api = "/api/v1/qa/asubmit"
        answer_content = "这是问题答案 -- %s" % (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data = {"user_id": e_id,
                "token": e_token,
                "qid": qid,
                "answer_content": answer_content}
        self.run_method.post(api, data)

    # 新增作品项目
    def get_project(self, user_id, token):
        # 作品 /api/v1/user/saveproject
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p_name = "作品名称 %s" % time_now
        p_desc = "作品简介 %s" % time_now
        p_img = "/1535965522439599110?imageView2/2/w/212/h/136/q/100"
        api = "/api/v1/user/saveproject"
        data = {
            "user_id": user_id,
            "token": token,
            "p_name": p_name,
            "p_desc": p_desc,
            "p_img": p_img}
        res = self.run_method.post(api, data)
        return res


if __name__ == "__main__":
    get_data = SQLData()
