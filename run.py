import multiprocessing
import time
from common import IpProxy, fuc_process, logger, devices_list, get_proxy, start_adb, get_run_num, get_proxies, check_ip
from common import get_apk, get_apk_path, get_action, get_apk_name, remove_apk

directory_name = get_apk_path()
action = get_action()
apk_package = get_apk_name()


def run(devices, proxys, apks):
    logger.info(f"apk: {apks}")
    ad = IpProxy(devices)
    ip = proxys.split(":")
    ad.check_proxy_enabled(ip[0], ip[1])
    time.sleep(2)
    apk_path = directory_name + "\\" + apks
    logger.info("开始安装apk，等稍等")
    ad.apk_install(apk_path)
    logger.info("apk安装完成")
    try:
        remove_apk(apk_path)
    except Exception as e:
        logger.error(e)
    ad.check_apk_install()
    ad.d.app_start(apk_package)
    fuc_process(action, ad)
    time.sleep(1)
    ad.d.app_stop(apk_package)
    ad.apk_uninstall(apk_package)


def get_apk_list(dev_num):
    dir_list = get_apk(directory_name)[:dev_num]
    return dir_list


def get_ip_list(plist, dev_num):
    ip_list = plist[:dev_num]
    return ip_list


if __name__ == "__main__":
    start_adb()
    logger.error("等待启动")
    time.sleep(5)
    s1 = devices_list()
    if not s1:
        logger.error("没有连接任何设备")
        time.sleep(5)
    else:
        for x in range(5):
            if len(s1) == 0:
                s1 = devices_list()
                time.sleep(1)
            else:
                logger.info(s1)
                break
        run_num = get_run_num()
        if len(s1) < run_num:
            s = s1
        else:
            s = s1[:run_num]
        while 1:
            f = get_proxies()
            logger.info(f"获取的代理：{f}")
            ip_lists = []
            for i in f:
                if check_ip(i) is True:
                    ip_lists.append(i)
            logger.info(f"检测后可用的代理：{ip_lists}")
            apks1 = get_apk_list(len(s))
            proxys1 = get_ip_list(ip_lists, len(s))
            for ix in proxys1:
                if check_ip(ix) is True:
                    logger.info(f"再次验证通过：{ix}")
            dir_list1 = get_apk(directory_name)
            if len(dir_list1) < 1:
                logger.info("没有可用的apk文件，全部运行完成")
                time.sleep(5)
                break
            elif len(dir_list1) == 1:
                run(s[0], proxys1[-1], apks1[-1])
            else:
                params = list(zip(s, proxys1, apks1))
                with multiprocessing.Pool() as pool:
                    pool.starmap(run, params)
