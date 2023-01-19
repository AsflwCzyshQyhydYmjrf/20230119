import socket
from multiprocessing.dummy \
    import Pool as ThreadPool

def main():
    global host_ip
    host = input("Enter a host to scan:")
    startPort = int(input("Enter the start port:"))
    endPort = int(input("Enter the end port:"))
    processes_num = int(input("Enter processes num :"))
    host_ip = socket.gethostbyname(host)
    ports = []
    print('-' * 30)
    print('Please wait,scanning host',host_ip)
    print('-' * 30)
    socket.setdefaulttimeout(0.4)
    for port in range(startPort, endPort):
        ports.append(port)
    pool = ThreadPool(processes = processes_num)
    results = pool.map(get_ip_status,ports)
    pool.close()       #关闭进程池，不在接收新的进程
    pool.join()        #主线程阻塞等在子进程的退出
    print('port scan end')
def get_ip_status(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((host_ip, port))
        print('[+] {0} port {1} is open'.format(host_ip, port))
    except Exception as err:
        pass
    finally:
        server.close()

if __name__ == '__main__':
    main()

