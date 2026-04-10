class Header:
    def __init__(self):
        self.headers = {}

    def set_header(self, key, value):
        self.headers[key] = value

    def set_header_from_dict(self, kv):
        for k, v in kv.items():
            self.set_header(k, v)

    def remove_header(self, key):
        if key in self.headers:
            del self.headers[key]

    def get(self):
        return self.headers

class HeaderBuilder:
    @staticmethod
    def build_common_header():
        common_header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
        }
        header = Header()
        header.set_header_from_dict(common_header)
        return header
    @staticmethod
    def build_request_header(auth):
        headers = {
            "accept": "application/vnd.linkedin.normalized+json+2.1",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "csrf-token": auth.cookie["JSESSIONID"].replace("\"", ""),
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.linkedin.com/",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
            "x-li-lang": "zh_CN",
            "x-li-track": "{\"clientVersion\":\"1.13.21043\",\"mpVersion\":\"1.13.21043\",\"osName\":\"web\",\"timezoneOffset\":8,\"timezone\":\"Asia/Shanghai\",\"deviceFormFactor\":\"DESKTOP\",\"mpName\":\"voyager-web\",\"displayDensity\":1,\"displayWidth\":2560,\"displayHeight\":1600}",
            "x-restli-protocol-version": "2.0.0"
        }
        header = Header()
        header.set_header_from_dict(headers)
        return header