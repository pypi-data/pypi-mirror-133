import os
from .Config import dirs as dirs
import nltk
from .Data import Data
import re


class Stops:

    def __init__(self):
        self._path = os.getcwd() + "\\"
        self.loadedFile = ""
        self.Data = Data()

    def isStopword(self, token, method="nltk"):
        stops = self.NLTKList()
        if token in stops:
            return True
        else:
            return False

    def cleanStops(self, text, method="file", file=False):
        newlist = []
        if method == "file" and self.loadedFile != file:
            self.stops = self.loadList(file)
        elif method == "nltk":
            self.stops = self.NLTKList()
        elif method == "list":
            if isinstance(file, list):
                self.stops = file
            else:
                raise EnvironmentError("Liste vermelisiniz")
        for word in text:
            if word not in self.stops:
                newlist.append(word)
        return newlist

    def loadList(self, file=False):
        if self.loadedFile != file:
            file = self._path + dirs._datapath + "\\" + dirs._stoplist
        else:
            file = self._path + dirs._datapath + "\\" + file
        lines = open(file, "r", encoding='utf-8').readlines()
        stops = [w.replace('\n', '') for w in lines]
        return stops

    def NLTKList(self):
        stops = nltk.corpus.stopwords.words('turkish')
        return stops

    def CleanShorterWorker(self, text, num):
        list = []
        for word in text:
            if len(word) >= num:
                list.append(word)
        return list

    def loadQuery(self, query=False, fields=["ad", "soyad", "adsoyad"]):
        if query == False:
            query = """SELECT ad,soyad,CONCAT(ad," ",soyad) as adsoyad FROM hrzm_personel"""

        data = self.Data.QueryReturn(query)
        ret = set()
        for key, row in data.iterrows():
            for field in fields:
                dt = self.cleanQuery(row[field])
                vals = set(dt)

                ret.update(vals)
        print(list(ret))
        return list(ret)

    def cleanQuery(self, text):

        text = text.replace('İ', 'i')
        text = text.replace('-', '')
        text = text.lower()
        text = text.replace("'", '')
        text = re.sub(re.compile(r'[^a-zA-ZçığöüşÇİĞÖÜŞ ]'), '', text)
        text = text.split(" ")
        while " " in text: text.remove(" ")
        while "" in text: text.remove("")
        return text

    def CleanWithList(self, text, list):
        newlist = []
        for word in text:
            if word not in list:
                newlist.append(word)
        return newlist
