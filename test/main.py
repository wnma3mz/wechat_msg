# coding: utf-8
from wechat_msg.WeChat import Authorize, Send, Upload

username = "LuJiangHu"
corpid = 'wwadb2ec01598c29d7'
corpsecret = '38N8xFLWcC_bD-9KuVw6yGA5MkGhOvg2e4iEC5TYy_U'
agentid = 1000003
a = Authorize(corpid, corpsecret)
token = a.get_token()
se = Send(agentid, token)

# send_txt = 'TEST'
# s = se.send_msg(send_txt, name=username)

# img_path = 'D:\\software\\FileLocator Pro\\help\\img\\contentsreport.png'
# s = se.send_img(img_path=img_path,name=username)

# textcard = {
#     'title': '领奖通知',
#     'description':
#     '<div class=\"gray\">2016年9月26日</div> <div class=\"normal\">恭喜你抽中iPhone 7一台，领奖码：xxxx</div><div class=\"highlight\">请于2016年10月10日前联系行政同事领取</div>',
#     'url': 'https://www.baidu.com',
#     'btntxt': '按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。',
# }
# s = se.send_textcard(textcard=textcard, name=username)

# news = [{
#     "title":
#     "中秋节礼品领取",
#     "description":
#     "今年中秋节公司有豪礼相送",
#     "url":
#     "https://www.baidu.com",
#     "picurl":
#     "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
# }, {
#     "title":
#     "中秋节礼品领取",
#     "description":
#     "今年中秋节公司有豪礼相送",
#     "url":
#     "https://www.baidu.com",
#     "picurl":
#     "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
# }]
# s = se.send_news(news=news, name=username)

markdown = """
                您的会议室已经预定，稍后会同步到`邮箱`
>**事项详情**
>事　项：<font color=\"info\">开会</font>
>组织者：@miglioguan
>参与者：@miglioguan、@kunliu、@jamdeezhou、@kanexiong、@kisonwang
>
>会议室：<font color=\"info\">广州TIT 1楼 301</font>
>日　期：<font color=\"warning\">2018年5月18日</font>
>时　间：<font color=\"comment\">上午9:00-11:00</font>
>
>请准时参加会议。
>
>如需修改会议信息，请点击：[修改会议信息](https://work.weixin.qq.com)
"""
# 普通微信不支持此消息类型
s = se.send_markdown(markdown=markdown, name=username)