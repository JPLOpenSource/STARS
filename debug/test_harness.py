#!/usr/bin/env python3
# -------------------------------------------------------------------------------------
# test_harness()
#
# Executes a state machine in the test_harness
# Runs interactively in ipython
#
# Example:
# cp ../models/TestModels/simple/Simple.plantuml .
# ipython
# > %run test_harness.py
# > set_model("Simple.plantuml")
# View the file: Simple.png
# > send_event("EV1")
# > set_guard(<guard>, "True")
# -------------------------------------------------------------------------------------

import subprocess
import json
from pydantic import BaseModel
from typing import List
import os
from plantuml import PlantUML
import re

# Pydantic classes that specify the configSm.json
class Guard(BaseModel):
    name: str
    state: str
    
class TestConfig(BaseModel):
    currentState: str
    event: str
    guards: List[Guard]

class OutputConfig(BaseModel):
    actions: List[str]
    state: str


# -------------------------------------------------------------------------------------
# commands()
#
# Print out the list of commands
# -------------------------------------------------------------------------------------
def commands():
    print("Commands:")
    print(f"set_model(<model>.plantuml)")
    print(f"send_event(<event>)")
    print(f'set_guard(<guard>, "True"|"False")')
    print(f"commands()")

# -------------------------------------------------------------------------------------
# update_config_json
#
# Write the latest config information to the test.json file
# -------------------------------------------------------------------------------------
def update_config_json():
    global config

    with open('test.json', 'w') as file:
        file.write(config.model_dump_json())

# -------------------------------------------------------------------------------------
# update_diagram
#
# Update the plantuml state machine diagram with a new state
# -------------------------------------------------------------------------------------
def update_diagram(state: str):
    with open(command[-1], 'r') as file:
        content = file.read()
        pattern = r"\bstate " + re.escape(state) + r"\b"
        updated_content = re.sub(pattern, f"state {state} #gold", content)
    raw_pdf = generate_diagram_from_string(updated_content)
    with open(command[-1].replace("plantuml", "png"), 'wb') as file:
        file.write(raw_pdf)

# -------------------------------------------------------------------------------------
# generate_diagram_from_string
#
# Return the raw png plantuml state machine diagram from the contents of a plantuml file
#
# This routine uses the plantuml server at www.plantuml.com
# 
# Here are the steps to run the server on your local machine: 
# 1) Install docker if not already installed:
# docker --version
# sudo apt update
# sudo apt install docker.io
#
# 2) Pull the plantuml docker image:
# -----------------------------------
# docker pull plantuml/plantuml-server
#
# 3) Run the docker image using port 8080:
# ----------------------------------------
# docker run --detach --publish 8080:8080 plantuml/plantuml-server:jetty
#
# To check docker processes:
# --------------------------
# docker ps
#
# To stop and remove a docker process:
# ------------------------------------
#  docker stop 007a1c2ef9c4
#  docker rm 007a1c2ef9c4
#
# 4) Check that its working:
# -----------------------
# On a browser go to:  http://localhost:8080
#
# -------------------------------------------------------------------------------------
def generate_diagram_from_string(content):
    plantuml_url = 'http://www.plantuml.com/plantuml/img/'
    # To use a local plantuml server
    #plantuml_url = 'http://localhost:8080/img/'
    plantuml = PlantUML(plantuml_url)
    try:
        rawpng = plantuml.processes(content)
        return rawpng  # Return the raw PNG data
    except Exception as e:
        # Updated error handling
        print(f"An error occurred while generating the diagram: {str(e)}")
        return None  # Return None in case of an error

# -------------------------------------------------------------------------------------
# update_state
#
# Invoke the Stars Autocoder to get the next state based on the json configuration
# -------------------------------------------------------------------------------------
def update_state():
    if command[-1] == "None":
        print(f"Error:  First set the model by invoking 'set_model(<model.plantuml>)'")
        return
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        output_data = result.stdout.splitlines()[-1]
        json_data = json.loads(output_data)
        out_state = OutputConfig(**json_data)
        config.currentState = out_state.state
        update_diagram(out_state.state)
        print(f'State = {out_state.state}')
        print(f'Actions = {out_state.actions}')

    except subprocess.CalledProcessError as e:
        print("Error occurred:", e.stderr)


# -------------------------------------------------------------------------------------
# send_event
#
# Update the json configuration with an event and then invoke update_state
# -------------------------------------------------------------------------------------
def send_event(event: str):
    global config

    config.event = event
    update_config_json()
    update_state()
     

# -------------------------------------------------------------------------------------
# set_model
#
# Update the command line with a plantuml model
# Then update the json configuration and update the state
# -------------------------------------------------------------------------------------
def set_model(model_name: str):
    global command

    if os.path.exists(model_name):
        command[-1] = model_name

        config.currentState = "None"
        config.event =  "None"

        update_config_json()
        update_state()
    else:
        print(f"Error:  {model_name} does not exist")

# -------------------------------------------------------------------------------------
# set_guard
#
# Update json configuration with a guard state
# -------------------------------------------------------------------------------------
def set_guard(guard: str, state: str):
    global config
    if state != "True" and state != "False":
        print(f'Error: Set the guard to either "True" or "False"')
        return
    for i in range(len(config.guards)):
        if config.guards[i].name == guard:
            config.guards[i].state = state
            return
    config.guards.append(Guard(name = guard, state = state))

# -------------------------------------------------------------------------------------
# set_initial_config
#
# Set the state machine configuration to its initial default state
# -------------------------------------------------------------------------------------
def set_initial_config():
    global config
    config = TestConfig(currentState = "None",
                    event = "None",
                    guards = [])

# -------------------------------------------------------------------------------------
# Main routine
# -------------------------------------------------------------------------------------
command = ["../autocoder/Stars.py", "-backend", "test", "-model", "None"]

set_initial_config()

print("State machine Test Harness Ready:")
commands()
