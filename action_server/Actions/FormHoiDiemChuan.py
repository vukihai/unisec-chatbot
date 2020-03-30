from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormHoiDiemChuan(UnisecForm):
   def name(self):
      return "form_hoi_diem_chuan"

   def required_slots(self, tracker):
      if tracker.get_slot('entity_truong_dai_hoc') == None:
         return ['entity_truong_dai_hoc']
      if tracker.get_slot('entity_nganh_hoc') == None:
         return ['entity_nganh_hoc']

   def before_slot_fill(self, dispatcher, tracker, domain):
      # utter universities fited with current slot.
      print("before slot fill")
      truong_dai_hoc = tracker.get_slot('entity_truong_dai_hoc')
      nganh_hoc = tracker.get_slot('entity_nganh_hoc')
      if truong_dai_hoc == None and nganh_hoc == None:
          return []
      res = self.getResponse(tracker)
      dispatcher.utter_message(res[0])
      dispatcher.utter_message(json_message=res[1])
      print(res[1])
      return []

   def validate_entity_truong_dai_hoc(self, value, dispatcher, tracker, domain):
       print("validate truong dai hoc")
       print(value)
       val = UnisecValidator.getInstance().validate_uni(value[0])
       print(val)
       if val[0] > 0.55:
           return {'entity_truong_dai_hoc': val[1], 'entity_ma_truong': val[2]}
       else:
           return {'entity_truong_dai_hoc': None, 'entity_ma_truong': None}

   def validate_entity_nganh_hoc(self, value, dispatcher, tracker, domain):
       val = UnisecValidator.getInstance().validate_major(value)
       if val[0] > 0.35:
           return {'entity_nganh_hoc': val[1]}
       else:
           return {'entity_nganh_hoc': None}   

   def submit(self, dispatcher, tracker, domain):
      # reset all slot if needed
      # add utter_chao_mung
      # finish form
      return [AllSlotsReset()]

   ##
   ## query db. 
   ##
   def getResponse(self, tracker):
      truong_dai_hoc = tracker.get_slot('entity_truong_dai_hoc')
      nganh_hoc = tracker.get_slot('entity_nganh_hoc')
      nam = tracker.get_slot('entity_nam')
      if nam == None:
          nam = 2019
      
      mes = "Điểm chuẩn"
      query = {}
      if truong_dai_hoc != None:
          query['uni'] =  re.compile('^' + truong_dai_hoc + '$', re.IGNORECASE)
          mes += " trường " + truong_dai_hoc
      if nganh_hoc != None:
          query['major_name'] = re.compile('^' + nganh_hoc + '$', re.IGNORECASE)
          mes += " ngành " + nganh_hoc
      query['year'] = nam
      mes += " năm " + str(nam)
      
      data = db.admission_scores.find(query)
      ret = []
      for entry in data:
          try:
            ret.append([entry['university'], entry['major_name'],entry['score'], entry['combine']])
          except:
            print("vukihai:error while loading admision score: FormHoiDiemChuan - get response")
      return (mes, ret)

      
      



