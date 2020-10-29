#!/bin/bash
daml build
make start_daml_server
make start_triggers TRIG='Test'
