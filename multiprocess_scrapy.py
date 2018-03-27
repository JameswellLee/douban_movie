# coding=utf-8
# author=Alan Lee
# date=2018-03-25

import random
import requests
import configparser
import constants
import time
import os
import multiprocessing as mp
from login import CookiesHelper
from page_parser import MovieParser
from page_parser import CommentParser
from storage import DbHelper

# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')


def run_func(args):
    crawl_by_lines(args[0], args[1], args[2], args[3])

def crawl_by_lines(queue, lines, start_line, area):
    movie_parser = MovieParser.MovieParser()
    comment_parser = CommentParser.CommentParser()
    db_helper = DbHelper.DbHelper()
    for i in range(start_line, len(lines)):
        line = lines[i]
        if len(line) < 5:
            continue
        start_time = time.time()
        movie_data = eval(line)
        movie_url = movie_data['url']
        movie_id = movie_data['id']
        comment_url = constants.URL_COMMENTS_FORMAT % movie_id

        headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        # 获取豆瓣页面(API)数据
        r = requests.get(
            movie_url,
            headers=headers,
            # cookies=cookies
        )
        r.encoding = 'utf-8'

        # 提取豆瓣数据
        movie_parser.set_html_doc(r.text)
        movie = movie_parser.extract_movie_info()

        # 获取电影评论页面数据
        r = requests.get(
            comment_url,
            headers=headers,
            # cookies=cookies
        )
        r.encoding = 'utf-8'
        comment_parser.set_html_doc(r.text)
        comments = comment_parser.extract_comments_str(movie_id)

        # 如果没获取到电影评论数据要重新爬取
        if not comments:
            movie = None
        # 如果获取的数据为空，延时以减轻对目标服务器的压力,并跳过。
        if not movie:
            queue.put(str(movie_data))

        if movie:
            movie['link'] = movie_url
            movie['douban_id'] = str(movie_id)
            movie['comments'] = comments
            db_helper.insert_movie(movie)
        cost_time = time.time() - start_time
        print('crawl status : area=%s, line=%d, url=%s, state=%s, time=%s' % (area, i, movie_data['url'], not not movie, cost_time))
        # 释放资源
    movie_parser = None
    db_helper.close_db()


if __name__ == '__main__':
    # 通过电影地区获取到的url进行电影爬取
    m = mp.Manager()
    fail_url_queue = m.Queue()
    pool = mp.Pool(8)
    fail_url_file = config['common']['fail_url_file']
    fail_url_file = open(fail_url_file, 'w')
    args = []
    for i in range(len(constants.ALL_AREAS)):
        url_file_name = os.path.join(config['common']['url_dir'], constants.ALL_AREAS[i] + '.txt')
        url_file = open(url_file_name, 'r')
        lines = url_file.readlines()
        print(len(lines))
        args.append((fail_url_queue, lines, 0, constants.ALL_AREAS[i]))

    pool.map(run_func, args)
    pool.close()
    pool.join()

    while not fail_url_queue.empty:
        fail_url_file.write(fail_url_queue.get() + '\n')
    fail_url_file.close()





