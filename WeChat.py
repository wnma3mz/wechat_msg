# coding: utf-8
import requests
import os


class Authorize(object):
    # Get Token
    def __init__(self, corpid, corpsecret):
        # corpid    : wechat id
        # corpsecret: wechat secret
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'

    def get_token(self):
        # get_token
        json_ = requests.get(
            self.token_url.format(self.corpid, self.corpsecret)).json()
        return json_['access_token']


class Send(object):
    # Send Message (text, image, video, voice...)
    # TO-DO: Send video, voice...
    def __init__(self, agentid, token, data=None):
        # agentid: application id
        # token  : Authorize get token
        self.agentid = agentid
        self.token = token
        self.send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'

        if data != None:
            self.data = data
        else:
            self.data = {
                "agentid": self.agentid,
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            }

    def _type(self, to_type, name):
        # to_type: touser or topary or totag
        if to_type in ["touser", "toparty", "totag"]:
            self.data[to_type] = name
        else:
            raise Exception(
                'please input the correct to_type, in ["to_user", "toparty", "totag"]'
            )

    def _send(self):
        s = requests.post(self.send_url.format(self.token),
                          json=self.data).json()
        return s

    def send_msg(self, content, name="", to_type="touser"):
        # content: send msg
        # to_type: touser or topary or totag
        # name   : multiple names are separated by "|"
        assert name != ""
        self.data["msgtype"] = "text"
        self._type(to_type, name)
        self.data["text"] = {}
        self.data["text"]["content"] = content
        return self._send()

    def send_img(self,
                 media_id=None,
                 img_path=None,
                 name="",
                 to_type="touser"):
        # media_id: wechat temp media id (three days)
        # img_path: local image path
        # TO-DO:    suport img url
        assert name != ""
        self._type(to_type, name)
        self.data["msgtype"] = "image"
        if media_id == None and img_path == None:
            raise Exception("please input media_id or img_path")
        if img_path != None:
            u = Upload(self.token)
            media_id = u.upload_img(img_path)
        print(media_id)
        self.data["image"] = {}
        self.data["image"]["media_id"] = media_id
        return self._send()


class Upload(object):
    # Upload Data(image, video, voice...)
    # TO-DO: Upload video, voice...

    def __init__(self, token):
        self.token = token
        self.headers = {
            "content-type": "multipart/form-data",
        }
        self.upload_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}'

    def upload_img(self, img_path):
        # img_path: local image path
        # TO-DO:    suport img url
        type_ = 'image'
        with open(img_path, 'rb') as f:
            f_img_b = f.read()

        files = {'image': (os.path.basename(img_path), f_img_b, 'image/jpg')}
        s = requests.post(self.upload_url.format(self.token, type_),
                          files=files).json()
        return s['media_id']
