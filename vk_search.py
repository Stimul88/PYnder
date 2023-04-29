import requests
from fake_headers import Headers
from functions import current_age, sort_photo_by_likes
from secondary_token import secondary_token

class Vk:

    def __init__(self, vk_id, version='5.131'):
        self.token = secondary_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.url = 'https://api.vk.com/method/'
        self.headers = Headers(os='win', browser='chrome').generate()
        self.vk_id = vk_id

    def get_params_for_search(self):
        '''получаем параметры для поиска с помощью id пользователя который пишет, если их нет, просим задать вручную'''

        params = {'user_ids': self.vk_id, 'fields': 'bdate, city, sex'}
        response = requests.get(self.url + 'users.get', headers=self.headers, params={**self.params, **params}).json()


        user_age = current_age(response['response'][0]['bdate'])

        user_city = response['response'][0]['city']['id']

        if response['response'][0]['sex'] == 2:
            sex_for_search = 1
        else:
            sex_for_search = 2
        search_params = {
            'age_from': user_age - 5,
            'age_to': user_age + 5,
            'city_id': user_city,
            'sex': sex_for_search,
            'is_closed': False,
            'has_photo': 1,
            'count': 1000,
            'fields[]': ['city', 'sex', 'domain', 'bdate']
        }
        return search_params

    def search_peoples(self):

        '''ищем людей по поиску ВК, задается возраст от и до, города задаются айдишниками 1- москва, 2-питер и тд
        пол 1-Ж 2-М, возвращаем максимумум 1000 найденных пользователей'''

        search_params = self.get_params_for_search()

        response = requests.get(self.url + 'users.search', params={**self.params, **search_params},
                                headers=self.headers)
        result = []

        for people in response.json()['response']['items']:
            try:
                if people['city']['id'] != search_params['city_id']:
                    continue

                elif people['is_closed'] == True:
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
                'vk_id': people['id'],
                'birth_date': people['bdate'],
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


def main(vk_id):
    vk = Vk(vk_id)
    return vk.get_final_data()


if __name__ == '__main__':
    main(vk_id='780086634')
