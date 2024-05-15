import multiprocessing
import time
from common import IpProxy, fuc_process, logger, devices_list, start_adb, get_run_num, get_proxies, check_ip, \
    get_ld_path
from common import get_apk, get_apk_path, get_action, get_apk_name, remove_apk, get_proxy_switch, s_ld

directory_name = get_apk_path()
action = get_action()
apk_package = get_apk_name()
ldpath = get_ld_path()
ldnum = get_run_num()


def run(devices, proxys, apks):
    logger.info(f"apk: {apks}")
    ad = IpProxy(devices)
    ip = proxys.split(":")
    ad.check_proxy_enabled(ip[0], ip[1])
    time.sleep(2)
    apk_path = directory_name + "\\" + apks
    logger.info("开始安装apk，等稍等！")
    ad.apk_install(apk_path)
    logger.info("apk安装完成！")
    remove_apk(apk_path)
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
    s_ld(ldpath, ldnum)
    time.sleep(30)
    start_adb()
    logger.info("开始")
    time.sleep(5)
    s1 = devices_list()
    if not s1:
        logger.error("没有设备")
        time.sleep(5)
    else:
        for x in range(5):
            if len(s1) == 0:
                s1 = devices_list()
                time.sleep(1)
            else:
                break
        run_num = get_run_num()
        if len(s1) < run_num:
            s = s1
        else:
            s = s1[:run_num]
        proxy_on_off = get_proxy_switch()
        while 1:
            if proxy_on_off == "ture":
                logger.info("代理模式开启")
                f = get_proxies()
                ip_lists = []
                if len(f) == 0:
                    logger.info("请检查代理")
                else:
                    for i in f:
                        if check_ip(i) is True:
                            ip_lists.append(i)
                    logger.info(f"检测后可用的代理：{ip_lists}")
                    apks1 = get_apk_list(len(s))
                    proxys1 = get_ip_list(ip_lists, len(s))
                    dir_list1 = get_apk(directory_name)
                    if len(dir_list1) < 1:
                        logger.info("全部运行完成")
                        time.sleep(5)
                        break
                    else:
                        params = list(zip(s, proxys1, apks1))
                        with multiprocessing.Pool() as pool:
                            pool.starmap(run, params)

            else:
                logger.info("代理模式关闭")
                num_duplicates = len(s)
                apks1 = get_apk_list(len(s))
                proxys1 = [x for x in [":0"] for _ in range(num_duplicates)]
                dir_list1 = get_apk(directory_name)
                if len(dir_list1) < 1:
                    logger.info("全部运行完成")
                    time.sleep(5)
                    break
                else:
                    params = list(zip(s, proxys1, apks1))
                    with multiprocessing.Pool() as pool:
                        pool.starmap(run, params)
