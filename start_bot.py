import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import db_function as dbf
from vk_search import Vk
import configparser


def sender(user_id_, text):
    vk.messages.send(user_id=user_id_, message=text, random_id=0)


def first_keyboards(user_id_, text):
    vk.messages.send(
        user_id=user_id_,
        message=text,
        random_id=0,
        keyboard=open("keyboards/first_button.json", "r", encoding="UTF-8").read(),
    )


def favorite_buttons(user_id_, text, images_list):
    vk.messages.send(
        user_id=user_id_,
        message=text,
        attachment=images_list,
        random_id=0,
        keyboard=open("keyboards/favorite_buttons.json", "r", encoding="UTF-8").read(),
    )


def all_buttons(user_id_, text, images_list):
    vk.messages.send(
        user_id=user_id_,
        message=text,
        attachment=images_list,
        random_id=0,
        keyboard=open("keyboards/all_buttons.json", "r", encoding="UTF-8").read(),
    )


def settings_buttons(user_id_, text):
    vk.messages.send(
        user_id=user_id_,
        message=text,
        random_id=0,
        keyboard=open(
            "keyboards/setting_for_search_but.json", "r", encoding="UTF-8"
        ).read(),
    )


def start_button(user_id, index_m):
    my_pynder.add_owner(str(user_id))
    sender(user_id, "Секунду, ищу варианты для тебя.\n")
    data_m = vk_search.get_final_data()
    if len(data_m) == 0:
        sender(user_id, "Ничего не найдено.\n "
                        "Попробуй задать другие параметры поиска.\n")
        return None
    sender(user_id, f"Найдено вариантов: {len(data_m)}.")
    user_text, user_photo = vk_search.search_favorite(index_m, data_m)
    all_buttons(user_id, user_text, user_photo)
    return data_m


def search_back_button(user_id, data_m, index_m):
    if index_m == 0:
        sender(user_id, "Это самая первая запись, предыдущих нет.\n")
    else:
        index_m -= 1
        user_text, user_photo = vk_search.search_favorite(index_m, data_m)
        all_buttons(user_id, user_text, user_photo)
    return index_m


def search_forward_button(user_id, data_m, index_m):
    if index_m == len(data_m) - 1:
        # Тима, наверное здесь стоит сделать запрос новых записей если можно вытащить не первые 10,
        # например, а вторые 10, потом третьи и т.д. (Саша)
        sender(
            user_id,
            "Это последняя запись, выбирай из того что есть.\n",
        )
    else:
        index_m += 1
        user_text, user_photo = vk_search.search_favorite(index_m, data_m)
        all_buttons(user_id, user_text, user_photo)
    return index_m


def add_favorite_button(user_id, data_m, index_m):
    if my_pynder.add_favorite(data_m[index_m], str(user_id)):
        sender(user_id, "Добавлено.\n")
    else:
        sender(user_id, "Уже добавлено.\n")


def delete_favorite_button(user_id, data_m, index_m, data_f, index_f, mode_):
    if mode_ == 1:
        delete_result = my_pynder.delete_favorite(
            my_data[index_m]["vk_id"], str(user_id)
        )
    elif mode_ == 2:
        if len(data_f) == 0:
            delete_result = False
        else:
            delete_result = my_pynder.delete_favorite(
                data_f[index_f]["vk_id"], str(user_id)
            )
    if delete_result:
        sender(user_id, "Удалено.\n")
        data_f = my_pynder.get_favorite(str(user_id))
        if len(data_f) == 0:
            sender(user_id, "В Избранном ничего нет.\n")
            if mode_ == 2:
                sender(user_id, "Возвращаюсь в режим поиска.\n")
                user_text, user_photo = vk_search.search_favorite(index_m, data_m)
                all_buttons(user_id, user_text, user_photo)
        else:
            if mode_ == 2:
                if index_f > len(data_f) - 1:
                    index_f = len(data_f) - 1
                f_user_text, f_user_photo = vk_search.search_favorite(index_f, data_f)
                favorite_buttons(user_id, f_user_text, f_user_photo)
    else:
        sender(user_id, "Не найдено в Избранном.\n")


def view_favorite_button(user_id, data_f):
    if len(data_f) == 0:
        sender(user_id, "В избранном ничего нет.\n")
    else:
        sender(user_id, "Захожу в Избранное.\n")
        sender(user_id, f"Записей в Избранном: {len(data_f)}.\n")
        f_user_text, f_user_photo = vk_search.search_favorite(0, data_f)
        favorite_buttons(user_id, f_user_text, f_user_photo)


def return_search_button(user_id, data_m, index_m):
    sender(user_id, "Возвращаюсь в режим поиска. Ты остановился здесь:\n")
    user_text, user_photo = vk_search.search_favorite(index_m, data_m)
    all_buttons(user_id, user_text, user_photo)


