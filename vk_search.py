import requests
from fake_headers import Headers
from functions import sort_photo_by_likes, current_age
import configparser


config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")


class Vk:
    def __init__(self, vk_id: str, version="5.131"):
        self.token = config["VK_token"]["user_token"]
        self.version = version
        self.params = {"access_token": self.token, "v": self.version}
        self.url = "https://api.vk.com/method/"
        self.headers = Headers(os="win", browser="chrome").generate()
        self.vk_id = vk_id

    def check_user_acc(self, user_id):
        params = {"user_ids": user_id, "fields": "city, bdate"}
        response = requests.get(
            self.url + "users.get",
            params={**self.params, **params},
            headers=self.headers,
        ).json()
        if (
            response["response"][0]["is_closed"]
            or not response["response"][0]["bdate"]
            or not response["response"][0]["city"]
        ):
            return True

    def get_city_id(self, city: str):
        # (Саша) временно закоментировал выбор города, возвращаю константу 1
        """когда у пользователя скрыт город, получаем id города из названия для вк апи"""
        try:
            params = {"country_id": 1, "q": city, "count": 1}
            response = requests.get(
                self.url + "database.getCities",
                headers=self.headers,
                params={**self.params, **params},
            ).json()
            return response['response']['items'][0]['id']
        except:
            pass

    def get_params_for_search(self, city=None, age=None):
        """получаем параметры для поиска с помощью id пользователя который пишет, если их нет, просим задать вручную"""

        params = {"user_ids": self.vk_id, "fields": "bdate, city, sex"}
        response = requests.get(
            self.url + "users.get",
            headers=self.headers,
            params={**self.params, **params},
        ).json()
        try:
            user_age = current_age(response["response"][0]["bdate"])

        except:
            user_age = age  # сюда подставить возраст который напишет в вк сообщение

        if not city:
            user_city = response["response"][0]["city"]["id"]
        else:
            user_city = self.get_city_id(
                city
            )  # сюда подставляем город в котором ищет если не указан
        if response["response"][0]["sex"] == 2:
            sex_for_search = 1
        else:
            sex_for_search = 2
        search_params = {
            "age_from": user_age - 5,
            "age_to": user_age + 5,
            "city_id": user_city,
            "sex": sex_for_search,
            "is_closed": False,
            "has_photo": 1,
            "count": 200,
            "fields[]": ["city", "sex", "domain", "bdate"],
        }
        return search_params

    def search_peoples(self, city=None, age=None):
        """ищем людей по поиску ВК, задается возраст от и до, города задаются айдишниками 1- москва, 2-питер и тд
        пол 1-Ж 2-М, возвращаем максимумум 1000 найденных пользователей"""

        search_params = self.get_params_for_search(city, age)

        response = requests.get(
            self.url + "users.search",
            params={**self.params, **search_params},
            headers=self.headers,
        ).json()
        result = []

        for people in response["response"]["items"]:
            try:
                if people["city"]["id"] != search_params["city_id"]:
                    continue

                elif people["is_closed"]:
                    continue

                # elif current_age(people['bdate']) < 18:
                #     continue

                else:
                    result.append(people)
                    continue

            except KeyError:
                continue
        return result

    def create_data(self, city=None, age=None):
        """фильтруем полученную ранее информацию, на вход все те же переменные, сохраняем нужные данные в data"""

        data = []
        search_result = self.search_peoples(city, age)
        for people in search_result:
            data.append(
                {
                    "first_name": people["first_name"],
                    "last_name": people["last_name"],
                    "vk_id": str(people["id"]),
                    "birth_date": people["bdate"],
                    "sex": people["sex"],
                    "city": people["city"]["title"],
                    "url": f'https://vk.ru/id{str(people["id"])}',
                }
            )
        return data

    def get_final_data(self, city=None, age=None, album_id="profile"):
        """на вход подаем уже отфильрованную инфу, пробегаемся по айдишникам, отсеиваем закрытые страницы,
        берем только адекватные фото"""

        peoples = self.create_data(city, age)
        photo_url = self.url + "photos.get"
        final_data = []
        for person in peoples:
            vk_id = person["vk_id"]
            photo_params = {
                "owner_id": vk_id,
                "extended": 1,
                "photo_sizes": 1,
                "album_id": album_id,
            }
            response = requests.get(
                photo_url, params={**self.params, **photo_params}, headers=self.headers
            ).json()
            photos = []
            try:
                for photo in response["response"]["items"]:
                    current_likes = photo["likes"]["count"]
                    link = photo["id"]
                    result = {"url": link, "likes": current_likes}
                    photos.append(result)
                person["images"] = sort_photo_by_likes(photos)
                final_data.append(person)
            except:
                pass

        return final_data

    def search_favorite(self, search_index, data_):
        links = ""
        for photo in data_[search_index]["images"]:
            links += f'photo{data_[search_index]["vk_id"]}_{photo["url"]},'
        user_page_url = f'https://vk.ru/id{data_[search_index]["vk_id"]}'
        final_output = (
            f"Имя: {data_[search_index]['first_name']},\n "
            f"Фамилия: {data_[search_index]['last_name']},\n "
            f"Дата рождения: {data_[search_index]['birth_date']},\n"
            f"Город: {data_[search_index]['city']},\n"
            f"Страница: {user_page_url},\n"
        )
        return final_output, links
