from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class ActionHoiDiemChuan(Action):
   def name(self):
      return "action_hoi_diem_chuan"

   def run(self, dispatcher, tracker, domain):
      university = tracker.get_slot("ten_truong")
      major = tracker.get_slot("ten_nganh")
      year = tracker.get_slot("nam")
      res = db.admission_scores.find({'university': re.compile('^' + university + '$', re.IGNORECASE), 'year': 2019})

      mes = ""
      for entry in res:
         mes = mes + entry["major_name"] + entry["score"] + "\n"
      if len(mes) == 0:
         res = db.admission_scores.find({'university': re.compile('^' + university + '$', re.IGNORECASE), 'year': 2018})
         for entry in res:
            mes = mes + entry["major_name"] + entry["score"] + "\n"
               
      if len(mes) == 0:
         dispatcher.utter_message("Hiện chưa có thông tin điểm chuẩn " + university)
      else:
         dispatcher.utter_message("điểm chuẩn: "  + mes)
      #dispatcher.utter_message("hello")
      #return [SlotSet("diem_chuan",["vukihai"])]