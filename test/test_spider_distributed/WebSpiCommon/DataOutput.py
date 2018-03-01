# -*- coding: utf-8 -*-
'''
程序名称 DataOutput - 写入缓存释放
数据存储器
@Author: AC
2018-2-26
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import codecs
import chardet

##############################################
#------------------常量定义------------------#
##############################################


##############################################
#------------------函数定义------------------#
##############################################
def ToUTF8(content):
    if isinstance(content, unicode):
        return content.encode('utf-8')
    elif isinstance(content, str):
        return content.decode(chardet.detect(content)['encoding']).encode('utf-8')
    else:
        raise TypeError('content must be basestring, not %s'%(type(content),))

##############################################
#------------------类定义--------------------#
##############################################
class DataOutput(object):

    def __init__(self, filename='Crawled.html', title='Crawled'):
        self.datas = []
        self.idx = 1
        self.filename = filename
        self.first_flag = True
        self.SaveHtmlHeader(self.filename, title)

    def StoreData(self, data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas) > 10:
            self.SaveHtmlData(self.filename)

    def __del__(self):
        self.SaveHtmlData(self.filename)
        self.SaveHtmlEnd(self.filename)

    def SaveHtml(self, filename='Crawled.html', title='Crawled'):
        '''
        Save All Data to Html (Old Process)
        :param filename:
        :param title:
        :return:
        '''
        with codecs.open(filename, 'wb', encoding='utf-8') as fout:
            self._SaveHtmlHeader(fout, title)
            self._SaveHtmlStart(fout, title)
            self._SaveHtmlData(fout)
            self._SaveHtmlEnd(fout)

    def SaveHtmlHeader(self, filename='Crawled.html', title='Crawled'):
        with codecs.open(filename, 'wb', encoding='utf-8') as fout:
            self._SaveHtmlHeader(fout, title)
            self._SaveHtmlStart(fout, title)

    def SaveHtmlData(self, filename='Crawled.html'):
        with codecs.open(filename, 'ab+', encoding='utf-8') as fout:
            self._SaveHtmlData(fout)

    def SaveHtmlEnd(self, filename='Crawled.html'):
        with codecs.open(filename, 'ab+', encoding='utf-8') as fout:
            self._SaveHtmlEnd(fout)

    def _SaveHtmlHeader(self, fout, title='Crawled'):
        '''
        headers, styles
        :param fout:
        :param title:
        :return:
        '''
        fout.write("<html>\n")
        fout.write("<head>\n<meta charset='utf-8'/>\n")
        fout.write("<title>%s</title>\n"%(title,))
        fout.write("<style type='text/css'>\n")
        fout.write("body {background-color: #222222; font-family:Verdana, sans-serif}\n")
        fout.write("table {border:0; border-spacing:2px; width: 98%; margin:auto}\n")
        fout.write("table caption{font-family: arial; font-weight:800; font-size:24px; color:#eeeeee}\n")
        fout.write("tr.headline {background-color: #666666}\n")
        fout.write("tr.oddline {background-color: #afafaf}\n")
        fout.write("tr.evenline {background-color: #cccccc}\n")
        fout.write("th {text-align: left; padding: 0.5ex;}\n")
        fout.write("td {text-align: left; padding: 0.5ex;}\n")
        fout.write("</style>\n")
        fout.write("</head>\n")

    def _SaveHtmlStart(self, fout, title):
        '''
        from <body> to <table>headers
        :param fout:
        :param title:
        :return:
        '''
        fout.write("<body>\n")
        fout.write("<table>\n")
        fout.write("<caption>%s</caption>\n" % (title,))
        fout.write("<tr class='headline'>\n")
        fout.write("<th>Index</th>\n")
        fout.write("<th>Title</th>\n")
        fout.write("<th>Summary</th>\n")
        fout.write("</tr>\n")

    def _SaveHtmlData(self, fout):
        '''
        <tr>data</tr>
        :param fout:
        :return:
        '''
        if len(self.datas) == 0:
            return
        for data in self.datas:
            if self.idx % 2 == 1:
                fout.write("<tr class='oddline'>\n")
            else:
                fout.write("<tr class='evenline'>\n")
            fout.write("<td>%s</td>\n" % (self.idx))
            fout.write("<td><a href='%s' target='_blank'>%s</a></td>\n" % (data['url'], data['title'],))
            fout.write("<td>%s</td>\n" % (data['summary'],))
            fout.write("</tr>\n")
            self.idx += 1
        self.datas = []  # 写入后删除

    def _SaveHtmlEnd(self, fout):
        '''
        table end to html end
        :param fout:
        :return:
        '''
        fout.write("</table>\n")
        fout.write("</body>\n")
        fout.write("</html>\n")






##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    datas = [{'url': u'1', 'title': u'1\'s name', 'summary': u'赵'},
             {'url': u'2', 'title': u'2\'s name', 'summary': u'钱'},
             {'url': u'3', 'title': u'3\'s name', 'summary': u'孙'},
             {'url': u'4', 'title': u'4\'s name', 'summary': u'李'},
             {'url': u'5', 'title': u'5\'s name', 'summary': u'周'},
             {'url': u'6', 'title': u'6\'s name', 'summary': u'吴'},
             {'url': u'7', 'title': u'7\'s name', 'summary': u'郑'},
             {'url': u'8', 'title': u'8\'s name', 'summary': u'王'},
             {'url': u'9', 'title': u'9\'s name', 'summary': u'冯'},
             {'url': u'10', 'title': u'10\'s name', 'summary': u'陈'},
             {'url': u'11', 'title': u'11\'s name', 'summary': u'褚'},
             {'url': u'12', 'title': u'12\'s name', 'summary': u'卫'},
             ]
    dout = DataOutput('Test.html',title='Test')
    for data in datas:
        dout.StoreData(data)
    # dout.SaveHtml('Test.html')

