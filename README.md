## Wechat_msg

企业微信发送消息接口，Python

```python
from wechat_msg.WeChat import Authorize, Send, Upload

corpid = ''
corpsecret = ''
agentid = ''

a = Authorize(corpid, corpsecret)
token = a.get_token()

s = Send(agentid, token)
s.send_msg("TEST", name="username")
s.send_img("img_path", name="username")
```