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
first_run = True
index = 0
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        try:
            if event.to_me:
                if first_run:
                    first_run = False
                    my_id = event.user_id
                    vk_search = Vk(my_id)
                    my_data = vk_search.get_final_data()
                    print(len(my_data))
                msg = event.text.lower()
                my_msg = event.message

                match msg:
                    case 'старт':
                        sender(my_id, 'Секунду, ищу варианты для тебя')
                        my_pynder.add_owner(str(my_id))
                        my_data = vk_search.get_final_data()
                        user_text, user_photo = vk_search.search_favorite(index, my_data)
                        all_buttons(my_id, user_text, user_photo)
                        # continue
                    case 'назад':
                        if index == 0:
                            sender(my_id, 'Это самая первая запись, предыдущих нет.\n')
                        else:
                            index -= 1
                            print(index)
                            user_text, user_photo = vk_search.search_favorite(index, my_data)
                            all_buttons(my_id, user_text, user_photo)
                            # continue
                    case 'дальше':
                        if index == len(my_data)-1:
                            # Тима, наверное здесь стоит сделать запрос новых записей если можно вытащить не первые 10,
                            # например, а вторые 10, потом третьи и т.д. (Саша)
                            sender(my_id, 'Это последняя запись, выбирай из того что есть.\n')
                        index += 1
                        print(index)
                        user_text, user_photo = vk_search.search_favorite(index, my_data)
                        all_buttons(my_id, user_text, user_photo)
                        # continue
                    case 'добавить в избранное':
                        my_pynder.add_favorite(my_data[index], my_id)
                    case 'удалить из избранного':
                        pass
                    case 'просмотреть избранное':
                        pass
                    case _:
                        if len(msg) > 0:
                            first_keyboards(my_id, 'Привет, я бот для поиска новых знакомств!\nНажми на кнопку Старт.\n')

        except Exception as ex:
            print(ex)
