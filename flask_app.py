import vk_api
import json
from mysql.connector import MySQLConnection, Error
from DB_read import read_ini
from datetime import datetime

token = ""

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
    [get_button(label="Записать данные", color="primary"),
     get_button(label="Вывести данные", color="primary")] ]}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

keyboard_data = {
    "one_time": False,
    "buttons": [
    [get_button(label="Тренировки", color="primary"),
    get_button(label="Feed", color="primary"),
     get_button(label="Другое", color="primary")] ]}

keyboard_data = json.dumps(keyboard_data, ensure_ascii=False).encode('utf-8')
keyboard_data = str(keyboard_data.decode('utf-8'))

while True:
    time = datetime.today()
    #print(time)
    ini = read_ini()
    conn = MySQLConnection(**ini)
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            if body == "Создать напоминание":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Введите то, что мне нужно будет вам напомнить \n Формат записи 'мм-дд чч:мм/напоминание'", "keyboard": keyboard})
                i = 1
            elif body == "Записать данные":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Запишите то, что я должен запомнить", "keyboard": keyboard})
                i = 2
            #elif body == "Вывести данные":
            #    vk.method("messages.send", {"peer_id": id,
            #                                "message": "Выберите тип данных", "keyboard": keyboard_data})
            else:
                if i == 1:
                    cur=conn.cursor()
                    cur.execute("INSERT INTO remember(Text) VALUES('"+str(body)+"')")
                    conn.commit()
                    conn.close()
                    #print(body)
                    vk.method("messages.send", {"peer_id": id, "message": "Хорошо, я напомню", "keyboard": keyboard})
                    i = 0
                elif i == 2:
                    cur=conn.cursor()
                    cur.execute("INSERT INTO info(Information) VALUES('"+str(body)+"')")
                    conn.commit()
                    conn.close()
                    vk.method("messages.send", {"peer_id": id, "message": "Окей, я запомнил", "keyboard": keyboard})
                    i = 0
                else:
                    vk.method("messages.send", {"peer_id": id, "message": "Я не знаю такой команды", "keyboard": keyboard})
                    
        else:
            ini = read_ini()
            conn = MySQLConnection(**ini)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM remember")
            rows = cursor.fetchall()
            rowcount = cursor.rowcount

            inf = []
            for row in rows:
                for info in row:
                    inf.append(info)
                    #print(info)

            for j in range(0,len(inf)):
                #print(inf[2*j-1])
                a = inf[j]
                a = a.split("/")
                now = datetime.now()
                year = now.year
                now = str(now)
                #print(a)
                now = now.split(':')
                now = now[0] + ':' + now [1]
                #print(now)
                date = a[0].split(" ")
                date1 = str(date[1])
                date2 = str(year) + '-' + str(date[0])
                dt = date2 + ' ' + date1
                #print(dt)
                print(a[1])
                if now == dt:
                    vk.method("messages.send", {"peer_id": id, "message": "Вы просили меня напомнить \n"+a[1], "keyboard": keyboard})
                    cur=conn.cursor()
                    cur.execute("DELETE FROM remember WHERE Text = '"+inf[j]+"'")
                    conn.commit()
                    conn.close()
                else:
                    pass

    except Exception as E:
        pass
        #print(E)
