# coding=utf-8
# author=Alan Lee
# date=2018-03-25

import random
import requests
import configparser
import json
import constants
import sys
import multiprocessing as mp
from utils import Utils
from page_parser import MovieParser
from page_parser import CommentParser
from storage import DbHelper

config = configparser.ConfigParser()
config.read('config.ini')


def crawl_page_by_url(url, parser):
    try:
        headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        # 获取豆瓣页面(API)数据
        r = requests.get(
            url,
            headers=headers,
            proxies=constants.proxies,
            timeout=constants.CHECK_PROXY_TIMEOUT
        )
        if r.status_code == 403:
            print('403 error!!!!!!')
        r.encoding = 'utf-8'
        parser.set_html_doc(r.text)
        entity = parser.extract_page_entity()
        return entity
    except:
        return None


def crawl_movie_and_save(movie_url, db_helper):
    movie_parser = MovieParser.MovieParser()
    comment_parser = CommentParser.CommentParser()
    #check in database
    douban_id = movie_url.split('/')[-2]
    if db_helper.is_contains_movie(douban_id):
        print('contains movie url=%s' % movie_url)
        return False
    #start crawl movie page
    Utils.Utils.delay(1, 2)
    movie = crawl_page_by_url(movie_url, movie_parser)
    if not movie:
        print('failed crawl movie url=%s' % movie_url)
        return False
    # if movie['want_to_watch'] < constants.WHAT_TO_WATCH_LIMIT:
    #     print('want_to_watch=%d, failed crawl movie url: url=%s' %(movie['want_to_watch'], movie_url))
    #     return False
    #start crawl comment page
    comment_url = constants.URL_COMMENTS_FORMAT % douban_id
    comments = crawl_page_by_url(comment_url, comment_parser)
    # 如果没获取到电影评论数据要重新爬取
    if not comments or not movie:
        print('failed crawl comments, url=%s' % movie_url)
        return False
    if movie:
        movie['link'] = movie_url
        movie['douban_id'] = str(douban_id)
        movie['comments'] = json.dumps(comments)
        db_helper.insert_movie(movie)
        print('crawl success url=%s' % movie_url)
        return True


def load_urls(url_file):
    url_set = []
    url_file = open(url_file, 'r')
    for line in url_file:
        if 'http' in line:
            url = line.strip()
            url_set.append(url)
    return url_set


def run_func(args):
    dp_helper = DbHelper.DbHelper()
    urls = args
    for url in urls:
        crawl_movie_and_save(url, dp_helper)


def multi_process_crawl():
    reload(sys)
    sys.setdefaultencoding('utf8')
    thread_num = 1
    pool = mp.Pool(thread_num)

    up_now_playing_urls = load_urls('热门.txt')
    hot_movie_urls = load_urls('up_now_playing.txt')
    dianyin_urls = load_urls('电影.txt')
    classical_urls = load_urls('经典.txt')
    high_score_urls = load_urls('豆瓣高分.txt')
    all_urls = []
    all_urls.extend(up_now_playing_urls)
    all_urls.extend(hot_movie_urls)
    all_urls.extend(classical_urls)
    all_urls.extend(high_score_urls)
    all_urls.extend(dianyin_urls)

    all_urls = [url.replace('https', 'http') for url in all_urls]
    start_url = "http://movie.douban.com/subject/27114911/"
    start_url_idx = all_urls.index(start_url)
    start_url_idx = 1000
    all_urls = all_urls[start_url_idx:]
    print("start from %d, url=%s" % (start_url_idx, start_url))

    args = []
    step = len(all_urls) / thread_num
    for i in range(thread_num):
        if i < thread_num-1:
            args.append((all_urls[i * step: (i + step)]))
        else:
            args.append((all_urls[i * step:]))
    pool.map(run_func, args)
    pool.close()
    pool.join()


if __name__ == '__main__':
    multi_process_crawl()


