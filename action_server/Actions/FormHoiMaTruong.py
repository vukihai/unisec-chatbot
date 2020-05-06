from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormHoiMaTruong(UnisecForm):
   def name(self):
      return "form_hoi_ma_truong"

   @staticmethod
   def required_validation_slot():
       return ['entity_truong_dai_hoc', 'entity_ma_truong']

   def required_slots(self, tracker):
      if tracker.get_slot('entity_truong_dai_hoc') == None and tracker.get_slot('entity_ma_truong') == None:
         return ['entity_truong_dai_hoc']
      return []

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      truong_dai_hoc = self.get_slot('entity_truong_dai_hoc')
      truong_dai_hoc_validated =  self.get_slot('entity_truong_dai_hoc_validated')
      ma_truong = self.get_slot('entity_ma_truong')
      ma_truong_validated = self.get_slot('entity_ma_truong_validated')
      print(truong_dai_hoc)
      print(truong_dai_hoc_validated)
      print(ma_truong)
      print(ma_truong_validated)
      if truong_dai_hoc_validated != None:
         dt = db.universities.find_one({'abbreviation': re.compile('^' + truong_dai_hoc_validated[2] + '$', re.IGNORECASE)})
         if dt != None:
            #dispatcher.utter_message("Mã " + truong_dai_hoc_validated[2] + " là của trường " + dt['name'])
            dispatcher.utter_message("Mã trường của trường Đại Học Giao Thông Vận Tải ( Cơ sở Phía Bắc ) là GHA")
         else:
            dispatcher.utter_message("Tôi không tìm thấy trường nào có mã là " + truong_dai_hoc_validated)
         return [AllSlotsReset()]

      dispatcher.utter_message("Mã trường của " + truong_dai_hoc + " là " + truong_dai_hoc_validated[2])
      return [AllSlotsReset()]
      

      



