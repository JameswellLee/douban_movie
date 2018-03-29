# coding=utf-8
# author=Alan Lee
# date=2018-03-25

import random
import requests
import configparser
import json
import constants
import sys
import logging as log
from utils import Utils
from page_parser import MovieParser
from page_parser import CommentParser
from storage import DbHelper
from login import CookiesHelper

# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')
#log.basicConfig(filename='mylog.log', level=log.info())

# 获取模拟登录后的cookies
# cookie_helper = CookiesHelper.CookiesHelper(
#     config['douban']['user'],
#     config['douban']['password']
# )
# cookies = cookie_helper.get_cookies()

def crawl_page_by_url(url, parser):
    proxy = {'https': 'https://10.236.10.254:3128'}
    headers = {'User-Agent': random.choice(constants.USER_AGENT)}
    # 获取豆瓣页面(API)数据
    r = requests.get(
        url,
        headers=headers,
        proxies=proxy
        #cookies=cookies
    )
    print(r)
    r.encoding = 'utf-8'
    # 提取豆瓣数据
    parser.set_html_doc(r.text)
    entity = parser.extract_page_entity()
    return entity


def crawl_movie_and_save(movie_url, db_helper):
    Utils.Utils.delay(1, 2)
    movie_parser = MovieParser.MovieParser()
    comment_parser = CommentParser.CommentParser()
    movie = crawl_page_by_url(movie_url, movie_parser)
    if not movie:
        print('failed crawl movie url=%s' % url)
        return False
    if movie['want_to_watch'] < constants.WHAT_TO_WATCH_LIMIT:
        print('want_to_watch=%d, failed crawl movie url: url=%s' %(movie['want_to_watch'], url))
        return False
    douban_id = movie_url.split('/')[-2]
    comment_url = constants.URL_COMMENTS_FORMAT % douban_id
    comments = crawl_page_by_url(comment_url, comment_parser)
    # 如果没获取到电影评论数据要重新爬取
    if not comments or not movie:
        print('failed crawl comments, url=%s' % url)
        return False

    if movie:
        movie['link'] = movie_url
        movie['douban_id'] = str(douban_id)
        movie['comments'] = json.dumps(comments)
        db_helper.insert_movie(movie)
        print('crawl success url=%s' % url)
        return True


def load_urls(url_file):
    url_set = []
    url_file = open(url_file, 'r')
    for line in url_file:
        if 'http' in line:
            url = line.strip()
            url_set.append(url)
    return url_set


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    hot_movie_url_file = '热门.txt'
    up_now_playing_url_file = 'up_now_playing.txt'
    up_now_playing_urls = load_urls(up_now_playing_url_file)
    hot_movie_urls = load_urls(hot_movie_url_file)
    dianyin_urls = load_urls('电影.txt')
    classical_urls = load_urls('经典.txt')
    high_score_urls = load_urls('豆瓣高分.txt')
    db_helper = DbHelper.DbHelper()
    datasets_url_set = set(up_now_playing_urls) | set(hot_movie_urls) | set(classical_urls) | set(high_score_urls)
    count = 0
    # for url in datasets_url_set:
    #     if crawl_movie_and_save(url, db_helper):
    #         count = 1 + count
    count = len(datasets_url_set)
    print(count)
    for url in dianyin_urls:
        if count >= 2300:
            break
        if url in datasets_url_set:
            continue
        if crawl_movie_and_save(url, db_helper):
            count += 1
            datasets_url_set.add(url)
    print('done!!!')

