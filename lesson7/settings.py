BOT_NAME = 'books-scraper'

ITEM_PIPELINES = {
    'pipelines.SaveProductPipeline': 300,
    'pipelines.SavePhotosPipeline': 200,
}

IMAGES_STORE = 'files/product_photos'

LOG_ENABLE = True
LOG_LEVEL = 'DEBUG'

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1
COOKIES_ENABLED = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 ' \
             'Safari/605.1.15'
