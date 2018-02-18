# SpiderNovel
下小说的爬虫脚本  
调用方法 python NovelDownloader_[SITENAME].py http_url(小说目录页) 章节数(续下用，默认为1)  

## 2018-2-18
####[SpiNovel]
NovelDownloader 增加对&amp;lt;u&amp;gt;的处理
####[NovelDownloader_Biquwu]
新增NovelDownloader_Biquwu

## 2017-12-30  
#### [SpiNovel]  
重构NovelDownloader、NovelDownloaderMulti、NovelDownloaderGev为SpiNovel包
下载完毕去掉pickleFile
#### [NovelDownloader_23us]   
NovelDownloader23us重命名
#### [NovelDownloader_Quyuege]  
新增NovelDownloader_Quyuege

## 2017-12-30  
#### [NovelDownloaderMulti]  
StartChap统一为从1开始
下载完毕去掉pickleFile
#### [NovelDownloaderGev]  
增加对应协程gevent版本  
调用方法 python NovelDownloaderGev.py http_url(小说目录页) 章节数(续下用，默认为1)  

## 2017-12-27  
#### [NovelDownloader]  
修正去BR和空格的模块  
打开网页增加超时重试  
保存文件修改  
增加保存Title模块（便于重构）  
#### [NovelDownloaderMulti]  
新增多进程版本（稳定性有待提高）  
#### [NovelDownloader23us]  
增加对应Multi版本  

## 2017-12-25
#### [NovelDownloader]  
QuYueGe下载器重构为NovelDownloader类  
#### [NovelDownloader23us]  
新增23us下载器  

## 2017-12-8
#### [QuYueGeDownloader]  
QuYueGe下载器  

