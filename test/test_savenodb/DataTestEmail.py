# -*- coding: utf-8 -*-
'''
程序名称 DataTestEmail
@Author: AC
2018-2-25
'''
__author__ = 'AC'

##############################################
# ------------------import--------------------#
##############################################
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

##############################################
# ------------------常量定义------------------#
##############################################


##############################################
# ------------------函数定义------------------#
##############################################
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def load_user_info(filename):
    with open(filename) as f:
        username = f.readline().replace('\n', '')
        password = f.readline().replace('\n', '')
    return username, password
##############################################
# ------------------类定义--------------------#
##############################################


##############################################
# ------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    err = 'WTF!'

    # email
    from_addr, password = load_user_info('setting.txt')
    to_addr = 'ac2sherry@126.com'
    smtp_server = 'smtp.yeah.net'

    # message
    msg = MIMEText('Python 爬虫运行异常, %s' % (err,), 'plain', 'utf-8')
    msg['From'] = _format_addr('Python Spider LSP <%s>' % from_addr)
    msg['To'] = _format_addr('Python Spider Manager <%s>' % to_addr)
    msg['Subject'] = Header('Spider Running Status', 'utf-8').encode()
    # print msg

    # send
    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr,password)
    server.sendmail(from_addr,[to_addr],msg.as_string())
    server.quit()

