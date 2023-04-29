import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv

import db_function as dbf
from vk_search import main

my_pynder = dbf.PYnder_DB(rebuild=True)

load_dotenv()

access_token = os.getenv('TOKEN')
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


# функция вызова первой клавиатуры
def first_keyboards(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0, keyboard=open('keyboards/first_button.json', "r", encoding="UTF-8").read())


# функция вызова втрой клавиатуры
def all_buttons(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0, keyboard=open('keyboards/all_buttons.json', "r", encoding="UTF-8").read())


def sender(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0)


# логика бота
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            my_msg = event.message
            if msg == 'старт':
                my_pynder.add_owner(str(id))
                all_buttons(id, main(str(id), None))
            elif msg == 'назад':
                # sender(id, 'че это?')
                main(id, msg)
            elif msg == 'дальше':
                main(id, msg)
            elif msg == 'добавить в избранное':
                for i in main(str(id), msg):
                    # print(i)
                    my_pynder.add_favorite(i, str(id))

            elif msg == 'удалить из избранного':
                pass
            elif msg == 'просмотреть избранное':
                pass
            elif len(msg) > 0:
                first_keyboards(id, 'Привет!Я бот для поиска новых знакомств!Нажми на кнопку Старт')