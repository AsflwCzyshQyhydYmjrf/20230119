import platform
import sys
import os
import _thread
import time


def get_os():
    os = platform.system()  # 判断系统
    if os == "Windows":
        return "Windows"
    else:
        return "Others"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()), "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()

    flag = False  # 关闭回显
    for line in list(output):
        if not line:
            continue
        if str(line).upper().find("TTL") >= 0:
            flag = True
            break
    if flag:
        print("ip: %s is ok ***" % ip_str)


def find_ip(ip_prefix):
    for i in range(1, 256):
        ip = '%s.%s' % (ip_prefix, i)
        _thread.start_new_thread(ping_ip, (ip,))
        time.sleep(0.3)


if __name__ == "__main__":
    try:
        print("start time %s" % time.ctime())
        commandargs = sys.argv[1:]
        args = "".join(commandargs)

        ip_prefix = '.'.join(args.split('.')[:-1])
        find_ip(ip_prefix)
        print("end time %s" % time.ctime())
    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        sys.exit()