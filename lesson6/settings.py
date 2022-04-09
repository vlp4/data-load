BOT_NAME = 'books-scraper'

ITEM_PIPELINES = {
    'pipelines.BooksPipeline': 100
}

LOG_ENABLE = True
LOG_LEVEL = 'DEBUG'

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 10
DOWNLOAD_DELAY = 1
COOKIES_ENABLED = False
USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.4) Gecko/20070508 Iceweasel/2.0.0.4 ' \
    '(Debian-2.0.0.4-1; F*** Firefox/2.0) (India; Papa; Victor; 6)'
