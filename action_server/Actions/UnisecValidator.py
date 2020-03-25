import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class UnisecValidator:
    #impliment singleton
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if UnisecValidator.__instance == None:
            UnisecValidator()
        return UnisecValidator.__instance
    def __init__(self):
        if UnisecValidator.__instance != None:
            raise Exception("This class is a singleton!")
        else:  
            self.loadData()
            UnisecValidator.__instance = self
    # load & train data once
    def loadData(self):
        self.uniDataframe = pd.read_csv('university_lookup.csv')
        print(self.uniDataframe)
        self.uniVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.uniModel = self.uniVectorizer.fit_transform(self.uniDataframe.iloc[:,1])

    # validate university name. => tuble (%, name)
    def validate_uni(self, name):
        name = name.lower()
        vec = self.uniVectorizer.transform([name])
        cos = cosine_similarity(self.uniModel, vec)
        index = cos.argmax()
        return (cos[index],self.uniDataframe.iloc[index,1])
        #print(index)
    

#validator = UnisecValidator.getInstance()
#print(validator.validate_uni("đại học công nghiệp hn"))