# coding=utf-8
# author=XingLong Pan
# date=2016-12-04

# 豆瓣电影的登录入口页面
DOUBAN_MOVIE_LOGIN_URL = 'https://accounts.douban.com/login'

# 搜索引擎（SEO爬虫）的请求头
USER_AGENT = [
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
        'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
        'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)'
    ]
AGENT_SIZE = 7

# 延时设置
DELAY_MIN_SECOND = 1
DELAY_MAX_SECOND = 2

# 豆瓣电影的url前缀
URL_PREFIX = 'https://movie.douban.com/subject/'
URL_MOVIE_TYPE = 'https://movie.douban.com/j/new_search_subjects'
URL_MOVIE_TYPE_OLD = 'https://movie.douban.com/j/search_subjects'
URL_COMMENTS_FORMAT = 'https://movie.douban.com/subject/%s/comments?status=P'
ALL_FORMS = [u'电影', u'电视剧', u'综艺', u'动画', u'纪录片', u'短片']
ALL_TYPES = [u'剧情', u'爱情', u'喜剧', u'科幻', u'动作', u'悬疑', u'犯罪', u'恐怖', u'青春', u'励志', u'战争', u'文艺', u'黑色幽默', u'传记', u'情色', u'暴力', u'音乐', u'家庭']
ALL_AREAS = [u'大陆', u'美国', u'香港', u'台湾', u'日本', u'韩国', u'英国', u'法国', u'德国',u'意大利', u'西班牙', u'印度', u'泰国', u'俄罗斯', u'伊朗', u'加拿大', u'澳大利亚', u'爱尔兰', u'瑞典', u'巴西', u'丹麦']
COMMENT_RATING_DICT = {
    u'很差': 1,
    u'较差': 2,
    u'还行': 3,
    u'推荐': 4,
    u'力荐': 5
}
"""
这里用到了阿布云代理动态版。使用影梭或者其他代理，甚至不用代理也可以
"""
# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HT1LX50X8R4P0I8D"
proxyPass = "1133BD889583B72A"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
