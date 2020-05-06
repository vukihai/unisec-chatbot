from rasa_sdk.events import SlotSet
from rasa_sdk import Action
class ActionChaoMung(Action):
    def name(self):
        return "action_chao_mung"

    def run(self,dispatcher, tracker, domain):
        data = []
        data.append({'img':"https://searchengineland.com/figz/wp-content/seloads/2017/12/compare-seo-ss-1920-800x450.jpg", 'name': 'chọn trường', 'payload':'chọn trường'})
        data.append({'img':"https://daihoc.fpt.edu.vn/media/2019/02/img20161006041230575.jpg", 'name': 'chọn ngành', 'payload':'chọn ngành'})
        data.append({'img':' img', 'name': 'điểm chuẩn', 'payload': 'điểm chuẩn'})
        data.append({'img':' img', 'name': 'thông tin tuyển sinh', 'payload': 'thông tin tuyển sinh'})
        data.append({'img':' img', 'name': 'mã trường', 'payload': 'mã trường'})
        data.append({'img':' img', 'name': 'mã ngành', 'payload': 'mã ngành'})
        data.append({'img':' img', 'name': 'xếp hạng', 'payload': 'xếp hạng'})
        dispatcher.utter_message(json_message={"data":{"slider" : data}})
        return []