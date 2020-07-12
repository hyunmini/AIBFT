'''
    FeatureExtractor.py 
        
        - for 'Digital Forensics Challenge 2019 / tech part winner'

        last updated 2019.07.17 
            v0.1: FeatureExtractor class design&implementation
'''
import os,sys
import platform
import random
import glob
import time 
import re
import csv
import codecs
# for entropy
import numpy as np
from scipy.stats import entropy

class FeatureExtractor():
    '''
    main class to extract features

        features:
            1) strings : indexOf , FromCharCode, 0x, substr, charAt, 
            2) operator & special char : 
               <<, >> ,  +, -, [ , ] , {, } , | , :, \\ ,  ^, ~,  !,  * , $, \\x, _, %%
            3) tag : iframe
            4) function : document.write, onbeforeunload, eval(, onload, onunload, onbeforeload, 
            5) object : ActiveXObject(FileSystemObject, Wscript.Shell, ADODB.Stream,...), Math.

    '''
    def __init__(self):
        # init variables and features
        self.basePath = os.getcwd()
        self.baseDataPath = os.getcwd() + '/dataset'
        self.malDataPath = self.baseDataPath + '/mal'
        self.norDataPath = self.baseDataPath + '/nor'
        self.outPath = self.basePath + '/output'
        self.allFeature = []
        self.features = {
                # special char
				"feature1":b"\\x",
				"feature2":b"0x",
				"feature3":b"$",
				"feature4":b"+",
				"feature5":b"*",
				"feature6":b"%",
				"feature7":b"[",
				"feature8":b"_",
				"feature9":b"|",
				"feature10":b"{",
				"feature11":b":",
				"feature12":b"&",
                "feature13":b"~",
                "feature14":b"!",
				"feature15":b">>",
				"feature16":b"<<",
				"feature17":b"^",
                # tag, function
                "feature18":b"iframe",
                "feature19":b"http://",
                "feature20":b"onbeforeunload",
                "feature21":b"eval(",
                "feature22":b"onload",
                "feature23":b"onunload",
                "feature24":b"indexOf",
                "feature25":b"FromCharCode",
                "feature26":b"substr",
                "feature27":b"charAt",
                # object
                "feature28":b"ActiveXObject",
                "feature29":b"Wscript.Shell",
                "feature30":b"WScript",
                "feature31":b"ADODB.Stream",
                "feature32":b"Math.",
                "feature33":b"toString",
                "feature34":b".btoa(", 
                "feature35":b"entropy_sp",     # special entropy *
                "feature36":b"lineCount",     # line count
                "feature37":b"filesize",     # file size
                "feature38":b"maxlinesize",     # maximum line size
                "feature39":b"multilinecmt"     # /* multiline comment
        }

    def setPath(self, basepath='', malpath='', norpath='', outpath=''):
        # set working path
        if basepath != '':
            self.baseDataPath = basepath
        if malpath != '':
            self.malDataPath = malpath
        if norpath != '':
            self.norDataPath = norpath
        if outpath != '':
            self.outPath = outpath

    def getDatesetToList(self, type='all'):
        # make dataset list
        flist = []
        tlist = glob.glob(self.malDataPath + '/**', recursive=True) + \
                glob.glob(self.norDataPath + '/**', recursive=True)
        for f in tlist:
            if os.path.isfile(f):
                flist.append(f)
        return flist

    def readFile(self, filenamePath, encoding=None):
        try:
            #if(encoding == 'bytes'):
            fd = open(filenamePath, 'rb')
            lines = fd.read()
            fd.close()
            return lines
        except IOError as e:
            print("I/O error({0}): {1}:".format(e.errno, e.strerror))
            return None
        except:
            print("Unexpected Error:", sys.exc_info()[0])
            return None

    def getFeature(self, targetFile):
        # extract feature one file
        contents = ''
        featureList = []
        #print(targetFile)
        contents = self.readFile(targetFile)
        cLen = len(contents)
        if contents:
            if '/mal' in targetFile:
                featureList.append('1')
            else:
                featureList.append('0')    
            for index in range(len(self.features)):
                cnt = contents.count(self.features['feature'+str(index+1)]) * 100
                if index < 17:
                    cnt = round(float(cnt)/cLen, 2)
                    featureList.append(str(cnt))   
                if index >= 17 and index < 34:
                    if cnt >= 1:
                        cnt = 1
                    if index == 0:
                        cnt = cnt*2 # eval
                    featureList.append(str(cnt))
                if index >=34:
                    break
            entropy = self.getEntropy(contents,1)/5
            if entropy > 1.0:
                featureList.append("1")   # 35
            else:
                featureList.append(str(entropy))   

            linecount = contents.count(b'\n')/1000
            if linecount > 1.0:
                featureList.append("1")
            else:
                featureList.append(str(linecount))         # 36

            filesize = len(contents)/100000
            if filesize> 1.0:
                featureList.append("1")
            else:
                featureList.append(str(filesize))                 # 37

            maxLinesize = self.getMaxLinesize(contents)/10000
            if maxLinesize> 1.0:
                featureList.append("1")
            else:
                featureList.append(str(maxLinesize))                 # 38

            multilinecmt = contents.count(b'/*')/100
            if multilinecmt> 1.0:
                featureList.append("1")
            else:
                featureList.append(str(multilinecmt))                 # 39
        return featureList
            
    def getAllFeatures(self, header = True):
        # extract feature from all files
        results = []
        targets = self.getDatesetToList()
        maxlen = len(targets)
        index = 0
        for target in targets:
            if index % 100 == 0:
                print("[+] processing {}/{}...".format(index, maxlen))
            index += 1
            results.append(self.getFeature(target))
        self.allFeature = results        
        return results

    def getMaxLinesize(self, contents):
        size = 0
        for line in contents.split(b'\n'):
            if size < len(line):
                size = len(line)
        return size

    def getEntropy(self, contents, mode=1):
        # mode 0: char only
        # mode 1: non char only
        # mode 2: all char
        labels = list(contents)
        alList = []
        spList = []
        for c in labels:
            if chr(c).isalnum():
                alList.append(c)
            else:
                spList.append(c)
            # except:
            #     print("!!!", c, ", type:", type(c))
        if mode == 0:
            labels = alList
        elif mode == 1:
            labels = spList
        else:
            pass
        # labels = list (ex: ['a','b','h','0'])
        value,counts = np.unique(labels, return_counts=True)
        return entropy(counts, base=None)
                    
    def saveResultToFile(self):
        # save features to file
        if len(self.allFeature) == 0:
            self.getAllFeatures()
        if not os.path.exists(self.outPath):
            os.mkdir(self.outPath)
        # header
        headers = 'mal,'
        for index in range(len(self.features)):
            headers += self.features['feature'+str(index+1)].decode('ascii') + ','
        # contents(features list)
        contents = ''
        for feature in self.allFeature:
            contents += ','.join(feature) + '\n'

        findex = time.strftime("%Y%m%d")
        with open(self.outPath + '/features_{}.csv'.format(findex),'w') as fp:
            fp.write(headers + '\n' + contents)

if __name__ == '__main__':
    print("[*] Start!!")
    import time
    start_time = time.time()
    features = FeatureExtractor()
    features.getAllFeatures()
    features.saveResultToFile()

    end_time = time.time()
    print("WorkingTime: {} sec".format(end_time-start_time))

    print("[*] Finish!!")