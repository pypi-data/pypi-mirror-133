import TurkishTopicModel.PreProcess as PreProcess
import TurkishTopicModel.TopicModel.Main as TopicModel

PreProcess = PreProcess.Main
Data = PreProcess.Data
TopicModel = TopicModel.Main()


def transferData():
    TopicModel.datafrm = PreProcess.Data.datafrm
