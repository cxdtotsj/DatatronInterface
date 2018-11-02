import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_method import BaseMethod
from requests_toolbelt.multipart import MultipartEncoder
import requests
from data.public_param import PublicParam


pp = PublicParam()

corp_header,corp_id = pp.get_corp_user()

api = "https://dt-dev.arctron.cn/api/building/model/upload"

filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'dataconfig','Office.objr')



data = {
        "building_id" :"114713326885286963",
        "model_type":"M"
    }
# files = {"file":open(filename,'rb')}
with open(filename,'rb') as fileop:
    files = {"file":fileop}
# headers = {}
    r = requests.post(api,data=data,files=files,headers=corp_header)
    print(r.status_code)
    print(r.json())


# r = requests.get("https://s3.arctron.cn/bim/109777231634510875/cvt/114419753606459948/data.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=9EZ4QY1DB3QQ1W75AAR1%2F20181030%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20181030T082215Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=ae903286ef422eb1fffb3f9865e9a8fd7c5984cbc6bd2c7cbbcebcb0d77cd111")
# print(r.json()["Floors"][0]["Guid"])