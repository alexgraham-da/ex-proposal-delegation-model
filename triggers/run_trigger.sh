#!/bin/bash

PARTY=${1}
daml build
while ! nc -z localhost 6865; do sleep 1; done
daml trigger --dar .daml/dist/proposal-trigger-0.0.2.dar --trigger-name ProposalTrigger:handleProposals --ledger-host localhost --ledger-port 6865 --ledger-party $PARTY
