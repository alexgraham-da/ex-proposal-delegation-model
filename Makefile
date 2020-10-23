.PHONY: package
model_dar_version := $(shell grep "^version" daml.yaml | sed 's/version: //g')
trigger_dar_version := $(shell grep "^version" triggers/daml.yaml | sed 's/version: //g')

state_dir := .dev
trigger_build_log = $(state_dir)/trigger_build.log
daml_build_log = $(state_dir)/daml_build.log
sandbox_pid := $(state_dir)/sandbox.pid
sandbox_log := $(state_dir)/sandbox.log

trigger_a_pid := $(state_dir)/trigger_a.pid
trigger_a_log := $(state_dir)/trigger_a.log

trigger_b_pid := $(state_dir)/trigger_b.pid
trigger_b_log := $(state_dir)/trigger_b.log

.PHONY: clean

$(state_dir):
	mkdir $(state_dir)

$(daml_build_log): |$(state_dir)
	daml build > $(daml_build_log)

$(trigger_build_log): |$(state_dir)
	cd triggers && daml build > ../$(trigger_build_log)

$(sandbox_pid): |$(daml_build_log)
	daml start > $(sandbox_log) & echo "$$!" > $(sandbox_pid)
	# daml sandbox .daml/dist/proposal-model-0.0.1.dar > $(sandbox_log) & echo "$$!" > $(sandbox_pid)

start_daml_server: $(sandbox_pid)

stop_daml_server:
	pkill -F $(sandbox_pid) && rm -f $(sandbox_pid) $(sandbox_log)

# triggers
$(trigger_a_pid): |$(state_dir) $(trigger_dir)
	cd triggers && (./run_trigger.sh CompanyA$(TRIG) > ../$(trigger_a_log) & echo "$$!" > ../$(trigger_a_pid))

$(trigger_b_pid): |$(state_dir) $(trigger_dir)
	cd triggers && (./run_trigger.sh CompanyB$(TRIG) > ../$(trigger_b_log) & echo "$$!" > ../$(trigger_b_pid))

start_triggers: $(trigger_a_pid) $(trigger_b_pid)

stop_triggers:
	pkill -F $(trigger_a_pid); rm -f $(trigger_a_pid) $(trigger_a_log); pkill -F $(trigger_b_pid); rm -rf $(trigger_b_pid) $(trigger_b_log)


# packaging
target_dir := target

model_dar := $(target_dir)/proposal-model-$(model_dar_version).dar
trigger_dar := $(target_dir)/proposal-trigger-$(trigger_dar_version).dar

$(target_dir):
	mkdir $@

.PHONY: package
package: $(model_dar) $(trigger_dar)
	cd $(target_dir) && zip proposal-model.zip *

$(model_dar): $(target_dir) $(daml_build_log)
	cp .daml/dist/proposal-model-$(model_dar_version).dar $@

$(trigger_dar): $(target_dir) $(trigger_build_log)
	cp triggers/.daml/dist/proposal-trigger-$(model_dar_version).dar $@

.PHONY: clean
clean:
	rm -rf $(state_dir) $(model_dar) $(trigger_dar)

build:
	daml build && cd triggers && daml build

run_daml_script: build
	daml script --participant-config dabl/participants.json --json-api --dar .daml/dist/proposal-model-0.0.1.dar --script-name Setup:initialize --input-file dabl/ledger-parties.json

run_daml_script_local: build
	daml script --dar .daml/dist/proposal-model-0.0.1.dar --script-name Setup:initialize --ledger-host localhost --ledger-port 6865 --input-file dabl/ledger-parties-local.json
