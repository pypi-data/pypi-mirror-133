import requests
from .Config import dirs as dirs


class ITUNLPTools:
    tools = "ner", "morphanalyzer", "isturkish", "morphgenerator", "sentencesplitter", "tokenizer", "normalize", "deasciifier", "Vowelizer", "DepParserFormal", "DepParserNoisy", "spellcheck", "disambiguator", "pipelineFormal", "pipelineFormalwSentenceSplitter", "pipelineNoisy", "pipelineNoisywSentenceSplitter", "pipelineSSMorph"

    def __init__(self):
        pass

    def ask(self, tool, text):
        if (tool in self.tools) and len(text) > 0:
            rdata = {"tool": tool,
                     "input": text,
                     "token": dirs._itutoken}
            self.r = requests.get(url=dirs._itutools, params=rdata)
            text = self.r.text
        return text
