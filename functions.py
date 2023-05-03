from datetime import date


def current_age(bday):
    """
    Функция считает и возвращает возраст в годах
    :param bday:
    :return:
    """
    today = date.today()
    if len(bday) >= 8:
        return today.year - int(bday[6:])
    else:
        return None


def sort_photo_by_likes(photos: list):
    """
    Функция сортирует фотографии профиля по количеству лайков, возвращает 3 самые популярные
    :param photos: 
    :return:
    """
    sorted_list = sorted(photos, key=lambda x: x["likes"], reverse=True)
    return sorted_list[:3]
