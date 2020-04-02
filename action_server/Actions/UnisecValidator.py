import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
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
            print("vukihai: instantiated Unisec Validator")
            self.path = os.path.abspath(os.path.dirname(__file__))
            self.loadData()
            UnisecValidator.__instance = self

    # load & train data once time
    def loadData(self):
        ## university name
        self.uniDataframe = pd.read_csv(self.path + '/university_lookup.csv')
        self.uniVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.uniModel = self.uniVectorizer.fit_transform(self.uniDataframe.iloc[:,1])

        ## region
        self.regionDataframe = pd.read_csv(self.path + '/macro_region_lookup.csv')
        self.regionVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.regionModel = self.regionVectorizer.fit_transform(self.regionDataframe.iloc[:,1])

        ## majors
        self.majorDataframe = pd.read_csv(self.path + '/major_lookup.csv')
        self.majorVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.majorModel = self.majorVectorizer.fit_transform(self.majorDataframe.iloc[:,1])
        
    def validate_entity_diem(self, name):
        return (1, name, name)
    def validate_entity_gioi_tinh(self, name):
        return (1, name, name)
    def validate_entity_khoi_thi(self, name):
        return (1, name, name)
    def validate_entity_mon_hoc(self, name):
        return (1, name, name)
    def validate_entity_nam(self, name):
        return (1, name, name)
    def validate_entity_nganh_hoc(self, name):
        vec = self.majorVectorizer.transform([name])
        cos = cosine_similarity(self.majorModel, vec)
        index = cos.argmax()
        return (cos[index][0],self.majorDataframe.iloc[index,1],str(self.majorDataframe.iloc[index,2]))
    
    def validate_entity_so_thich(self, name):
        return (1, name, name)
    def validate_entity_tinh_thanh(self, name):
        return (1, name, name)
    def validate_entity_vung_mien(self, name):
        vec = self.regionVectorizer.transform([name])
        cos = cosine_similarity(self.regionModel, vec)
        index = cos.argmax()
        return (cos[index][0],self.regionDataframe.iloc[index,0],str(self.regionDataframe.iloc[index,1]))
        
    def validate_entity_ma_truong(self, name):
        return (1,name, name)
    def validate_entity_truong_dai_hoc(self, name):
        vec = self.uniVectorizer.transform([name])
        cos = cosine_similarity(self.uniModel, vec)
        index = cos.argmax()
        return (cos[index][0],self.uniDataframe.iloc[index,1],self.uniDataframe.iloc[index,2])
    
UnisecValidator.getInstance() # load & train data immediately after import
