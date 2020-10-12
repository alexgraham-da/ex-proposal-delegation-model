#!/bin/bash

PARTY=${1}
daml build
daml trigger --dar .daml/dist/proposal-trigger-0.0.1.dar --trigger-name ProposalTrigger:handleProposals --ledger-host localhost --ledger-port 6865 --ledger-party $PARTY
