# coding=utf-8


import sys
import requests
import re
import constants
import json
import random
import hashlib

from storage import DbHelper
from utils import Utils
from my_main import load_urls
from page_parser import CommentParser
from utils import box_office_helper

logger = Utils.Utils.get_logger('dataclean', 'dataclean.log')
reload(sys)
sys.setdefaultencoding('utf8')
db_helper = DbHelper.DbHelper()


def update_box_office(id_title_dicts, crawl_box_office):
    search_count = len(id_title_dicts)
    #search_count = 10
    for i in range(search_count):
        logger.info('-----------------------------------------')
        id_title_dict = id_title_dicts[i]
        douban_id = id_title_dict['douban_id']
        # if douban_id <= '4036000':
        #     continue
        title_short = id_title_dict['title_short']
        box_office = id_title_dict['box_office']
        logger.info('douban_id=%s, titlt_short=%s, box_office=%s' % (douban_id, title_short, box_office))
        # if douban_id < '1291571':
        #     continue
        # if box_office:
        #     continue
        #Utils.Utils.delay(2, 5)
        result = crawl_box_office(id_title_dict['title'])
        if result != 'not found':
            box_office = result
            logger.info('update dataset title_short=%s, box_office=%s' % (title_short, box_office))
            db_helper.update_box_office_by_id(douban_id=douban_id, box_office=box_office)
        else:
            logger.info('not found title=%s' % id_title_dict['title'])


def crawl_empty_comments():
    id_title_dicts = db_helper.select_all_dicts()
    search_count = len(id_title_dicts)
    comment_parser = CommentParser.CommentParser()
    for i in range(search_count):
        logger.info('-----------------------------------------')
        id_title_dict = id_title_dicts[i]
        douban_id = id_title_dict['douban_id']
        comments = id_title_dict['comments']
        comments = json.loads(comments)
        title_short = id_title_dict['title_short']
        print(douban_id)
        if comments and len(comments) > 1:
            logger.info('douban_id=%s, titlt_short=%s, comments=%s' % (douban_id, title_short, comments[0]))
            continue
        comment_url = constants.URL_COMMENTS_FORMAT % douban_id
        Utils.Utils.delay(2, 5)
        r = requests.get(comment_url)
        comment_parser.set_html_doc(r.text)
        comments = comment_parser.extract_page_entity()
        if len(comments) > 0:
            comments_str = json.dumps(comments)
            db_helper.update_comments_by_id(douban_id, comments_str)
            logger.info('update dataset title_short=%s, comments=%s' % (title_short, str(comments[0])))


def delete_want_to_watch_below(limit=10000):
    up_now_playing_urls = load_urls('up_now_playing.txt')
    del_num = 0
    for url in up_now_playing_urls:
        douban_id = url.split('/')[-2]
        row_dict = db_helper.select_by_id(douban_id)
        if not row_dict:
            continue
        want_to_watch = row_dict['want_to_watch']
        print('douban_id=%s, want_to_watch=%s' % (douban_id, want_to_watch))
        if int(want_to_watch) < limit:
            db_helper.delete_by_id(douban_id)
            print('title=%s, want_to_watch=%s, delte!!!!!' %(row_dict['title_short'], want_to_watch))
            del_num += 1
    print('total delete %d' % del_num)


def update_descraption():
    id_title_dicts = db_helper.select_all_dicts()
    search_count = len(id_title_dicts)
    for i in range(search_count):
        id_title_dict = id_title_dicts[i]
        douban_id = id_title_dict['douban_id']
        description = id_title_dict['description']
        print('before:%s' % description)
        description = replace_english_description(description)
        print('after:%s' % description)
        db_helper.update_description_by_id(douban_id, description)
        logger.info('update description douban_id=%s, description=%s' % (douban_id, description))
        print('----------------------------------------')


