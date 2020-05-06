from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormHoiThongTinNganh(UnisecForm):
   def name(self):
      return "form_hoi_thong_tin_nganh"

   @staticmethod
   def required_validation_slot():
       return ['entity_nganh_hoc']

   def required_slots(self, tracker):
      if tracker.get_slot('entity_nganh_hoc') == None:
         return ['entity_nganh_hoc']
      return []

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      try:
         entity_nganh_hoc = self.get_slot('entity_nganh_hoc')[0]
         entity_nganh_hoc_validated =  self.get_slot('entity_nganh_hoc_validated')[0]
      except:
         entity_nganh_hoc = None
         entity_nganh_hoc_validated = None
      
      if entity_nganh_hoc_validated != None:   
         res = ""
         try:
            dt = db.major_info.find_one({'id': re.compile('^' + entity_nganh_hoc_validated + '$', re.IGNORECASE)})
            res = dt['intro']
            dispatcher.utter_message("sau đây là giới thiệu ngành " + entity_nganh_hoc)
            dispatcher.utter_message(res)
         except:
             dispatcher.utter_message("không tìm thấy thông tin ngành " + entity_nganh_hoc)
    
      return [AllSlotsReset()]
      

      



