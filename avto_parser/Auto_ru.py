import requests #Библиотека для запроса
import csv
import os
import ctypes
import colorama
from colorama import Fore
from proxy import proxy_lists
from datetime import datetime


colorama.init()
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

info = []

name_error = None
phone_error = None
photo = None

def main():
    try:
        pag = int(input(Fore.GREEN + 'С какой страницы начинаем парсинг: '))
    except:
        pag = int(input(Fore.RED) + 'Неверное значение. Попробуйте еще раз: ')
    address_files = input(Fore.GREEN + 'Введите адрес сохранения файла csv (данные парсинга): ')
    while int(pag) <= 99:
        HEADERS = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Content-Length': '137',
            'content-type': 'application/json',
            'Cookie': '_csrf_token=1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24; autoru_sid=a%3Ag5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270%7C1580931467355.604800.8HnYnADZ6dSuzP1gctE0Fw.cd59AHgDSjoJxSYHCHfDUoj-f2orbR5pKj6U0ddu1G4; autoruuid=g5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270; suid=48a075680eac323f3f9ad5304157467a.bc50c5bde34519f174ccdba0bd791787; from_lifetime=1580933172327; from=yandex; X-Vertis-DC=myt; crookie=bp+bI7U7P7sm6q0mpUwAgWZrbzx3jePMKp8OPHqMwu9FdPseXCTs3bUqyAjp1fRRTDJ9Z5RZEdQLKToDLIpc7dWxb90=; cmtchd=MTU4MDkzMTQ3MjU0NQ==; yandexuid=1758388111580931457; bltsr=1; navigation_promo_seen-recalls=true',
            'Host': 'auto.ru',
            'origin': 'https://auto.ru',
            'Referer': 'https://auto.ru/moskva/truck/used/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'x-client-app-version': '202002.03.092255',
            'x-client-date': '1580933207763',
            'x-csrf-token': '1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24',
            'x-page-request-id': '60142cd4f0c0edf51f96fd0134c6f02a',
            'x-requested-with': 'fetch'
        }
        PARAMS = {
            # 'catalog_filter' : [{"mark": "BAW"}],
            'section': "used",
            'category': "trucks",
            'sort': "fresh_relevance_1-desc",
            'page': pag
        }
        URL = 'https://auto.ru/-/ajax/desktop/listing/'  # URL на который будет отправлен запрос

        try:
            response = requests.post(URL, json=PARAMS, headers=HEADERS)
        except:
            response = requests.post(URL, json=PARAMS, headers=HEADERS, proxies=proxy_lists())

        data = response.json()['offers']
        for d in data:
            PARAMS_2 = {
                "category": "trucks",
                "offerIdHash": d['saleId']
            }
            URL_2 = 'https://auto.ru/-/ajax/desktop/getPhones'
            try:
                response_2 = requests.post(URL_2, json=PARAMS_2, headers=HEADERS)
            except:
                response_2 = requests.post(URL_2, json=PARAMS_2, headers=HEADERS, proxies=proxy_lists())
            try:
                data_2 = response_2.json()['phones'][0]
                name_error = data_2['phone']
                phone_error = data_2['title']
            except:
                try:
                    data_2 = response_2.json()
                    name_error = data_2['error']
                    phone_error = data_2['detailed_error']
                except:
                    name_error = 'Не указано'
                    phone_error = 'Не указано'
            try:
                photo = d['state']['image_urls'][0]['sizes']['1200x900n']
            except:
                photo = 'Без фото'

            try:
                owners = d['documents']['owners_number']
            except:
                owners = 'Не указано'
            try:
                vin = d['documents']['vin']
            except:
                vin = 'Не указано'
            try:
                pts = d['documents']['pts']
            except:
                pts = 'Не указано'
            try:
                trailer_type = d['vehicle_info']['trailer_type']
            except:
                trailer_type = 'Не указано'
            try:
                truck_category = d['vehicle_info']['truck_category']
            except:
                truck_category = 'Не указано'
            try:
                engine = d['vehicle_info']['engine']
            except:
                engine = 'Не указано'
            try:
                transmission = d['vehicle_info']['transmission']
            except:
                transmission = 'Не указано'
            try:
                rul = d['vehicle_info']['steering_wheel']
            except:
                rul = 'Не указано'

            creation_date_ts = int(d['additional_info']['creation_date']) / 1000
            update_date_ts = int(d['additional_info']['update_date']) / 1000
            creation_date = datetime.utcfromtimestamp(creation_date_ts).strftime('%Y-%m-%d %H:%M:%S')
            update_date = datetime.utcfromtimestamp(update_date_ts).strftime('%Y-%m-%d %H:%M:%S')

            #creation_date = datetime.utcfromtimestamp(int(d['additional_info']['creation_date'])).strftime('%Y-%m-%d %H:%M:%S')
            #update_date = datetime.utcfromtimestamp(int(d['additional_info']['update_date'])).strftime('%Y-%m-%d '


            info.append({
                'name_vladelech': name_error,
                'phone': phone_error,
                'price_info_RUR': d['price_info']['RUR'],
                'price_info_EUR': d['price_info']['EUR'],
                'price_info_USD': d['price_info']['USD'],
                'photo': photo,
                'truck': d['vehicle_info']['mark_info']['name'] + ' ' + d['vehicle_info']['model_info']['name'],
                'tamozh': d['documents']['custom_cleared'],
                'year': d['documents']['year'],
                'seller_type': d['seller_type'],
                'location': d['seller']['location']['region_info']['name'],
                'lk': d['lk_summary'],
                'owners': owners,
                'vin': vin,
                'pts': pts,
                'trailer_type': trailer_type,
                'truck_category': truck_category,
                'engine': engine,
                'transmission': transmission,
                'rul': rul,
                'creation_date': creation_date,
                'update_date': update_date

                #'creation_date': creation_date,
                #'update_date': update_date
            })

            if os.path.isfile(address_files + '\\save_car.csv') == True:
                key = 'a'
            else:
                key = 'w'

            with open(address_files + '\\save_car.csv', key, newline='', encoding='UTF-8') as f:
                a_pen = csv.writer(f, delimiter='@')
                for a in info:
                    a_pen.writerow((a['name_vladelech'], a['phone'], a['price_info_RUR'], a['price_info_EUR'],
                                    a['price_info_USD'], a['photo'], a['truck'],
                                    a['tamozh'], a['year'], a['seller_type'], a['location'], a['lk'], a['owners'],
                                    a['vin'], a['pts'], a['truck_category'], a['trailer_type'], a['engine'],
                                    a['transmission'], a['rul'], a['creation_date'], a['update_date']))
            pag += 1
            print(Fore.GREEN + 'Страница выполнена: ' + str(pag))

if __name__ == '__main__':
    main()
    print(Fore.GREEN + 'Выполнено')




