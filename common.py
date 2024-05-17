# coding=utf-8

import time
import requests
from adbutils import adb
import yaml
import os
from loguru import logger

logger.configure()


def devices_list():
    d_list = []
    for d in adb.device_list():
        d_list.append(d.serial)
    return d_list


def fuc_process(action, ad):
    for k, v in action.items():
        for a, b in v.items():
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


class IPro:

    def __init__(self, devices):
        self.d = adb.device(serial=devices)

    def set_adb_proxy(self, ip, port):
        self.d.shell(f"settings put global http_proxy {ip}:{port}")

    def disable_adb_proxy(self):
        self.d.shell("settings put global http_proxy :0")

    def check_proxy(self):
        result = self.d.shell("settings get global http_proxy")
        if "null" in result:
            logger.info(f"Proxy setting fail")
        else:
            logger.info(f"Proxy setting ok")

    def c_proxy(self, ip, port):
        self.set_adb_proxy(ip, port)
        time.sleep(2)
        self.check_proxy()

    def a_install(self, apk_path):
        try:
            self.d.install(apk_path)
        except Exception as e:
            logger.info("install fail", e)

    def a_uninstall(self, apk_name):
        try:
            self.d.uninstall(apk_name)
        except Exception as e:
            logger.info("uninstall fail", e)

    def press_back(self):
        self.d.keyevent("BACK")

    def click(self, x, y):
        self.d.click(x, y)

    def swipe(self, x1, y1, x2, y2):
        self.d.swipe(x1, y1, x2, y2)


def get_apk_path():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result['apk_path']


def get_ld_path():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result['ld_path']


def get_proxy_switch():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result['proxy_switch']


def s_ld(path, count):
    lists = os.popen(f"{path}\\ldconsole.exe list").read().split("\n")
    if count > len(lists) - 1:
        for i in range(1, len(lists) - 1):
            os.popen(f"{path}\\ldconsole.exe launch --index {i}")
            time.sleep(1)
    else:
        for i in range(1, count + 1):
            os.popen(f"{path}\\ldconsole.exe launch --index {i}")
            time.sleep(1)


def get_run_num():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result['run_num']


def get_apk_name():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result['apk_name']


def get_action():
    with open(r'./config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    return result['action']


def get_apk(directory_name):
    try:
        for i, j, k in os.walk(directory_name):
            return k
    except Exception as e:
        logger.info(e)


def r_apk(apk_path: str):
    try:
        apk_name = apk_path.split("\\")[-1]
        os.remove(apk_path)
        logger.info(f"{apk_name} delete completely ")
    except Exception as e:
        logger.info(e)


def start_adb():
    s = os.system("adb start-server")
    if s == 0:
        logger.info("start ok")
    else:
        logger.info("start error")


def check_ip(ipp):
    proxies = {'http': ipp, 'https': ipp}
    url = "http://www.ip138.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    try:
        requests.get(url, headers=headers, proxies=proxies)
        return True
    except Exception as e:
        logger.warning(f"The proxy IP is invalid！", e)
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
        logger.error(f"The proxy IP address is invalid")
        return []
