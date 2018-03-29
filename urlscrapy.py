# coding=utf-8
# author=XingLong Pan
# date=2016-11-07

import random
import requests
import configparser
import json
import constants
from login import CookiesHelper
from utils import Utils

# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')

# 获取模拟登录后的cookies
cookie_helper = CookiesHelper.CookiesHelper(
    config['douban']['user'],
    config['douban']['password']
)
#cookies = cookie_helper.get_cookies()
#print(cookies)

payload = {'sort': 'T', 'range': '0,10', 'tags': '大陆', 'start': None}
movies_count_dict = {}
for area in constants.ALL_AREAS:
    payload['tags'] = area
    start = 0
    movies_count_dict[area] = 0
    movie_list_fn = 'urls/%s.txt' % area
    movie_list_f = open(movie_list_fn, 'w+')

    print(movie_list_fn)
    while True:
        payload['start'] = start
        headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        r = requests.get(
          constants.URL_MOVIE_TYPE,
          headers=headers,
          #cookies=cookies,
          params=payload
        )
        start = start + 20
        r.encoding = 'utf-8'
        data_dic = json.loads(r.text)
        movie_list = data_dic['data']
        # '{"directors":["陈正道"],' \
        # '"rate":"7.2",' \
        # '"cover_x":1020,' \
        # '"star":"35",' \
        # '"title":"重返20岁",' \
        # '"url":"https:\/\/movie.douban.com\/subject\/25870084\/",' \
        # '"casts":["杨子姗","归亚蕾","陈柏霖","鹿晗","王德顺"],' \
        # '"cover":"https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2216353367.webp",' \
        # '"id":"25870084",' \
        # '"cover_y":1486}'
        for movie in movie_list:
            movie_list_f.write(str(movie) + '\n')
        movie_list_f.flush()
        movies_count_dict[area] = movies_count_dict[area] + len(movie_list)
        print('area = %s, count = %d' % (area, movies_count_dict[area]))
        if len(movie_list) == 0:
            break
        Utils.Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)






