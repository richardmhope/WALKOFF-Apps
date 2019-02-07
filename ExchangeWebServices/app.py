from apps import App, action
from exchangelib import Credentials, Account, Configuration, DELEGATE, ItemAttachment, Message
from exchangelib.protocol import NoVerifyHTTPAdapter, BaseProtocol
import os

# Don't verify cert, this should be removed if the certificate has been installed in the trust store
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

class ExchangeWebServices(App):
    def __init__(self, name, device, context):
        App.__init__(self, name, device, context)
        self.username = self.device_fields['username']
        self.password = self.device.get_encrypted_field('password')
        self.host = self.device_fields['host']
        self.inbox = self.device_fields['inbox']

        self.credentials = Credentials(self.username, self.password)
        self.config = Configuration(server=self.host, credentials=self.credentials)
        
        # Setting this here causes an error, it needs to be in each action because reasons...
        #self.account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
    
    @action
    def read_message(self, item_id):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
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
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
        to_folder = self.account.inbox / folder
        email.move(to_folder)
        return 'Successfully moved email to %s' % (folder)

    @action
    def delete_message(self, item_id):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
        email.move_to_trash()
        return 'Successfully moved message to Deleted Items'

    @action
    def hard_delete_message(self, item_id):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
        email.delete()
        return 'Successfully deleted message'

    @action
    def categorize_message(self, item_id, categories):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
        email.categories = categories
        email.save()
        return 'Email categorized successfully'

    @action
    def get_attachment_count(self, item_id):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
        return len(email.attachments)
    
    @action
    def attachment_is_message(self, item_id):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
        attachment = email.attachments[0]
        if isinstance(attachment, ItemAttachment):
            if isinstance(attachment.item, Message):
                return True
        else:
            return False

    @action 
    def get_message_attachment(self, item_id):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
        attachment = email.attachments[0]
        return {
            'subject': attachment.item.subject,
            'sender': attachment.item.sender,
            'body': attachment.item.body,
            'categories': attachment.item.categories,
            'headers': attachment.item.headers
        }


    @action
    def get_message_attachments(self, item_id):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.get(item_id=item_id)
        for attachment in email.attachments:
            print(attachment.content)

    @action
    def get_inbox_folders(self, pattern=None):
        return [f.name for f in self.account.inbox.glob(pattern)]

    @action
    def get_inbox_messages(self):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        messages = []
        for item in account.inbox.all().order_by('-datetime_received'):
            messages.append({
                'item_id': item.item_id,
                'subject': item.subject,
                'sender': item.sender,
                'body': item.body
            })
        return messages

    @action
    def get_oldest_inbox_message(self):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.all().order_by('datetime_received')[0]
        return email.item_id

    @action
    def get_newest_inbox_message(self):
        account = Account(primary_smtp_address=self.inbox, config=self.config, autodiscover=False, access_type=DELEGATE)
        email = account.inbox.all().order_by('-datetime_received')[0]
        return email.item_id