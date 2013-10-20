# coding=utf-8

import urllib
import logging
from bs4 import BeautifulSoup

# define default values which would be used in other not specified in config file
DEFAULT_SEARCH_URL = "http://80.91.187.254:8080/servlet/SMCSearch2?lang=ua&barcode="

logger = logging.getLogger('tracker')

class Tracker:
    def __init__(self, config):
        # initialize default values
        self.searchUrl = DEFAULT_SEARCH_URL

        # override default values with values from config file
        self._process_config(config)

    def _process_config(self, config):
        if config.has_option("tracker", "search_url"):
            self.searchUrl = config.get("tracker", "search_url")

    def get_status_all(self, postCodes):
        logger.debug("+ getStatusAll(), post_codes = " + postCodes)

        resultList = []
        for post_code in postCodes:
            status = self.get_status()
            resultList.append({"code": post_code, "status": status})

        logger.debug("- getStatusAll(), result_list = " + resultList)
        return resultList


    def get_status(self, postCode):
        pageText = self._get_search_results_page(postCode)
        parser = BeautifulSoup(pageText)
        statusDiv = parser.find("div", style="text-align:center;padding:10px;")
        if statusDiv is None:
            logger.error(u"statusDiv was not found for postCode = " + postCode)
            return None
        return statusDiv.text.strip()

    def _get_search_results_page(self, postCode):
        """  """
        url = self.searchUrl + postCode
        logger.debug(u"open url \"" + url + "\"")
        page = urllib.urlopen(url)
        if page is None:
            logger.error(u"fail to open page with url \"" + url + "\"")
            return None
        text = page.read()
        # parser = BeautifulSoup(text)
        # if parser.find("div", class_="no-hits-search"):
        #     #_print(u"sku " + skuCode + u": поиск на сайте не дал результата (" + page.geturl() + u")")
        #     return None
        return text
