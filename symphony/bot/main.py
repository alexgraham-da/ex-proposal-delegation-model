import os
import sys
import asyncio
import logging

from grpc import RpcError
from grpc.aio import  AioRpcError

import dazl
from dazl import AIOPartyClient, exercise

from im_listener import IMListener
from action_processor import ActionProcessor
from symphony_integration import SymphonyIntegration
from utils import Utils
from model import (
    SYMPHONY,
    PROPOSAL,
    COMPANY,
    NOTIFICATION
)

dazl.setup_default_logger(logging.INFO)

def main():
    logging.info("starting...")
    # load DAZL
    party = os.getenv('DAML_LEDGER_PARTY')
    party = "Bot" if not party else party

    url = os.getenv('DAML_LEDGER_URL')
    network = dazl.Network()
    network.set_config(url=url)

    async_client = setup_client(network, party)
    try:
        network.run_forever()
    except (KeyboardInterrupt, SystemExit):
        None
    except:
        raise


def setup_client(network, party) -> AIOPartyClient:
    client = network.aio_party(party)
    symphony_int = SymphonyIntegration(client)
    im_listener = IMListener(client, symphony_int)
    action_processor = ActionProcessor(client, symphony_int)

    @client.ledger_ready()
    async def say_hello(event):
        logging.info("Connected to proposal model!")

    @client.ledger_created(SYMPHONY.InboundDirectMessage)
    async def handle_inbound_message(event):
        logging.info(f"incoming message {event}")
        await im_listener.on_im_message(event.cdata)
        return [exercise(event.cid, 'Archive', {})]

    @client.ledger_created(SYMPHONY.InboundElementAction)
    async def handle_inbound_element_action(event):
        logging.info(f"incoming action {event}")
        await action_processor.process_im_action(event.cdata)
        return [exercise(event.cid, 'Archive', {})]


    @client.ledger_created(NOTIFICATION.Notification)
    async def handle_notification(event):
        logging.info('processing notification...')
        receiver = event.cdata['receiver']
        sender = event.cdata['sender']
        notification_message = event.cdata['message']
        logging.info(f'receiver: {receiver}')
        logging.info(f'sender: {sender}')
        employees = client.find_active(COMPANY.Employee, dict(party = receiver))
        if not (not employees):
            (_, employee_contract) = await client.find_one(COMPANY.Employee, dict(party = receiver))
            email = employee_contract['email']
            user_streams = client.find_active(SYMPHONY.UserStream, dict(username = email))

            for _, user_stream in user_streams.items():
                message = Utils.format_message(f'<b>Notification received:</b> {notification_message}')
                symphony_int.send_message(user_stream['streamId'], message)

    @client.ledger_created(PROPOSAL.DelegatedProposal)
    async def handle_delegated_proposal(event):
        employee_party = event.cdata['employee']
        proposal = event.cdata['proposal']
        proposer = proposal['proposer']

        employees = client.find_active(COMPANY.Employee, dict(party = employee_party))
        if not (not employees):
            (_, employee_contract) = await client.find_one(COMPANY.Employee, dict(party = employee_party))
            email = employee_contract['email']
            user_streams = client.find_active(SYMPHONY.UserStream, dict(username = email))

            for _, user_stream in user_streams.items():
                message = Utils.format_message(f'<b>New proposal received from:</b> {proposer}.')
                symphony_int.send_message(user_stream['streamId'], message)
    return client

if __name__ == "__main__":
    main()
