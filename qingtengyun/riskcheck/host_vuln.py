import requests,json
from qingtengyun.login.getcookie import getCookie
import time
from baiduyun.baiduyun import Baiduyun
from qingtengyun.config import qingtenyun_domain

baiduyun = Baiduyun()
outboundip = baiduyun.outbound_all_by_eip_list()
class hostVuln(object):
    def host_with_vuln(self,vulId,level):
        url = f"{qingtenyun_domain}/v1/assets/vul3/poc/hosts_with_vul"
        data = {"page":1,"size":50,"orders":[{"field":"ip","ascend":True}],"filters":["group"],"params":{"vulId":vulId}}
        try:
            req = requests.post(url=url,json=data,headers=getCookie().getcookie())
            res = json.loads(req.text)
            data = res.get('data')
            rows = data.get('rows')
            host_vuln = []
            remedDesc = ""
            title = ""

            if level == "critical":
                for row in rows:
                    ip = row.get('displayIp')
                    hostname = row.get('hostname')
                    title = row.get('title')
                    remedDesc = row.get('remedDesc')
                    pocCheckResults = row.get('pocCheckResults')
                    vuln_info = ""
                    for i in pocCheckResults:
                        checkResult = i.get('checkResult')+"\n"
                        vuln_info+=checkResult
                    host = {
                        "tag": "div",
                        "text": {
                            "content": f"**IP：{ip}，主机名：{hostname}**\n - **POC验证**\n{vuln_info}",
                            "tag": "lark_md"
                        }
                    }
                    host_vuln.append(host)
                remedDesc_dict = {
                    "tag": "div",
                    "text": {
                        "content": remedDesc,
                        "tag": "lark_md"
                    }
                }
            elif level == "high":
                for row in rows:
                    ip = row.get('displayIp')
                    if ip in outboundip:
                        hostname = row.get('hostname')
                        title = row.get('title')
                        remedDesc = row.get('remedDesc')
                        pocCheckResults = row.get('pocCheckResults')
                        vuln_info = ""
                        for i in pocCheckResults:
                            checkResult = i.get('checkResult') + "\n"
                            vuln_info += checkResult
                        host = {
                            "tag": "div",
                            "text": {
                                "content": f"**IP：{ip}，主机名：{hostname}**\n - **POC验证**\n{vuln_info}",
                                "tag": "lark_md"
                            }
                        }
                        host_vuln.append(host)
                remedDesc_dict = {
                    "tag": "div",
                    "text": {
                        "content": remedDesc,
                        "tag": "lark_md"
                    }
                }
            host_vuln.append(remedDesc_dict)
            return {"content":host_vuln,"title":title}
        except Exception as e:
            print(e)

    def must_fix_vuln(self):
        url = f"{qingtenyun_domain}/v1/assets/vul3/poc/vul_view"
        data = {"filters":["group","apps"],"orders":[{"field":"severity","ascend":False},{"field":"total","ascend":False}],"page":1,"size":50,"search":{}}
        try:
            req = requests.post(url=url,json=data,headers=getCookie().getcookie())
            data = json.loads(req.text)
            rows = data.get('data')['rows']
            critical_vulnId_list = []
            high_vulnId_list = []
            for row in rows:
                severity = row.get('severity')
                isExp = row.get('isExp')
                if(severity==4): #严重
                    critical_vulnId_list.append(row.get('vulId'))
                elif(severity==3): #高危
                    high_vulnId_list.append(row.get('vulId'))
            return {"critical":critical_vulnId_list,"high":high_vulnId_list}
        except Exception as e:
            print(e)

if __name__ == "__main__":
    vuln = hostVuln()
    critical_vulnid_list = vuln.must_fix_vuln().get('critical')
    high_vulnid_list = vuln.must_fix_vuln().get('high')