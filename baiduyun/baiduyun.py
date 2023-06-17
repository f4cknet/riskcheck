from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.eip import eip_client
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.blb import blb_client
import os
import hashlib

class Baiduyun(object):
    def __init__(self):
        self.ak = os.getenv('BAIDUYUN_AK')
        self.sk = os.getenv('BAIDUYUN_SK')
        self.eip_endpoint = os.getenv('BAIDUYUN_EIP_ENDPOINT')
        self.blb_endpoint = os.getenv('BAIDUYUN_BLB_ENDPOINT')

    '''绑定了EIP的BCC实例IP地址'''
    def bcc_binded_eip_list(self):
        config = BceClientConfiguration(credentials=BceCredentials(self.ak, self.sk),endpoint=self.eip_endpoint)
        eip = eip_client.EipClient(config)
        bcc_ip = [{"eip":i.eip,"private_ip":i.instance_ip} for i in eip.list_eips(status="binded",instance_type="BCC").eip_list]
        return bcc_ip

    '''绑定了EIP的BLB实例ID'''
    def blb_binded_eip_list(self):
        config = BceClientConfiguration(credentials=BceCredentials(self.ak, self.sk), endpoint=self.eip_endpoint)
        eip = eip_client.EipClient(config)
        blb = [(i.instance_id,i.eip) for i in eip.list_eips(status="binded",instance_type="BLB").eip_list]
        return blb

    '''绑定了的EIP的BLB实例的后端服务器地址,即互联网可以访问的内网服务器'''
    def bcc_binded_blb_binded_eip_list(self):
        config = BceClientConfiguration(credentials=BceCredentials(self.ak, self.sk),endpoint=self.blb_endpoint)
        blb =  blb_client.BlbClient(config)
        blb_list = []
        for b in self.blb_binded_eip_list():
            private_ip = [backend_server.private_ip for backend_server in blb.describe_backend_servers(blb_id=b[0]).backend_server_list]
            if len(private_ip)>0:
                blb_list.append({"eip":b[1],"private_ip":private_ip})
        return  blb_list
       # return private_ip

    '''通过EIP可以访问的主机'''
    def outbound_all_by_eip_dict(self):
        return self.bcc_binded_eip_list() + self.bcc_binded_blb_binded_eip_list()

    def outbound_all_by_eip_list(self):
        ip_list = []
        for i in self.outbound_all_by_eip_dict():
            if type(i.get('private_ip')) is list:
                for k in i.get('private_ip'):
                    ip_list.append(k)
            else:
                ip_list.append(i.get('private_ip'))
        return ip_list


if __name__ == "__main__":
    baiduyun = Baiduyun()
    e_list = baiduyun.outbound_all_by_eip_list()
    print(e_list)
