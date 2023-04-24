import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from dotenv import load_dotenv
load_dotenv()

access_token = os.getenv('TOKEN')
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# функция вызова первой клавиатуры
def first_keyboards(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0, keyboard=open('keyboards/first_button.json', "r", encoding="UTF-8").read())

# функция вызова втрой клавиатуры
def second_keyboards(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0, keyboard=open('keyboards/buttons.json', "r", encoding="UTF-8").read())

# логика бота
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            if msg == 'поиск подходящих знакомств':
                second_keyboards(id, 'Пользуйся')
            elif msg == 'следующий':
                pass
            elif msg == 'добавить':
                pass
            elif msg == 'посмотреть список':
                pass
            elif len(msg) > 0:
                first_keyboards(id, 'Привет!Я бот для поиска новых знакомств!Нажми на кнопку')