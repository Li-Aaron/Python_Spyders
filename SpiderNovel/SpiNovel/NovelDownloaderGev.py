# -*- coding: utf-8 -*-
'''
程序名称 NovelDownloader
@Author: AC
2017-12-8
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import sys, os
from NovelDownloader import NovelDownloader
from gevent import monkey; monkey.patch_all()
# from gevent.pool import Pool
from gevent.lock import Semaphore
from gevent.queue import Queue
import gevent
try:
    import cPickle as pickle
except ImportError:
    import pickle

##############################################
#------------------常量定义------------------#
##############################################
# URL = 'http://www.quyuege.com/xs/43/43176/'
URL = 'http://www.quyuege.com/xs/144/144341/'
EOL = u'\n'
pickleFile = os.getcwd()+'pickle.txt'

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class NovelDownloaderGev(NovelDownloader):
    sem_pickle = Semaphore(1)
    sem_idx = Semaphore(1)
    # sem_queue = Semaphore(2)
    startChap = 1 # Start Chapter Index (int)
    idxValue = 1 # Next Chapter Index (int)
    idxMax = 1 # Max Chapter Index (int)
    processes = 2 # Download Processes

    def GetNovelTextProcess(self, queue):
        '''
        multitask process (using multiprocessing.Pool)
        :param queue: gevent.queue.Queue()
        :return: N/A
        '''
        # print '[load][start]'
        with self.sem_pickle:
            with open(pickleFile, 'r') as f:
                novelUrlList = pickle.load(f)
        while True:
            with self.sem_idx:
                nextChapterIdx = self.idxValue
                if (nextChapterIdx > self.idxMax):
                    break
                self.idxValue += 1
                url = novelUrlList[nextChapterIdx-1]
                # print (nextChapterIdx, url)

            textUrl = self.NovelUrlComb(url)
            chapterText = self.GetNovelTextFromUrl(textUrl).encode('utf-8')
            chapterPatch = {nextChapterIdx: chapterText}
            # print chapterPatch
            # with self.sem_queue:
            queue.put(chapterPatch, True, timeout=1)
        # print '[load][stop]'

    def SaveToFileProcess(self, queue):
        '''
        :param queue: multiprocessing.Manager().Queue()
        :return:
        '''
        # print '[save][start]'
        chapterWaitDict = {}
        startChap = self.startChap
        idxNext = self.startChap
        idxMax = self.idxMax
        while (idxNext <= idxMax):
            if (chapterWaitDict):
                if idxNext in chapterWaitDict.keys():
                    chapterText = chapterWaitDict.pop(idxNext)
                    self.SaveToFile(chapterText, attr='a+')
                    print "[%4.3f%%] %5d of %5d is done ..." % (100.0 * (idxNext-startChap) / (idxMax-startChap), idxNext, idxMax)
                    idxNext += 1
            else:
                while (True):
                    # with self.sem_queue:
                    chapterPatch = queue.get(True, timeout=5)
                    idxNow = chapterPatch.keys()[0]
                    # print idxNow
                    if (idxNow != idxNext):
                        chapterWaitDict.update(chapterPatch)
                    else:
                        chapterText = chapterPatch[idxNext]
                        self.SaveToFile(chapterText, attr='a+')
                        print "[%4.3f%%] %5d of %5d is done ..." % (100.0 * (idxNext-startChap) / (idxMax-startChap), idxNext, idxMax)
                        idxNext += 1
                        break
        # print '[save][stop]'

    def GetNovel(self, startChap = 1):
        '''
        DownLoad Text Start (using Multitask)
        :return:
        '''
        self.startChap = startChap
        self.GetNovelList()
        print self.novel['Title']
        # get novel
        self.SaveNovelTitle()

        # multiprocess start
        queue = Queue()
        numChapter = len(self.novel['UrlList'])
        # dump novelUrlList otherwise push error
        with open(pickleFile, 'w') as f:
            pickle.dump(self.novel['UrlList'], f)
        self.novel = {}
        self.idxValue = startChap
        self.idxMax = numChapter

        # write process
        writeProc = gevent.spawn(self.SaveToFileProcess, queue)

        # spyder processes ( to many processes cause unstable)
        for i in range(self.processes):
            spyProc = gevent.spawn(self.GetNovelTextProcess, queue)
            spyProc.start()
            # spyProc.join()

        writeProc.start()
        writeProc.join()
        os.remove(pickleFile)
        print '[Process Done]'

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    webPageUrl = URL
    startChap = 1
    if len(sys.argv) < 2:
        print 'For debug usage!'
    elif len(sys.argv) == 2:
        webPageUrl = str(sys.argv[1])
    elif len(sys.argv) == 3:
        webPageUrl = str(sys.argv[1])
        startChap = int(sys.argv[2])
    else:
        raise Exception("too many input parameters (>2)")

    novelDL = NovelDownloaderGev(webPageUrl)
    novelDL.GetNovel(startChap)
