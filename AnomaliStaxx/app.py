import logging
from apps import App, action
import requests



logger = logging.getLogger(__name__)


class AnomaliStaxx(App):

    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.api_key = self.device_fields['key']

    @action
    def export_indicators(self, search=None proxy=None):
        pass
