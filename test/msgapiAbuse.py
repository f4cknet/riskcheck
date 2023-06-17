from aes import AESTool
import requests,time
import os

aes = AESTool()
domain = os.getenv('domain')
endpoint = f'{domain}/clue/api/getVeriCode"
for num in range(100,150):
    time.sleep(1)
    phone = f"1361{num}2930"
    encrypt_phone = aes.aes_encrypt(phone)
    req = requests.post(url=endpoint,json={"phone":encrypt_phone},headers={"Content-Type":"application/json"})
    print(phone,req.text)