import logging
from apps import App, action
import requests

logger = logging.getLogger(__name__)

class VirusTotal(App):
    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.url = 'https://www.virustotal.com/vtapi/v2/file/report'
        
        print(self.device_fields)
        self.api_key = self.device_fields['api_key']

    @action
    def search_hash(self, file_hash):
        params = {'apikey': self.api_key, 'resource': file_hash}
        response = requests.get(self.url, params=params, proxies=self.proxy).json()
        return response
