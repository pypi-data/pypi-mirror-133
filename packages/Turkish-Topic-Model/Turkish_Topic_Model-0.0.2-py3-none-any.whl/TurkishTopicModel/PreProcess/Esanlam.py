import os
import requests
import re
import pickle
from .Config import dirs as dirs


class Esanlam:
    esanlamsozluk = dirs._esanlamSozluk

    def __init__(self):

        self.processdir = dirs._path + dirs._datapath + "\\" + dirs._processdir
        self.sozluk = False
        self.dictloaded = False
        self.online = False
        self.DEUinited = False

    def loadDict(self, file=False):
        if file == False:
            file = dirs._path + dirs._esanlamSozluk
        self.dict = dict()
        try:
            lines = open(file, "r", encoding='utf-8').read()
            for line in lines.split("\n"):
                veri = line.split("\t")
                if len(veri) > 1:
                    if veri[0] in self.dict.keys():
                        self.dict[veri[0]].append(veri[1])
                    else:
                        self.dict[veri[0]] = list({veri[1]})
            self.dictloaded = True
        except:
            raise FileNotFoundError("Sözlük bulunamadı")

    def fromDict(self, counts, dictionary=False):

        if self.dictloaded == False or self.sozluk != dictionary:
            if dictionary == False: dictionary = self.sozluk
            self.sozluk = dictionary
            self.loadDict(dictionary)
        suggest = {}
        self.oneri = {}

        for word in counts.keys():
            if word not in suggest.keys():
                sug = dict()
                if (len(word) > 2):
                    if word in self.dict.keys():
                        sug = self.dict[word]
                if len(sug) > 0:
                    suggest[word] = sug
                    suggest[word].append(word)
        return suggest

    def fromDEU(self, counts):
        if (self.DEUinited == False): self.initDEU()
        list = {}
        for word in counts:
            ret = self.askDEU(word)
            if len(ret) > 0:
                list[word] = ret
                list[word].append(word)

        with open(self.processdir + "\\DEU_dictionary.dict", "wb") as f:
            pickle.dump(self.DEUdict, f)

        with open(self.processdir + "\\DEU_asked.dict", "wb") as f:
            pickle.dump(self.DEUasked, f)

        return list

    def askDEU(self, word):

        if (word not in self.DEUasked) and (word not in self.DEUdict.keys()) and self.online == True:
            try:
                rdata = {
                    "__VIEWSTATE": self.VIEWSTATE[0],
                    "__VIEWSTATEGENERATOR": self.VIEWSTATEGENERATOR[0],
                    "__EVENTVALIDATION": self.EVENTVALIDATION[0],

                    "TextBox1": word,
                    "Button1": "Ara"}
                self.r = requests.post(dirs._esanlamurl, data=rdata, json=rdata,
                                       cookies=self.r.cookies)
                oneri = re.findall('<font color="CadetBlue" size="4">(.*)<\/font>', self.r.text)
                if (len(oneri) > 0):
                    oneri = oneri[0].replace(" ", "")
                    oneri = oneri.split("/")
                    self.DEUdict[word] = oneri
                self.DEUasked.append(word)
            except:
                oneri = {}

        elif (word in self.DEUdict.keys()):
            oneri = self.DEUdict[word]

        else:
            oneri = {}
        print(oneri)
        return oneri

    def initDEU(self):
        print("DEU Başlatılıyor...")
        try:
            self.r = requests.get(dirs._esanlamurl)
            self.VIEWSTATE = re.findall('id="__VIEWSTATE" value="(.*)"', self.r.text)
            self.VIEWSTATEGENERATOR = re.findall('id="__VIEWSTATEGENERATOR" value="(.*)"', self.r.text)
            self.EVENTVALIDATION = re.findall('id="__EVENTVALIDATION" value="(.*)"', self.r.text)
            self.online = True
            print("Bağlandı")
        except:
            self.online = False

        try:

            with open(self.processdir + "\\DEU_dictionary.dict", "rb") as f:
                self.DEUdict = pickle.load(f)
        except:
            self.DEUdict = {}

        try:

            with open(self.processdir + "\\DEU_asked.dict", "rb") as f:
                self.DEUasked = pickle.load(f)
        except:
            self.DEUasked = []

        self.DEUinited = True
