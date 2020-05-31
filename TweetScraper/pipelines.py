# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings
import logging
import json
import os

from data_mining.TweetScraper.TweetScraper.items import Tweet
from data_mining.TweetScraper.TweetScraper.utils import mkdirs

SETTINGS = get_project_settings()

logger = logging.getLogger(__name__)


# class SaveToFilePipeline(object):
#     ''' pipeline that save data to disk '''
#     def __init__(self):
#         self.saveTweetsPath = SETTINGS['SAVE_TWEET_PATH']
#         self.filename
#         mkdirs(self.saveTweetPath) # ensure the path exists
#
#     def process_item(self, item, spider):
#         if isinstance(item, Tweet):
#             self.save_to_file(item,)
#             logger.debug("Add tweet:%s" %item['url'])
#         else:
#             logger.info("Item type is not recognized! type = %s" %type(item))
#
#     def save_to_file(self, item, fname):
#         ''' input:
#                 item - a dict like object
#                 fname - where to save
#         '''
#         with open(fname, 'w', encoding='utf-8') as f:
#             json.dump(dict(item), f, ensure_ascii=False)
