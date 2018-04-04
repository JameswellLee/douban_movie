# coding=utf-8
# author=XingLong Pan
# date=2016-11-07

import time
import random
import logging
import hashlib
import requests
import json

class Utils:

    @staticmethod
    def delay(min_second, max_second):
        time.sleep(random.randrange(min_second, max_second))

    @staticmethod
    def get_logger(logname, filename):
        logger = logging.getLogger(logname)
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(filename)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        # add the handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)
        return logger
    @staticmethod
    def baidu_translate(q):
        md5 = hashlib.md5()
        trans_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        param = {'q': '',
                 'from': 'en',
                 'to': 'zh',
                 'appid': 20180404000142935,
                 'salt': 0,
                 'sign': ''}
        appid = 20180404000142935
        private_key = 'mbUwxDDkDUrc_KsyMQ4Y'

        q = q.encode('utf-8')
        param['q'] = q
        salt = random.randint(-10000, 10000)
        param['salt'] = salt
        sign_str = str(appid)+q+str(salt)+str(private_key)
        md5.update(sign_str)
        sign = md5.hexdigest()
        param['sign'] = sign
        r = requests.post(trans_url, param)
        result = json.loads(r.text)
        return result


name_dict = {u'CPH': 'CPH', u'MIKE': '\xe8\xbf\x88\xe5\x85\x8b', u'Hal': '\xe5\x93\x88\xe5\xb0\x94', u'SeanAmbrose': '肖恩安布罗斯', u'Fit': '\xe9\x80\x82\xe5\x90\x88', u'PAX': '\xe5\x9c\xa3\xe5\x83\x8f\xe7\x89\x8c', u'Geta': '\xe6\x9c\xa8\xe5\xb1\x90', u'MIB': 'MIB', u'EmilBlonsky': '埃米', u'MiniMo': '\xe7\xbc\xa9\xe5\x8d\xb0\xe7\x89\x88', u'Benji': '\xe7\x9f\xb3\xe7\xa3\x8a', u'Wayne': '\xe9\x9f\xa6\xe6\x81\xa9', u'THEENDOFTHEWORLD': 'theendoftheworld', u'Elias': '\xe5\x9f\x83\xe5\x88\xa9\xe4\xba\x9a\xe6\x96\xaf', u'Sherry': '\xe9\x9b\xaa\xe8\x8e\x89', u'gonein': 'gonein', u'YouTube': 'YouTube', u'Philippe': '\xe8\x8f\xb2\xe5\x88\xa9\xe6\x99\xae', u'peter': '\xe5\xbd\xbc\xe5\xbe\x97', u'Driss': '\xe5\xbe\xb7\xe9\x87\x8c\xe6\x96\xaf', u'Samantha': '\xe8\x90\xa8\xe6\x9b\xbc\xe8\x8e\x8e', u'Jordan': '\xe4\xb9\x94\xe4\xb8\xb9', u'SPT': 'SPT', u'fans': '\xe7\x90\x83\xe8\xbf\xb7', u'MyWay': '\xe8\xbf\x88\xe6\x9c\xaa', u'Dak': '\xe9\xa9\xbf\xe7\xab\x99', u'Avery': '\xe5\x9f\x83\xe5\xbc\x97\xe9\x87\x8c', u'Nana': '\xe5\xa8\x9c\xe5\xa8\x9c', u'Jennie': '\xe7\x8f\x8d\xe5\xa6\xae', u'yoyo': '\xe6\xba\x9c\xe6\xba\x9c\xe7\x90\x83', u'CateBlanchett': '\xe5\x87\xaf\xe7\x89\xb9\xc2\xb7\xe5\xb8\x83\xe5\x85\xb0\xe5\x88\x87\xe7\x89\xb9', u'Shirley': '\xe9\x9b\xaa\xe8\x8e\x89', u'VOGUE': '\xe6\x97\xb6\xe5\xb0\x9a', u'Grace': '\xe6\x81\xa9\xe5\x85\xb8', u'Joe': '\xe4\xb9\x94', u'Michelle': '\xe7\xb1\xb3\xe6\xad\x87\xe5\xb0\x94', u'V': 'v', u'HAL': '\xe5\x93\x88\xe5\xb0\x94', u'D': 'D', u'NicoMirallegro': '', u'Virginian': '\xe5\xbc\x97\xe5\x90\x89\xe5\xb0\xbc\xe4\xba\x9a', u'Hancock': '\xe6\xb1\x89\xe8\x80\x83\xe5\x85\x8b', u'Jackie': '\xe6\x9d\xb0\xe5\x9f\xba', u'Loser': '\xe5\xa4\xb1\xe8\xb4\xa5\xe8\x80\x85', u'SolomonNorthup': '所罗门·诺瑟普', u'MadameM': 'madamem', u'Club': '\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8', u'Elaine': '\xe4\xbc\x8a\xe8\x8e\xb1\xe6\x81\xa9', u'T': 'T', u'EthanHunt': '伊森亨特', u'SteveCarell': '史蒂夫·卡瑞尔', u'X': 'X', u'LuciaAniello': '露西娅', u'FrankAdler': '弗兰克·艾德勒', u'Amir': '\xe9\x98\xbf\xe7\xb1\xb3\xe5\xb0\x94', u'Summer': '\xe5\xa4\x8f\xe5\xa4\xa9', u'Thomas': '\xe6\x89\x98\xe9\xa9\xac\xe6\x96\xaf', u'OL': 'OL', u'Kenny': '\xe8\x82\xaf\xe5\xb0\xbc', u'Pim': 'PIM', u'Sam': '\xe5\xb1\xb1\xe5\xa7\x86', u'KarenSettman': '凯伦赛特蒙', u'Tim': '\xe6\x8f\x90\xe5\xa7\x86', u'OK': '\xe5\xa5\xbd\xe5\x95\x8a', u'VIP': '\xe8\xb4\xb5\xe5\xae\xbe', u'Zahra': '\xe8\x90\xa8\xe6\x8b\x89', u'SNS': 'SNS', u'Allen': '\xe8\x89\xbe\xe4\xbc\xa6', u'Branson': '\xe5\xb8\x83\xe5\x85\xb0\xe6\xa3\xae', u'RUNWAY': '\xe8\xb7\x91\xe9\x81\x93', u'Bronski': '布龙斯基', u'MariaTura': '玛丽亚', u'AveryMartin': '埃弗里', u'WilliamParrish': '帕利斯', u'Colonel': '\xe4\xb8\x8a\xe6\xa0\xa1', u'CJE': '\xe6\xa8\x9f\xe7\xa7\x91\xe6\x8f\x90\xe5\x8f\x96\xe7\x89\xa9', u'Georges': '\xe4\xb9\x94\xe6\xb2\xbb\xe6\x96\xaf', u'Mark': '\xe4\xbd\x9c\xe8\xae\xb0\xe5\x8f\xb7', u'A': '\xe4\xb8\x80', u'AE': 'AE', u'Amber': '\xe7\x90\xa5\xe7\x8f\x80', u'John': '\xe7\xba\xa6\xe7\xbf\xb0', u'Anne': '\xe5\xae\x89\xe5\xa6\xae', u'Andr': '\xe5\xae\x89\xe5\xbe\xb7\xe7\x83\x88', u'PS': 'PS', u'Nyah': 'Nyah', u'keiko': '\xe6\x83\xa0\xe5\xad\x90', u'CEO': '\xe9\xa6\x96\xe5\xb8\xad\xe6\x89\xa7\xe8\xa1\x8c\xe5\xae\x98', u'Frank': '\xe5\xbc\x97\xe5\x85\xb0\xe5\x85\x8b', u'Netflix': '\xe7\xbd\x91\xe9\xa3\x9e\xe5\x85\xac\xe5\x8f\xb8', u'Wasabi': '\xe8\x8a\xa5\xe6\x9c\xab', u'KenTaylor': '肯·泰勒', u'William': '\xe5\xa8\x81\xe5\xbb\x89', u'Mew': '缪', u'Werner': '\xe6\xb2\x83\xe7\xba\xb3', u'DragQueen': '变装皇后', u'Baby': '\xe5\xae\x9d\xe8\xb4\x9d', u'PTU': 'PTU', u'OmniCorp': 'Omnicorp', u'Jeanne': '\xe7\x8f\x8d\xe5\xa6\xae', u'Marty': '\xe9\xa9\xac\xe8\x92\x82', u'Cipher': '\xe5\xaf\x86\xe7\xa0\x81', u'C': 'C', u'ZOE': '\xe4\xbd\x90\xe4\xbc\x8a', u'G': 'G', u'Eudes': '\xe5\x8e\x84\xe5\xbe\xb7', u'seconds': '\xe7\xa7\x92', u'K': 'K', u'Gifted': '\xe6\x9c\x89\xe5\xa4\xa9\xe8\xb5\x8b\xe7\x9a\x84', u'Mi': '\xe6\x83\xaf\xe6\x80\xa7\xe7\x9f\xa9', u'NJ': '\xe6\x96\xb0\xe6\xb3\xbd\xe8\xa5\xbf', u'O': 'o', u'David': '\xe6\x88\xb4\xe7\xbb\xb4', u'Nina': '\xe5\xa6\xae\xe5\xa8\x9c', u'Tony': '\xe6\x89\x98\xe5\xb0\xbc', u'MAGI': '\xe6\xb3\x95\xe5\xb8\x88', u'Halley': '\xe5\x93\x88\xe9\x9b\xb7', u'W': 'W', u'Mr': '\xe5\x85\x88\xe7\x94\x9f', u'Mrs': '\xe5\xa4\xab\xe4\xba\xba', u'SEELE': 'SEELE', u'Susan': '\xe8\x8b\x8f\xe7\x8f\x8a', u'JohnnieGray': '约翰尼', u'Maggie': '\xe9\xba\xa6\xe7\x90\xaa', u'ErikaKohut': '爱丽卡', u'Jimmy': '\xe5\x90\x89\xe7\xb1\xb3', u'Dean': '\xe9\x99\xa2\xe9\x95\xbf', u'Bart': '\xe5\xb7\xb4\xe7\x89\xb9', u'Johnny': '\xe7\xba\xa6\xe7\xbf\xb0\xe5\xb0\xbc', u'JoeBlack': '乔·布莱克', u'App': '\xe5\xba\x94\xe7\x94\xa8\xe7\xa8\x8b\xe5\xba\x8f', u'Owen': '\xe6\xac\xa7\xe6\x96\x87', u'MI': '\xe5\x8c\xbb\xe7\x96\x97\xe4\xbf\x9d\xe9\x99\xa9', u'S': 'S', u'Ginger': '\xe7\x94\x9f\xe5\xa7\x9c', u'Kana': '\xe5\x81\x87\xe5\x90\x8d', u'JohnConnor': '约翰·康纳', u'Cure': '\xe6\xb2\xbb\xe6\x84\x88', u'YOYO': '\xe6\xba\x9c\xe6\xba\x9c\xe7\x90\x83', u'Scrooge': '\xe6\x96\xaf\xe5\x85\x8b\xe7\xbd\x97\xe5\x90\x89', u'AV': '\xe6\x88\x90\xe4\xba\xba\xe5\xbd\xb1\xe7\x89\x87', u'Doug': '\xe9\x81\x93\xe6\xa0\xbc', u'U': 'u', u'ChrisEvans': '\xe5\x85\x8b\xe9\x87\x8c\xe6\x96\xaf\xe5\x9f\x83\xe6\x96\x87\xe6\x96\xaf', u'HowardHughes': '\xe9\x9c\x8d\xe5\x8d\x8e\xe5\xbe\xb7\xe4\xbc\x91\xe6\x96\xaf', u'Nancy': '\xe5\x8d\x97\xe5\xb8\x8c', u'cm': '\xe5\x8e\x98\xe7\xb1\xb3', u'IlMare': 'ilmare', u'DVD': 'DVD', u'Robert': '\xe7\xbd\x97\xe4\xbc\xaf\xe7\x89\xb9', u'DOA': 'DOA', u'CIA': '\xe7\xbe\x8e\xe5\x9b\xbd\xe4\xb8\xad\xe5\xa4\xae\xe6\x83\x85\xe6\x8a\xa5\xe5\xb1\x80', u'EmmaStone': '\xe8\x89\xbe\xe7\x8e\x9b\xc2\xb7\xe6\x96\xaf\xe9\x80\x9a', u'Geoffroy': '杰弗洛伊', u'Clotaire': '\xe5\x85\x8b\xe6\xb4\x9b\xe6\xb3\xb0\xe5\xb0\x94', u'Ada': '\xe8\x89\xbe\xe8\xbe\xbe', u'MBJet': 'mbjet', u'CDS': 'CD', u'Molly': '\xe8\x8e\xab\xe8\x8e\x89', u'Lena': '\xe8\x8e\xb1\xe5\xa8\x9c', u'WhereRainbowsEnd': 'whererainbowsend', u'August': '\xe5\x85\xab\xe6\x9c\x88', u'Margaret': '\xe7\x8e\x9b\xe6\xa0\xbc\xe4\xb8\xbd\xe7\x89\xb9', u'BlackStone': '\xe9\xbb\x91\xe7\x9f\xb3\xe9\x9b\x86\xe5\x9b\xa2', u'Macy': '\xe6\xa2\x85\xe8\xa5\xbf', u'Alan': '\xe8\x89\xbe\xe4\xbc\xa6', u'Amy': '\xe8\x89\xbe\xe7\xb1\xb3', u'msn': 'MSN', u'Delphine': '\xe5\xbe\xb7\xe5\xb0\x94\xe8\x8f\xb2\xe5\xa8\x9c', u'GiGi': '\xe5\x90\x89\xe5\x90\x89', u'Anita': '\xe5\xae\x89\xe5\xa6\xae\xe5\xa1\x94', u'Moss': '\xe8\x8b\x94\xe8\x97\x93', u'Hans': '\xe6\xb1\x89\xe6\x96\xaf', u'JosephTura': '约瑟夫·图拉', u'Beth': '\xe8\xb4\x9d\xe4\xb8\x9d', u'Jeannie': '\xe7\x8f\x8d\xe5\xa6\xae', u'TheOrigin': '\xe8\xb5\xb7\xe6\xba\x90', u'BoBo': '\xe6\xb3\xa2\xe6\xb3\xa2', u'Baxter': '\xe5\xb7\xb4\xe5\x85\x8b\xe6\x96\xaf\xe7\x89\xb9', u'B': 'B', u'Ben': '\xe6\x9c\xac', u'P': 'P', u'IMF': '\xe5\x9b\xbd\xe9\x99\x85\xe8\xb4\xa7\xe5\xb8\x81\xe5\x9f\xba\xe9\x87\x91\xe7\xbb\x84\xe7\xbb\x87', u'Patrick': '\xe5\xb8\x95\xe7\x89\xb9\xe9\x87\x8c\xe5\x85\x8b', u'LeightonMeester': '莉顿·梅斯特', u'J': 'J', u'NERV': 'NERV', u'Stu': '\xe6\x96\xaf\xe5\x9b\xbe', u'GPS': '\xe5\x85\xa8\xe7\x90\x83\xe5\xae\x9a\xe4\xbd\x8d\xe7\xb3\xbb\xe7\xbb\x9f', u'Rapunzel': '\xe9\x95\xbf\xe5\x8f\x91\xe5\x85\xac\xe4\xb8\xbb', u'Harry': '\xe5\x93\x88\xe5\x88\xa9', u'Hassan': '\xe5\x93\x88\xe6\xa1\x91', u'Alceste': '\xe5\x88\x87\xe6\x96\xaf\xe7\x89\xb9', u'CW': 'CW', u'Rama': '\xe7\xbd\x97\xe6\x91\xa9', u'Rufus': '\xe9\xb2\x81\xe5\xbc\x97\xe6\x96\xaf', u'Tong': '\xe7\x94\xa8\xe9\x92\xb3\xe5\xad\x90\xe9\x92\xb3\xe8\xb5\xb7', u'Bell': '\xe8\xb4\x9d\xe5\xb0\x94', u'Birdy': '\xe9\xb8\x9f\xe4\xba\xba', u'Kimmy': '\xe5\x90\x89\xe7\xb1\xb3', u'Ali': '\xe9\x98\xbf\xe9\x87\x8c', u'okja': 'Okja', u'n': 'n', u'EXILETRIBE': 'exiletribe', u'MARS': '\xe7\x81\xab\xe6\x98\x9f', u'coco': '\xe5\x8f\xaf\xe5\x8f\xaf', u'Elise': '\xe7\x88\xb1\xe4\xb8\xbd\xe4\xb8\x9d', u'FBI': '\xe8\x81\x94\xe9\x82\xa6\xe8\xb0\x83\xe6\x9f\xa5\xe5\xb1\x80', u'AlirezaKhatami': '阿里哈塔米', u'MMA': 'MMA', u'Hayley': '\xe6\xb5\xb7\xe5\x88\xa9', u'ProtozoaPictures': 'protozoapictures', u'CeceliaAhern': '西西莉亚', u'Maise': '\xe7\x8e\x89\xe7\xb1\xb3', u'DJ': '\xe6\xb5\x81\xe8\xa1\x8c\xe9\x9f\xb3\xe4\xb9\x90\xe6\x92\xad\xe9\x9f\xb3\xe5\x91\x98', u'DH': 'DH', u'CJ': 'CJ', u'WALL': '\xe5\xa2\x99', u'TOP': '\xe9\xa1\xb6', u'DB': 'DB', u'DC': '\xe7\x9b\xb4\xe6\xb5\x81', u'IPSC': 'IPSC', u'BillMarks': '比尔·马克思', u'PlanB': '\xe8\xae\xa1\xe5\x88\x92', u'Noah': '\xe8\xaf\xba\xe4\xba\x9a', u'DV': '\xe6\x95\xb0\xe7\xa0\x81\xe6\x91\x84\xe5\x83\x8f', u'BFG': '\xe9\xab\x98\xe7\x82\x89\xe7\x85\xa4\xe6\xb0\x94', u'Moonee': '\xe5\xb9\x95\xe5\xbf\x86', u'AZT': 'AZT', u'Banana': '\xe9\xa6\x99\xe8\x95\x89', u'Janine': '\xe7\x8f\x8d\xe5\xa6\xae', u'Cheryl': '\xe8\xb0\xa2\xe4\xb8\xbd\xe5\xb0\x94', u'Michelangelo': '\xe7\xb1\xb3\xe5\x88\x87\xe6\x9c\x97\xe5\x9f\xba\xe7\xbd\x97', u'BATTLEOFTHESEXES': 'battleofthesexes', u'May': '\xe4\xba\x94\xe6\x9c\x88', u'NSA': '\xe5\x9b\xbd\xe5\xae\xb6\xe5\xae\x89\xe5\x85\xa8\xe5\xb1\x80', u'botak': '\xe5\x85\x89\xe5\xa4\xb4', u'Bobby': '\xe9\xb2\x8d\xe6\xaf\x94', u'Jasmine': '\xe8\x8c\x89\xe8\x8e\x89', u'Eleanor': '\xe5\x9f\x83\xe5\x88\xa9\xe8\xaf\xba', u'Poirot': '\xe6\x99\xae\xe7\x93\xa6\xe7\xbd\x97', u'DailyTopic': 'dailytopic', u'MV': 'MV', u'Mae': 'Mae', u'Jack': '\xe6\x9d\xb0\xe5\x85\x8b', u'Kim': '\xe5\x9f\xba\xe5\xa7\x86', u'Eva': '\xe4\xbc\x8a\xe5\xa8\x83', u'JACK': '\xe6\x9d\xb0\xe5\x85\x8b', u'TRF': '\xe6\x89\xb6\xe8\xbd\xae\xe5\x9f\xba\xe9\x87\x91\xe4\xbc\x9a', u'Ghost': '\xe9\xac\xbc', u'Phil': '\xe8\x8f\xb2\xe5\xb0\x94', u'E': 'E', u'BDSM': 'BDSM', u'NZT': '\xe6\x96\xb0\xe5\xbb\xba\xe8\xb4\xa6\xe6\x88\xb7', u'Kinki': '\xe8\xbf\x91\xe7\x95\xbf', u'M': 'M', u'L': 'l', u'Q': 'Q', u'JavierGull': '哈维尔', u'VR': '\xe8\x99\x9a\xe6\x8b\x9f\xe7\x8e\xb0\xe5\xae\x9e', u'Facemash': 'Facemash', u'Cindy': '\xe8\xbe\x9b\xe8\x92\x82', u'Miku': 'Miku', u'VX': 'VX', u'Susie': '\xe8\x8b\x8f\xe8\xa5\xbf', u'CD': '\xe5\x85\x89\xe7\x9b\x98', u'Agnan': '\xe9\x98\xbf\xe8\x94\xab', u'Mary': '\xe7\x8e\x9b\xe4\xb8\xbd', u'SOS': '\xe7\xb4\xa7\xe6\x80\xa5\xe6\xb1\x82\xe6\x95\x91\xe4\xbf\xa1\xe5\x8f\xb7', u'MLB': '\xe7\xbe\x8e\xe5\x9b\xbd\xe8\x81\x8c\xe6\xa3\x92\xe5\xa4\xa7\xe8\x81\x94\xe7\x9b\x9f', u'Osbourne': '\xe5\xa5\xa5\xe6\x96\xaf\xe6\x9c\xac', u'Billy': '\xe6\xaf\x94\xe5\x88\xa9', u'ChanelCresswell': '克雷斯·韦尔', u'Benz': '\xe8\x8b\xaf', u'MilaKunis': '\xe7\xb1\xb3\xe6\x8b\x89\xe5\xba\x93\xe5\xa6\xae\xe4\xb8\x9d', u'TheAgency': '\xe8\xaf\xa5\xe6\x9c\xba\xe6\x9e\x84', u'AbigailLawrie': '劳里', u'NASA': '\xe7\xbe\x8e\xe5\x9b\xbd\xe5\xae\x87\xe8\x88\xaa\xe5\xb1\x80', u'Big': '\xe5\xa4\xa7', u'Rekall': '\xe6\xa4\x8d\xe5\x85\xa5\xe8\xae\xb0\xe5\xbf\x86', u'RaymondBriggs': '雷蒙·布力格斯', u'NoahAshby': '诺亚·阿什比', u'Katie': '\xe5\x87\xaf\xe8\x92\x82', u'Erika': '\xe5\x9f\x83\xe9\x87\x8c\xe5\x8d\xa1', u'CharmingBird': 'charmingbird', u'Emoji': '\xe8\xa1\xa8\xe6\x83\x85\xe7\xac\xa6\xe5\x8f\xb7'}

