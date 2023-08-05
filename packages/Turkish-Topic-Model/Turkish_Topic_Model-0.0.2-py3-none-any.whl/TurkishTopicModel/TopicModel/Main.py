import pandas as pd
import tomotopy as tp
import TurkishTopicModel.PreProcess as PreProcess
import numpy as np
from TurkishTopicModel.PreProcess.Config import dirs as dirs
import pickle
import multiprocessing
import time
import operator


class Main:
    datafrm = pd.DataFrame()

    def __init__(self):
        self.col = ""
        self.saveDir = dirs._datapath
        self.modelData = self.saveDir + "\\ModelData\\"
        self.cpucores = multiprocessing.cpu_count()

    def documentf(self, data):
        veriler = {}
        for v in data:
            metin = "_".join(v)
            if metin in veriler.keys():
                veriler[metin] += 1
            else:
                veriler[metin] = 1
        return veriler

    def createCorpus(self, column, minlen=0, maxlen=99999, compare=False, stops=False, clean=False, df=False):
        self.col = column
        alivecolumn = "alive_" + column
        self.datafrm[alivecolumn] = object()
        documentfreq = self.documentf(self.datafrm[column])
        cikarilan = 0

        if (stops == False):
            stops = []

        corpus = tp.utils.Corpus(stopwords=stops)
        alive = list()
        for key, line in self.datafrm.iterrows():
            veri = line[column]

            if df != False and documentfreq["_".join(line[column])] > df:
                cikarilan += 1
                veri = list()

            if compare != False and np.array_equal(line[column], line[compare]):
                veri = list()
                cikarilan += 1

            if compare != False and line[compare] == ['']:
                print(line[column], line[compare])
                veri = list()
                cikarilan += 1

            if clean != False:
                temizleveri = set()
                for tealan in clean:
                    for kelime in tealan:
                        temizleveri.add(kelime)
                for kelime in temizleveri:
                    while kelime in veri: veri.remove(kelime)

            while '' in veri: veri.remove('')
            while ' ' in veri: veri.remove(' ')
            sonveri = []
            for kelime in veri:
                if len(kelime) > 2:
                    sonveri.append(kelime)

            if (len(sonveri) >= minlen) and (len(sonveri) <= maxlen):
                corpus.add_doc(sonveri)
                print(sonveri)
                alive.append(1)
            else:
                alive.append(0)
        self.datafrm[alivecolumn] = alive
        self.corpus = corpus
        self.saveCorpus(column)

    def saveCorpus(self, column):
        with open(self.saveDir + "\\ModelData\\" + column + ".corpus", "wb") as f:
            pickle.dump(self.corpus, f)

    def loadCorpus(self, column):
        self.col = column
        self.corpus = tp.utils.Corpus()
        with open(self.saveDir + "\\ModelData\\" + column + ".corpus", "rb") as f:
            self.corpus = pickle.load(f)

    def loadCoherence(self, column):

        try:
            with open(self.modelData + "/perplexity[" + column + "].data", 'rb') as f:
                self.perplexity = pickle.load(f)
        except:
            self.perplexity = pd.DataFrame(columns={"column", "k", "iteration", "score"})

        try:
            with open(self.modelData + "/c_v[" + column + "].data", 'rb') as f:
                self.c_v = pickle.load(f)
        except:
            self.c_v = pd.DataFrame(columns={"column", "k", "iteration", "score"})

        try:
            with open(self.modelData + "/_stat[" + column + "].data", 'rb') as f:
                self.stat = pickle.load(f)
        except:
            self.stat = [column, 2]

    def saveCoherence(self, column):

        try:
            with open(self.modelData + "/perplexity[" + column + "].data", 'wb') as f:
                pickle.dump(self.perplexity, f)
        except:
            raise FileNotFoundError("Dosya yazılamıyor")

        try:
            with open(self.modelData + "/c_v[" + column + "].data", 'wb') as f:
                pickle.dump(self.c_v, f)
        except:
            raise FileNotFoundError("Dosya yazılamıyor")

        try:
            with open(self.modelData + "/_stat[" + column + "].data", 'wb') as f:
                pickle.dump(self.stat, f)
        except:
            raise FileNotFoundError("Dosya yazılamıyor")

    def Model(self, k, tw=tp.TermWeight.PMI, seed=9999, min_df=10, alpha=False, eta=False):
        if (alpha == False): alpha = 50 / k

        self.mdl = tp.LDAModel(tw=tw, k=k, seed=seed, min_df=min_df, corpus=self.corpus, alpha=alpha)

        self.mdl.train(0, workers=self.cpucores, parallel=tp.ParallelScheme.PARTITION)

        print('Num docs:{}, Num Vocabs:{}, Total Words:{}'.format(
            len(self.mdl.docs), len(self.mdl.used_vocabs), self.mdl.num_words
        ))
        if eta == False:
            new_eta = 200 / len(self.mdl.used_vocabs)
        else:
            new_eta = eta

        self.mdl = tp.LDAModel(tw=tw, k=k, seed=seed, min_df=min_df, corpus=self.corpus, alpha=50 / k, eta=new_eta)

    def autoCoherence(self, column, tw="PMI", start=2, finish=100, iteration=500):
        if tw == "PMI":
            tw = tp.TermWeight.PMI
        elif tw == "IDF":
            tw = tp.TermWeight.IDF
        else:
            tw = tp.TermWeight.ONE

        if 'corpus' not in globals() or self.col != column:
            self.loadCorpus(column)

        self.loadCoherence(column)

        if self.stat[1] > start:
            start = self.stat[1]

        if start >= finish:
            print(column + " hesaplamaları bitmiş!!!")
            return

        for k in range(start, finish + 1):
            self.Model(k, tw=tw)
            for i in range(100, iteration + 1, 100):
                self.mdl.train(100, workers=self.cpucores, parallel=tp.ParallelScheme.PARTITION)
                self.perplexity = self.perplexity.append(
                    {"column": column, "k": k, "iteration": i, "score": self.mdl.perplexity}, ignore_index=True)

            coh = tp.coherence.Coherence(self.mdl, coherence="c_v")
            average_coherence = coh.get_score()
            self.c_v = self.c_v.append({"column": column, "k": k, "iteration": i, "score": average_coherence},
                                       ignore_index=True)
            print("Konu:{},C_V:{}".format(k, average_coherence))
            print("Konu:{},Perplexity:{}".format(k, self.mdl.perplexity))
            self.stat = [column, k]
            print(self.stat)
            self.saveCoherence(column)

    def saveLDAModel(self, column):
        self.mdl.save(self.modelData + column + ".model")

    def loadLDAModel(self, column):
        self.mdl = tp.LDAModel.load(self.modelData + column + ".model")

    def LDAModel(self, column, k, tw="PMI", iteration=2000, alpha=False, eta=False, save=True):
        if tw == "PMI":
            tw = tp.TermWeight.PMI
        elif tw == "IDF":
            tw = tp.TermWeight.IDF
        else:
            tw = tp.TermWeight.ONE

        t = time.time()
        print("Start:{}".format(t))
        if 'corpus' not in globals() or self.col != column:
            self.loadCorpus(column)

        self.Model(k, tw=tw, alpha=alpha, eta=eta)
        self.mdl.train(iteration, workers=self.cpucores, parallel=tp.ParallelScheme.PARTITION)
        print("Perplexity", self.mdl.perplexity)
        coh = tp.coherence.Coherence(self.mdl, coherence="c_v")
        average_coherence = coh.get_score()
        print("Konu:{},C_V:{}".format(k, average_coherence))
        print("Konu:{},Perplexity:{}".format(k, self.mdl.perplexity))
        print('Num docs:{}, Num Vocabs:{}, Total Words:{}'.format(
            len(self.mdl.docs), len(self.mdl.used_vocabs), self.mdl.num_words
        ))
        if save == True:
            self.saveLDAModel(column)
        tf = time.time()
        print("Finish:{}".format(tf))
        print("Elapsed: {}".format(tf - t))

    def ldavis(self, column=False):
        if column != False:
            self.loadLDAModel(column)

        import pyLDAvis
        topic_term_dists = np.stack([self.mdl.get_topic_word_dist(k) for k in range(self.mdl.k)])
        doc_topic_dists = np.stack([doc.get_topic_dist() for doc in self.mdl.docs])
        doc_lengths = np.array([len(doc.words) for doc in self.mdl.docs])
        vocab = list(self.mdl.used_vocabs)
        term_frequency = self.mdl.used_vocab_freq

        prepared_data = pyLDAvis.prepare(
            topic_term_dists,
            doc_topic_dists,
            doc_lengths,
            vocab,
            term_frequency,
            sort_topics=False,
            start_index=0,
            plot_opts=True
        )
        pyLDAvis.save_html(prepared_data, self.modelData + column + "pyLDAvis.html")

    def graphMage(self, column, start=2, finish=100, iteration=False, save=False):
        import seaborn as sns
        import matplotlib.pyplot as plt
        sns.set_style("white")
        sns.set_palette("husl")
        self.loadCoherence(column)
        pmax = max(self.perplexity["score"])
        pmin = min(self.perplexity["score"])
        perp = pd.DataFrame(columns={"tur", "k", "score"})
        for key, row in self.perplexity.iterrows():
            if row["k"] >= start and row["k"] <= finish:
                if iteration == False or row["iteration"] == iteration:
                    print(row)
                    pdeg = 1 - ((row["score"] - pmin) / (pmax - pmin))
                    perp = perp.append({"tur": "Perplexity", "k": row["k"], "score": pdeg}, ignore_index=True)
        print("Populated Perplexity")
        for key, row in self.c_v.iterrows():
            if row["k"] >= start and row["k"] <= finish:
                perp = perp.append({"tur": "C_v", "k": row["k"], "score": row["score"]}, ignore_index=True)
        ax = sns.lineplot(x="k", y="score", data=perp,

                          legend="brief",
                          hue="tur",
                          style="tur"
                          ).set_title(column + " Ölçümler")

        plt.show()

    def infer(self, column, ingore=[]):
        if column != False:
            self.loadLDAModel(column)
        area = "infer_" + column
        self.datafrm[area] = object()
        infering = list()
        for key, row in self.datafrm.iterrows():
            line = row[column]
            if row['alive_' + column] == 1:
                try:
                    doc_inst = self.mdl.make_doc(line)
                    topic_dist, ll = self.mdl.infer(doc_inst)
                    td = {}
                    i = 0
                    for k in topic_dist:
                        td[i] = k
                        i += 1
                    if len(ingore) > 0:
                        for ing in ingore:
                            del td[ing]
                    topic = max(td, key=td.get)
                    print(line, topic)
                except:
                    topic = -1
                infering.append(topic)
            else:
                infering.append(-1)
        print(infering)
        self.datafrm[area] = infering

    def createDTCorpus(self, column, timecolumn, time_start=False, time_finish=False, minlen=0, maxlen=99999,
                       compare=False, stops=False, clean=False, df=False):
        self.col = column
        alivecolumn = "alive_" + column
        self.datafrm[alivecolumn] = object()
        documentfreq = self.documentf(self.datafrm[column])
        cikarilan = 0

        if (stops == False):
            stops = []

        corpus = tp.utils.Corpus(stopwords=stops)
        alive = list()
        for key, line in self.datafrm.iterrows():
            veri = line[column]

            if df != False and documentfreq["_".join(line[column])] > df:
                cikarilan += 1
                veri = list()

            if compare != False and np.array_equal(line[column], line[compare]):
                veri = list()
                cikarilan += 1

            if compare != False and line[compare] == ['']:
                print(line[column], line[compare])
                veri = list()
                cikarilan += 1

            if clean != False:
                temizleveri = set()
                for tealan in clean:
                    for kelime in tealan:
                        temizleveri.add(kelime)
                for kelime in temizleveri:
                    while kelime in veri: veri.remove(kelime)

            while '' in veri: veri.remove('')
            while ' ' in veri: veri.remove(' ')
            sonveri = []
            for kelime in veri:
                if len(kelime) > 2:
                    sonveri.append(kelime)

            if (len(sonveri) >= minlen) and (len(sonveri) <= maxlen):
                if (time_start == False or line[timecolumn] >= time_start) and (
                        time_finish == False or line[timecolumn] <= time_finish):
                    corpus.add_doc(words=sonveri, timepoint=line[timecolumn])
                    print(sonveri)
                    alive.append(1)
            else:
                alive.append(0)
        self.datafrm[alivecolumn] = alive
        self.dtcorpus = corpus
        self.saveDTCorpus(column)

    def DTModel(self, column, k, t, tw="PMI", iteration=2000, alpha=False, eta=False, save=True):
        if tw == "PMI":
            tw = tp.TermWeight.PMI
        elif tw == "IDF":
            tw = tp.TermWeight.IDF
        else:
            tw = tp.TermWeight.ONE

        t = time.time()
        print("Start:{}".format(t))
        if 'corpus' not in globals() or self.col != column:
            self.loadDTCorpus(column)

        self.DTModel(k=k, t=t, tw=tw, corpus=self.dtcorpus)
        self.mdl.train(iteration, workers=self.cpucores, parallel=tp.ParallelScheme.PARTITION)
        print("Perplexity", self.mdl.perplexity)
        coh = tp.coherence.Coherence(self.mdl, coherence="c_v")
        average_coherence = coh.get_score()
        print("Konu:{},C_V:{}".format(k, average_coherence))
        print("Konu:{},Perplexity:{}".format(k, self.mdl.perplexity))
        print('Num docs:{}, Num Vocabs:{}, Total Words:{}'.format(
            len(self.mdl.docs), len(self.mdl.used_vocabs), self.mdl.num_words
        ))
        if save == True:
            self.saveDTModel(column)
        tf = time.time()
        print("Finish:{}".format(tf))
        print("Elapsed: {}".format(tf - t))

    def saveDTCorpus(self, column):
        with open(self.saveDir + "\\ModelData\\" + column + ".DTcorpus", "wb") as f:
            pickle.dump(self.dtcorpus, f)

    def loadDTCorpus(self, column):
        self.col = column
        self.dtcorpus = tp.utils.Corpus()
        with open(self.saveDir + "\\ModelData\\" + column + ".DTcorpus", "rb") as f:
            self.dtcorpus = pickle.load(f)

    def saveDTModel(self, column):
        self.mdl.save(self.modelData + column + ".DTmodel")

    def loadDTModel(self, column):
        self.mdl = tp.LDAModel.load(self.modelData + column + ".DTmodel")
