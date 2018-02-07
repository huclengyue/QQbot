from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '10723084'
API_KEY = 'l1ddO816pvSukFhHOrfdnty7'
SECRET_KEY = '54tSUS2u8IHdrpObaVVZXckNmGK0PBAl'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def image_orc(url):
    msg = ""
    """ 如果有可选参数 """
    options = {"detect_direction": "true", "detect_language": "false"}
    """ 带参数调用网络图片文字识别, 图片参数为远程url图片 """
    info = client.webImageUrl(url, options)
    if "words_result_num" in info and info["words_result_num"] > 0:
        for text in info["words_result"]:
            msg = text + "\n"
        print(msg)
        return msg
    else:
        return "识别错误"


if __name__ == '__main__':
    url = "http://p1.gexing.com/G1/M00/FB/F2/rBACFFI7yr_yD7a9AABZATC8j00783.jpg"
    image_orc(url)
