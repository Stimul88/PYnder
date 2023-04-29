import requests
from fake_headers import Headers
from functions import current_age, sort_photo_by_likes
from secondary_token import secondary_token

class Vk:

    def __init__(self, vk_id: str, version='5.131'):
        self.token = secondary_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.url = 'https://api.vk.com/method/'
        self.headers = Headers(os='win', browser='chrome').generate()
        self.vk_id = vk_id
        self.search_index = 0

    def get_city_id(self, city: str):

        '''когда у пользователя скрыт город, получаем id города из названия для вк апи'''
        try:
            params = {'country_id': 1, 'q': city, 'count': 1}
            response = requests.get(self.url + 'database.getCities', headers=self.headers, params={**self.params, **params}).json()
            return response['response']['items'][0]['id']
        except:
            pass

    def get_params_for_search(self, city=None, age=None):

        '''получаем параметры для поиска с помощью id пользователя который пишет, если их нет, просим задать вручную'''

        params = {'user_ids': self.vk_id, 'fields': 'bdate, city, sex'}
        response = requests.get(self.url + 'users.get', headers=self.headers, params={**self.params, **params}).json()
        try:
            user_age = current_age(response['response'][0]['bdate'])
        except:
            user_age = age #сюда подставить возраст который напишет в вк сообщение
        try:
            user_city = response['response'][0]['city']['id']
        except:
            user_city = self.get_city_id(city) #сюда подставляем город в котором ищет если не указан
        if response['response'][0]['sex'] == 2:
            sex_for_search = 1
        else:
            sex_for_search = 2
        search_params = {
            # 'age_from': user_age - 5,
            # 'age_to': user_age + 5,
            'city_id': user_city,
            'sex': sex_for_search,
            'is_closed': False,
            'has_photo': 1,
            'count': 10,
            'fields[]': ['city', 'sex', 'domain', 'bdate']
            }

        return search_params


    def search_peoples(self):

        '''ищем людей по поиску ВК, задается возраст от и до, города задаются айдишниками 1- москва, 2-питер и тд
        пол 1-Ж 2-М, возвращаем максимумум 1000 найденных пользователей'''

        search_params = self.get_params_for_search()

        response = requests.get(self.url + 'users.search', params={**self.params, **search_params},
                                headers=self.headers).json()
        result = []

        for people in response['response']['items']:

            try:
                if people['city']['id'] != search_params['city_id']:
                    continue

                elif people['is_closed']:
                    continue

                else:
                    result.append(people)
                    continue
            except KeyError:
                continue

        return result

    def create_data(self):

        '''фильтруем полученную ранее информацию, на вход все те же переменные, сохраняем нужные данные в data '''

        data = []
        search_result = self.search_peoples()
        for people in search_result:

            city = people['city']['title']

            data.append({
                'firstname': people['first_name'],
                'last_name': people['last_name'],
                'vk_id': str(people['id']),
                # 'birth_date': people['bdate'],
                'gender': people['sex'],
                'city': city
                         })
        return data

    def get_final_data(self, album_id='profile'):

        '''на вход подаем уже отфильрованную инфу, пробегаемся по айдишникам, отсеиваем закрытые страницы,
        берем только адекватные фото'''

        peoples = self.create_data()
        photo_url = self.url + 'photos.get'
        final_data = []
        for person in peoples:
            vk_id = person['vk_id']
            photo_params = {'owner_id': vk_id, 'extended': 1, 'photo_sizes': 1, 'album_id': album_id}
            response = requests.get(photo_url, params={**self.params, **photo_params}, headers=self.headers).json()
            photos = []
            try:
                for photo in response['response']['items']:
                    for size in photo['sizes']:
                        if 'w' in size['type'] or 'z' in size['type'] or 'y' in size['type'] or 'r' in size['type'] \
                                or 'q' in size['type'] or 'p' in size['type']:
                            current_likes = photo['likes']['count']
                            link = size['url']
                            result = {'url': link, 'likes': current_likes}
                            photos.append(result)
                            break

                person['images'] = sort_photo_by_likes(photos)
                final_data.append(person)
            except:
                pass

        return final_data
    def search_favorite(self, data):

        return f'{data[self.search_index]["firstname"]} {data[self.search_index]["last_name"]} \n' \
              f'https://vk.ru/id{data[self.search_index]["vk_id"]} {data[self.search_index]["images"]}'



def main(vk_id, button_click):
    vk = Vk(vk_id)
    vk.search_index = 0
    data = vk.get_final_data()
    while True:
        vk.search_favorite(data)
        button = button_click
        if button == 'дальше':
            vk.search_index += 1
        elif button == 'назад':
            vk.search_index -= 1



# if __name__ == '__main__':
#     main(vk_id='780086634')
