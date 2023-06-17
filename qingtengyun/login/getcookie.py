from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
import time,pyotp
import requests
from common.config import BASE_DIR
from qingtengyun.config import qingtengyun_user,qingtenyun_domain,qingtengyun_pass


class getCookie(object):
    def __init__(self):
        self.user = qingtengyun_user
        self.passwd = qingtengyun_pass
        self.qingtengyun_domain = qingtenyun_domain
        self.login_url = self.qingtengyun_domain + '/login'

    def login(self):
        if Path(BASE_DIR+'/common/mac_chromedriver').exists():
            driver = webdriver.Chrome()
        else:
            print('异常：未找到浏览器驱动')
            print('提示：请下载对应版本的浏览器驱动，并放置于目录：' + os.getcwd())
            print('chrome: http://npm.taobao.org/mirrors/chromedriver/')
            print('Firefox: http://npm.taobao.org/mirrors/geckodriver/')
            exit(0)
        driver.maximize_window()
        driver.get(self.login_url)
        time.sleep(3)
        username = driver.find_element(By.XPATH,"//div[@class='login-system-form-username']/input")
        username.send_keys(self.user)
        password = driver.find_element(By.XPATH,"//div[@class='login-system-form-password']/input")
        password.send_keys(self.passwd)
        otp = driver.find_element(By.XPATH, "//div[@class='login-system-form-otp']/input")
        otp.send_keys(self.generate_otp())
        login = driver.find_element(By.CLASS_NAME,"login-system-submit")
        login.click()
        time.sleep(3)
        cookie = "; ".join([item["name"] + "=" + item["value"] for item in driver.get_cookies()])
        return cookie

    def save_cookie(self):
        with open(BASE_DIR+'/common/cookie.txt', 'w')as f:
            f.write(self.login())

    def getcookie(self):
        with open(BASE_DIR+'/common/cookie.txt', 'r')as f:
            cookie = f.read()
        header = {
            "Cookie": cookie,
            "Referer": self.qingtengyun_domain + "/v3"
        }
        url = f"{self.qingtengyun_domain}/v1/assets/vul3/poc/hosts_with_vul"
        data = {"page":1,"size":50,"orders":[{"field":"ip","ascend":True}],"filters":["group"],"params":{"vulId":"QT042017000069"}}
        try:
            req = requests.post(url=url,json=data,headers=header)
            if req.status_code == 401:
                self.save_cookie()
                self.getcookie()
            elif req.status_code == 200:
                auth = {"Cookie": cookie, "Referer": f"{self.qingtengyun_domain}/next"}
                return auth
        except Exception as e:
            return e

    def generate_otp(self):
        otp = pyotp.TOTP("NLPRPJGD4TPDWJ4D")
        otp_value = otp.now()
        while not otp.verify(otp_value):
            otp_value = otp.now()
        return otp_value

if __name__ == "__main__":
    g = getCookie()
    # a = g.generate_otp("NLPRPJGD4TPDWJ4D")
    a = g.getcookie()
    print(a)


