import time
import logging
from apps import App, action
import requests

logger = logging.getLogger(__name__)

class OpenPhish(App):
    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.feed_url = 'https://openphish.com/feed.txt'

    @action
    def fetch_list(self):
        response = requests.get(self.feed_url)
        return [line for line in response.text]

