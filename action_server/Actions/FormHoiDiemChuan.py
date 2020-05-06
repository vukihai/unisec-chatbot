from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from .UnisecLogger import UnisecLogger
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormHoiDiemChuan(UnisecForm):
   def name(self):
      return "form_hoi_diem_chuan"

   @staticmethod
   def required_validation_slot():
       return ['entity_truong_dai_hoc', 'entity_nganh_hoc', 'entity_nam']
   
   def required_slots(self, tracker):
      # if tracker.get_slot('entity_truong_dai_hoc') == None:
      #    return ['entity_truong_dai_hoc']
      return ['entity_truong_dai_hoc']

   def before_slot_fill(self, dispatcher, tracker, domain):
      # utter universities fited with current slot.
      truong_dai_hoc = tracker.get_slot('entity_truong_dai_hoc')
      nganh_hoc = tracker.get_slot('entity_nganh_hoc')
      if truong_dai_hoc == None and nganh_hoc == None:
          return []
      res = self.getResponse()
      dispatcher.utter_message(res[0])
      if len(res[1]) >1:
         dispatcher.utter_message(json_message={"data":{"table" : res[1]}})
      return []

   def submit(self, dispatcher, tracker, domain):
      # reset all slot if needed
      # add utter_chao_mung
      # finish form
      return [AllSlotsReset()]

   ##
   ## query db. 
   ##
   def getResponse(self):
      try:
         truong_dai_hoc = self.get_slot('entity_truong_dai_hoc')[0]
         truong_dai_hoc_validated =  self.get_slot('entity_truong_dai_hoc_validated')[0]
      except:
         truong_dai_hoc = None
         truong_dai_hoc_validated = None
      try:
         nganh_hoc =  self.get_slot('entity_nganh_hoc')[0]
         nganh_hoc_validated =  self.get_slot('entity_nganh_hoc_validated')[0]
      except:
         nganh_hoc = None
         nganh_hoc_validated = None
      try:
         nam_validated =  self.get_slot('entity_nam_validated')[0]
      except:
         nam_validated = '2019'
      mes = "Sau đây là điểm chuẩn"
      query = {}
      if truong_dai_hoc_validated != None:
          query['university_id'] =  re.compile('^' + truong_dai_hoc_validated + '$', re.IGNORECASE)
          mes += " trường " + truong_dai_hoc
          UnisecLogger.log_university(truong_dai_hoc_validated, truong_dai_hoc)
      if nganh_hoc_validated != None:
          query['major_group_id'] = re.compile('^' + nganh_hoc_validated + '$', re.IGNORECASE)
          mes += " ngành " + nganh_hoc
          UnisecLogger.log_major(nganh_hoc_validated, nganh_hoc)

      if (truong_dai_hoc_validated != None and nganh_hoc_validated != None):
         # query['year'] = str(nam_validated)
         # mes += " năm " + str(nam_validated)
         data = db.admission_scores.find(query)
         ret = []
         ret.append(["năm", "trường", "ngành học", "điểm", "tổ hợp môn"])
         for entry in data:
            try:
               ret.append([entry['year'],entry['university'], entry['major_name'],entry['score'], entry['combine']])
            except:
               print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
      else:
         query['year'] = int(nam_validated)
         mes += " năm " + str(nam_validated)
         data = db.admission_scores.find(query)
         ret = []
         ret.append(["trường", "ngành học", "điểm", "tổ hợp môn"])
         for entry in data:
            try:
               ret.append([entry['university'], entry['major_name'],entry['score'], entry['combine']])
            except:
               print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
      print(query)
      if len(ret) == 1:
         mes = "Tiếc quá, tôi không tìm thấy thông tin điểm chuẩn"
      return (mes, ret)
