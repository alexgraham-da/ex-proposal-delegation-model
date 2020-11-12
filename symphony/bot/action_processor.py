import sys
import traceback
import xml.etree.ElementTree as ET
import logging
import base64
import json
from grpc import RpcError
from grpc.aio import  AioRpcError

from dazl import ContractId, AIOPartyClient
import dazl

import logging
import ast
import json
from .model import SYMPHONY, COMPANY, PROPOSAL
from .symphony_integration import SymphonyIntegration
from .render import render_propose_form, render_review_form
from .utils import Utils
from .model import COMPANY, PROPOSAL

class ElementAction:
    username: str
    stream_id: str
    form_id: str
    form_action: str
    contents: dict
    def __init__(self, action):
        self.username = action['symphonyUser']
        self.stream_id = action['symphonyStreamId']
        self.form_id = action['formId']
        self.form_action = action['action']
        self.contents = json.loads(action['formJSON'])

class ActionProcessor:

    def __init__(self, dazl_client: AIOPartyClient, symphony_int: SymphonyIntegration):
        self.dazl_client = dazl_client
        self.symphony_int = symphony_int
        self.action_processed_message = Utils.format_message('Your action has been processed.')

    async def process_im_action(self, action_contract):
        action = ElementAction(action_contract)
        logging.debug('action_processor/im_process')

        id_split = action.form_id.split('::')
        form_id = id_split[0]

        processor = {
            'proposal_form_id': self.process_proposal_form,
            'review_form_id': self.process_review_form
        }.get(form_id, self.process_default)

        await processor(action, id_split)

    async def process_proposal_form(self, action, id_split):
        button_action = action.form_action
        form_contents = action.contents
        username = action.username

        if button_action == 'submit_button':
            self.response_message = Utils.format_message('Proposal submitted!')
            proposed_to = form_contents['propose_to']
            proposal = form_contents['proposal']
            args = dict(employeeEmail = username, proposedTo = proposed_to, proposalText = proposal)
            party = self.dazl_client.party
            try:
                await self.dazl_client.submit_exercise_by_key(COMPANY.CompanySymphony, party, 'CompanySymphony_MakeProposal', args)
            except AioRpcError as err:
                self.response_message = Utils.format_message(f'Command failed: {err.details()}')

        self.symphony_int.send_message(action.stream_id, self.response_message)

    async def process_review_form(self, action, id_split):
        button_action = action.form_action

        cid = id_split[1]
        tid = id_split[2]

        contractId = ContractId(cid, tid)
        delegated_proposal = self.dazl_client.find_by_id(contractId)
        proposal_data = delegated_proposal.cdata['proposal']
        (proposal_cid, _) = await self.dazl_client.find_one(PROPOSAL.Proposal, proposal_data)

        if button_action == 'accept_button':
            try : self.dazl_client.submit_exercise(proposal_cid, 'Proposal_Accept')
            except Exception as x: print(x)
            self.response_message = Utils.format_message('Accepted!')

        elif button_action == 'reject_button':
            try: self.dazl_client.submit_exercise(proposal_cid, 'Proposal_Reject')
            except Exception as x : print(x)
            self.response_message = Utils.format_message('Rejected!')

        self.symphony_int.send_message(action.stream_id, self.response_message)

    async def process_default(self, action, id_split):
        logging.debug('Unknown form')

