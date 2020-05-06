from rasa_sdk import Action
from .UnisecForm import UnisecForm
from .UnisecValidator import UnisecValidator
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered, FollowupAction
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormHoiKhungDaoTao(UnisecForm):
   def name(self):
      return "form_hoi_khung_dao_tao"

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
         res = []
         res.append(['môn học'])
         try:
            dt = db.major_info.find_one({'id': re.compile('^' + entity_nganh_hoc_validated + '$', re.IGNORECASE)})
            dt = dt['subjects']
            for i in dt:
                res.append([i])
         except:
             dispatcher.utter_message("không tìm thấy thông tin về khung đào tạo ngành " + entity_nganh_hoc)
             return [AllSlotsReset()]
         if len(res) == 1:
             dispatcher.utter_message("không tìm thấy thông tin về khung đào tạo ngành " + entity_nganh_hoc)
             return [AllSlotsReset()]
         dispatcher.utter_message("sau đây là khung đào tạo chuẩn của " + entity_nganh_hoc)
         dispatcher.utter_message("Tuy nhiên, một số trường có thể có những điều chỉnh so với khung đào tạo này.")
         dispatcher.utter_message(json_message={"data":{"table" : res}})
      return [AllSlotsReset()]
      

      



