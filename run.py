import multiprocessing
import time
from common import IpProxy, fuc_process, logger, devices_list, get_proxy, start_adb, get_run_num
from common import get_apk, get_apk_path, get_action, get_apk_name, remove_apk

p_list = ["60.174.0.72:8089",
          "223.247.46.31:8089",
          "121.5.130.51:8899",
          "60.174.0.172:8089",
          "39.98.204.54:7890",
          "47.93.249.121:8118",
          "139.196.196.74:80",
          "222.74.73.202:42055",
          '118.31.1.154:80',
          '47.92.155.21:8118',
          "114.231.8.228:8888",
          '223.247.46.61:8089',
          "120.25.159.66:8118"]

proxy = get_proxy(p_list)
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
    ad.apk_install(apk_path)
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
            apks1 = get_apk_list(len(s))
            proxys1 = get_ip_list(p_list, len(s))
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
