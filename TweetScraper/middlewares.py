# -*- coding: utf-8 -*-
import time
from random import randint

from scrapy import signals
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import Popularity, SoftwareType, HardwareType, SoftwareName, OperatingSystem
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from w3lib.http import basic_auth_header
from socket import gethostbyname

from scrapy.utils.project import get_project_settings

settings = get_project_settings()
LUMINATI_USER = settings.get("LUMINATI_PROXY_LOGIN", '')
LUMINATI_PASS = settings.get("LUMINATI_PROXY_PASS", '')

class LuminatiProxy(object):
    """
        Class to use Luminati.io proxy
    """
    login_temp = "lum-customer-{user}-zone-static-session-{n}"

    user = LUMINATI_USER
    password = LUMINATI_PASS

    def process_request(self, request, spider):
        session = request.meta.get('cookiejar', randint(0, 9999))

        request.meta["proxy"] = "http://zproxy.lum-superproxy.io:22225"
        request.headers["Proxy-Authorization"] = basic_auth_header(
            self.login_temp.format(user=self.user, n=session),
            self.password
        )
        return None


class LuminatiProxyUS(LuminatiProxy):
    login_temp = "lum-customer-{user}-zone-static-session-{n}-country-us"


class LuminatiProxyResidentalStatic(LuminatiProxy):
    login_temp = "lum-customer-{user}-zone-static_residental-session-{n}"



class RandomUserAgentMiddleware(object):
    def __init__(self, *args, **kwargs):
        pupularity = [
            Popularity.POPULAR.value,
            # Popularity.COMMON.value
        ]
        hardware_types = [
            HardwareType.COMPUTER.value,
        ]
        software_types = [SoftwareType.WEB_BROWSER.value]
        software_names = [SoftwareName.FIREFOX.value]
        operating_system = [OperatingSystem.WINDOWS]
        self.user_agent_rotator = UserAgent(
            software_types=software_types,
            hardware_types=hardware_types,
            pupularity=pupularity,
            software_names=software_names,
            operating_system=operating_system
        )
        self.session = 1
        self.user_agent = self.user_agent_rotator.get_random_user_agent()

    def process_request(self, request, spider):
        session = request.meta.get("cookiejar")
        if session:
            if session != self.session:
                self.session = session
                self.user_agent = self.user_agent_rotator.get_random_user_agent()
            request.headers['User-Agent'] = self.user_agent
        else:
            request.headers['User-Agent'] = self.user_agent_rotator.get_random_user_agent()
        return None


class TooManyRequestsRetryMiddleware(RetryMiddleware):

    def __init__(self, crawler):
        super(TooManyRequestsRetryMiddleware, self).__init__(crawler.settings)
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        elif response.status == 429:
            self.crawler.engine.pause()
            time.sleep(60) # If the rate limit is renewed in a minute, put 60 seconds, and so on.
            self.crawler.engine.unpause()
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        elif response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response