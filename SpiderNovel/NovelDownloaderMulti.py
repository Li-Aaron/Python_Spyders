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
import multiprocessing as mp
try:
    import cPickle as pickle
except ImportError:
    import pickle

##############################################
#------------------常量定义------------------#
##############################################
URL = 'http://www.quyuege.com/xs/43/43176/'
# URL = 'http://www.quyuege.com/xs/144/144341/'
EOL = u'\n'
pickleFile = os.getcwd()+'pickle.txt'

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################
class NovelDownloaderMulti(NovelDownloader):

    def GetNovelTextProcess(self, queue, lock, idxValue, idxMax):
        '''
        multitask process (using multiprocessing.Pool)
        :param queue: multiprocessing.Manager().Queue()
        :param lock: multiprocessing.Lock()
        :param idx: multiprocessing.Manager().Value() idx.value -> nextChapterIdx
        :param idx: Max Chapter Index (int)
        :return: N/A
        '''
        # print 'process start %d' % (os.getpid())
        with lock:
            with open(pickleFile, 'r') as f:
                novelUrlList = pickle.load(f)
        while True:
            with lock:
                idxValue.value += 1
                nextChapterIdx = idxValue.value
                if (nextChapterIdx > idxMax):
                    break
                url = novelUrlList[nextChapterIdx-1]
                # print (nextChapterIdx, url)

            textUrl = self.NovelUrlComb(url)
            chapterText = self.GetNovelTextFromUrl(textUrl).encode('utf-8')
            chapterPatch = {nextChapterIdx: chapterText}
            queue.put(chapterPatch, True, timeout=1)
        # print 'process stop %d' % (os.getpid())

    def SaveToFileProcess(self, queue, idxMax):
        '''
        :param nd: NovelDownloaderMulti instance
        :param queue: multiprocessing.Manager().Queue()
        :param idxMax: process(chapter) max index
        :return:
        '''
        chapterWaitDict = {}
        idxNext = 1  # start from 1
        while (idxNext <= idxMax):
            if (chapterWaitDict):
                if idxNext in chapterWaitDict.keys():
                    chapterText = chapterWaitDict.pop(idxNext)
                    self.SaveToFile(chapterText, attr='a+')
                    print "[%4.3f%%] %5d of %5d is done ..." % (100.0 * idxNext / idxMax, idxNext, idxMax)
                    idxNext += 1
            else:
                while (True):
                    chapterPatch = queue.get(True, timeout=60)
                    idxNow = chapterPatch.keys()[0]
                    if (idxNow != idxNext):
                        chapterWaitDict.update(chapterPatch)
                    else:
                        chapterText = chapterPatch[idxNext]
                        self.SaveToFile(chapterText, attr='a+')
                        print "[%4.3f%%] %5d of %5d is done ..." % (100.0 * idxNext / idxMax, idxNext, idxMax)
                        idxNext += 1
                        break


    def GetNovel(self, startChap = 0):
        '''
        DownLoad Text Start (using Multitask)
        :return:
        '''
        self.GetNovelList()
        print self.novel['Title']
        # get novel
        self.SaveNovelTitle()

        # multiprocess start
        manager = mp.Manager()
        nextChapterIdx = manager.Value('tmp', startChap)
        queue = manager.Queue()
        lock = mp.Lock()
        # s = mp.Semaphore(1)
        numChapter = len(self.novel['UrlList'])
        # dump novelUrlList otherwise push error
        with open(pickleFile, 'w') as f:
            pickle.dump(self.novel['UrlList'], f)
        self.novel = {}

        # write process
        writeProc = mp.Process(target=self.SaveToFileProcess, args=(queue, (numChapter - startChap)))

        # spyder processes ( to many processes cause unstable)
        for i in range(mp.cpu_count()-2):
            spyProc = mp.Process(target=self.GetNovelTextProcess, args = (queue, lock, nextChapterIdx, numChapter))
            spyProc.start()
            # spyProc.join()

        writeProc.start()
        writeProc.join()
        print '[Process Done]'

##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
    # argv check
    webPageUrl = URL
    startChap = 0
    if len(sys.argv) < 2:
        print 'For debug usage!'
    elif len(sys.argv) == 2:
        webPageUrl = str(sys.argv[1])
    elif len(sys.argv) == 3:
        webPageUrl = str(sys.argv[1])
        startChap = int(sys.argv[2]) - 1
    else:
        raise Exception("too many input parameters (>2)")

    novelDL = NovelDownloaderMulti(webPageUrl)
    novelDL.GetNovel(startChap)