new_name_dict = {
'MIKE': '迈克',
'Hal': '哈尔',
'SeanAmbrose': '肖恩安布罗斯',
'EmilBlonsky': '埃米',
'Alan': '艾伦',
'Wayne': '韦恩',
'Elias': '埃利亚斯',
'Mrs': '夫人',
'Sherry': '雪莉',
'Philippe': '菲利普',
'Driss': '德里斯',
'Samantha': '萨曼莎',
'Mew': '缪',
'Nana': '娜娜',
'Jennie': '珍妮',
'Shirley': '雪莉',
'Phil': '菲尔',
'Amir': '阿米尔',
'AbigailLawrie': '劳里',
'DragQueen': '变装皇后',
'Michelle': '米歇尔',
'HAL': '哈尔',
'NicoMirallegro': '尼克·迈瑞莱格伦',
'Virginian': '弗吉尼亚',
'Hancock': '汉考克',
'CateBlanchett': '凯特·布兰切特',
'Loser': '失败者',
'SolomonNorthup': '所罗门·诺瑟普',
'Delphine': '德尔菲娜',
'MadameM': 'M夫人',
'Elaine': '伊莱恩',
'EthanHunt': '伊森亨特',
'LuciaAniello': '露西娅',
'FrankAdler': '弗兰克·艾德勒',
'Summer': '夏天',
'Thomas': '托马斯',
'Kenny': '肯尼',
'Pim': '皮姆',
'Sam': '山姆',
'KarenSettman': '凯伦·赛特蒙',
'Zahra': '萨拉',
'Allen': '艾伦',
'Branson': '布兰森',
'Kimmy': '吉米',
'Clotaire': '克洛泰尔',
'MariaTura': '玛丽亚',
'AveryMartin': '埃弗里',
'WilliamParrish': '帕利斯',
'Colonel': '上校',
'Mark': '马克',
'peter': '彼得',
'Anne': '安妮',
'Andr': '安德烈',
'Avery': '埃弗里',
'Frank': '弗兰克',
'Susan': '苏珊',
'KenTaylor': '肯·泰勒',
'William': '威廉',
'fans': '球迷',
'Werner': '沃纳',
'Joe': '乔',
'Baby': '宝贝',
'Janine': '珍妮',
'Billy': '比利',
'Jeanne': '珍妮',
'Marty': '马蒂',
'Cheryl': '谢丽尔',
'ZOE': '佐伊',
'keiko': '惠子',
'Eudes': '厄德',
'Lena': '莱娜',
'Nina': '妮娜',
'coco': '可可',
'MAGI': '法师',
'Halley': '哈雷',
'David': '戴维',
'Anita': '安妮塔',
'JohnnieGray': '约翰尼',
'Amber': '安伯',
'ErikaKohut': '爱丽卡',
'Jasmine': '茉莉',
'Jimmy': '吉米',
'Dean': '院长',
'Bart': '巴特',
'Johnny': '约翰尼',
'JoeBlack': '乔·布莱克',
'Owen': '欧文',
'Ginger': '生姜',
'Kana': '假名',
'JohnConnor': '约翰·康纳',
'YOYO': '溜溜球',
'Scrooge': '斯克罗吉',
'Doug': '道格',
'JACK': '杰克',
'ChrisEvans': '克里斯·埃文斯',
'HowardHughes': '霍华德·休斯',
'Cindy': '辛蒂',
'Robert': '罗伯特',
'CeceliaAhern': '西西莉亚',
'EmmaStone': '艾玛·斯通',
'Geoffroy': '杰弗洛伊',
'Bronski': '布龙斯基',
'Ada': '艾达',
'Harry': '哈利',
'August': '八月',
'Margaret': '玛格丽特',
'JavierGull': '哈维尔',
'BlackStone': '黑石集团',
'Macy': '梅西',
'Amy': '艾米',
'Cipher': '密码',
'GiGi': '吉吉',
'Maise': '玉米',
'Moss': '苔藓',
'Hans': '汉斯',
'Beth': '贝丝',
'Jeannie': '珍妮',
'TheOrigin': '起源',
'BoBo': '波波',
'Maggie': '麦琪',
'Ben': '本',
'Patrick': '帕特里克',
'LeightonMeester': '莉顿·梅斯特',
'Stu': '斯图',
'GPS': '全球定位系统',
'Susie': '苏西',
'Rapunzel': '长发公主',
'Hassan': '哈桑',
'Rama': '罗摩',
'Rufus': '鲁弗斯',
'Tong': '用钳子钳起',
'Bell': '贝尔',
'Ali': '阿里',
'CD': '光盘',
'Tony': '托尼',
'Elise': '爱丽丝',
'FBI': '联邦调查局',
'AlirezaKhatami': '阿里哈塔米',
'Baxter': '巴克斯特',
'Hayley': '海利',
'Tim': '提姆',
'BillMarks': '比尔·马克思',
'PlanB': 'B计划',
'Noah': '诺亚',
'Moonee': '幕忆',
'Banana': '香蕉',
'Georges': '乔治斯',
'JosephTura': '约瑟夫·图拉',
'Michelangelo': '米切朗基罗',
'John': '约翰',
'Club': '俱乐部',
'Bobby': '鲍比',
'Molly': '莫莉',
'Poirot': '普瓦罗',
'MV': 'MV',
'Jordan': '乔丹',
'Jack': '杰克',
'Kim': '基姆',
'Eva': '伊娃',
'SteveCarell': '史蒂夫·卡瑞尔',
'Agnan': '阿蔫',
'Netflix': '网飞公司',
'Birdy': '鸟人',
'Jackie': '杰基',
'Nancy': '南希',
'May': '五月',
'Eleanor': '埃利诺',
'Alceste': '切斯特',
'Mary': '玛丽',
'Osbourne': '奥斯本',
'ChanelCresswell': '克雷斯·韦尔',
'MilaKunis': '米拉库妮丝',
'RaymondBriggs': '雷蒙·布力格斯',
'NoahAshby': '诺亚·阿什比',
'Katie': '凯蒂',
'Erika': '埃里卡',
'Grace': '格雷斯'


}
add_word_dict = {
'WhereRainbowsEnd':'彩虹尽头',
'Dak': '达克',
'Wasabi': '芥末',
'botak': '光头',
'Geta': '耶塔',
'Cure': '治愈',
'cm': '厘米',
'Facemash': '脸谱',
'Ghost': '鬼魂',
'Miku': '米古',
'EXILETRIBE': '放浪家族',
'yoyo': '悠悠',
'BATTLEOFTHESEXES': '性别之战',
'okja': '',
'Mae': '梅',
'OL': '白领女性',
'DailyTopic': '每日话题',
'TheAgency': '黑暗代理人',
'THEENDOFTHEWORLD': '世界末日',
'Benji': '笨',
'CharmingBird': '迷人女郎',
'SEELE': '西尔',
'Kinki': '近畿',
'Mi': '米',
'MiniMo': '迷你魔',
'gonein60seconds': '60秒神偷手',
'Nyah': '恩娅',
'Benz': '奔驰',
'Gifted': '天才少女',
'MyWay': '迈威',
'Emoji': '表情',
'ProtozoaPictures': '原生影业',
}