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
        fname = self.uniVectorizer.get_feature_names()
        # print(fname[810])
        #print(self.uniModel)
        
        ## region
        self.regionDataframe = pd.read_csv(self.path + '/macro_region_lookup.csv')
        self.regionVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.regionModel = self.regionVectorizer.fit_transform(self.regionDataframe.iloc[:,1])

        ## majors
        self.majorDataframe = pd.read_csv(self.path + '/major_lookup.csv')
        self.majorVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.majorModel = self.majorVectorizer.fit_transform(self.majorDataframe.iloc[:,1])
        ## grades
        self.gradeDataframe = pd.read_csv(self.path + '/khoi_lookup.csv')
        self.gradeVectorizer = TfidfVectorizer(ngram_range=(1,1), analyzer='char')
        self.gradeModel = self.gradeVectorizer.fit_transform(self.gradeDataframe.iloc[:,1])
        ## subjects
        self.subjectDataframe = pd.read_csv(self.path + '/subject_lookup.csv')
        self.subjectVectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
        self.subjectModel = self.subjectVectorizer.fit_transform(self.subjectDataframe.iloc[:,1])
    def validate_entity_diem(self, name):
        return (1, name, name)
    def validate_entity_gioi_tinh(self, name):
        return (1, name, name)
    def validate_entity_khoi_thi(self, name):
        vec = self.gradeVectorizer.transform([name])
        cos = cosine_similarity(self.gradeModel, vec)
        index = cos.argmax()
        li = list(name)
        print(len(li))
        num = len(li)
        if num == 1:
            ch = name.upper() + "00"
            return ch
        if num == 2:
            #li = list(name)
            ch = li[0].upper() + "0" + li[1]
            return ch
        #li = list(name)
        ch = li[0].upper() + li[1] + li[2]
        return ch
    def validate_entity_mon_hoc(self, name):
        vec = self.subjectVectorizer.transform([name])
        cos = cosine_similarity(self.subjectModel, vec)
        index = cos.argmax()
        return (cos[index][0], self.subjectDataframe.iloc[index,1])
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
    def validate_entity_truong_dai_hoc(self, name):
        vec = self.uniVectorizer.transform([name])
        cos = cosine_similarity(self.uniModel, vec)
        index = cos.argmax()
        return (cos[index][0],self.uniDataframe.iloc[index,1],self.uniDataframe.iloc[index,2])
    
UnisecValidator.getInstance() # load & train data immediately after import
# UnisecValidator.getInstance().loadData()
# print(UnisecValidator.getInstance().validate_entity_nganh_hoc("y đa khoa y hà nội"))
# print(UnisecValidator.getInstance().validate_entity_truong_dai_hoc("đại công nghiệp hà"))
print(UnisecValidator.getInstance().validate_entity_khoi_thi("b3"))