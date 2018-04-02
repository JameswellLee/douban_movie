# coding=utf-8


import sys
import requests
import editdistance

from storage import DbHelper
from bs4 import BeautifulSoup
from utils import Utils


logger = Utils.Utils.get_logger('dataclean', 'dataclena.log')


def crawl_box_office(title_short):
    searh_url ='http://www.cbooo.cn/search?'
    param = {'k': title_short}
    r = requests.get(searh_url, params=param)
    bs = BeautifulSoup(r.text, 'html.parser')
    lis = bs.find('ul', {'class': 'ulzx03'}).find_all('li')
    info_list = []
    for li in lis:
        name = li.find('a')['title']
        box_office = li.find('span').text.split(' ')[-1]
        distance = editdistance.eval(title_short.encode('utf-8'), name.encode('utf-8'))
        info_list.append((title_short, name, box_office, distance))
    if len(info_list) == 0:
        logger.info('not found for title_short=%s' % title_short)
        return 'not found'
    info_list = sorted(info_list, key=lambda x: x[3])
    best_match = info_list[0]
    logger.info('best_match info:title_short=%s, name=%s, box_office=%s, distance=%s' % (best_match))
    return info_list[0][2]


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    db_helper = DbHelper.DbHelper()
    id_title_dicts = db_helper.get_id_title_dicts()

    search_count = len(id_title_dicts)
    #search_count = 10
    for i in range(search_count):
        id_title_dict = id_title_dicts[i]
        douban_id = id_title_dict['douban_id']
        title_short = id_title_dict['title_short']
        logger.info('douban_id=%s, titlt_short=%s' % (id_title_dict['douban_id'], id_title_dict['title_short']))
        Utils.Utils.delay(2, 5)
        result = crawl_box_office(id_title_dict['title_short'])
        if result != 'not found' and len(result) > 1:
            box_office = result
            logger.info('update dataset title_short=%s, box_office=%s' % (title_short, box_office))
            db_helper.update_box_office_by_id(douban_id=douban_id, box_office=box_office)
        logger.info('-----------------------------------------')