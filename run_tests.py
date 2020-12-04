#!/usr/bin/python3

import json
import sys
import os

def scriptCommand(scriptName, inputFile, outputFile):
    return f'daml script --dar .daml/dist/proposal-model-0.0.2.dar --script-name Tests:{scriptName} --ledger-host localhost --ledger-port 6865 --input-file {inputFile} --output-file {outputFile}'

tests = ["testStepTwo", "testStepThree", "testStepFour"]

os.system("daml build")
os.system("while ! nc -z localhost 6865; do sleep 1; done")

print("Initializing...")
setupTest = os.system(scriptCommand("initializeTests", "dabl/ledger-parties-local.json", "test_results.json"))
if (setupTest != 0):
    print('Failed to initialize')
    sys.exit()

for step in tests:
    print(f'Running {step}...')
    exitCode = os.system(scriptCommand(step, "test_results.json", "test_results.json"))
    if (exitCode != 0):
        print(f'Failed on {step}')
        sys.exit()

print('Tests complete!')
