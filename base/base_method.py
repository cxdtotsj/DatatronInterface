from base.get_url import GetUrl
from base.grpc_base_run import GrpcBaseRun
import json
import requests
from copy import deepcopy


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
        return requests.post(url=url, data=data, json=json, headers=headers, cookies=cookies, files=files,timeout=30)

    def get(self, api, data=None, json=None, headers=None, cookies=None):
        '''
        api: 请求资源
        data: content-type为 form 时，使用data参数
        json: content-type为 json 时，使用data参数
        cookies:
        headers:
        '''
        url = self.get_url.http_api_url(api)
        return requests.get(url=url,params=data,json=json,headers=headers,cookies=cookies,timeout=30)

    def put(self,api,data=None):
        """
        api: URL
        data: 文件流
        """
        return requests.put(url=api,data=data,timeout=60)

    def errInfo(self,res):
        """
        res: http的response对象
        request_id: response对象中的request_id
        """
        if isinstance(res,object):
            return "\033[31m {} \033[0m".format({"err":res.text,"request_id":res.headers["X-Request-Id"]})
    
    def assertInfo(self,message):
        """assert错误信息输出"""
        return "\033[31m {} \033[0m".format(message)
    
    def dict_in_list(self,k,iter):
        """
        在list中增加字典,
        k为字典的key
        iter为可迭代对象,每个迭代元素为value值
        """
        data_list = []
        d = {}
        for i in range(len(iter)):
            d[k] = iter[i]
            data_list.append(d)
            d = deepcopy(d)
        return data_list

if __name__ == "__main__":
    import os
    api = "/user/create"
    base = BaseMethod()
    url = 'https://s3.arctron.cn/test/citest?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=9EZ4QY1DB3QQ1W75AAR1%2F20181218%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20181218T051908Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=c330cbb3269f03fb6cf8626b0a4b6501a2cb74eceaa9e0a0774166063f9cbb6d'
    file_Office = os.path.join(os.path.dirname(os.path.dirname(__file__)),'dataconfig','Office.objr')
    with open(file_Office, 'rb') as fileop:
        res = base.put(url,data=fileop)
        print(res.status_code)
        print(res.text)
