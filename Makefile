build:
	daml build

run_daml_script: build
	daml script --participant-config dabl/participants.json --json-api --dar .daml/dist/proposal-model-0.0.1.dar --script-name Setup:initialize --input-file dabl/ledger-parties.json

run_daml_script_local: build
	daml script --dar .daml/dist/proposal-model-0.0.1.dar --script-name Setup:initialize --ledger-host localhost --ledger-port 6865 --input-file dabl/ledger-parties-local.json
