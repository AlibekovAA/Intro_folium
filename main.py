import requests
import folium


def get_info_ip(ip='94.79.33.19'):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        data = {
            '[IP]': response.get('query'),
            '[Int prov]': response.get('isp'),
            '[Org]': response.get('org'),
            '[Country]': response.get('country'),
            '[Region]': response.get('regionName'),
            '[City]': response.get('city'),
            '[ZIP]': response.get('zip'),
            '[Lat]': response.get('lat'),
            '[Lon]': response.get('lon'),
        }
        for k, v in data.items():
            print(f'{k}: {v}')

        area = folium.Map(location=[response.get('lat'), response.get('lon')])

        folium.Marker([response.get('lat'), response.get('lon')],
                      popup=f'Location: {response.get("city")}, {response.get("country")}').add_to(area)

        area.save(f'{response.get("query")}_{response.get("city")}.html')
    except requests.exceptions.ConnectionError:
        print('Check your connection')


def get_location(address):
    try:
        response = requests.get(f'https://nominatim.openstreetmap.org/search?format=json&q={address}').json()
        if len(response) > 0:
            lat = float(response[0]['lat'])
            lon = float(response[0]['lon'])
            map = folium.Map(location=[lat, lon], zoom_start=35)
            folium.Marker([lat, lon], popup=address).add_to(map)
            map.save(f'{address}.html')
            print(f"Карта для адреса '{address}' создана. Откройте '{address}_map.html' в браузере.")
        else:
            print(f"Адрес '{address}' не был найден.")
    except requests.exceptions.ConnectionError:
        print('Проверьте ваше подключение к интернету.')


def main():
    choice = input("Выберите действие ('1' для поиска по IP, '2' для поиска по адресу): ")
    if choice == '1':
        ip = input('Пожалуйста, введите IP-адрес: ')
        get_info_ip(ip)
    elif choice == '2':
        address = input('Пожалуйста, введите адрес: ')
        get_location(address)
    else:
        print('Неправильный выбор. Пожалуйста, введите "1" или "2".')


if __name__ == '__main__':
    main()
