# coding=utf-8
# author=Alan Lee
# date=2018-03-25

import random
import requests
import configparser
import constants
import json
import os
from login import CookiesHelper
from page_parser import MovieParser
from utils import Utils
#from storage import DbHelper

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

# 实例化爬虫类和数据库连接工具类
movie_parser = MovieParser.MovieParser()
#db_helper = DbHelper.DbHelper()

# 读取抓取配置
START_ID = int(config['common']['start_id'])
END_ID = int(config['common']['end_id'])

# 通过ID进行遍历
for area in constants.ALL_AREAS:
    url_file_name = os.path.join(config['common']['url_dir'] ,area + '.txt')
    with open(url_file_name, 'r') as url_file:
        line = url_file.readline()
        movie_data = eval(line)
        movie_url = movie_data['url']
        movie_id = movie_data['id']
        print(movie_data)
        # exit(1)
        headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        # 获取豆瓣页面(API)数据
        r = requests.get(
            movie_url,
            headers=headers,
            #cookies=cookies
        )
        r.encoding = 'utf-8'

        # 提示当前到达的id(log)
        print('urls:%s' % movie_data['url'])

        # 提取豆瓣数据
        movie_parser.set_html_doc(r.text)
        movie = movie_parser.extract_movie_info()
        movie['link'] = movie_url
        movie['douban_id'] = str(movie_id)
        print(movie)
        # 如果获取的数据为空，延时以减轻对目标服务器的压力,并跳过。
        if not movie:
            Utils.Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            continue

        if movie:
            pass
            #db_helper.insert_movie(movie)
        Utils.Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
        exit(1)
# 释放资源
movie_parser = None
#db_helper.close_db()
