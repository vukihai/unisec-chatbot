from pymongo import MongoClient
from pymongo import ASCENDING
import datetime
import requests
client = MongoClient("localhost", 27017)
db=client["unisec-db"]
log_collection = db.log
log_collection.create_index([("timestamp", ASCENDING)])  

class UnisecLogger():
    FORM_ACTIVATED = "form_activated"
    ENTITY_EXTRACTED = "entity_extracted"

    @staticmethod
    def log(type, target, value, message):
        """ Log to mongo """
        entry = {}
        entry['timestamp'] = datetime.datetime.utcnow()
        entry['type'] = type
        entry['target'] = target
        entry['value'] = value
        entry['message'] = message
        log_collection.insert_one(entry)
        data = {}
        print(entry)
    def log_intent(intent, value):
        url = "http://77c0975d.ngrok.io/intent/"+intent+"" 
        data = {"name":value}
        res = requests.put(url, json=data)
        print(res.url)
    def log_major(major, value):
        url = "http://77c0975d.ngrok.io/major/"+major+"/"
        data = {"major_name":major, "name":value}
        res = requests.put(url, json=data)
        print(res.url)
    def log_university(uni, value):
        url = "http://77c0975d.ngrok.io/university/"+uni+"/"
        data = {"university_name":uni, "name":value}
        res = requests.put(url, json=data)
        print(res.url)
# UnisecLogger.log(UnisecLogger.TYPE_INTENT_ACTIVATED, "intent_chon_truong", "chọn trường")
UnisecLogger.log_major("xay_dung","xây dựng")