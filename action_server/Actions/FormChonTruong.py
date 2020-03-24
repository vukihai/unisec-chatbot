from rasa_sdk import Action
from .UnisecForm import UnisecForm
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered

class FormChonTruong(UnisecForm):
   def name(self):
      return "form_chon_truong"

   @staticmethod
   def required_slots(tracker):
      print("slot fill called")
      #vukihai: if response is detail enough
      # return []
      # else request more slot in order
      # do not request all slot at the same time
      if tracker.get_slot('entity_vung_mien') == None:
         return ['entity_vung_mien']
      if tracker.get_slot('entity_diem') == None:
         return ['entity_diem']
      if tracker.get_slot('entity_diem') == None:
         return ['entity_diem']
      

   def before_slot_fill(self, dispatcher, tracker, domain):
      # utter universities fited with current slot.
      dispatcher.utter_message("before form chọn trường active")
      return []

   def submit(self, dispatcher, tracker, domain):
      # reset all slot if needed
      # add utter_chao_mung
      # finish form
      dispatcher.utter_message("active form chọn trường")
      return []

   ##
   ## query db. 
   ##
   def getResponse(self, tracker):
      vung_mien = tracker.get_slot('entity_vung_mien')
      diem_thi = tracker.get_slot('entity_diem')

