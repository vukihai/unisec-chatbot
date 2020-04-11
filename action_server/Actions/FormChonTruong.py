from rasa_sdk import Action
from .UnisecForm import UnisecForm
from rasa_sdk.events import SlotSet, AllSlotsReset, BotUttered
import pymongo
import re
client = pymongo.MongoClient("localhost", 27017)
db=client["unisec-db"]

class FormChonTruong(UnisecForm):
   def name(self):
      return "form_chon_truong"

   @staticmethod
   def required_validation_slot():
      return ['entity_vung_mien', 'entity_tinh_thanh', 'entity_diem', 'entity_khoi_thi', 'entity_nganh_hoc']

   def required_slots(self, tracker):
      print("slot fill called")
      if len(self.getResponse(tracker)[1]) < 10:
         return []
      #vukihai: if response is detail enough
      # return []
      # else request more slot in order
      # do not request all slot at the same time
      if tracker.get_slot('entity_vung_mien') == None and tracker.get_slot('entity_tinh_thanh') == None:
         return ['entity_vung_mien']
      if tracker.get_slot('entity_diem') == None:
         return ['entity_diem']
      if tracker.get_slot('entity_khoi_thi') == None:
         return ['entity_khoi_thi']
      if tracker.get_slot('entity_nganh_hoc') == None:
         return ['entity_nganh_hoc']
      return []
      

   def before_slot_fill(self, dispatcher, tracker, domain):
      # utter universities fited with current slot.
      res = self.getResponse(tracker)
      dispatcher.utter_message(res[0])
      dispatcher.utter_message(json_message = {'table': res[1]})
      return []

   def submit(self, dispatcher, tracker, domain):
      # reset all slot if needed
      # add utter_chao_mung
      # finish form
      dispatcher.utter_message("active form chọn trường")
      return [AllSlotsReset()]

   ##
   ## query db. 
   ##
   def getResponse(self, tracker):
      try:
         vung_mien = self.get_slot('entity_vung_mien')[0]
      except:
         vung_mien = None
      try:
         tinh_thanh = self.get_slot('entity_tinh_thanh')[0]
      except:
         tinh_thanh = None
      try:
         diem_thi = self.get_slot('entity_diem')[0]
      except:
         diem_thi = None
      try:
         khoi_thi = self.get_slot('entity_khoi_thi')[0]
      except:
         khoi_thi = None
      try:
         nganh_hoc = self.get_slot('entity_nganh_hoc')[0]
      except:
         nganh_hoc = None
      if vung_mien == None and tinh_thanh == None and diem_thi == None and khoi_thi == None and nganh_hoc == None:
         ret = db.universities.find({})
         mes = """Hiện cả nước có {} trường đại học.""".format(ret.count())
         list = []
         for uni in ret:
            try:
               list.append((uni["name"], uni["province"]))
            except:
               print("vukihai: error while create response: FormChonTruong > getResponse > no slot ")
         return (mes, list)
      #query
      query = {}
      if tinh_thanh != None:
         query['province'] = re.compile('^' + tinh_thanh + '$', re.IGNORECASE)
      elif vung_mien != None:
         query['macro_region'] = re.compile('^' + vung_mien + '$', re.IGNORECASE)
      if diem_thi != None:
         pass
      if khoi_thi != None:
         pass
      if nganh_hoc != None:
         query['majors'] = {'$elemMatch': {'major_name':re.compile('^' + nganh_hoc + '$', re.IGNORECASE)}}
      data = db.universities.find(query)
      ret = []
      if nganh_hoc != None:
         for uni in data:
            for major in uni['majors']:
               try:
                  ret.append((uni['name'], major['major_name']))
               except:
                  print("vukihai: error while create response: FormChonTruong > getResponse > has majorslot")
                 
      else:
         for uni in data:
            try:
               ret.append((uni['name'], uni['province']))
            except:
               print("vukihai: error while create response: FormChonTruong > getResponse > majorslot None")

      mes =""
      if tinh_thanh != None:
         mes += "Tại " + tinh_thanh + " có "
      elif vung_mien != None:
         mes += "Tại miền " + vung_mien + " có "
      else:
         mes += "Hiện cả nước có "
      mes += str(len(ret)) + " trường"
      return (mes, ret)

      



