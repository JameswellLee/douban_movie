# coding=utf-8
from storage import DbHelper
from login import CookiesHelper
from utils import Utils
import configparser
import random
import constants
import requests
import json
import sys


# 读取配置文件信息
config = configparser.ConfigParser()
config.read('config.ini')

# 获取模拟登录后的cookies
cookie_helper = CookiesHelper.CookiesHelper(
    config['douban']['user'],
    config['douban']['password']
)
cookies = cookie_helper.get_cookies()

logger = Utils.Utils.get_logger('crawl_html', 'crawl_html.log')


def crawl_html(url):
    try:
        headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        # 获取豆瓣页面(API)数据
        r = requests.get(
            url,
            headers=headers,
            cookies=cookies
        )
        r.encoding = 'utf-8'
        if r.status_code != 200:
            return None
        return r.text
    except:
        print(r.status_code)
        return None


def crawl_and_save(db_helper):
    movie_dict_list = db_helper.select_all_dicts()
    movie_html_list = []
    for i in range(len(movie_dict_list)):
        movie_dict = movie_dict_list[i]
        douban_id = movie_dict['douban_id']

        url = constants.URL_PREFIX + douban_id
        Utils.Utils.delay(5, 10)
        movie_html = crawl_html(url)
        movie_html = None
        if movie_html:
            Utils.Utils.delay(3, 5)
            movie_html_list.append({'douban_id': douban_id,
                                'url': url,
                                'html': movie_html})
            logger.info('success crawl url:%s' % url)
        else:
            logger.info('crawl failed!!')

    with open('movie_htmls.json', 'w+') as f:
        json.dump(movie_html_list, f)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    db_helper = DbHelper.DbHelper()
    crawl_and_save(db_helper)
