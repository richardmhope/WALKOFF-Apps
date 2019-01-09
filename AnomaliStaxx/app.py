import logging
from apps import App, action
import requests

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)


class AnomaliStaxx(App):

    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.base_url = 'https://10.170.27.107:8080/api/v1/'
        self.headers = {'content-type': 'application/json'}
        self.api_key = self.device_fields['key']

    def authenticate(user, password):
        url = BASE_URL + 'login'
        data  = json.dumps({'username':user, 'password':password})
        request = requests.post(url, data=data, headers=HEADERS, verify=False)
        if request.status_code == 200:
            return request.json()['token_id']

    @action
    def export_indicators(self, search=None proxy=None):
        url = BASE_URL + 'intelligence'
        data = json.dumps({'token':token, 'query':query, 'type':'json'})
        request = requests.post(url, data=data, headers=HEADERS, verify=False)
        if request.status_code == 200:
            return request.json