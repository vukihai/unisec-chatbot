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
       return ['entity_truong_dai_hoc']

   def required_slots(self, tracker):
      return ['entity_truong_dai_hoc']
   

   def before_slot_fill(self, dispatcher, tracker, domain): 
      return []

   def submit(self, dispatcher, tracker, domain):
      truong_dai_hoc = self.get_slot('entity_truong_dai_hoc')
      truong_dai_hoc_validated =  self.get_slot('entity_truong_dai_hoc_validated')
      dispatcher.utter_message("Mã trường của " + truong_dai_hoc + " là " + truong_dai_hoc_validated)
      return [AllSlotsReset()]

      



