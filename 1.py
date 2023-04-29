import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv
from random import randrange

load_dotenv()

vk_session = vk_api.VkApi(token=os.getenv('TOKEN'))
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def first_keyboards(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0,
                     keyboard=open('keyboards/first_button.json', "r", encoding="UTF-8").read())


def add_favorite(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0,
                     keyboard=open('keyboards/add_favorite.json', "r", encoding="UTF-8").read())


def write_msg(user_id, message, key):
    try:
      vk('messages.send', {'user_id': user_id, 'message': message, 'keyboard': key, 'random_id': random.randint(0, 100000000)})
    except Exception as ex:
      print("error (write_msg, {0}, {1}):".format(user_id, message), ex)

for event in longpoll.listen():
          if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            id = event.user_id
            msg = event.text.lower()
            if msg == "подписаться":
                write_msg(id, 'Подписались', keyboard2)