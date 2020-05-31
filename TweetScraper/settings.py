# -*- coding: utf-8 -*-

# !!! # Crawl responsibly by identifying yourself (and your website/e-mail) on the user-agent
#USER_AGENT = 'TweetScraper'

# settings for spiders
BOT_NAME = 'TweetScraper'
LOG_LEVEL = 'INFO'
DOWNLOAD_HANDLERS = {'s3': None}  # from http://stackoverflow.com/a/31233576/2297751, TODO

SPIDER_MODULES = ['TweetScraper.spiders']
NEWSPIDER_MODULE = 'TweetScraper.spiders'
# ITEM_PIPELINES = {
#     'TweetScraper.pipelines.SaveToFilePipeline': 100,
#     #'TweetScraper.pipelines.SaveToMongoPipeline': 100, # replace `SaveToFilePipeline` with this to use MongoDB
#     #'TweetScraper.pipelines.SavetoMySQLPipeline': 100, # replace `SaveToFilePipeline` with this to use MySQL
# }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    #'TweetScraper.middlewares.TooManyRequestsRetryMiddleware': 543,
    'TweetScraper.middlewares.LuminatiProxy': 500,
    'TweetScraper.middlewares.RandomUserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
# settings for where to save data on disk
SAVE_TWEET_PATH = './data/tweets/'
FEED_EXPORT_ENCODING = 'utf-8'

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
