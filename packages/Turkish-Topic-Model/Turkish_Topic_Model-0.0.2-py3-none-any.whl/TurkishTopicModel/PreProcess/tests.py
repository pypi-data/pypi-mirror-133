from TurkishTopicModel import PreProcess

sentence = """mustafa kemal atatürk 19 Mayıs 1919'da bandırma vapuru ile samsuna çıktı."""
print(PreProcess.Zemberek.TurkishNER(sentence))
morph = PreProcess.ITUNLPTools.ask("pipelineSSMorph", sentence)
morph = "<DOC> <DOC>+BDTag\n" + morph + "\n<DOC> <DOC>+EDTag"
print(PreProcess.ITUNLPTools.ask("ner", morph))
pipelineSSMorph
sentence = """Merhabaaaa bu gün çoooook heyecanliyim"""
print(PreProcess.Zemberek.TurkishNormalizer(sentence))
print(PreProcess.ITUNLPTools.ask("normalize", sentence))

import datetime

sentence = """Mustafa Kemal Atatürk 19 Mayıs 1919'da Bandırma Vapuru ile Samsun'a çıktı. 23 Nisan 1920'de Türkiye Büyük Millet Meclisi'ni kurdu"""
sentence = sentence.lower()
time = datetime.datetime.now()
for i in range(0, 1000):
    print(i, PreProcess.Zemberek.TurkishNER(sentence))
print(datetime.datetime.now() - time)

time = datetime.datetime.now()
for i in range(0, 10):
    print(i, PreProcess.ITUNLPTools.ask("ner", sentence))
print(datetime.datetime.now() - time)
