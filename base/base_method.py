import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.get_url import GetUrl
from base.grpc_base_run import GrpcBaseRun
import json
import requests


class BaseMethod:

    def __init__(self):
        self.grpcBaseRun = GrpcBaseRun()
        self.get_url = GetUrl()

    def grpc(self, proto_method, data_dict=None):
        res = None
        if data_dict is None:
            data_dict = {}
        data_str = json.dumps(data_dict)
        url = self.get_url.proto_api_url(data_str, proto_method)
        returncode = self.grpcBaseRun.run_bas_grpc(url)
        if returncode[0] == 0:
            res = json.loads(returncode[1])
        elif returncode[0] == 1:
            res = returncode[2]
        else:
            res = "指令错误"
        return res

    def post(self, api, data=None, json=None, headers=None, cookies=None, files=None):
        '''
        api: 请求资源
        data: content-type为 form 时，使用data参数
        json: content-type为 json 时，使用data参数
        cookies:
        headers:
        files:
        '''
        url = self.get_url.http_api_url(api)
        return requests.post(url=url, data=data, json=json, headers=headers, cookies=cookies, files=files)

    def get(self, api, data=None, json=None, headers=None, cookies=None):
        '''
        api: 请求资源
        data: content-type为 form 时，使用data参数
        json: content-type为 json 时，使用data参数
        cookies:
        headers:
        '''
        url = self.get_url.http_api_url(api)
        return requests.get(url=url,params=data,json=json,headers=headers,cookies=cookies)
    
    def errInfo(self,res):
        """
        res: http的response对象
        request_id: response对象中的request_id
        """
        if isinstance(res,object):
            return {"err":res.text,"request_id":res.headers["X-Request-Id"]}


if __name__ == "__main__":
    api = "/zone/list"
    base = BaseMethod()
    data = {"page":1,
            "size":1}
    res = base.post(api,data)
    err = base.errInfo(res)
    print(err)
    
