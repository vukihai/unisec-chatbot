from rasa_sdk import Action
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered
import re
import pymongo
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]
class FormHoiDiemChuan(FormAction):
   def name(self):
      return "form_hoi_ten_truong"
   @staticmethod
   def required_slots(tracker):
      return ["entity_ma_truong"]

   def submit(self, dispatcher, tracker, domain):
      ma_truong = tracker.get_slot("entity_ma_truong")
      query = {'abbreviation': re.compile('^' + ma_truong + '$', re.IGNORECASE)}
      data = db.universities.find(query)
      ret = []
      for entry in data:
        ret.append(entry['name'])
      if len(ret) != 1:
          dispatcher.utter_message('Rất tiếc, tôi không tìm thấy trường nào có mã là ' + ma_truong)
      else:
          dispatcher.utter_message('Mã ' + ma_truong + " là của trường " + ret[0])
      return [AllSlotsReset()]
      