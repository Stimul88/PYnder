import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv

import db_function as dbf
from vk_search import Vk

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
        index = 0
        try:
            if event.to_me:
                id = event.user_id
                vk_search = Vk(id)
                data = vk_search.get_final_data()
                msg = event.text.lower()
                my_msg = event.message

                if msg == 'старт':
                    sender(id, 'Секунду, ищу варианты для тебя')
                    my_pynder.add_owner(str(id))
                    all_buttons(id, vk_search.search_favorite(index, data))
                    continue
                if msg == 'назад':
                    index -= 1
                    print(index)
                    all_buttons(id, vk_search.search_favorite(index, data))
                    continue
                if msg == 'дальше':
                    index += 1
                    print(index)
                    all_buttons(id, vk_search.search_favorite(index, data))
                    continue
                if msg == 'добавить в избранное':
                    pass
                if msg == 'удалить из избранного':
                    pass

                if msg == 'просмотреть избранное':
                    pass

                if len(msg) > 0:
                    first_keyboards(id, 'Привет!Я бот для поиска новых знакомств!Нажми на кнопку Старт')

        except Exception as ex:
            print(ex)
