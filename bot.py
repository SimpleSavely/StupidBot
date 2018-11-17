import vk_api
import time
import json

token = "a61f9d92937c5616611b943ea7da3b30be41479dde662b2cf1883c95f57bde18b9190b45fbe0d4a91d7e0"

vk = vk_api.VkApi(token=token)

vk._auth_token()

def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

keyboard = {
    "one_time": False,
    "buttons": [
    [get_button(label="Создать напоминание", color="primary")],
    [get_button(label="Записать данные", color="primary")] ]}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

keyboard2 = {
    "one_time": False,
    "buttons": [
    [get_button(label="Учёба", color="primary")], 
    [get_button(label="Тренировка", color="primary")] ]}
keyboard2 = json.dumps(keyboard2, ensure_ascii=False).encode('utf-8')
keyboard2 = str(keyboard2.decode('utf-8'))

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            #i = 0 
            #vk.method("messages.send", {"peer_id": id, "message": "сек", "keyboard": keyboard})
            if body == "Создать напоминание":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Введите то, что мне нужно будет вам напомнить \n Формат записи 'мм-дд чч:мм/напоминание'"})
                print(id)
                i = 1
            elif body == "Записать данные":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Запишите то, что я должен запомнить"})
                i = 2
            else:
                if i == 1:
                    print(body)
                    vk.method("messages.send", {"peer_id": id, "message": "Хорошо, я напомню"})
                    i = 0
                elif i == 2:
                    vk.method("messages.send", {"peer_id": id, "message": "Окей, я запомнил"})
                    i = 0
                elif i == 0:
                    vk.method("messages.send", {"peer_id": id, "message": "Я не знаю такой команды"})

        time.sleep(0.5)
    except Exception as E:
        time.sleep(1)
