# -*- coding: utf-8 -*-
import time
import json
from selenium import webdriver
from loguru import logger
import random



chrome_driver=r"chromedriver.exe"


class WB:
    def __init__(self):
        f = open('data.json', "a+")
        f.close()
        with open('data.json', 'r') as file:
            data = json.load(file)
            self.username = data['username']
            self.password = data['password']
            self.refreshTime = data['refreshTime']
            self.isShow = data['isShow']
            self.isRepeatForward = data['isRepeatForward']
            logger.info(data)
        option = webdriver.ChromeOptions()
        if self.isShow=='False':
            option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-gpu')
        option.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone X'})
        option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.driver = webdriver.Chrome(chrome_options=option,executable_path=chrome_driver)  # 选择Chrome浏览器
        self.driver.implicitly_wait(30)  # seconds''
        pass

    def login(self):
        self.driver.get("https://m.weibo.cn/login?backURL=https%253A%252F%252Fm.weibo.cn%252F")
        self.driver.find_element_by_class_name("b-left").click()
        self.driver.find_element_by_id("loginName").send_keys(self.username)
        self.driver.find_element_by_id("loginPassword").send_keys(self.password)
        self.driver.find_element_by_id("loginAction").click()

    def thisClick(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
        except Exception as e:
            logger.error(e)

    def start(self):
        self.login()
        time.sleep(3)
        while True:
            try:
                self.forward()
                time.sleep(int(self.refreshTime))
                #time.sleep(60*10)
            except Exception as e:
                logger.error(e)

    def forward(self):
        f = open('转发点赞记录.txt', "a+")
        f.close()
        self.driver.get('https://m.weibo.cn/u/5581785513?from=myfollow_all')  # 打开网站
        with open('转发点赞记录.txt', "r") as f:
            previous = f.read()
        element = self.driver.find_elements_by_class_name("card-vip")[1]
        text = element.find_element_by_class_name("weibo-og").text
        forward=True
        if self.isRepeatForward=='False':
            forward=False
        if (not previous.count(text)) and (not forward):
            forward=True
        if forward  and len(element.find_elements_by_css_selector(".weibo-rp")) > 0:
            self.thisClick(element.find_element_by_css_selector(".weibo-rp .weibo-text"))
            self.thisClick(self.driver.find_element_by_css_selector(".lite-page-editor .lite-iconf-like"))  # 点赞

            like=self.driver.find_elements_by_class_name('lite-iconf-like');
            for i in like:
                self.thisClick(i)  # 点赞

            values = ['中奖选我选我选我', '你这条转发评论是最近的巅峰',
                     '好运锦鲤 捞我吧', '鼠年好运',
                     '所有好运非你莫鼠', '这层@ 你的一位小伙伴，一起来这里脱非', '人生不长唯有暴富'
                     , '何以解忧，唯有暴富', '何以解忧，唯有中奖', '新年快乐']
            value = random.choice(values)
            self.thisClick(self.driver.find_element_by_class_name("lite-iconf-report"))  # 转发
            self.driver.find_element_by_css_selector(".m-pos-r textarea").send_keys(value)
            self.thisClick(self.driver.find_element_by_class_name("m-checkbox"))  # 同时评论
            self.thisClick(self.driver.find_element_by_class_name("m-send-btn"))  # 发送
            logger.info(text + "    评论内容：" + value)
            f = open('转发点赞记录.txt', "a+")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "，" + text + "    评论内容：" + value + '\r')
            f.close()
            self.thisClick(self.driver.find_element_by_css_selector(".weibo-top .m-avatar-box a"))
            followBtns=self.driver.find_elements_by_class_name("m-followBtn")
            for i in followBtns:
                self.thisClick(i)  # 关注
if __name__ == '__main__':
    wb = WB()
    wb.start()