from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from .UnisecLogger import UnisecLogger
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormHoiDiaChiTruon(UnisecForm):
   def name(self):
      return "form_hoi_dia_chi_truong"

   @staticmethod
   def required_validation_slot():
       return ['entity_truong_dai_hoc']

   def required_slots(self, tracker):
      return ['entity_truong_dai_hoc']
   

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      try:
         truong_dai_hoc = self.get_slot('entity_truong_dai_hoc')[0]
         truong_dai_hoc_validated =  self.get_slot('entity_truong_dai_hoc_validated')[0]
      except:
         truong_dai_hoc = None
         truong_dai_hoc_validated =  None
      data = []
      if truong_dai_hoc_validated != None:
        data = db.universities.find({'abbreviation': re.compile('^' + truong_dai_hoc_validated + '$', re.IGNORECASE)})
      ret = []
      for entry in data:
          try:
              ret.append(entry['address'])
          except:
              pass
      if len(ret) != 1:
        dispatcher.utter_message("Tiếc quá, tôi không tìm thấy thông tin về địa chỉ trường " + truong_dai_hoc)
      else:
        dispatcher.utter_message("Địa chỉ trường "+ truong_dai_hoc + " là " + ret[0])

      return [AllSlotsReset()]

      



