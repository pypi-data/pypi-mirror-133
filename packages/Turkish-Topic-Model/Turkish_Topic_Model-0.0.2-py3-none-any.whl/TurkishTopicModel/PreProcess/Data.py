import pymysql as pymysql
import pandas as pd
from .Config import mysql as config
import pickle
import os
from .Config import dirs as dirs


class Data:
    serverConnection = False
    datafrm = pd.DataFrame()

    def __init__(self, host=False, user=False, password=False, db=False):
        self.saveDir = dirs._datapath

    def Connect(self, host=False, user=False, password=False, db=False):
        if host == False:
            host = config.host
            user = config.user
            password = config.password
            db = config.db

        try:
            self.db = pymysql.connect(host=host, user=user, password=password, db=db, use_unicode=True, charset='utf8',
                                      init_command='SET NAMES UTF8')
            self.serverConnection = True
            return True
        except ConnectionRefusedError:
            raise ConnectionError("MYSQL Bağlantısı yapılamadı")
        return False

    def Query(self, query):
        if self.serverConnection == False:
            self.Connect()

        c = self.db.cursor()
        c.execute(query)
        data = c.fetchall()
        num_fields = len(c.description)
        field_names = [i[0] for i in c.description]
        self.datafrm = pd.DataFrame(data, columns=field_names)
        return data

    def QueryReturn(self, query):
        if self.serverConnection == False:
            self.Connect()

        c = self.db.cursor()
        c.execute(query)
        data = c.fetchall()
        num_fields = len(c.description)
        field_names = [i[0] for i in c.description]
        return pd.DataFrame(data, columns=field_names)

    def read_csv(self, file, header=True):
        self.datafrm = pd.read_csv(file, header=header)

    def savePickle(self, file=False):
        if file == False:
            file = "data.pickle"

        file = self.saveDir + "\\" + file

        if not os.path.exists(os.getcwd() + "\\" + self.saveDir):
            os.makedirs(os.getcwd() + "\\" + self.saveDir)

        with open(file, "wb") as f:
            pickle.dump(self.datafrm, f)

    def loadPickle(self, file=False):
        if file == False:
            file = "data.pickle"
        file = self.saveDir + "\\" + file

        with open(file, "rb") as f:
            self.datafrm = pickle.load(f)

    def printDifferent(self, first, second, limit=False):
        if limit != False:
            dt = self.datafrm.sample(limit)
        else:
            dt = self.datafrm
        for key, row in dt.iterrows():
            if (row[first] != row[second]):
                print(row[first], row[second])

    def wordCound(self, column):
        count = []
        self.datafrm["cnt_" + column] = pd.Series()
        for key, line in self.datafrm.iterrows():
            if not isinstance(line[column], list):
                words = line[column].split(" ")
            else:
                words = line[column]
            count.append(len(words))

        self.datafrm["cnt_" + column] = count
