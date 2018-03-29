# coding=utf-8
# author=Alan Lee
# date=2018-03-25

import random
import requests
import configparser
import json
import constants
import sys
from page_parser import MovieParser
from page_parser import CommentParser
from storage import DbHelper

# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')


def crawl_page_by_url(url, parser):
    headers = {'User-Agent': random.choice(constants.USER_AGENT)}
    # 获取豆瓣页面(API)数据
    r = requests.get(
        url,
        headers=headers,
        # cookies=cookies
    )
    r.encoding = 'utf-8'
    # 提取豆瓣数据
    parser.set_html_doc(r.text)
    entity = parser.extract_page_entity()
    return entity


def crawl_movie_and_save(movie_url, db_helper):

    movie_parser = MovieParser.MovieParser()
    comment_parser = CommentParser.CommentParser()
    movie = crawl_page_by_url(movie_url, movie_parser)
    #download fail
    if not movie:
        return False
    #fliter movie which is not hot
    if movie['want_to_watch'] < constants.WHAT_TO_WATCH_LIMIT:
        return False
    douban_id = movie_url.split('/')[-2]
    comment_url = constants.URL_COMMENTS_FORMAT % douban_id
    comments = crawl_page_by_url(comment_url, comment_parser)
    # 如果没获取到电影评论数据要重新爬取
    if not comments or not movie:
        return False

    if movie:
        movie['link'] = movie_url
        movie['douban_id'] = str(douban_id)
        movie['comments'] = json.dumps(comments)
        db_helper.insert_movie(movie)
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

    hot_movie_url_file = 'hot_movie.txt'
    up_now_playing_url_file = 'up_now_playing.txt'
    up_now_playing_urls = load_urls(up_now_playing_url_file)
    hot_movie_urls = load_urls(hot_movie_url_file)
    db_helper = DbHelper.DbHelper()
    datasets_url_set = set(up_now_playing_urls)
    # for url in up_now_playing_urls:
    #     state = crawl_movie_and_save(url, db_helper)
    #     print('crawl now and up playing movies: url=%s, state=%s' % (url, str(state)))
    count = 0
    print(len(hot_movie_urls))
    for url in hot_movie_urls:
        if count >= 2000:
            break
        if url in datasets_url_set:
            continue
        if crawl_movie_and_save(url, db_helper):
            count += 1
            datasets_url_set.add(url)
            print('crawl hot movies: url=%s, count=%d' % (url, count))
    print('done!!!')

