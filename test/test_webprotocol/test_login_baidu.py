#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
百度云登陆
@Author: AC
2018-3-25
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import base64
import re
import requests
import time

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import PyV8
from urllib import quote

from Common import logger, OpenImg

##############################################
#------------------常量定义------------------#
##############################################
url = 'http://yun.baidu.com'
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0'
headers = {
    'User-Agent': agent,
}
username = 'lsp_python'
password = '49e7b513'

data = {
    'staticpage': 'https://yun.baidu.com/res/static/thirdparty/pass_v3_jump.html',
    'charset': 'UTF-8',
    'tpl': 'netdisk',
    'subpro': 'netdisk_web',
    'apiver': 'v3',
    'codestring': '',
    'safeflg': 0,
    'u': 'https://yun.baidu.com/disk/home',
    'isPhone': 'false',
    'detect': 1,
    'quick_user': 0,
    'logintype': 'basicLogin',
    'logLoginType': 'pc_loginBasic',
    'idc': '',
    'loginmerge': True,
    'foreignusername': '',
    'mem_pass': 'on',
    'crypttype': 12,
    'ppui_logintime': 35001,
    'countrycode': '',
# 'fp_uid': '2f801c1b794d3f6eb164c04e1fad1863',
# 'fp_info': '2f801c1b794d3f6eb164c04e1fad1863002~~~oFgw3-eU1i7_pooHsgzpAtzpY0ypmtWggzpAtzpY0jsm7_Yoi0cCoi0cKoocLoi~uNglO4rPpYjrsiny1i7jsmod1~3NO4y~sTj~Bm9fHJy~D7__BpooDpooPpooOpooug0zi6etLIZcsOJ9cDfel7-w7p46xHd6ip-1sInQWDZ9P552fB5dyBW1yE-dl6AdN6etLIZcsOJ9cDfel7-w7p46xHd6ip-1sInQWDZ9P552fB5dyBW1yE-dl6AW_vpocTpocxpoczpocrootygwIf0R7Wz_wgH2Jj~O43iXJD9DJ7_opocHooodpoocpooUpookpooQpoomgYaAnU1mty1m7zsmt~smOW1~tW17__',
# 'loginversion': 'v4',
# 'dv': 'tk0.48391911070307251522063628303@mqb0acCkqgAk2z2ogztrEYAkhwCkqLAk2gtmgL2rnYAkhwCrUgAkn-2mgR2VBYAkhw2rq~tog~2knYt~BRAmggOq__-ccswcz23tHFhzbh2og~AkEyubr5pYgAVE-2~3bCr0b2kNg2~ql2VBbtrnz2kG~tVn-2~q~hbrFvDLNv2dAzci5I-HGTuKsvBHGycZAzbRPTDXsTXHsIE_Hb0mc2r0LAk0i2VqY2rny2zgl2rNY2rn-2mgb2knLAk0zCkqY2rnit1gb2kqgAb0vc2mg~t1g~CogL2mgl2zgb2k2Y2rnbAk0~2ogbtVBY2rUzAk0-2zgz2VUY2V2lAknyt1gzt~GY2VNlAk2Ltzg~trGY2~GgAk2-togL2rE_',
# 'traceid': '38F1EF01',
}
##############################################
#------------------函数定义------------------#
##############################################
def post_value(session, url, data, pattern=re.compile(r'.*'), value_name='value'):
    response = session.post(url, data=data)
    logger.info('post %s response: <%s>'%(value_name,response.status_code))
    logger.debug(response.text)
    match = pattern.search(response.text)
    if match:
        value = match.group(1)
        logger.info('%s=%s' % (value_name,value))
        return value, response.text
    else:
        logger.error('%s get failed' % (value_name,))
        raise Exception

def get_value(session, url, pattern=re.compile(r'.*'), value_name='value'):
    response = session.get(url)
    logger.info('get %s response: <%s>'%(value_name,response.status_code))
    logger.debug(response.text)
    match = pattern.search(response.text)
    if match:
        value = match.group(1)
        logger.info('%s=%s' % (value_name, value))
        return value, response.text
    else:
        logger.error('%s get failed' % (value_name,))
        raise Exception
