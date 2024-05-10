# coding=utf-8
import random
import time
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

    def check_enabled(self):
        re = self.d.shell("ping -c 1 www.baidu.com")
        if "0 received" in re:
            logger.info("代理不可用")
            return False
        else:
            logger.info("代理可用")
            return True

    def set_adb_proxy(self, ip, port):
        self.d.shell(f"settings put global http_proxy {ip}:{port}")

    def check_adb_proxy(self):
        result = self.d.shell("settings get global http_proxy")
        if "null" in result:
            logger.info(f"代理 IP:{result} 未设置成功")
        else:
            logger.info(f"代理 IP:{result} 设置成功")

    def check_proxy_enabled(self, ip, port):
        self.set_adb_proxy(ip, port)
        time.sleep(2)
        self.check_adb_proxy()

    def apk_install(self, apk_path):
        try:
            self.d.install(apk_path)
        except Exception as e:
            logger.info("安装失败")

    def apk_uninstall(self, apk_name):
        try:
            self.d.uninstall(apk_name)
        except Exception as e:
            logger.info("卸载失败")

    def check_apk_install(self):
        try:
            s = self.d.list_packages()
            name = get_apk_name()
            for i in range(10):
                if name in s:
                    logger.info("安装成功")
                    break
                else:
                    time.sleep(1)
        except Exception as e:
            logger.info("未查询到app")

    def press_back(self):
        self.d.keyevent("BACK")

    def click(self, x, y):
        self.d.click(x, y)

    def swipe(self, x1, y1, x2, y2):
        self.d.swipe(x1, y1, x2, y2)


def get_apk_path():
    with open(r'../u2_opt/config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['apk_path']
    return s


def get_run_num():
    with open(r'../u2_opt/config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['run_num']
    return s


def get_apk_name():
    with open(r'../u2_opt/config.yaml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
    s = result['apk_name']
    return s


def get_action():
    with open(r'../u2_opt/config.yaml', 'r', encoding='utf-8') as f:
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
        logger.info(f"{apk_name},删除完成")
    except Exception as e:
        logger.info(e)


def get_proxy(proxy_list: list):
    return random.choice(proxy_list)


def start_adb():
    s = os.system("adb start-server")
    logger.info(s)
