#encoding=utf-8
import socket,time
from threading import *

ip=str(input('输入测试服务的IP地址或域名:'))
port=int(input('输入该服务使用的业务端口号:'))
num=int(input('输入每次测试发起TCP连接数：'))
# ip='8.8.8.8'/www.baidu.com
# port=53
# num=50


s1=Semaphore(value=num)
s2=Semaphore(value=1)
class test():
    m=0
    def __init__(self,ip,port,ii):
        self.ip=ip
        self.port=port
        self.ii=ii
    def Port_connect(self):
        s1.acquire()
        sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # sk.settimeout(0.05)
        try:
            # print(self.ip,self.port)
            sk.connect((self.ip,self.port))
            # print('连接成功',time.localtime(time.time()))
            self.m+=1
        except Exception as e:
            s2.acquire()
            print('第'+str(ii)+'次测试连接失败一次')
            # print(e)
            s2.release()
        # time.sleep(1)
        s1.release()
        sk.close()
        # print(self.m)
        # time.sleep(0.2)


# a.Port_connect()
for ii in range(10000):
    a=test(ip,port,ii)
    for i in range(num):
        t1=Thread(target=a.Port_connect,args=())  
        t1.start()
    # time.sleep(5)
    # t1.join()
    while t1.is_alive()==True:  #子线程运行状态判断
        # pass
        # print('*',end="")
        time.sleep(15)

    # print(t1.is_alive())
    print (ip+':'+str(port)+' 第'+str(ii+1)+'测试'+str(num)+'包丢包率为: {:.2%}'.format((num-a.m)/num), a.m)
    a.m=0

