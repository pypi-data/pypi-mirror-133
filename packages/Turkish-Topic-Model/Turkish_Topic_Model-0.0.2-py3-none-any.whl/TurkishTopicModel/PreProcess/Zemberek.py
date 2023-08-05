import jpype as jp
import locale
import logging
import warnings
import sys
from os.path import join
import os


class Zemberek:
    passTypes = {"Word",
                 "WordAlphanumerical",
                 "WordWithSymbol",
                 "Abbreviation",
                 "AbbreviationWithDots",
                 "Number",
                 "PercentNumeral",
                 "RomanNumeral"
                 "Time",
                 "Date",
                 "URL",
                 "Email",
                 "HashTag",
                 "Mention",
                 "MetaTag",
                 "Emoji",
                 "Emoticon"}

    def __init__(self):
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
        if not sys.warnoptions:
            warnings.simplefilter("ignore")
        locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')
        self._path = os.path.dirname(os.path.abspath(__file__)) + "\\"
        self.initZemberek()

    def initZemberek(self):
        ZEMBEREK_PATH = self._path + 'zemberek-nlp\\zemberek-full.jar'

        if not jp.isJVMStarted():
            try:
                jp.startJVM(jp.getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))
            except:
                raise EnvironmentError("https://www.java.com/tr/ adresine gidip JVM'yi makinenize kurunuz.")
                raise FileNotFoundError("Zemberek Başlatılamadı. Lütfen JVM kurunuz.")
        self.ZemberekClass = {}
        self.zo = {}
        self.ltc()

    def loadZemberekClass(self, classes):
        if hasattr(classes, "__len__"):
            for c in classes:
                self.ZemberekClass[c] = jp.JClass(c)
        else:
            self.ZemberekClass[classes] = jp.JClass(classes)

    def ltc(self):
        self.loadZemberekClass({"zemberek.tokenization.TurkishTokenizer",
                                "zemberek.tokenization.TurkishSentenceExtractor",
                                "zemberek.tokenization.Token",
                                "zemberek.tokenization.antlr.TurkishLexer",
                                "zemberek.normalization.TurkishSpellChecker",
                                "zemberek.morphology.TurkishMorphology"})

        self.morph = self.ZemberekClass['zemberek.morphology.TurkishMorphology'].createWithDefaults()
        self.spell = self.ZemberekClass['zemberek.normalization.TurkishSpellChecker'](self.morph)

        self.tokenizer = self.ZemberekClass['zemberek.tokenization.TurkishTokenizer'].ALL;
        self.sentenceextractor = self.ZemberekClass['zemberek.tokenization.TurkishSentenceExtractor'].DEFAULT
        self.token = self.ZemberekClass['zemberek.tokenization.Token']
        self.TurkishLexer = self.ZemberekClass['zemberek.tokenization.Token']
        tok = self.tokenizer.tokenize("Test")
        self.texttype = tok[0].getType()

    def TurkishTextToken(self, text):
        t = list()
        if type(text) is str:
            tokens = self.tokenizer.tokenize(text)
            for token in tokens:
                if token.getType().toString() in self.passTypes:
                    t.append(str(token.getText()))
        else:
            t.append("")
        return t

    def TurkishSentences(self, text, method=1):
        t = list()
        if type(text) is str:
            if method == 1:
                tokens = self.sentenceextractor.fromParagraph(text)
            else:
                tokens = self.sentenceextractor.fromDocument(text)
            for token in tokens:
                t.append(str(token))
        else:
            t.append("")
        return t

    def TurkishTokens(self, text):
        t = list()
        if type(text) is str:
            tokens = self.tokenizer.tokenize(text)
            for token in tokens:
                t.append([token.getText(), token.getType().toString()])
        else:
            t.append("")
        return t

    def TurkishNormalizer(self, string):
        Paths: jp.JClass = jp.JClass('java.nio.file.Paths')
        if not 'zemberek.morphology.TurkishMorphology' in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.morphology.TurkishMorphology"})
            self.morph = self.ZemberekClass['zemberek.morphology.TurkishMorphology']

        if not 'zemberek.normalization.TurkishSentenceNormalizer' in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.normalization.TurkishSentenceNormalizer"})
            norm = self.ZemberekClass['zemberek.normalization.TurkishSentenceNormalizer']
            self.normalizer = norm(
                self.morph.createWithDefaults(),
                Paths.get(
                    self._path + "zemberek-nlp\\data\\normalization"
                ),
                Paths.get(
                    join(self._path + "zemberek-nlp\\data\\lm\\lm.2gram.slm")
                )
            )

        if isinstance(string, list):
            string = " ".join(string)

        try:
            newstring = self.normalizer.normalize(jp.JString(string))
            newarray = self.TurkishTextToken(str(newstring))
            return newarray
        except:
            return [" "]

    def TurkishWordNormalizer(self, string):
        Paths: jp.JClass = jp.JClass('java.nio.file.Paths')
        if not 'zemberek.morphology.TurkishMorphology' in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.morphology.TurkishMorphology"})
            self.morph = self.ZemberekClass['zemberek.morphology.TurkishMorphology']
        if not "zemberek.normalization.TurkishSpellChecker" in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.normalization.TurkishSpellChecker"})
            self.spell = self.ZemberekClass['zemberek.normalization.TurkishSpellChecker'](self.morph)

        if not 'zemberek.normalization.TurkishSentenceNormalizer' in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.normalization.TurkishSentenceNormalizer"})
            norm = self.ZemberekClass['zemberek.normalization.TurkishSentenceNormalizer']
            self.normalizer = norm(
                self.morph.createWithDefaults(),
                Paths.get(
                    self._path + "zemberek-nlp\\data\\normalization"
                ),
                Paths.get(
                    join(self._path + "zemberek-nlp\\data\\lm\\lm.2gram.slm")
                )
            )

        if isinstance(string, str):
            strarray = string.split(" ")
        else:
            strarray = string

        newstring = []
        for token in strarray:
            if not self.spell.check(jp.JString(token)):
                try:
                    newstring.append(self.normalizer.normalize(jp.JString(token)))
                except:
                    pass
            else:
                newstring.append(token)

        return self.TurkishTextToken(str(newstring))

    def TurkishSpelling(self, text):
        if not "zemberek.morphology.TurkishMorphology" in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.morphology.TurkishMorphology"})
            self.morph = self.ZemberekClass['zemberek.morphology.TurkishMorphology'].createWithDefaults()
        if not "zemberek.normalization.TurkishSpellChecker" in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.normalization.TurkishSpellChecker"})
            self.spell = self.ZemberekClass['zemberek.normalization.TurkishSpellChecker'](self.morph)
        if isinstance(text, str):
            text = self.TurkishTextToken(text)
        suggestion = {}
        for word in text:
            c = [str(x) for x in self.spell.suggestForWord(word)]
            c = list(c)
            try:
                if word not in c:
                    suggestion[word] = c
                    suggestion[word].append(word)
                else:
                    suggestion[word] = [word]
            except:
                pass
        return suggestion

    def TurkishSpellingWithNormal(self, text):
        if not "zemberek.morphology.TurkishMorphology" in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.morphology.TurkishMorphology"})
            self.morph = self.ZemberekClass['zemberek.morphology.TurkishMorphology'].createWithDefaults()
        if not "zemberek.normalization.TurkishSpellChecker" in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.normalization.TurkishSpellChecker"})
            self.spell = self.ZemberekClass['zemberek.normalization.TurkishSpellChecker'](self.morph)
        if isinstance(text, str):
            text = self.TurkishTextToken(text)
        suggestion = {}
        for word in text:
            c = self.spell.suggestForWord(word)
            normal = self.TurkishNormalizer(word)
            c = list(c)
            try:
                if word not in c:
                    suggestion[word] = c
                    suggestion[word].append(word)
                    suggestion[word] += normal
                else:
                    suggestion[word] = [word]
                    if word != normal[0]:
                        suggestion[word] += normal
            except:
                pass

        return suggestion

    def Morphology(self, text, type="lemma", length="max"):
        if not "zemberek.morphology.TurkishMorphology" in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.morphology.TurkishMorphology"})
            self.morph = self.ZemberekClass['zemberek.morphology.TurkishMorphology'].createWithDefaults()
        if isinstance(text, str):
            text = self.TurkishTextToken(text)
        roots = {}
        suggestion = {}
        for word in text:
            root = []
            try:
                results = self.morph.analyze(word)
                if results.getAnalysisResults():
                    result = list(results.getAnalysisResults())

                    if type == "lemma":
                        [[root.append(l) for l in list(n.getLemmas())] for n in result]
                    elif type == "stem":
                        [[root.append(l) for l in list(n.getStems())] for n in result]
                    elif type == "root":
                        root.append(result[0].getDictionaryItem().root)
            except:
                pass

            if len(root) == 0:
                root = [word]

            if length == "max":
                suggest = max(root)
            elif length == "min":
                suggest = min(root)
            roots[word] = str(root)

            suggestion[word] = str(suggest)
        print(suggestion)
        return suggestion

    def TurkishNER(self, text):
        if isinstance(text, list):
            text = " ".join(text)

        trainPath = self._path + "zemberek-nlp\\data\\ner\\ne-enamex.train.txt"
        testPath = self._path + "zemberek-nlp\\data\\ner\\ne-enamex.test.txt"
        modelRoot = self._path + "zemberek-nlp\\test-model\\model-compressed"

        if not "zemberek.morphology.TurkishMorphology" in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.morphology.TurkishMorphology"})
            self.morph = self.ZemberekClass['zemberek.morphology.TurkishMorphology'].createWithDefaults()

        if not "zemberek.ner.PerceptronNer" in self.ZemberekClass:
            self.loadZemberekClass({"zemberek.ner.PerceptronNer"})
            self.loadZemberekClass({"zemberek.ner.NerDataSet"})
            self.loadZemberekClass({"java.nio.file.Path"})
            self.loadZemberekClass({"java.nio.file.Paths"})

            Paths = self.ZemberekClass['java.nio.file.Paths']
            self.xpath = Paths.get(modelRoot)
            self.morph = self.ZemberekClass['zemberek.morphology.TurkishMorphology'].createWithDefaults()
            self.ner = self.ZemberekClass['zemberek.ner.PerceptronNer'].loadModel(self.xpath, self.morph)

        try:
            analysis = self.ner.findNamedEntities(jp.JString(text))
            namedEntities = analysis.getAllEntities()
            entities = []
            if len(namedEntities) > 0:

                for entity in namedEntities:
                    ent = str(entity.toString())
                    ent = ent.replace("[", "")
                    ent = ent.replace("]", "")
                    ent = ent.split(" ")
                    entities.append([ent[0], ent[1:]])
        except:
            entities = ["OUT", [""]]
        return entities
