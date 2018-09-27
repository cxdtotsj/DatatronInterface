import subprocess


class GrpcBaseRun:

    def run_bas_grpc(self, url):
        recomd = subprocess.run(
            url,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True)
        return recomd.returncode, recomd.stdout, recomd.stderr


if __name__ == '__main__':

    url = "/home/bear/go/src/pb/grpcurl -plaintext -d '{\"mobile\": \"18321829313\", \"code\": \"781315\", \"passwd\": \"Password01!\"}' -import-path /home/bear/go/src/pb/ -proto ./user.proto 10.241.11.4:6443 pb.User/Register"
    base = GrpcBaseRun()
    res = base.run_bas_grpc(url)
    print(res[0])
