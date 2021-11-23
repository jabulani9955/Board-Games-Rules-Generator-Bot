import re
import time
from random import randrange

import requests
import numpy as np
from bs4 import BeautifulSoup


URL_LINKS = "https://www.mosigra.ru/nastolnye-igry/"
# В словаре HEADERS необходимо заменить значения на свои.
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.0.1967 (beta) Yowser/2.5 Safari/537.36", 
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
FILE_SUCCESS = 'data/all_pages_rules_test.txt'
FILE_FAILED = 'data/all_pages_rules_failed_test.txt'
FILE_LINKS = 'data/all_links.txt'


def get_html(url, params=None):
    """ Возвращает всю html-вёрстку определённого сайта. """
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_links(html):
    """ Возвращает список ссылок на все настольные игры с сайта Мосигра. """
    soup = BeautifulSoup(html, 'lxml')
    # Применим регулярное выражение к ссылке на последнюю страницу: href="?page=79&results_per_page=33". Заберём номер страницы.
    pagination_count = int(re.findall(r'\d+', soup.find('a', class_='last').get('href'))[0])
    all_links = []
    for page in range(1, pagination_count + 1):
        url = f'https://www.mosigra.ru/nastolnye-igry/?page={page}&availability=none&parameter_type=0'
        html = get_html(url)
        soup = BeautifulSoup(html.content, 'lxml')
        all_a = soup.find_all('a', class_='card__image')
        for aa in all_a:
            all_links.append(aa.get('href'))
        time.sleep(randrange(2, 5))
        print(f'Обработал {page}/{pagination_count}')

    with open(FILE_LINKS, 'w') as w_file:
        for link in all_links:
            w_file.write(f'{link}\n')
            
    return 'Все ссылки собраны!'


def get_content(html):
    """ Функция для получения правил игры. """
    soup = BeautifulSoup(html, 'lxml')
    return soup.find('section', id='rules').get_text(separator='\n', strip=True)


def save_file(items, path):
    """ Записывает полученный контент в файл. """
    with open(path, 'w') as w_file:
        for game in items:
            w_file.write(f'{game}\n')


def parse():
    """ Основная функция парсинга. """
    all_text = []
    no_rules_games = []
    # Выбор рандомной задержки, чтобы не забанили на сайте.
    delays = [11, 12, 13, 11.5, 12.5, 13.5, 11.2, 12.3, 11.8]
    time.sleep(np.random.choice(delays))
    with open(FILE_LINKS) as file:
        url_list = [line.strip() for line in file.readlines()]
    
    urls_count = len(url_list)

    for i, url in enumerate(url_list):
        time.sleep(randrange(1, 3))
        try:
            html = get_html(url + 'rules/')
            all_text.append(get_content(html.text))
            print(f'Обработал {i + 1} из {urls_count}')
        except AttributeError:
            print(f'У игры {i + 1} нет правил')
            no_rules_games.append(url)
    
    save_file(all_text, FILE_SUCCESS)
    save_file(no_rules_games, FILE_FAILED)

    return f"{'=' * 30}\nПарсинг закончен.\nПолучены правила {len(all_text)} из {urls_count} игр.\nОтсутствуют правила у {len(no_rules_games)} игр."


if __name__ == '__main__':
    # Строчку ниже нужно запустить ТОЛЬКО ОДИН РАЗ, чтобы собрать все ссылки в один файл. Затем её надо закомментировать.
    html = get_html(URL_LINKS)
    print(get_links(html.text))

    # Запуск парсинга. 
    print(parse())
  