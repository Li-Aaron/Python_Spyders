# -*- coding: utf-8 -*-
'''
TCP Server
@Author: AC
2017-11-5
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import socket
import threading
import time

##############################################
#------------------常量定义------------------#
##############################################

##############################################
#------------------函数定义------------------#
##############################################

###################################
# dealClient
# server函数
################################### 
def dealClient(sock, addr):
    # receiving transported data and send Loop_Msg
    print 'Accept new connection from %s: %s' % addr
    sock.send(b'Hello, I am server!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        print '-->>%s!' % data.decode('utf-8')
        sock.send(('Loop_Msg: %s!' % data.decode('utf-8')).encode('utf-8'))

##############################################
#------------------类定义--------------------#
##############################################

###################################
# class
# 类
################################### 

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # 主线程
    # socket bind IP = 127.0.0.1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1',9999))

    # listen connection
    s.listen(5)
    print('Waiting for connection...')
    while True:
        # get a connection
        sock, addr = s.accept()
        # create new thread to deal with TCP connection
        t = threading.Thread(target=dealClient, args=(sock, addr))
        t.start()
