import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv

import db_function as dbf
from vk_search import Vk

my_pynder = dbf.PYnder_DB(rebuild=True)

load_dotenv()

access_token = 'vk1.a.DgZYkbQunPH3tt2laq6yTrug7UXP_qZSY-rd9hn7yzM16rhv0pUR17TKeCR-35AlskBuo4wNYFhtNHXJj_JVa1ZBOSPBOiU9lAfIXy6MDgSKMH6e6VzHE6vu0-tILMneTopl6IstYB6d3A01powr38KXsFPTTwJIDhXWakU4F0dh5lu8D__youAwZ0cEQsdfbM8w_Fe19rDxNKPE3Al3pA'
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


# функция вызова первой клавиатуры
def first_keyboards(id_, text):
    vk.messages.send(user_id=id_, message=text, random_id=0, keyboard=open('keyboards/first_button.json', "r", encoding="UTF-8").read())


# функция вызова второй клавиатуры
def all_buttons(id_, text, images_list):
    vk.messages.send(user_id=id_, message=text, attachment=images_list, random_id=0, keyboard=open('keyboards/all_buttons.json', "r", encoding="UTF-8").read())


def sender(id_, text):
    vk.messages.send(user_id=id_, message=text, random_id=0)


# логика бота


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        index = 0
        try:
            if event.to_me:
                my_id = event.user_id
                vk_search = Vk(my_id)
                data = vk_search.get_final_data()
                msg = event.text.lower()
                my_msg = event.message

                if msg == 'старт':
                    sender(my_id, 'Секунду, ищу варианты для тебя')
                    my_pynder.add_owner(str(my_id))
                    data = vk_search.get_final_data()
                    user_text, user_photo = vk_search.search_favorite(index, data, access_token)
                    all_buttons(my_id, user_text, user_photo)
                    continue
                if msg == 'назад':
                    index -= 1
                    print(index)
                    user_text, user_photo = vk_search.search_favorite(index, data, access_token)
                    all_buttons(my_id, user_text, user_photo)
                    continue
                if msg == 'дальше':
                    index += 1
                    print(index)
                    user_text, user_photo = vk_search.search_favorite(index, data, access_token)
                    all_buttons(my_id, user_text, user_photo)
                    continue
                if msg == 'добавить в избранное':
                    pass
                if msg == 'удалить из избранного':
                    pass

                if msg == 'просмотреть избранное':
                    pass

                if len(msg) > 0:
                    first_keyboards(my_id, 'Привет!Я бот для поиска новых знакомств!Нажми на кнопку Старт')

        except Exception as ex:
            print(ex)
