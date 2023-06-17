import hashlib
import base64
import hmac,os
import time,json,requests


class sendMsg(object):
  def __init__(self):
    self.url = os.getenv('FEISHU_WEBHOOK_URL')
    self.secret = os.getenv('FEISHU_WEBHOOK_SECRET')

  def send(self,content,title):
    msg = self.msg_template(content,title)
    time_stamp = int(time.time())
    sign = self.gen_sign(time_stamp)
    msg["timestamp"] = time_stamp
    msg['sign'] = sign
    r = requests.post(url=self.url,json=msg)
    return r.text

  def gen_sign(self,timestamp):
    string_to_sign = '{}\n{}'.format(timestamp, self.secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign

  def msg_template(self,content,title):
    msg = {
      "msg_type": "interactive",
      "card":{
        "config": {
        "wide_screen_mode": True
        },
        "elements":content,
        "header":{
          "template": "red",
          "title": {
            "content": title,
            "tag": "plain_text"
          }
        }
      }
    }
    return msg
if __name__ == "__main__":
  s = sendMsg()
  with open('1.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
  s.send(data)