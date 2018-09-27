from base.getURL import API
from base.grpcBaseRun import GrpcBaseRun
import json
import requests


class BaseMethod:

    def __init__(self):
        self.grpcBaseRun = GrpcBaseRun()
        self.get_url = API()

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

    def post(self, api, data=None, cookies=None, headers=None):
        res = None
        url = self.get_url.http_api_url(api)
        if cookies is not None:
            if headers is not None:
                res = requests.post(url=url, json=data, cookies=cookies, headers=headers)
            else:
                res = requests.post(url=url, data=data, cookies=cookies)
        else:
            if headers is not None:
                res = requests.post(url=url, json=data, headers=headers)
            else:
                res = requests.post(url=url, data=data)
        return res

    def get(self, api, data=None, cookies=None,headers=None):
        res = None
        url = self.get_url.http_api_url(api)
        if cookies is not None:
            if headers is not None:
                res = requests.get(url=url, json=data, cookies=cookies,headers=headers)
            else:
                res = requests.get(url=url, params=data, cookies=cookies)
        else:
            if headers is not None:
                res = requests.get(url=url, json=data,headers=headers)
            else:
                res = requests.get(url=url, params=data)
        return res

    # 获取请求返回中的"result"结果
    def get_result(self, res):
        res_dict = res.json()
        status = res_dict["result"]
        return status

    # 获取请求返回中的errno
    def get_errno(self, res):
        res_dict = res.json()
        status = res_dict["data"]["errno"]
        return status

    def run_main(self, method, url, data=None, cookies=None,headers=None):
        res = None
        if method == "GRPC":
            res = self.grpc(proto_method=url, data_dict=data)
        elif method == "POST":
            res = self.post(api=url, data=data, cookies=cookies,headers=headers)
        elif method == "GET":
            res = self.get(api=url, data=data, cookies=cookies,headers=headers)
        return res


if __name__ == "__main__":
    api = "/api/v1/course/list"
    base = BaseMethod()
    data = {"l": 5, "p": 2}
    res = base.get(api, data).json()
    # print(res)
    result = res["data"]
    print(result)

    # url = "https://zyt-dev.arctron.cn/api/v1/course/list"
    # data = {"l": 3}
    # res = requests.get(url,params=data).json()
    # print(res)
