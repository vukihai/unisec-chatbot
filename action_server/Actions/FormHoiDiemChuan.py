from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
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
       return ['entity_truong_dai_hoc', 'entity_nganh_hoc']

   def required_slots(self, tracker):
      if tracker.get_slot('entity_truong_dai_hoc') == None:
         return ['entity_truong_dai_hoc']
      if tracker.get_slot('entity_nganh_hoc') == None:
         return ['entity_nganh_hoc']
      return []
   
   def before_slot_fill(self, dispatcher, tracker, domain):
      # utter universities fited with current slot.
      print("before slot fill called")
      truong_dai_hoc = tracker.get_slot('entity_truong_dai_hoc')
      nganh_hoc = tracker.get_slot('entity_nganh_hoc')
      if truong_dai_hoc == None and nganh_hoc == None:
          return []
      res = self.getResponse()
      dispatcher.utter_message(res[0])
      dispatcher.utter_message(json_message=res[1])
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
      truong_dai_hoc = self.get_slot('entity_truong_dai_hoc')
      truong_dai_hoc_validated =  self.get_slot('entity_truong_dai_hoc_validated')
      nganh_hoc =  self.get_slot('entity_nganh_hoc')
      nganh_hoc_validated =  self.get_slot('entity_nganh_hoc_validated')
      nam_validated =  self.get_slot('entity_nam_validated')
      if nam_validated == None:
        nam_validated = '2019'
      mes = "Điểm chuẩn"
      query = {}
      if truong_dai_hoc_validated != None:
          query['university_id'] =  re.compile('^' + truong_dai_hoc_validated + '$', re.IGNORECASE)
          mes += " trường " + truong_dai_hoc
      if nganh_hoc != None:
          query['major_name'] = re.compile('^' + nganh_hoc + '$', re.IGNORECASE)
          mes += " ngành " + nganh_hoc
      query['year'] = str(nam_validated)
      mes += " năm " + str(nam_validated)
      print(query)
      data = db.admission_scores.find(query)
      ret = []
      for entry in data:
          try:
            ret.append([entry['university'], entry['major_name'],entry['score'], entry['combine']])
          except:
            print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
      print(ret)
      return (mes, ret)

      
      


