import logging
from apps import App, action
import requests

logger = logging.getLogger(__name__)

class VirusTotal(App):
    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.url = 'https://www.virustotal.com/vtapi/v2/file/report'
        self.proxy = None
        if (self.device_fields['proxy_address'] and self.device_fields['proxy_port']):
            self.proxy = {
                        'http': 'http://%s:%s' % (self.device_fields['proxy_address'], self.device_fields['proxy_port']),
                        'https': 'https://%s:%s' % (self.device_fields['proxy_address'], self.device_fields['proxy_port']),
                    }
        self.api_key = self.device.get_encrypted_field('api_key')

    @action
    def search_hash(self, file_hash):
        params = {'apikey': self.api_key, 'resource': file_hash}
        response = requests.get(self.url, params=params, proxies=self.proxy).json()
        return response
