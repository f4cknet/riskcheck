import requests,json
from qingtengyun.login.getcookie import getCookie
import time
from qingtengyun.config import qingtenyun_domain

class weakPass(object):
    def weak_pass(self,app):
        url = f"{qingtenyun_domain}/v1/assets/vul3/weakpass/hosts_with_vul"
        print(app)
        data = {"page":1,"size":50,"filters":["group"],"charts":["group","type"],"search":{"status":[1]},"params":{"app":f"{app}","isCiphered":False},"orders":[{"field":"ip","ascend":True}]}
        try:
            req = requests.post(url=url,json=data,headers=getCookie().getcookie())
            res = json.loads(req.text)
            data = res.get('data')
            rows = data.get('rows')
            host_vuln = []
            for row in rows:
                ip = row.get('displayIp')
                hostname = row.get('hostname')
                title = row.get('title')
                user = row.get("username")
                passwd = row.get("passwd")
                host = {
                    "tag": "div",
                    "text": {
                        "content": f"**IP：{ip}，主机名：{hostname}**\n - **用户名/密码**\n{user}/{passwd}",
                        "tag": "lark_md"
                    }
                }
                host_vuln.append(host)
            remedDesc_dict = {
                    "tag": "div",
                    "text": {
                        "content": "请尽快修改密码",
                        "tag": "lark_md"
                    }
                }
            host_vuln.append(remedDesc_dict)


            result = {"content":host_vuln,"title":title}
            return result
        except Exception as e:
            print(e)

    def app_view(self):
        time.sleep(5) #先等待5秒，因为刚登陆进来资源没那么快加载
        url = f"{qingtenyun_domain}/v1/assets/vul3/weakpass/app_view"
        data = {"page":1,"size":50,"filters":["group","apps"],"charts":["apps"],"orders":[{"field":"total","ascend":False}],"search":{"status":[1]}}
        try:
            req = requests.post(url=url,json=data,headers=getCookie().getcookie())
            data = json.loads(req.text)
            rows = data.get('data')['rows']
            app_list = []
            for row in rows:
                vulnid = row.get('vulId')
                app = row.get('app')
            app_list.append(app)
            return app_list
        except Exception as e:
            print(e)


if __name__ == "__main__":
    weak = weakPass()
    app = weak.app_view()
    for i in app:
        weak.weak_pass(i)