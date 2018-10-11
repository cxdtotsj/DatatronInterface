import json
import os


class OperetionJson:

    def __init__(self, file_path=None):
        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]
        if file_path is None:
            self.file_path = os.path.join(rootPath,'dataconfig','datatron_dev.json')
        else:
            self.file_path = file_path
        self.data = self.read_data()

    # 读取json文件
    def read_data(self):
        with open(self.file_path, encoding='utf-8') as fp:
            data = json.load(fp)
            return data

    # 根据关键字获取数据
    def get_data(self, id):
        return self.data[id]

    # 写json
    def write_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(data,ensure_ascii=False))
            fp.close()

    # 重写json
    def check_json_value(self, depend_key, depend_vaule):
        json_data = self.data
        json_data[depend_key] = depend_vaule
        try:
            self.write_data(json_data)
        except TypeError:
            print("写入json文件失败")


if __name__ == '__main__':
    json_o = OperetionJson()
    a= json_o.get_data("test01_07_zone")
    print(a)
