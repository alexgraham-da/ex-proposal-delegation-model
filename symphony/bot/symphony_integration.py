import dazl
from dazl import AIOPartyClient

from .model import SYMPHONY, COMPANY

class SymphonyIntegration:
    def __init__(self, dazl_client: AIOPartyClient):
        self.dazl_client = dazl_client

    def send_message(self, stream_id, msg):
        self.dazl_client.submit_create(SYMPHONY.OutboundMessage, {
                    'integrationParty': self.dazl_client.party,
                    'symphonyStreamId': stream_id,
                    'messageText': msg,
                    'attemptCount': 0})

    async def run_for_employee(self, employee_party, fn):
        employees = self.dazl_client.find_active(COMPANY.Employee, dict(party = employee_party))
        if not (not employees):
            (_, employee_contract) = await self.dazl_client.find_one(COMPANY.Employee, dict(party = employee_party))
            email = employee_contract['email']
            user_streams = self.dazl_client.find_active(SYMPHONY.UserStream, dict(username = email))

            for _, user_stream in user_streams.items(): fn(user_stream)
