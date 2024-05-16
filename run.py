import multiprocessing
import time
from common import *

directory_name = get_apk_path()
action = get_action()
apk_package = get_apk_name()
ldpath = get_ld_path()
ldnum = int(get_run_num())


def run(devices, proxys, apks):
    ad = IPro(devices)
    ip = proxys.split(":")
    ad.c_proxy(ip[0], ip[1])
    time.sleep(2)
    apk_path = directory_name + "\\" + apks
    logger.info("start install！")
    ad.a_install(apk_path)
    logger.info("apk install complete！")
    r_apk(apk_path)
    ad.d.app_start(apk_package)
    fuc_process(action, ad)
    ad.d.app_stop(apk_package)
    ad.a_uninstall(apk_package)


def get_apk_list(dev_num):
    dir_list = get_apk(directory_name)[:dev_num]
    return dir_list


def get_ip_list(plist, dev_num):
    ip_list = plist[:dev_num]
    return ip_list


if __name__ == "__main__":
    s_ld(ldpath, ldnum)
    time.sleep(ldnum)
    start_adb()
    time.sleep(5)
    s1 = devices_list()
    if not s1:
        logger.error("find devices error")
        time.sleep(5)
    else:
        for x in range(5):
            if len(s1) == 0:
                s1 = devices_list()
                time.sleep(1)
            else:
                break
        if len(s1) < ldnum:
            s = s1
        else:
            s = s1[:ldnum]
        proxy_on_off = get_proxy_switch()
        while 1:
            if proxy_on_off == "ture":
                logger.info("proxy mode on")
                f = get_proxies()
                ip_lists = []
                if len(f) == 0:
                    logger.info("check proxy")
                else:
                    for i in f:
                        if check_ip(i) is True:
                            ip_lists.append(i)
                    logger.info(f"proxy：{ip_lists}")
                    apks1 = get_apk_list(len(s))
                    proxys1 = get_ip_list(ip_lists, len(s))
                    dir_list1 = get_apk(directory_name)
                    if len(dir_list1) < 1:
                        logger.info("complete")
                        time.sleep(5)
                        break
                    else:
                        params = list(zip(s, proxys1, apks1))
                        with multiprocessing.Pool() as pool:
                            pool.starmap(run, params)

            else:
                logger.info("proxy mode off")
                num_duplicates = len(s)
                apks1 = get_apk_list(len(s))
                proxys1 = [x for x in [":0"] for _ in range(num_duplicates)]
                dir_list1 = get_apk(directory_name)
                if len(dir_list1) < 1:
                    logger.info("complete")
                    time.sleep(5)
                    break
                else:
                    params = list(zip(s, proxys1, apks1))
                    with multiprocessing.Pool() as pool:
                        pool.starmap(run, params)