def favorite_forward_button(user_id, data_f, index_f):
    if len(data_f) == 0:
        sender(user_id, "В избранном ничего нет.\n")
    else:
        # сюда код для прохода по избранным вперед
        if index_f == len(data_f) - 1:
            sender(user_id, "Это последняя запись в Избранном.\n")
        elif index_f > len(data_f) - 1:
            # Это на случай реализации удаления внутри Избранного
            index_f = len(data_f) - 1
            sender(user_id, "Это последняя запись в Избранном.\n")
        else:
            index_f += 1
            f_user_text, f_user_photo = vk_search.search_favorite(index_f, data_f)
            favorite_buttons(user_id, f_user_text, f_user_photo)
    return index_f


def favorite_back_button(user_id, data_f, index_f):
    if len(data_f) == 0:
        sender(user_id, "В избранном ничего нет.\n")
    else:
        if index_f == 0:
            sender(user_id, "Это первая запись в Избранном.\n")
        else:
            index_f -= 1
            f_user_text, f_user_photo = vk_search.search_favorite(index_f, data_f)
            favorite_buttons(user_id, f_user_text, f_user_photo)
    return index_f


def finish_search_button(user_id):
    first_keyboards(
        user_id,
        f"Привет, я бот для поиска новых знакомств!\n "
        f"Нажми на кнопку 'Старт' для начала поиска"
        f" или 'Настройки поиска' для задания условий.\n",
    )


def search_configure_button(user_id):
    settings_buttons(user_id, "Настройки поиска.\n" "Введите все параметры по очереди.")
    my_min_age = 0
    my_max_age = 0
    my_city = ""
    while True:
        config_msg = get_user_choice(user_id)
        match config_msg:
            case "задать минимальный возраст":
                result = get_user_choice(user_id)
                if result.isdecimal():
                    my_min_age = int(result)
                    if my_min_age < 18:
                        sender(user_id, "Минимальный возраст - 18.")
                        my_min_age = 18
                else:
                    sender(
                        user_id,
                        "Неверный ввод, нажмите 'Задать минимальный возраст' снова."
                    )
            case "задать максимальный возраст":
                result = get_user_choice(user_id)
                if result.isdecimal():
                    my_max_age = int(result)
                else:
                    sender(
                        user_id,
                        "Неверный ввод, нажмите 'Задать максимальный возраст' снова."
                    )
            case "задать город":
                my_city = get_user_choice(user_id)
                if not my_city:
                    sender(
                        user_id,
                        "Неверный ввод, нажмите 'Задать город' снова."
                    )
            case "назад":
                if my_min_age < 1:
                    sender(user_id, "Задайте минимальный возраст.")
                elif my_max_age < 1:
                    sender(user_id, "Задайте максимальный возраст.")
                elif my_max_age < my_min_age:
                    sender(
                        user_id,
                        "Максимальный возраст не может быть меньше минимального.",
                    )
                elif my_city == "":
                    sender(user_id, "Задайте город")
                else:
                    sender(
                        user_id,
                        f"Минимальный возраст: {my_min_age}\n"
                        f"Максимальный возраст: {my_max_age}\n"
                        f"Город: {my_city}\n",
                    )
                    first_keyboards(user_id, "К поиску готов!")
                    return {
                        "min_age": my_min_age,
                        "max_age": my_max_age,
                        "city": my_city,
                    }


def get_user_choice(user_id):
    for user_event in longpoll.listen():
        if user_event.type == VkEventType.MESSAGE_NEW:
            try:
                if user_event.to_me:
                    user_msg = user_event.text.lower()
                    if user_event.user_id == user_id:
                        return user_msg
            except Exception as ex:
                print(ex)


config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")
my_pynder = dbf.PYnder_DB(rebuild=True)
access_token = config["VK_token"]["group_token"]
vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
event = next(longpoll.listen())
my_user_id = event.user_id
vk_search = Vk(my_user_id)
first_keyboards(
    my_user_id,
    f"Привет, я бот для поиска новых знакомств!\n "
    f"Нажми на кнопку 'Старт' для начала поиска"
    f" или 'Настройки поиска' для задания условий.\n",
)
main_index, favorite_index, mode = 0, 0, 0
favorite_data = {}
while True:
    my_message = get_user_choice(my_user_id)
    match my_message:
        case "старт🚀":
            my_data = start_button(my_user_id, main_index)
            if not my_data:
                continue
            mode = 1
        case "назад":
            main_index = search_back_button(my_user_id, my_data, main_index)
        case "дальше":
            main_index = search_forward_button(my_user_id, my_data, main_index)
        case "добавить в избранное":
            add_favorite_button(my_user_id, my_data, main_index)
        case "удалить из избранного":
            delete_favorite_button(
                my_user_id, my_data, main_index, favorite_data, favorite_index, mode
            )
        case "просмотреть избранное":
            favorite_data = my_pynder.get_favorite(str(my_user_id))
            mode = 2
            view_favorite_button(my_user_id, favorite_data)
        case "вернуться в поиск":
            mode = 1  # Режим поиска
            return_search_button(my_user_id, my_data, main_index)
        case "следующий":
            favorite_index = favorite_forward_button(
                my_user_id, favorite_data, favorite_index
            )
        case "предыдущий":
            favorite_index = favorite_back_button(
                my_user_id, favorite_data, favorite_index
            )
        case "закончить поиск":
            finish_search_button(my_user_id)
        case "настройки поиска":
            search_dict = search_configure_button(my_user_id)
