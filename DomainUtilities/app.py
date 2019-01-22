import re
import time
import logging
import socket

import tldextract

from apps import App, action

logger = logging.getLogger(__name__)

class DomainUtilities(App):
    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)


    @action
    def extract_urls_from_text(self, text):
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

    @action
    def hostname_from_url(self, url):
        extracted = tldextract.extract(url)
        return '.'.join(extracted)

    
    @action
    def tld_from_domain(self, domain):
        return tldextract.extract(domain).suffix

    @action
    def resolve_ip_for_host(self, hostname):
        return socket.gethostbyname(hostname)
    