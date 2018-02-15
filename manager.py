import db, AipOcr
from cqhttp import CQHttp

bot = CQHttp(api_root='http://127.0.0.1:5700/')

ORC = "图像识别"
simple = "简单模式"
enable = "全功能模式"
disabled = "禁用"


# 群管理
def group_manager(context, group, msg, image_msg, user):
    reply = ""
    if simple in msg:
        reply = db.select(group, db.SIMPLE)
    elif enable in msg:
        reply = db.select(group, db.ENABLE)
    elif disabled in msg:
        reply = db.select(group, db.DISABLED)
    elif ORC in msg:
        if image_msg:
            for image in image_msg:
                reply = reply + AipOcr.image_orc(image) + "\n"
        else:
            reply = "没有检测到图片"
    bot.send(context, reply)
    # 是否是图片
    if "[CQ:image" in msg:
        print(str(user) + " : " + msg.split("url=")[1].replace("]", ""))
    else:
        print(str(user) + " : " + msg)
        # bot.send(context, '你好呀，')
        get_group_list(group)
        # return {'reply': on_add(group, user), 'at_sender': False}
        # bot.send(context, '你好呀，下面一条是你刚刚发的：')


# 是否支持此群
def is_support(group, list):
    group_type = ""
    for group_info in list:
        if group_info["number"] == group:
            group_type = group_info["type"]
    return group_type


# 获得此群所有成员
def get_group_list(group_id):
    data = bot.get_group_member_list(group_id=group_id)
    if data:
        list = []
        print(len(data))


# 查询某个成员的群昵称\昵称\QQ号
def on_add(group_id, user_id):
    data = bot.get_group_member_info(group_id=group_id, user_id=user_id, no_cache=True)
    if data:
        if data["card"]:
            return data["card"]
        elif data["nickname"]:
            return data["nickname"]
        else:
            return data["user_id"]


def json_pare(json):
    text = []
    image_url = []

    for message in json:
        msg_type = message["type"]
        if msg_type == "image":
            image_url.append(message["data"]["url"])
        if msg_type == "text":
            text.append(message["data"]["text"])
    return "".join(text), image_url


# 陌生人的信息
def get_stranger_info(id):
    data = bot.get_stranger_info(user_id=id, no_cache=True)
    if data:
        if data["nickname"]:
            return data["nickname"]
        else:
            return id


def get_group_member_list():
    pass