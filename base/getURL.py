
import base.setting


class API:

    def proto_api_url(self, grpc_data=None, proto_method=None):
        format_url = base.setting.grpc_format_url
        if not format_url:
            raise RuntimeError("no url been set")
        url = format_url % (grpc_data, proto_method)
        return url

    def http_api_url(self, url_params=None):
        base_url = base.setting.http_base_url
        if not base_url:
            raise RuntimeError("no url been set")
        url = "{0}{1}".format(base_url, url_params)
        return url

    def get_url(
            self,
            method,
            grpc_data=None,
            proto_method=None,
            url_params=None):
        url = None
        if method == "GRPC":
            url = self.proto_api_url(
                grpc_data=grpc_data,
                proto_method=proto_method)
        elif method in ("HTTP", "HTTPS"):
            url = self.http_api_url(url_params=url_params)
        return url


if __name__ == "__main__":
    get_url =API()
    api = "v1/course/hour"
    url = get_url.http_api_url(api)
    print(url)