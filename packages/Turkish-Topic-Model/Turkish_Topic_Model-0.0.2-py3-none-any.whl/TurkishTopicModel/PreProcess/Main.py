from .Data import Data
from .Zemberek import Zemberek
from .Esanlam import Esanlam
import pandas as pd
import re
import json
from collections import OrderedDict
from operator import itemgetter
import os
from .Config import dirs as dirs
from .Stops import Stops
from .ITUNLPTools import ITUNLPTools


class Main():
    stats = []
    num = 1

    def __init__(self):
        print(dirs._path)

        if not os.path.exists(dirs._path + dirs._datapath):
            os.makedirs(dirs._path + dirs._datapath)
        if not os.path.exists(dirs._path + dirs._datapath + "\\" + dirs._processdir):
            os.makedirs(dirs._path + dirs._datapath + "\\" + dirs._processdir)

        self.Zemberek = Zemberek()
        self.Data = Data()
        self.Esanlam = Esanlam()
        self.Stops = Stops()
        self.ITUNLPTools = ITUNLPTools()

    def is_str(self, v):
        return type(v) is str

    def while_replace(self, string, neddle, haystack):
        while neddle in string: string = string.replace(neddle, haystack)
        return string

    def Tokenize(self, area, newarea=False):
        if (newarea == False): newarea = area
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.Zemberek.TurkishTextToken(x))

    def jsonunicode(self, data):
        if isinstance(data, str):
            return json.dumps(json.loads(data), ensure_ascii=False)
        else:
            return ""

    def fixUnicode(self, area, newarea=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.jsonunicode(x))

    def fixChars(self, area, newarea=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.__fixcharsworker(x))

    def __fixcharsworker(self, x):
        if isinstance(x, list):
            x = " ".join(x)

        newtext = ""
        length = 0
        charbefore = ""
        i = 0
        for char in x:
            if char == charbefore:
                length += 1
                if length < 2:
                    newtext += char
            else:
                newtext += char
                length = 0
            i += 1
            charbefore = char
        if (x != newtext): print(x, newtext)
        return self.Zemberek.TurkishTextToken(newtext)

    def Clean(self, area, newarea=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.__cleanerworker(x))

    def __cleanerworker(self, x):
        if isinstance(x, list):
            x = " ".join(x)

        x = x.replace('-', '')
        x = x.replace("'", '')
        x = x.replace("â", 'a')
        x = x.replace("İ", "i")
        x = x.replace("î", 'i')
        x = x.replace("î", 'i')
        x = re.sub(re.compile(r"[-'\"]"), '', x)
        x = re.sub(re.compile(r"[\\][ntrv]"), ' ', x)
        x = re.sub(re.compile(r'[^a-zA-ZçığöüşÇİĞÖÜŞ ]'), ' ', x)
        x = self.while_replace(x, "  ", " ")
        x = x.lower()
        x = self.Zemberek.TurkishTextToken(x)

        return x

    def __cleanword(self, x):
        if isinstance(x, list):
            x = " ".join(x)

        x = x.replace('-', '')
        x = x.replace("'", '')
        x = x.replace("â", 'a')
        x = x.replace("İ", "i")
        x = x.replace("î", 'i')
        x = x.replace("î", 'i')

        x = re.sub(re.compile(r"[-'\"]"), '', x)
        x = re.sub(re.compile(r"[\\][ntrv]"), ' ', x)
        x = re.sub(re.compile(r'[^a-zA-ZçığöüşÇİĞÖÜŞ ]'), ' ', x)
        x = self.while_replace(x, " ", "")
        x = x.lower()
        return x

    def lower(self, area, newarea=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self._lowerworker(x))

    def _lowerworker(self, text):
        if isinstance(text, str):
            tokens = self.Zemberek.TurkishTextToken(x)
        else:
            tokens = text
        newtext = []
        for token in tokens:
            token = token.replace('İ', 'i')
            token = token.replace("ardunio", 'arduino')
            token = token.replace("nardunio", 'arduino')
            token = token.lower()
            newtext.append(token)
        return newtext

    def Normalize(self, area, newarea):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.Zemberek.TurkishNormalizer(x))

    def NormalizeWords(self, area, newarea):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.Zemberek.TurkishWordNormalizer(x))

    def sorguBirlestir(self, x, sifirla=False):
        if sifirla == True:
            self.sorgumetni = ""

        self.sorgumetni += "\n\n" + " ".join(x)

    def ITUNormalize(self, area, newarea):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.sorguBirlestir("", True)
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.sorguBirlestir(x))
        print(self.sorgumetni)
        print(self.ITUNLPTools.ask("normalize", self.sorgumetni))

    def NormWithCorr(self, area, newarea):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        counts = self.TFBuilder(self.Data.datafrm[area])
        corrects = self.Zemberek.TurkishSpellingWithNormal(counts)
        suggestion = self.__suggestion(counts, corrects)
        self.__changeColumn(area, newarea, suggestion)

    def TFBuilder(self, text, topic=False):
        counts = {}
        for row in text:
            if not isinstance(row, list):
                if len(row) == 0:
                    row = [" "]
                else:
                    row = row.split(" ")

            for word in row:
                word = word.replace('"', '')
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
        self.stats.append([self.num, topic, len(counts)])
        self.TFMean = sum(counts.values()) / len(counts.values())
        return counts

    def NormalTFBuilder(self, text, topic=False):
        counts = self.TFBuilder(text, topic=False)
        mx = max(counts.values())
        mn = min(counts.values())
        newcounts = {}
        for key in counts.keys():
            newcounts[key] = (counts[key] - mn) / (mx - mn)

        return newcounts

    def __SpellingSuggestion(self, count, suggest):
        suggestion = dict()

        for key, val in count.items():
            suje = dict()
            if suggest.get(key):
                for sugval in suggest.get(key):
                    if count.get(key):
                        suje[sugval] = count.get(sugval)
                    else:
                        suje[sugval] = count.get(key) + 1
                    insert = dict()
                    for elem in suje.items():
                        if elem[1] is not None: insert[elem[0]] = elem[1]
                insert = OrderedDict(sorted(insert.items(), key=itemgetter(1), reverse=True))
                suggestion[key] = insert

        replace = dict()
        for key, val in suggestion.items():
            if key != list(val)[0]:
                pattern = key
                change = list(val)[0]
                replace[pattern] = str(change)

        return replace

    def __suggestion(self, count, suggest):
        suggestion = dict()

        for key, val in count.items():
            suje = dict()
            if suggest.get(key):
                for sugval in suggest.get(key):
                    if count.get(key):
                        suje[sugval] = count.get(sugval)
                    else:
                        suje[sugval] = count.get(key) + 1
                    insert = dict()
                    for elem in suje.items():
                        if elem[1] is not None: insert[elem[0]] = elem[1]
                insert = OrderedDict(sorted(insert.items(), key=itemgetter(1), reverse=True))
                suggestion[key] = insert

        replace = dict()
        for key, val in suggestion.items():
            if key != list(val)[0]:
                pattern = key
                change = list(val)[0]
                replace[pattern] = str(change)

        return replace

    def correctSpelling(self, area, newarea=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        counts = self.NormalTFBuilder(self.Data.datafrm[area])
        corrects = self.Zemberek.TurkishSpelling(counts)
        suggestion = self.__SpellingSuggestion(counts, corrects)
        self.__changeColumn(area, newarea, suggestion)

    def jaccard(self, text1, text2):
        set1 = set(text1)
        set2 = set(text2)
        similarity = len(set1.intersection(set2)) / len(set1.union(set2))
        return similarity

    def __SpellingSuggestion(self, count, suggest):
        suggestion = dict()

        for kelime, oneriler in suggest.items():
            skor = {}
            if len(suggest.get(kelime)) > 1:
                gf = 0.1
                for oneri in oneriler:

                    if count.get(oneri):
                        gf = count.get(oneri)
                        if gf < 0.1: gf = 0.1
                    oneri = oneri.lower()
                    oneri = self.__cleanword(oneri)
                    jaccard = self.jaccard(kelime, oneri)
                    sk = (gf * jaccard) ** 0.5
                    skor[oneri] = sk
                skor = OrderedDict(sorted(skor.items(), key=itemgetter(1), reverse=True))
                suggestion[kelime] = skor

        replace = dict()
        for key, val in suggestion.items():
            if key != list(val)[0]:
                pattern = key
                change = list(val)[0]
                replace[pattern] = str(change)
        print("Öneriler", suggestion)
        print("Düzeltme", replace)
        return replace

    def __changeColumn(self, area, newarea, suggestion):
        if (newarea == False): newarea = area
        if area != newarea: self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.__changeWords(x, suggestion))

    def __changeWords(self, row, suggestion):
        new = list()
        newstring = ""
        c = 0
        if len(row) > 0:
            for kelime in row:
                if kelime in suggestion.keys():
                    new.append(suggestion.get(kelime))
                    c += 1
                elif len(kelime) > 1:
                    new.append(kelime.replace("[$&+,:;=?@#|'<>.-^*()%!]", ''))
            if len(new) > 0:
                return new
            else:
                return list(' ')
        else:
            return list(' ')

    def Counter(self, area):
        print("Starting to count: '" + str(area))
        counts = self.TFBuilder(self.Data.datafrm[area])
        print(str(len(counts)) + " words")
        return counts

    def MorphologyReplace(self, area, newarea=False, type="stem", length="max"):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        counts = self.TFBuilder(self.Data.datafrm[area])
        corrects = self.Zemberek.Morphology(counts, type, length)
        self.__changeColumn(area, newarea, corrects)

    def tagNER(self, area, newarea=False, tagList=[]):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.__tagnerworker(x, tagList))

    def __tagnerworker(self, x, tagList=[]):
        tags = self.Zemberek.TurkishNER(x)
        newtext = []
        for tag in tags:
            if (tag[0] in tagList) or len(tagList) == 0:
                newtext.append("_".join(tag[1]))
            else:
                newtext += tag[1]
        return newtext

    def tagTerms(self, area, newarea=False, tagList={}):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        tags = {}
        maxsize = 0

        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.__tagtermsworker(x, tags))

    def __tagtermsworker(self, x, tags={}):
        if isinstance(x, str):
            tokens = self.Zemberek.TurkishTextToken(x)
        else:
            tokens = x
        match = False
        for i in range(0, len(tokens)):
            for k in range(max(tags.keys()) + 1, 1, -1):
                if (i - k) >= 0:
                    sorgu = tokens[i - k:i]
                    if sorgu in tags[k]:
                        match = True
                        change = tags[sorgu]
                        tokens[i - k] = change
                        for j in range(i - k + 1, i):
                            tokens[j] = False

        if False in tokens:
            tokens.remove(False)
        return tokens

    def tagTermsto(self, area, newarea=False, tagList=pd.DataFrame(), maxlength=0):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()

        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(
            lambda x: self.__tagtermstoworker(x, tagList, maxlength))

    def __tagtermstoworker(self, x, tagList, maxLength):
        if isinstance(x, str):
            tokens = self.Zemberek.TurkishTextToken(x)
        else:
            tokens = x
        match = False
        for i in range(0, len(tokens)):
            for k in range(maxLength + 1, 1, -1):
                if (i - k) >= 0:
                    sorgu = tokens[i - k:i]
                    df = ""
                    try:
                        df = tagList[tagList["find"].map(tuple) == tuple(sorgu)].iloc()[0]["replace"]
                    except:
                        pass

                    if df != "":
                        match = True
                        tokens[i - k] = df
                        for j in range(i - k + 1, i):
                            tokens[j] = False
                    """if sorgu in tags[k]:
                        index=tags.values ().index (sorgu)
                        match=True
                        tokens[i-k]=replace[index]
                        for j in range(i-k+1,i):
                            tokens[j]=False"""

        while False in tokens:
            tokens.remove(False)
        if match == True:
            print(x, tokens)
        return tokens

    def cleanNER(self, area, newarea=False, tagList=[]):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.__cleannerworker(x, tagList))

    def __cleannerworker(self, x, tagList=[]):
        tags = self.Zemberek.TurkishNER(x)
        newtext = []
        for tag in tags:
            if (tag[0] not in tagList) or len(tagList) == 0:
                for t in tag[1]:
                    newtext.append(t)

        return newtext

    def EsanlamDictReplace(self, area, newarea=False, dict=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        counts = self.TFBuilder(self.Data.datafrm[area])
        corrects = self.Esanlam.fromDict(counts, dict)
        suggestion = self.__suggestion(counts, corrects)
        self.__changeColumn(area, newarea, suggestion)

    def EsanlamDEUReplace(self, area, newarea=False, dict=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        counts = self.TFBuilder(self.Data.datafrm[area])
        corrects = self.Esanlam.fromDEU(counts)
        suggestion = self.__suggestion(counts, corrects)
        self.__changeColumn(area, newarea, suggestion)

    def cleanStops(self, area, newarea=False, method="file", file=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.Stops.cleanStops(x, method, file))

    def cleanWithQuery(self, area, newarea=False, query=False, fields=False):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        if query != False:
            stops = self.Stops.loadQuery(query, fields)
        else:
            stops = self.Stops.loadQuery()

        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.Stops.CleanWithList(x, stops))

    def cleanWithList(self, area, newarea=False, stops=[]):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.Stops.CleanWithList(x, stops))

    def cleanShorter(self, area, newarea=False, num=3):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(lambda x: self.Stops.CleanShorterWorker(x, num))

    def normalTFWords(self, area, min, max):
        counts = self.NormalTFBuilder(self.Data.datafrm[area])
        print([[key, val] for key, val in counts.items() if val >= min and val <= max])

    """
    type=1: Whole max and min
    type=2:max
    type=3:min
    """

    def cleanPercentage(self, area, newarea=False, percentage=0.05, type=1):
        if (newarea == False): newarea = area
        if (area != newarea): self.Data.datafrm[newarea] = pd.Series()
        counts = self.NormalTFBuilder(self.Data.datafrm[area])
        self.Data.datafrm[newarea] = self.Data.datafrm[area].apply(
            lambda x: self.cleanpercentageworker(x, counts, percentage, type))

    def cleanpercentageworker(self, text, counts, percentage, type):
        newtext = []
        for word in text:
            if type == 1:
                if counts[word] < (1 - percentage) and counts[word] > percentage:
                    newtext.append(word)
            if type == 2:
                if counts[word] < (1 - percentage):
                    newtext.append(word)
            if type == 3:
                if counts[word] > (percentage):
                    newtext.append(word)
        if newtext != text: print(text, newtext)
        return newtext

    def listDocs(self, column, words):
        i = 0
        for key, row in self.Data.datafrm.iterrows():
            found = False

            for word in words:
                if word in row[column]:
                    found = True
                else:
                    found = False

            if found == True:
                i += 1
                print(row[column])

        print("{} belgede geçiyor".format(i))

    def Polarity(self, column):
        lexicon = {}
        with open(dirs._path + dirs._datapath + "\\SWNetTR.csv", "r") as f:
            for line in f:
                l = line.split(";")
                lexicon[l[0]] = float(l[1].replace(",", "."))

        self.Data.datafrm["pol_" + column] = pd.Series()
        self.Data.datafrm["sc_" + column] = pd.Series()
        polarity_list = []
        sc_list = []
        for key, line in self.Data.datafrm.iterrows():
            poll = 0
            size = 0

            for word in line[column]:
                try:
                    if word in lexicon:
                        lec = lexicon[word]
                        size += 1
                        poll += float(lec)
                except:
                    pass

            if size > 0:
                sc = poll / size
                self.Data.datafrm["sc_" + column][key] = sc
                if sc > 0:
                    polarity = "p"
                elif sc < 0:
                    polarity = "n"
                else:
                    polarity = "o"
            else:
                polarity = "o"
                sc = 0

            polarity_list.append(polarity)
            sc_list.append(sc)

        self.Data.datafrm["pol_" + column] = polarity_list
        self.Data.datafrm["sc_" + column] = sc_list
