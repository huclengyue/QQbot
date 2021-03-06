import time
from apscheduler.schedulers.blocking import BlockingScheduler
from cqhttp import CQHttp
import db, manager, tuling_reply

bot = CQHttp(api_root='http://127.0.0.1:5700')
ROOT = 6965717
GROUP = 593465097

ORC = "图片识别"
simple = "简单模式"
enable = "全功能模式"
disabled = "禁用"
reply = True
global qq_list
qq_list = db.select_all()

SENSITIVE = db.select_sensitive_all()


@bot.on_message()
def handle_msg(context):
    print(context)
    user = context["user_id"]
    group = context["group_id"]
    # 群聊
    if context["message_type"] == "group":
        global qq_list
        # 解析数据
        msg, image_msg = manager.json_pare(context["message"])
        if str(msg).startswith("-") and user == ROOT:
            manager.group_manager(context, group, msg, image_msg, user)
            qq_list = db.select_all()

        else:
            if qq_list is None:
                qq_list = db.select_all()
            group_type = manager.is_support(group, qq_list)
            if group_type and group_type == db.ENABLE:
                for word in SENSITIVE:
                    if word in msg:
                        return {'reply': '含有敏感字：' + word + ' 警告一次', 'at_sender': True}
                bot.send(context, tuling_reply.send_msg(msg, user))
    # return {'reply': context['message'], 'at_sender': False}


@bot.on_event('group_increase')
def handle_group_increase(context):
    global qq_list
    if qq_list is None:
        qq_list = db.select_all()
    group_type = manager.is_support(context["group_id"], qq_list)
    if group_type:
        user = context["user_id"]
        bot.send(context, message='欢迎 @' + manager.on_add(context["group_id"],
                                                          user) + " 加入本群\n请自觉将群名片改为游戏ID，谢谢配合！",
                 is_raw=True)  # 发送欢迎新人


# 成员退出
@bot.on_event('group_decrease')
def handle_group_increase(context):
    global qq_list
    if qq_list is None:
        qq_list = db.select_all()
    group_type = manager.is_support(context["group_id"], qq_list)
    if group_type:
        reply = ""
        user = context["user_id"]
        type_event = context["sub_type"]
        if type_event == "leave":
            reply = "退出群"
        elif type_event == "kick" and type_event == "kick_me":
            reply = "被踢出群"
        bot.send(context, message=manager.get_stranger_info(user) + reply, is_raw=True)


@bot.on_request('friend')
def handle_request(context):
    return {'approve': True}  # 同意加好友请求


@bot.on_request('group')
def handle_group_request(context):
    if context['message'] is "":
        return {'approve': False, 'reason': '你填写的验证信息有误'}
    else:
        return {'approve': True}

    # 群: 303331009 QQ: 605774840


bot.run(host='127.0.0.1', port=8080)


# def my_job():
#     global qq_list
#     for group in qq_list:
#         bot.send_group_msg(group_id=group["number"],
#                                  message=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
#                                  auto_escape=False)
#
#
# sched = BlockingScheduler()
# sched.add_job(my_job, 'interval', seconds=10)
# sched.start()
