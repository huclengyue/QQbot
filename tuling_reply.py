import requests

ROOT_URL = "http://www.tuling123.com/openapi/api"
KEY = "f9b889620c9349f68534b2bdcdec458a"

TEXT = 100000  # 文本类
URL = 200000  # 链接类
NEWS = 302000  # 新闻类
CAI_PU = 308000  # 菜谱类


# 313000（儿童版）	儿歌类
# 314000（儿童版）	诗词类
def send_msg(info, userID):
    resp = requests.post(ROOT_URL, data={"key": KEY, "info": info, "userid": userID})
    if resp.ok:
        return analysis_json(resp.json())
    else:
        return "你说撒子嘛！"


def analysis_json(resp):
    print(resp)
    if resp:
        code = resp["code"]
        if code == TEXT:
            return resp["text"]
        elif code == URL:
            text = resp["text"] + "\n" + resp["url"]
            return text
        elif code == NEWS:
            text = resp["text"] + "\n "
            for news in resp["list"]:
                text = text + news["article"] + "\n" + "\n" + news["detailurl"] + "\n" + "\n"
            return text
        elif code == CAI_PU:
            text = resp["text"] + "\n"
            for news in resp["list"]:
                text = text + news["info"] + "\n" + "\n" + news["name"] + "\n" + \
                       news["detailurl"] + "\n" + "\n"
        return text
        # else
    # else:


if __name__ == '__main__':
    send_msg("新闻", 6965717)
