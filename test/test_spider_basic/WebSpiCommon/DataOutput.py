# -*- coding: utf-8 -*-
'''
程序名称 DataOutput
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
import csv
##############################################
#------------------常量定义------------------#
##############################################


##############################################
#------------------函数定义------------------#
##############################################
def ToUTF8(content):
    if isinstance(content, unicode):
        return content.encode('utf-8')
    else:
        return content.decode(chardet.detect(content)['encoding']).encode('utf-8')

##############################################
#------------------类定义--------------------#
##############################################
class DataOutput(object):

    def __init__(self):
        self.datas=[]

    def StoreData(self, data):
        if data is None:
            return
        self.datas.append(data)

    def SaveCsv(self, filename='Crawled.csv', first_flag=True):
        if self.datas:
            headers = self.datas[0].keys()
            # 不能直接写入unicode
            rows = [{key: ToUTF8(item) for key, item in x.items()}
                    for x in self.datas]
            self._SaveCsv(headers, rows, filename=filename, first_flag=first_flag)
        else:
            print 'no data stored'

    def _SaveCsv(self, headers, rows, filename='Crawled.csv', delimiter=' ', quotechar='|', first_flag=True):
        '''
        Save to Csv
        :param headers: row headers
        :param rows: datas
        :param filename:
        :param delimiter:
        :param quotechar:
        :param first_flag: if the file is first writed
        :return:
        '''
        if first_flag:
            with open(filename, 'wb') as fout:
                f_csv = csv.DictWriter(fout, headers, delimiter=delimiter, quotechar=quotechar)
                f_csv.writeheader()
                f_csv.writerows(rows)
        else:
            with open(filename, 'ab+') as fout:
                f_csv = csv.DictWriter(fout, headers, delimiter=delimiter, quotechar=quotechar)
                f_csv.writerows(rows)

    def LoadCsv(self, filename='Crawled.csv', delimiter=' ', quotechar='|'):
        '''
        Load from Csv
        :param filename:
        :param delimiter:
        :param quotechar:
        :return: headers and datas
        '''
        with open(filename, 'rb') as f:
            f_csv = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
            headers = f_csv.fieldnames
            rows = []
            for row in f_csv:
                rows.append(row)
        return headers, rows

    def SaveHtml(self, filename='Crawled.html', title='Crawled'):
        idx = 1
        with codecs.open(filename, 'wb', encoding='utf-8') as fout:
            self._SaveHtmlHeader(fout, title)
            fout.write("<body>\n")
            fout.write("<table>\n")
            fout.write("<caption>%s</caption>\n"%(title,))
            fout.write("<tr class='headline'>\n")
            fout.write("<th>Index</th>\n")
            fout.write("<th>Title</th>\n")
            fout.write("<th>Summary</th>\n")
            fout.write("</tr>\n")
            for data in self.datas:
                if idx % 2 == 1:
                    fout.write("<tr class='oddline'>\n")
                else:
                    fout.write("<tr class='evenline'>\n")
                fout.write("<td>%s</td>\n"%(idx))
                fout.write("<td><a href='%s' target='_blank'>%s</a></td>\n"%(data['url'],data['title'],))
                fout.write("<td>%s</td>\n"%(data['summary'],))
                fout.write("</tr>\n")
                idx += 1
            fout.write("</table>\n")
            fout.write("</body>\n")
            fout.write("</html>\n")

    def _SaveHtmlHeader(self, fout, title='Crawled'):
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



##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    datas = [{'url': u'First', 'title': u'First\'s name', 'summary': u'金坷垃'},
             {'url': u'Second', 'title': u'Second\'s name', 'summary': u'元首'},
             {'url': u'Third', 'title': u'Third\'s name', 'summary': u'葛炮'},
             {'url': u'Forth', 'title': u'Forth\'s name', 'summary': u'王司徒'},
             {'url': u'Fifth', 'title': u'Fifth\'s name', 'summary': u'比利王'},
             ]
    dout = DataOutput()
    for data in datas:
        dout.StoreData(data)
    dout.SaveHtml('Test.html')

    dout.SaveCsv('Test.csv')
    headers, rows = dout.LoadCsv('Test.csv')
    print headers
    for row in rows:
        print row
