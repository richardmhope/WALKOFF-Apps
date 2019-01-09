import logging
from apps import App, action
import requests

logger = logging.getLogger(__name__)

class VirusTotal(App):
    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.url = 'https://www.virustotal.com/vtapi/v2/file/report'
        
        if self.proxy_address and self.proxy_port:
            self.proxy = {
                        'http': 'http://%s:%s' % (self.device.proxy_address, self.device.proxy_port),
                        'https': 'https://%s:%s' % (self.device.proxy_address, self.device.proxy_port),
                    }
        self.api_key = self.device_fields['api_key']

    @action
    def search_hash(self, file_hash=None):
        params = {'apikey': self.api_key, 'resource': file_hash}
        response = requests.get(self.url, params=params, proxies=self.proxy).json()
        return response
