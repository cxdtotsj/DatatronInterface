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

    def post(self, api, data=None, json=None, cookies=None, headers=None):
        '''
        api: 请求资源
        data: content-type为 form 时，使用data参数
        json: content-type为 json 时，使用data参数
        cookies:
        headers:
        '''
        res = None
        url = self.get_url.http_api_url(api)
        if cookies is not None:
            if headers is not None:
                if data is not None:
                    res = requests.post(url=url, data=data,
                                        cookies=cookies, headers=headers)
                elif json is not None:
                    res = requests.post(url=url, json=json,
                                        cookies=cookies, headers=headers)
                else:
                    res = requests.post(
                        url=url, cookies=cookies, headers=headers)
            else:
                res = requests.post(url=url, data=data, cookies=cookies)
        else:
            if headers is not None:
                if data is not None:
                    res = requests.post(url=url, data=data, headers=headers)
                elif json is not None:
                    res = requests.post(url=url, json=json, headers=headers)
                else:
                    res = requests.post(url=url, headers=headers)
            else:
                res = requests.post(url=url, data=data)
        return res

    def get(self, api, data=None, json=None, cookies=None, headers=None):
        '''
        api: 请求资源
        data: content-type为 form 时，使用data参数
        json: content-type为 json 时，使用data参数
        cookies:
        headers:
        '''
        res = None
        url = self.get_url.http_api_url(api)
        if cookies is not None:
            if headers is not None:
                if data is not None:
                    res = requests.get(url=url, params=data,
                                       cookies=cookies, headers=headers)
                elif json is not None:
                    res = requests.get(url=url, json=json,
                                       cookies=cookies, headers=headers)
                else:
                    res = requests.get(
                        url=url, cookies=cookies, headers=headers)
            else:
                res = requests.get(url=url, params=data, cookies=cookies)
        else:
            if headers is not None:
                if data is not None:
                    res = requests.get(url=url, params=data, headers=headers)
                elif json is not None:
                    res = requests.get(url=url, json=json, headers=headers)
                else:
                    res = requests.get(url=url, headers=headers)
            else:
                res = requests.get(url=url, params=data)
        return res


if __name__ == "__main__":
    api = "/user/create"
    base = BaseMethod()
    data = {'name': "auto_test03",
            "password": "123456"}
    header = {"Authorization": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJTUEVDSUFMLUFETUlOLUlEIiwicm9sIjoxMDczNzQxODI0LCJpYXQiOjE1MzgwMjc4NDAsInNlcyI6ImFiY2QxMjM0In0.F_PxEwGsEITEAkLVInqPMI7kI348LSUx-4n7tqkpg9cRjqroZbe6_Y94euTXT8FnyaSSHDfDFTvzmMmVZje_T4SnVrbQsqHLONrc39kH7iq2Ci9Z7m6Itr5W4qifKFo6RZPh1MMn-Yz2bhc5Dn9fg0ENEA2uQPRgm95eiO0MDUE"}
    res = base.post(api, data, headers=header)