##############################################
#------------------类定义--------------------#
##############################################

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    s = requests.session()
    s.get(url, headers=headers)

    # PyV8 仿真js代码
    js='''
    function callback(){
        return 'bd__cbs__'+Math.floor(2147483648 * Math.random()).toString(36)
    }
    function gid(){
        return 'xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (e) {
        var t = 16 * Math.random() | 0,
        n = 'x' == e ? t : 3 & t | 8;
        return n.toString(16)
        }).toUpperCase()
    }
    '''
    ctxt = PyV8.JSContext()
    ctxt.enter()
    ctxt.eval(js)

    # 获取gid与callback
    gid = ctxt.locals.gid()
    callback = ctxt.locals.callback()
    logger.info('gid=%s'%gid)
    logger.info('callback=%s'%callback)

    # 获取token
    tokenUrl="https://passport.baidu.com/v2/api/?getapi&tpl=netdisk&subpro=netdisk_web&apiver=v3" \
             "&tt=%d&class=login&gid=%ss&loginversion=v4&logintype=basicLogin&traceid=&callback=%s"%(time.time()*1000,gid,callback)
    token_response = s.get(tokenUrl)
    pattern = re.compile(r'"token"\s*:\s*"(\w+)"')
    token = get_value(s, tokenUrl, pattern, 'token')


    callback = ctxt.locals.callback()
    logger.info('callback=%s' % callback)
    # 获取rsakey pubkey
    rsaUrl = "https://passport.baidu.com/v2/getpublickey?token=%s&" \
             "tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=%d&gid=%s&loginversion=v4&" \
             "traceid=&callback=%s"%(token,time.time()*1000,gid,callback)
    pattern = re.compile("\"key\"\s*:\s*'(\w+)'")
    key, rsa_response_text = get_value(s, rsaUrl, pattern, 'key')

    pattern = re.compile("\"pubkey\":'(.+?)'")
    match = pattern.search(rsa_response_text)
    if match:
        pubkey = match.group(1)
        pubkey = pubkey.replace('\\n', '\n').replace('\\', '')
        logger.info('pubkey=%s' % pubkey)
    else:
        logger.error('pubkey get failed')
        raise Exception

    # 加密password
    rsakey = RSA.importKey(pubkey)
    cipher = PKCS1_v1_5.new(rsakey)
    password = base64.b64encode(cipher.encrypt(password))
    logger.info('password=%s' % password)


    callback = ctxt.locals.callback()
    logger.info('callback=%s' % callback)
    data.update({
        'token': token,
        'tt': '%d' % (time.time() * 1000),
        'gid': gid,
        'username': username,
        'password': password,
        'rsakey': key,
        'callback': 'parent.%s'%callback,
    })

    # post1 获取 codestring
    loginUrl = 'https://passport.baidu.com/v2/api/?login'

    # 获取 errno ( 有可能直接成功 )
    pattern = re.compile("err_no=(\w+)&")
    errno, post1_response_text = post_value(s,loginUrl,data,pattern,'errno')
    if errno == '0':
        logger.warn('login success')
        exit(0)
    else:
        logger.warn('login failed')


    # 获取 codestring
    pattern = re.compile("codeString=(\w+)&")
    match = pattern.search(post1_response_text)
    if match:
        codeString = match.group(1)
        logger.info('codeString=%s' % codeString)
    else:
        logger.error('codeString get failed')
        raise Exception

    data['codestring'] = codeString

    # 获取验证码
    verifycode = ''
    verifyFail = True
    while verifyFail:
        genimage_param = ''
        if len(genimage_param)==0:
            genimage_param = codeString
        verifycodeUrl="https://passport.baidu.com/cgi-bin/genimage?%s"%genimage_param
        verifyImg = s.get(verifycodeUrl)
        # 下载验证码
        img = 'verifycode.png'
        with open(img,'wb') as codeWriter:
            codeWriter.write(verifyImg.content)
            codeWriter.close()
        OpenImg(img)
        verifycode = raw_input("Enter your input verifycode: ")

        callback = ctxt.locals.callback()
        logger.info('callback=%s' % callback)

        checkVerifycodeUrl='https://passport.baidu.com/v2/?' \
                        'checkvcode&token=%s' \
                        '&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=%d' \
                        '&verifycode=%s&codestring=%s' \
                        '&callback=%s'%(token,time.time()*1000,quote(verifycode),codeString,callback)
        logger.debug(quote(verifycode))
        logger.debug(checkVerifycodeUrl)
        state = s.get(checkVerifycodeUrl)
        logger.debug(state.text)
        if state.text.find(u'验证码有误') != -1:
            logger.warn('verification wrong...已经自动更换...')
            callback = ctxt.locals.callback()
            changeVerifyCodeUrl = "https://passport.baidu.com/v2/?reggetcodestr" \
                                  "&token=%s" \
                                  "&tpl=netdisk&subpro=netdisk_web&apiver=v3" \
                                  "&tt=%d&fr=login&" \
                                  "vcodetype=de94eTRcVz1GvhJFsiK5G+ni2k2Z78PYRxUaRJLEmxdJO5ftPhviQ3/JiT9vezbFtwCyqdkNWSP29oeOvYE0SYPocOGL+iTafSv8pw" \
                                  "&callback=%s" % (token, time.time() * 1000, callback)
            logger.debug(changeVerifyCodeUrl)
            pattern = re.compile('"verifyStr"\s*:\s*"(\w+)"')
            verifyString = get_value(s, changeVerifyCodeUrl, pattern, 'verifyString')
            genimage_param  = verifyString
        else:
            logger.warn('verification OK')
            verifyFail = False
    data['verifycode'] = verifycode

    # post2 获取 errno
    pattern = re.compile("err_no=(\w+)&")
    errno, post2_response_text = post_value(s, loginUrl, data, pattern, 'errno')
    if errno == '0':
        logger.warn('login success')
        exit(0)
    else:
        logger.warn('login failed')