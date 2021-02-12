# coding: utf-8
import requests
import os


class Authorize(object):
    # Get Token
    def __init__(self, corpid, corpsecret, proxies=None):
        # corpid    : wechat id
        # corpsecret: wechat secret
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.token_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}"
        )
        self.proxies = proxies

    def get_token(self):
        # get_token
        json_ = requests.get(
            self.token_url.format(self.corpid, self.corpsecret), proxies=self.proxies
        ).json()
        return json_["access_token"]


class Send(object):
    # Send Message (text, image, video, voice...)
    def __init__(self, agentid, token, data=None, proxies=None):
        # agentid: application id
        # token  : Authorize get token
        self.agentid = agentid
        self.token = token
        self.send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}"
        )
        self.proxies = proxies

        if data != None:
            self.data = data
        else:
            self.data = {
                "agentid": self.agentid,
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800,
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
        s = requests.post(
            self.send_url.format(self.token), json=self.data, proxies=self.proxies
        ).json()
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

    def send_img(self, media_id=None, img_path=None, name="", to_type="touser"):
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

    def send_voice(self, voice_id, voice_path, name="", to_type="touser"):
        # voice_id: wechat temp voice id (three days)
        # voice_path: local voice path
        assert name != ""
        self._type(to_type, name)
        self.data["msgtype"] = "voice"
        if voice_id == None and voice_path == None:
            raise Exception("please input voice_id or voice_path")
        if voice_path != None:
            u = Upload(self.token)
            voice_id = u.upload_voice(voice_path)
        print(voice_id)
        self.data["voice"] = {}
        self.data["voice"]["media_id"] = voice_id
        return self._send()

    def send_video(
        self, video_id, video_path, title="", description="", name="", to_type="touser"
    ):
        # video_id: wechat temp voice id (three days)
        # video_path: local voice path
        assert name != ""
        self._type(to_type, name)
        self.data["msgtype"] = "video"
        if video_id == None and video_path == None:
            raise Exception("please input video_id or video_path")
        if video_path != None:
            u = Upload(self.token)
            video_id = u.upload_video(video_path)
        print(video_id)
        self.data["video"] = {}
        self.data["video"]["media_id"] = video_id
        self.data["video"]["title"] = title
        self.data["video"]["description"] = description

        return self._send()

    def send_file(self, file_id=None, file_path=None, name="", to_type="touser"):
        # file_id: wechat temp media id (three days)
        # file_path: local file path
        # TO-DO:    suport file url
        assert name != ""
        self._type(to_type, name)
        self.data["msgtype"] = "file"
        if file_id == None and file_path == None:
            raise Exception("please input file_id or file_path")
        if file_path != None:
            u = Upload(self.token)
            file_id = u.upload_file(file_path)
        print(file_id)
        self.data["file"] = {}
        self.data["file"]["media_id"] = file_id
        return self._send()

    def send_textcard(self, textcard, name="", to_type="touser"):
        # textcard: send textcard
        # to_type: touser or topary or totag
        # name   : multiple names are separated by "|"
        assert name != ""
        self.data["msgtype"] = "textcard"
        self._type(to_type, name)
        self.data["textcard"] = textcard
        return self._send()

    def send_news(self, news, name="", to_type="touser"):
        # news   : send news
        # to_type: touser or topary or totag
        # name   : multiple names are separated by "|"
        assert name != ""
        self.data["msgtype"] = "news"
        self._type(to_type, name)
        self.data["news"] = {}
        self.data["news"]["articles"] = news
        return self._send()

    def send_markdown(self, markdown, name="", to_type="touser"):

        assert name != ""
        self.data["msgtype"] = "markdown"
        self._type(to_type, name)
        self.data["markdown"] = {}
        self.data["markdown"]["content"] = markdown
        return self._send()


class Upload(object):
    # Upload Data(image, video, voice...)
    # TO-DO: Upload video, voice...

    def __init__(self, token, proxies=None):
        self.token = token
        self.headers = {
            "content-type": "multipart/form-data",
        }
        self.upload_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}"
        )
        self.proxies = proxies

    def upload_img(self, img_path):
        # img_path: local image path
        # TO-DO:    suport img url
        type_ = "image"
        with open(img_path, "rb") as f:
            f_img_b = f.read()

        files = {"image": (os.path.basename(img_path), f_img_b, "image/jpg")}
        s = requests.post(
            self.upload_url.format(self.token, type_), files=files, proxies=self.proxies
        ).json()
        return s["media_id"]

    def upload_voice(self, voice_path):
        # voice_path: local voice path
        type_ = "voice"
        with open(voice_path, "rb") as f:
            f_voice_b = f.read()

        files = {"voice": (os.path.basename(voice_path), f_voice_b, "voice/amr")}
        s = requests.post(
            self.upload_url.format(self.token, type_), files=files, proxies=self.proxies
        ).json()
        return s["media_id"]

    def upload_video(self, video_path):
        # TO-DO
        video_id = 1
        return video_id

    def upload_file(self, file_path):
        # TO-DO
        file_id = 1
        return file_id