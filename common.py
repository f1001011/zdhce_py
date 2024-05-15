# coding=utf-8
import random
import time
import requests
from adbutils import adb
import yaml
import os
from loguru import logger


def devices_list():
    d_list = []
    for d in adb.device_list():
        d_list.append(d.serial)
    return d_list


def fuc_process(action, ad):
    for k, v in action.items():
        for a, b in v.items():
            logger.info(f"{a}:{b}")
            if a == "click":
                x = b.split(",")[0]
                y = b.split(",")[1]
                ad.click(eval(x), eval(y))
            elif a == "swipe":
                x1 = b.split(",")[0]
                y1 = b.split(",")[1]
                x2 = b.split(",")[2]
                y2 = b.split(",")[3]
                ad.swipe(eval(x1), eval(y1), eval(x2), eval(y2))
            elif a == "sleep":
                time.sleep(b)
            elif a == "press" and b == "BACK":
                ad.press_back()
            elif a == "press" and b == "HOME":
                ad.d.keyevent("HOME")


class IpProxy:

    def __init__(self, devices):
        self.d = adb.device(serial=devices)

    def set_adb_proxy(self, ip, port):
        self.d.shell(f"settings put global http_proxy {ip}:{port}")

    def disable_adb_proxy(self):
        self.d.shell("settings put global http_proxy :0")

    def check_adb_proxy(self):
        result = self.d.shell("settings get global http_proxy")
        if "null" in result:
            logger.info(f"代理设置失败")
        else:
            logger.info(f"代理设置成功")

    def check_proxy_enabled(self, ip, port):
        self.set_adb_proxy(ip, port)
        time.sleep(2)
        self.check_adb_proxy()

    def apk_install(self, apk_path):
        try:
            self.d.install(apk_path)
        except Exception as e:
            logger.info("安装失败", e)

    def apk_uninstall(self, apk_name):
        try:
            self.d.uninstall(apk_name)
        except Exception as e:
            logger.info("卸载失败", e)

    def press_back(self):
        self.d.keyevent("BACK")

    def click(self, x, y):
        self.d.click(x, y)

    def swipe(self, x1, y1, x2, y2):
        self.d.swipe(x1, y1, x2, y2)


def get_apk_path():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['apk_path']
    return s


def get_ld_path():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['ld_path']
    return s


def get_proxy_switch():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['proxy_switch']
    return s


def s_ld(path, count):
    lists = os.popen(f"{path}\\ldconsole.exe list").read().split("\n")
    num = len(lists) - 1
    if count > num:
        for i in range(1, num):
            os.popen(f"{path}\\ldconsole.exe launch --index {i}")
            time.sleep(1)
    else:
        for i in range(1, count+1):
            os.popen(f"{path}\\ldconsole.exe launch --index {i}")
            time.sleep(1)


def get_run_num():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['run_num']
    return s


def get_apk_name():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['apk_name']
    return s


def get_action():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['action']
    return s


def get_apk(directory_name):
    try:
        for i, j, k in os.walk(directory_name):
            return k
    except Exception as e:
        logger.info(e)


def remove_apk(apk_path: str):
    try:
        apk_name = apk_path.split("\\")[-1]
        os.remove(apk_path)
        logger.info(f"{apk_name}删除完成")
    except Exception as e:
        logger.info(e)


def get_proxy(proxy_list: list):
    return random.choice(proxy_list)


def start_adb():
    s = os.system("adb start-server")
    if s == 0:
        logger.info("启动成功")
    else:
        logger.info("启动失败")


def check_ip(ipp):
    proxies = {'http': ipp, 'https': ipp}
    url = "http://www.bilibili.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        return True
        # if response.status_code == 200:
        #     return True
        # else:
        #     return False
    except Exception as e:
        logger.warning(f"请求失败，代理IP无效！", e)
        return False


def get_proxies():
    urls = "https://api.proxyscrape.com/v3/free-proxy-list/get?request=getproxies&protocol=http&skip=1&proxy_format=protocolipport&format=json&limit=15&timeout=5000"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    try:
        r = requests.get(urls, headers=headers)
        ip_list = []
        a1 = r.json()['proxies']
        for i in a1:
            z = i['proxy']
            x = z.split(r"://")[1]
            ip_list.append(x)
        return ip_list
    except Exception as e:
        logger.error(f"代理IP获取失败")
        return []
