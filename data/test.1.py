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
        "building_id" :"115549442664313912",
        "model_type":"T"
    }
# files = {"file":open(filename,'rb')}
with open(filename,'rb') as fileop:
    files = {"file":fileop}
# headers = {}
    r = requests.post(api,data=data,files=files,headers=corp_header)
print(r.headers)
print(r.status_code)
print(r.json())
