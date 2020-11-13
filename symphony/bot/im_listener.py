import logging
import ast
import json
from .model import SYMPHONY, COMPANY, PROPOSAL
from .symphony_integration import SymphonyIntegration
from .render import render_propose_form, render_review_form, render_registration_form
from .utils import Utils

class IMListener():
    def __init__(self, dazl_client, symphony_int: SymphonyIntegration):
        self.dazl_client = dazl_client
        self.symphony_int = symphony_int

    async def on_im_message(self, msg):
        username = msg['symphonyUser']
        stream_id = msg['symphonyStreamId']

        user_args = dict(username = username, integration = self.dazl_client.party)
        user_streams = self.dazl_client.find_active(SYMPHONY.UserStream, user_args)
        if not user_streams:
            self.dazl_client.submit_create(SYMPHONY.UserStream, {
                        'integration': self.dazl_client.party,
                        'username': username,
                        'streamId': stream_id})

        await self.process_im(msg)

    async def process_im(self, msg):
        self.help_message = '/propose, /review, or /clear'

        commands = ast.literal_eval(msg['messageText'])# .split()
        stream_id = msg['symphonyStreamId']
        username = msg['symphonyUser']
        logging.info(f"message is {commands}, user is {username}")

        if commands[0] == '/propose':
            self.message_to_send = render_propose_form()
        elif commands[0] == '/register':
            self.message_to_send = render_registration_form()
        elif commands[0] == '/review':
            (_, employee_contract) = await self.dazl_client.find_one(COMPANY.Employee, dict(email = username))
            proposals = self.dazl_client.find_active(PROPOSAL.DelegatedProposal, dict(employee = employee_contract['party']))

            for contractId, cdata in proposals.items():
                cid = contractId.contract_id
                tid = contractId.template_id
                proposalText = cdata['proposal']['proposal']
                proposer = cdata['proposal']['proposer']
                current_form = render_review_form(proposalText, proposer, cid, tid)
                self.symphony_int.send_message(stream_id, current_form)
            if not proposals:
                self.message_to_send = Utils.format_message('No proposals to review.')
            else:
                self.message_to_send = Utils.format_message('Done listing proposals.')
        elif commands[0] == '/clear':
            self.message_to_send = Utils.format_message('<br/><br/><br/><br/><br/><br/><br/>')
        else:
            self.message_to_send = self.help_message

        self.symphony_int.send_message(stream_id, self.message_to_send)
