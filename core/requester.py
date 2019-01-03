import random
import requests
import time
from urllib3.exceptions import ProtocolError
import warnings

from core.colors import bad, info
import core.config
from core.config import globalVariables
from core.utils import converter, logger

warnings.filterwarnings('ignore')  # Disable SSL related warnings


def requester(url, data, headers, GET, delay, timeout):
    if core.config.globalVariables['jsonData']:
        data = converter(data)
    elif core.config.globalVariables['path']:
        url = converter(data, url)
        data = []
        GET, POST = True, False
    time.sleep(delay)
    user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991']
    if 'User-Agent' not in headers:
        headers['User-Agent'] = random.choice(user_agents)
    elif headers['User-Agent'] == '$':
        headers['User-Agent'] = random.choice(user_agents)
    if core.config.globalVariables['debug']:
        logger(url, flag='debug', variable='url', function='requester')
        logger(GET, flag='debug', variable='GET', function='requester')
        logger(data, flag='debug', variable='data', function='requester')
        logger(headers, flag='debug', variable='headers', function='requester')
    try:
        if GET:
            response = requests.get(url, params=data, headers=headers,
                                    timeout=timeout, verify=False, proxies=core.config.proxies)
        else:
            response = requests.post(url, data=data, headers=headers,
                                     timeout=timeout, verify=False, proxies=core.config.proxies)
        return response
    except ProtocolError:
        logger('%s WAF is dropping suspicious requests.')
        logger('%s Scanning will continue after 10 minutes.')
        time.sleep(600)
