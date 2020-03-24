from rasa_sdk import Action
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered
class FormChonTruong(FormAction):
   def name(self):
      return "form_chon_truong"

   @staticmethod
   def required_slots(tracker):
      if tracker.get_slot("entity_vung_mien") == None:
          print("test 1")
          return ['entity_vung_mien']
      else:
          print('test 2')
          
          return ['entity_diem']

   def submit(self, dispatcher, tracker, domain):
      dispatcher.utter_message("active form chọn trường")
      return []
