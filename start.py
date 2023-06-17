from qingtengyun.riskcheck.host_vuln import hostVuln
from service.webhook import sendMsg
from qingtengyun.riskcheck.weak_password import weakPass
from qingtengyun.riskcheck.checkagent import CheckAgent
import logging

sendmsg = sendMsg()
def send_vuln():
    hostvuln = hostVuln()
    critical_vuln_id_list = hostvuln.must_fix_vuln().get('critical')
    high_vuln_id_list = hostvuln.must_fix_vuln().get('high')
    for vulnId in critical_vuln_id_list:
        result = hostvuln.host_with_vuln(vulnId,"critical")
        if len(result.get('content'))>1:
            print(result.get('content'))
    for vulnId in high_vuln_id_list:
        result = hostvuln.host_with_vuln(vulnId,"high")
        if len(result.get('content'))>1:
            print(result.get('content'))


def send_weakpassword():
    weakpass = weakPass()
    app_list = weakpass.app_view()
    weak_pass = [weakpass.weak_pass(app) for app in app_list]
    for data in weak_pass:
        if len(data.get('content'))>1:
            sendmsg.send(data.get('content'),data.get('title'))

def send_unInstalledAgent():
    checkagentInstall = CheckAgent()
    unInstallAgent = checkagentInstall.checkInstall()
    if len(unInstallAgent.get('content'))>1:
        sendmsg.send(unInstallAgent.get('content'),unInstallAgent.get('title'))

send_vuln()