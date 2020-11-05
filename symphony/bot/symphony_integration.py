import dazl
from dazl import AIOPartyClient, create, exercise

from model import SYMPHONY

class SymphonyIntegration:
    def __init__(self, dazl_client: AIOPartyClient):
        self.dazl_client = dazl_client

    def send_message(self, stream_id, msg):
        self.dazl_client.submit_create(SYMPHONY.OutboundMessage, {
                    'integrationParty': self.dazl_client.party,
                    'symphonyStreamId': stream_id,
                    'messageText': msg,
                    'attemptCount': 0})


    # def store_message(msg):



        # self.dazl_client.submit_create(SYMPHONY.InboundDirectMessage, {
        #             'integrationParty': self.integration_party,
        #             'symphonyChannel': first_name,
        #             'symphonyUser': username,
        #             'symphonyStreamId': stream_id,
        #             'messageText': msg_text})
