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

filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'dataconfig','LangCha.objr')
print(filename)

me = MultipartEncoder(
    fields={
        "building_id" :"113665377212314155",
        "mt":"T",
        "coord":"0,0,0",
        "file":('LangCha.objr',filename,"application/octet-stream")
    })
# headers = {}
corp_header["Content-Type"] = me.content_type
r = requests.post(api,data=me,headers=corp_header)
print(r.status_code)
print(r.json())