from exchangelib import Credentials, Account, Configuration, DELEGATE
from exchangelib.protocol import NoVerifyHTTPAdapter, BaseProtocol
import os

# Don't verify cert, this should be removed if the certificate has been installed in the trust store
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

class ExchangeWebServices(App):
    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.credentials = Credentials(self.device_fields['username'], self.device.get_encrypted_field('password'))
        self.config = Configuration(self.device_fields['ews_host'], credentials=self.credentials)
        self.account = Account(primary_smtp_address=self.device_fields['inbox'], config=config,autodiscover=False, access_type=DELEGATE)
    
    @action
    def read_message(self, item_id):
        email = self.account.inbox.get(item_id=item_id)
        return {
            'item_id': email.item_id,
            'subject': email.subject,
            'sender': email.sender,
            'body': email.body,
            'categories': email.categories,
            'headers': email.headers
        }

    @action
    def move_message(self, item_id, folder):
        email = email = self.account.inbox.get(item_id=item_id)
        to_folder = self.account.inbox / folder
        email.move(to_folder)
        return 'Successfully moved email to %s' % (folder)

    @action
    def delete_message(self, item_id):
        email = self.account.inbox.get(item_id=item_id)
        email.move_to_trash()
        return 'Successfully moved message to Deleted Items'

    @action
    def hard_delete_message(self, item_id):
        email = self.account.inbox.get(item_id=item_id)
        email.delete()
        return 'Successfully deleted message'2

    @action
    def categorize_message(self, item_id, categories):
        email = self.account.inbox.get(item_id=item_id)
        email.categories = categories
        email.save()
        return 'Email categorized successfully'

    @action
    def get_message_attachments(self, item_id):
        email = self.account.inbox.get(item_id=item_id)
        for attachment in email.attachments:
            print(attachment.content)

    @action
    def get_inbox_folders(self, pattern=None):
        return [f.name for f in self.account.inbox.glob(pattern)]

    @action
    def get_inbox_messages(self):
    messages = []
    for item in self.account.inbox.all().order_by('-datetime_received'):
        messages.append({
            'item_id': item.item_id,
            'subject': item.subject,
            'sender': item.sender,
            'body': item.body
        })
    return messages

    @action
    def get_oldest_inbox_message(self)
        email = self.account.inbox.all().order_by('datetime_received')[0]
        return email.item_id

    @action
    def get_newest_inbox_message(self)
        email = self.account.inbox.all().order_by('-datetime_received')[0]
        return email.item_id