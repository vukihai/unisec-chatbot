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
      return "form_hoi_xep_hang"

   @staticmethod
   def required_validation_slot():
       return ['entity_truong_dai_hoc']

   def required_slots(self, tracker):
      if tracker.get_slot('entity_truong_dai_hoc') == None:
         return ['entity_truong_dai_hoc']
      return []

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      try:
         truong_dai_hoc = self.get_slot('entity_truong_dai_hoc')[0]
         truong_dai_hoc_validated =  self.get_slot('entity_truong_dai_hoc_validated')[0]
      except:
         truong_dai_hoc = None
         truong_dai_hoc_validated = None
      
      if truong_dai_hoc_validated != None:
         ret = "Trường " + truong_dai_hoc
         dt = db.rank_uni.find_one({'id': re.compile('^' + truong_dai_hoc_validated + '$', re.IGNORECASE)})
         if dt != None:
             ret += " xếp thứ " + str(dt['rank']) + " theo xếp hạng của unirank"
         dt2 = db.rank_metric.find_one({'id': re.compile('^' + truong_dai_hoc_validated + '$', re.IGNORECASE)})
         if dt != None:
             if dt2 != None :
                 ret += " và"
             ret += " xếp thứ " + str(dt2['rank']) + " theo xếp hạng của webometrics"
      if dt == None and dt2 == None:
         ret = "Không tìm thấy thông tin thứ hạng trường " + truong_dai_hoc
      dispatcher.utter_message(ret)
      return [AllSlotsReset()]
      

      



