from datetime import date


def current_age(bday):
    today = date.today()
    if len(bday) == 10:
        return today.year - int(bday[6:])
    else:
        return None


def sort_photo_by_likes(photos: list):
    sorted_list = sorted(photos, key=lambda x: x['likes'], reverse=True)
    return sorted_list[:3]



