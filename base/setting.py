import os


# 项目名称
ENV = "Datatron_Dev Testing"

# GRPC参数和方法名
gprc_base_url = "{} -plaintext -d '%s' -import-path {} -proto %s"

# GRPC命令及proto文件地址
grpc = "/home/bear/go/src/pb/grpcurl"
proto_file = "/home/bear/go/src/pb/"

# 拼接grpc_base_url
grpc_format_url = gprc_base_url.format(grpc, proto_file)


# HTTP域名，环境变量中存在key
http_base_url = os.environ.get("base_url") or "https://dt-dev.arctron.cn/api"


# 数据库信息
# db_url = "newhero.mysqldb.chinacloudapi1.cn:3306"
if "db_url" in os.environ:
    db_url = os.environ.get("db_url")
    if ":" in db_url:
        db_host = db_url.split(":")[0]
        db_port = int(db_url.split(":")[1])
    else:
        db_host = db_url
        db_port = 3306
else:
    db_host = "10.241.11.7"
    db_port = 4000

db_db = os.environ.get("db_db") or "datatron"

db_user = os.environ.get("db_user") or "root"

db_password = os.environ.get("db_password") or "pAssw0rd"


if __name__ == '__main__':
    db_url = os.environ.get("db_url").strip()
    db_host1 = db_url.split(":")[0].strip()
    db_port1 = int(db_url.split(":")[1])
    print(type(db_host))
    print(type(db_port))
