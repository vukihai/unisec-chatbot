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
      if len(res[1]) < 30:
         dispatcher.utter_message(json_message = {'table': res[1]})
      return []

   def submit(self, dispatcher, tracker, domain):
      # reset all slot if needed
      # add utter_chao_mung
      # finish form
      # dispatcher.utter_message("active form chọn trường")
      return [AllSlotsReset()]

   ##
   ## query db. 
   ##
   def getResponse(self, tracker):
      try:
         vung_mien = self.get_slot('entity_vung_mien_validated')[0]
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
         nganh_hoc_validated = self.get_slot('entity_nganh_hoc_validated')[0]
      except:
         nganh_hoc = None
         nganh_hoc_validated = None

      if vung_mien == None and tinh_thanh == None and diem_thi == None and khoi_thi == None and nganh_hoc == None:
         ret = db.universities.find({})
         mes = """Hiện cả nước có tất cả {} trường đại học.""".format(ret.count())
         list = []
         for entry in ret:
            list.append([entry['name']])
         return (mes, list)
      #gen query
      query = {}
      if tinh_thanh != None:
         query['province'] = re.compile('^' + tinh_thanh + '$', re.IGNORECASE)
      elif vung_mien != None:
         query['macro_region'] = re.compile('^' + vung_mien + '$', re.IGNORECASE)
      if diem_thi != None:
         if not "majors" in query:
            query["majors"] = {}
         if not '$elemMatch' in query["majors"]:
            query["majors"]['$elemMatch'] = {}
         query["majors"]['$elemMatch']['score'] =  { '$gte': float(diem_thi) - 2, '$lt': float(diem_thi) + 2 }
      if khoi_thi != None:
         if not "majors" in query:
            query["majors"] = {}
         if not '$elemMatch' in query["majors"]:
            query["majors"]['$elemMatch'] = {}
         if not 'major_combine' in query["majors"]['$elemMatch']:
            query["majors"]['$elemMatch']['major_combine'] = {}
         query["majors"]['$elemMatch']['major_combine']['$elemMatch'] =  re.compile('^' + khoi_thi + '$', re.IGNORECASE)
      if nganh_hoc != None:
         if not "majors" in query:
            query["majors"] = {}
         if not '$elemMatch' in query["majors"]:
            query["majors"]['$elemMatch'] = {}
         query["majors"]['$elemMatch']['major_group'] = nganh_hoc_validated      
      data = db.universities.find(query)
      # for test in data:
      #    print(test['name'])
      #gen answer
      ret = []
      ret.append(["trường", "ngành"])
      numOfUni = 0
      for uni in data:
         try:
            numOfUni += 1
            for major in uni['majors']:
                  if nganh_hoc is not None and major['major_group'] != nganh_hoc_validated:
                     print(uni['name'] + ' break 1')
                     continue
                  if diem_thi is not None and float(diem_thi)-2 > float(major['score']) and float(diem_thi) +2 < float(major['score']):
                     print(uni['name'] + ' break 2')
                     continue
                  if khoi_thi is not None and khoi_thi not in major['major_combine']:
                     print(uni['name'] + ' break 3')
                     continue
                  ret.append([uni['name'], major['major_name']])
         except:
            print("vukihai: error while create response: FormChonTruong > getResponse > has majorslot")          
      mes =""
      if tinh_thanh != None:
         mes += "Tại " + tinh_thanh + " có "
      elif vung_mien != None:
         mes += "Ở miền " + vung_mien + " có "
      else:
         mes += "Hiện cả nước có "
      mes += str(numOfUni) + " trường"
      if nganh_hoc is not None:
         mes += " có đào tạo ngành " + nganh_hoc
      if diem_thi is not None:
         mes += " phù hợp với mức điểm của bạn"
      print(query)

      if len(ret) == 1:
         mes = "Tôi không tìm được kết quả nào phù hợp với bạn cả :("
      return (mes, ret)

      



