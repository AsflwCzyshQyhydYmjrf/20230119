"""
scapy发送icmp包，进行主机发现 ping
"""
from scapy.all import *
from optparse import OptionParser
from concurrent.futures import ThreadPoolExecutor

def scan_host(ip):
    pkt = IP()/ICMP(seq=2000)/b'hello world'
    pkt['IP'].dst = ip
    results = sr1(pkt,timeout=3,iface = IFACES.dev_from_index(8),verbose=0)
    if results:
        print('[+] host: %s is up'%ip)

if __name__ == "__main__":
    opt = OptionParser("usage: %prog -i ip or ips")
    opt.add_option("-i", '--IP', type="string", dest="ips", help="input ip or ips")
    opt.add_option("-t", '--threads', type="int", dest="threads", help="threads number")
    options, args = opt.parse_args()
    ips = options.ips
    if "-" in ips:
        start_ip = ips.split("-")[0]
        start_num = int(start_ip.split('.')[-1])
        end_num = int(ips.split("-")[1])
        thread_num = options.threads
        with ThreadPoolExecutor(max_workers=thread_num) as pool:
            for num in range(start_num,end_num+1):
                tmp = start_ip.split(".")
                ip = tmp[0]+"."+tmp[1]+"."+tmp[2]+"."+str(num)
                pool.submit(scan_host,ip)
    else:
        scan_host(ips)