def update_comment_final():
    dirty_file_intent = 'jingwei/intent_rule.txt'
    dirty_file_query = 'jingwei/query_rule_blacklist.txt'
    dirty_regexs = []
    dirty_substrs = []
    with open(dirty_file_intent) as f:
        for line in f:
            if 'DIRTY' in line:
                line = line.strip()
                line_parts = line.split('\t')
                if 'REGEX' in line and len(line_parts) > 2:
                    dirty_regexs.append(line_parts[2])
                if 'SUBSTR' in line and len(line_parts) > 2:
                    dirty_substrs.append(line_parts[2])
    with open(dirty_file_query) as f:
        for line in f:
            if 'BLACKLIST_FORBIDDEN' in line or 'BLACKLIST_DIRTY' in line:
                line = line.strip()
                line_parts = line.split('\t')
                if 'SUBSTR' in line and len(line_parts) > 2:
                    dirty_substrs.append(line_parts[2])
                if 'REGEX' in line and len(line_parts) > 2:
                    dirty_regexs.append(line_parts[2])
    dirty_regexs = [re.compile(d_r) for d_r in dirty_regexs]

    def group_comment(comments):
        comments = sorted(comments, key=lambda x: x['votes'], reverse=True)
        rating_dict = {key: [] for key in range(1, 6)}
        for comment in comments:
            if comment['rating'] in rating_dict.keys():
                rating_dict[comment['rating']].append(comment)
        return rating_dict

    def validate_comment(comment):
        for d_s in dirty_substrs:
            if d_s in comment.lower():
                return False
        for d_r in dirty_regexs:
            results = d_r.findall(comment)
            if results:
                return False
        return True

    def process_comment(comment):
        comment = comment.strip()
        regex_one = re.compile(ur"(\uff08[^\uff08\uff09]*\uff09)|(\([^\(\)]*\))|(\u3010[^\u3010\u3011]*\u3011)")
        comment = regex_one.sub("", comment)
        return comment

    id_title_dicts = db_helper.select_all_dicts()
    search_count = len(id_title_dicts)
    no_match_count = 0
    for i in range(search_count):
        id_title_dict = id_title_dicts[i]
        douban_id = id_title_dict['douban_id']
        comments = id_title_dict['comments']
        comment_final = id_title_dict['comment_final']
        print(douban_id)

        if comment_final:
           continue
        comments = json.loads(comments)
        if not comments or len(comments) == 0:
            continue

        best_comment = None
        comments = sorted(comments, key=lambda x: x['votes'], reverse=True)
        for comment in comments:
            if validate_comment(comment['description']):
                best_comment = comment
                break
        if best_comment:
            best_comment['description'] = process_comment(best_comment['description'])
            comment_final = best_comment['description']
            # if douban_id == '30159456':
            #     comment_final = comment_final.split('，强推')[0]
            #     comment_final = comment_final.split('10。')[-1]
            # print(comment_final)
            #exit(1)
            db_helper.update_comment_final_by_id(douban_id=douban_id, comment_final=comment_final)
            logger.info('update description douban_id=%s, votes=%s, rating=%s, comment_short=%s' % (douban_id, best_comment['votes'], best_comment['rating'], best_comment['description']))
        else:
            logger.info('not comment match the conditions!!!')
            no_match_count += 1
    print('no_match_count=%d' % no_match_count)




def cut_description(description):
    # 替换掉“（.*饰）”内容
    regex_one = re.compile(ur"(\uff08[^\uff08\uff09]*\uff09)|(\([^\(\)]*\))")
    description = regex_one.sub("", description)
    if len(description) < 100:
        return description
    description_parts = description.split('\n')
    #选取最长的段落
    description = sorted([(desp, len(desp)) for desp in description_parts], key=lambda x: x[1])[-1][0]
    description = description.strip()
    comma_parts = description.split('。')
    #连接之后都句子长度在100以下
    final_description = comma_parts[0] + '。'
    for i in range(1, len(comma_parts)):
        if len(comma_parts[i]) < 3:
            continue
        if len(final_description + '。' + comma_parts[i]) > 100:
            break
        final_description = final_description + comma_parts[i] + '。'
    return final_description


def is_english_description(description):
    regex_en = re.compile(r"[a-zA-Z]+")

    result = regex_en.findall(description)
    if result:
        sign = False
        for rtl in result:
            if len(rtl) > 2:
                sign = True
                print(rtl)
        if sign:
            print(description)


def replace_english_description(description):
    regex_en = re.compile(r"[a-zA-Z]+")
    result = regex_en.findall(description)
    if result:
        for rtl in result:
            if rtl in Utils.new_name_dict.keys():
                description = description.replace(rtl, Utils.new_name_dict[rtl])
            if rtl in Utils.add_word_dict.keys():
                description = description.replace(rtl, Utils.add_word_dict[rtl])
    return description


def update_box_office_mojo():
    id_title_dicts = db_helper.select_all_dicts()
    id_title_dicts = [movie for movie in id_title_dicts if movie['release_region'] and '美国' in movie['release_region']]
    id_title_dicts = [movie for movie in id_title_dicts if movie['douban_id'] > '3654340']

    print(len(id_title_dicts))
    update_box_office(id_title_dicts, box_office_helper.crawl_box_office_mojo)


def baidu_translate(word_dict):
    for q, value in word_dict.items():
        Utils.Utils.delay(2, 5)
        result_json= Utils.Utils.baidu_translate(q)
        results = result_json['trans_result']
        if not results or len(results) == 0:
            continue
        chinese_rtls = []
        for rtl in results:
            chinese_rtls.append(rtl['dst'].encode('utf-8'))
        word_dict[q] = chinese_rtls[0]
        print('%s--->%s' % (q,chinese_rtls[0]))
    print(word_dict)


def print_dict(word_dict):
    print('{')
    for key, value in word_dict.items():
        print('\'%s\': \'%s\',' % (key, value))
    print('}')


if __name__ == '__main__':
    #update_descraption()
    #baidu_translate(name_dict)
    update_comment_final()
