from baiduyun.baiduyun import Baiduyun
import requests,json
from qingtengyun.login.getcookie import getCookie
import time
from qingtengyun.config import qingtenyun_domain

class CheckAgent(object):
    def __init__(self):
        pass
    '''获取已安装agent主机'''
    def isInstalledAgent(self):
        url = f"{qingtenyun_domain}/v1/assets/host/list"
        data = {"page": 1, "size": 50, "filters": ["group", "platform", "hostLocation", "chargeName"],
         "orders": [{"field": "agentStatus", "ascend": True}], "search": {"agentStatus": [0]}, "params": {}}
        try:
            req = requests.post(url=url,json=data,headers=getCookie().getcookie())
            result = json.loads(req.text)
            total = result.get('data')['total']
            page = int(total/50)+1
            host_list = []
            for i in range(1,page+1):
                data = {"page": i, "size": 50, "filters": ["group", "platform", "hostLocation", "chargeName"],
         "orders": [{"field": "agentStatus", "ascend": True}], "search": {"agentStatus": [0]}, "params": {}}
                req = requests.post(url=url,json=data,headers=getCookie().getcookie())
                result = json.loads(req.text)
                rows = result.get('data')['rows']
                host_list += [row.get('displayIp') for row in rows]
            return host_list
        except Exception as e:
            print(e)

    def checkInstall(self):
        time.sleep(5) #先等待5秒，因为刚登陆进来资源没那么快加载
        host_set = set(self.isInstalledAgent())  #已安装agent主机
        outbounds = Baiduyun().outbound_all_by_eip_dict()
        noagent_list = [] #未安装agent
        for i in outbounds:
            if type(i.get('private_ip')) is list:
                for private_ip in i.get('private_ip'):
                    if private_ip not in host_set:
                        content = f"**公网ip**：{i.get('eip')} -- **内网IP:**{private_ip}\n"
                        noagent_list.append(self.body(content))
                        print(content)
            else:
                if i.get('private_ip') not in host_set:
                    content = f"**公网ip**：{i.get('eip')} -- **内网IP:**{i.get('private_ip')}\n"
                    noagent_list.append(self.body(content))
                    print(content)
        remedDesc_dict = {
            "tag": "div",
            "text": {
                "content": "主机绑定了eip，或者绑定了SLB且SLB绑定了EIP，能够被互联网用户访问，请尽快安装青藤云agent",
                "tag": "lark_md"
            }
        }
        noagent_list.append(remedDesc_dict)
        title = "以下主机互联网能访问，且未安装青藤云agent"
        return {"content":noagent_list,"title":title}

    def body(self,content):
        host = {
            "tag": "div",
            "text": {
                "content": content,
                "tag": "lark_md"
            }
        }
        return host

if __name__ == "__main__":
    check = CheckAgent()
    isInstall = check.isInstalledAgent()
    with open('baidu.txt','r')as f:
        result = [host.strip() for host in f.readlines() if host.strip() not in isInstall]
    print(result)
    c = check.checkInstall()
    print(c)
