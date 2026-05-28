# STARS

STARS (State Autocoding for Real time Systems) is an innovative software tool designed to streamline and optimize the development of embedded real-time applications. Leveraging state-of-the-art autocoding technology, Stars transforms state-machine models into efficient, reliable, and maintainable code, suitable for a wide range of applications. Developed with a focus on user-friendliness and versatility, it supports multiple modeling tools and generates code in C or C++ and specifically generates code for two different frameworks - the F' framework and the Quantum Framework, addressing the diverse needs of developers and engineers. By automating the code generation process, Stars not only accelerates development cycles but also significantly reduces the potential for human error, ensuring higher quality and performance in the final product. Whether you are working on small-scale projects or complex embedded systems, Stars is engineered to enhance productivity and foster innovation in your development endeavors.

State machine models may be specified using any of these modeling tools:
1. MagicDraw Cameo Systems Modeler
2. Quantum Modeler
3. PlantUML text

The Autocoder processes the model into any one of the following:
1. C state machine code
2. C++ state machine code
3. F' component state machine code and F' FPP
4. Quantum Framework state machine code

## Interface and Design

This diagram highlights the input models (front end) and the autocoder products (back end)

![STARS Interfaces](STARSDocs.png)

This diagram highlights the design and process flow of the QM State Machine Autocoder:

![STARS Design](STARSDesign.png)

## Installation and checkout
- Install the Python module:
```bash
pip install -r requirements.txt
```

- Check that it all works by running the test models using the pytest framework
```bash
# Navigate to the TestModels directory
cd models/TestModels

# Run all tests
pytest -v

# Expected output: Tests passed (multiple combinations across models)
```

## Testing Framework

STARS uses a pytest-based testing framework that validates the autocoder across multiple models, input formats, and backend code generators. The testing framework verifies that:

1. The autocoder correctly processes different input formats (QM, PlantUML, Cameo)
2. The generated code compiles successfully for different backends (C, C++, QF, F')
3. The compiled code produces expected outputs when executed

### Filtering Tests

You can easily filter tests to focus on specific models, backends, or input formats:

#### Filter by Model
```bash
# Test only the Simple model
pytest -m Simple

# Test only the Complex_Junction model
pytest -m Complex_Junction
```

#### Filter by Backend
```bash
# Test only C backend
pytest -m c

# Test only F' (fprime) backend
pytest -m fprime
```

#### Filter by Input Format
```bash
# Test only QM input format
pytest -k qm

# Test only PlantUML input format
pytest -k plantuml

# Test only Cameo input format
pytest -k cameo
```

#### Combine Filters
```bash
# Test Simple model with C backend
pytest -k "Simple and c"

# Test QM input with F' backend
pytest -k "qm and fprime"

# Test Transitions model with PlantUML input and C++ backend
pytest -k "Transitions and plantuml and c++"
```

> **Note:** The `-k` option matches substrings in test names, which include the model name, input format, and backend. This makes it easy to combine filters with logical operators like `and`.

### Advanced Testing Options

#### Run Tests in Parallel
```bash
# Run with 4 parallel workers (requires pytest-xdist)
pytest -n 4
```

#### Update Golden Files
```bash
# Update golden file for a specific test
pytest -k "simple and c" --update-golden

# Update all golden files (use carefully!)
pytest --update-golden
```

For more details on the testing framework, see [TestModels README](models/TestModels/tests/README.md)

## Model Tool Support

### Quantum Modeler

The Quantum Modeler tool is a free open source application for Windows, Linux or Mac that can be downloaded from:
https://www.state-machine.com/#Downloads

The full users guide is here:
https://www.state-machine.com/qm/bm_diagram.html

But the quick approach is to to open up an existing model 
i.e. Open up [Simple.qm](models/TestModels/Simple/Simple.qm) and just rename the model.

Otherwise this is the procedure:
- From the File pull down menu, select 'New Model'
- In the Model Template, select None
- In the Framework, select qpc
- Highlight 'model' in the Model Explorer, right click and Add Package
- Highlight 'package', right click and Add Class
- In the Property Editor, rename 'Class1' with the name of your state machine (ie 'MySm')
- In the Property Editor, in the superclass, select 'qpc::QHsm'
- In the Model Explorer, right click the named state machine (ie 'MySm:QHsm') and Add State Machine
- In the Model Explorer, double click the SM icon
- Expand the drawing canvas
- On right hand side, select the state icon, move to the canvas and click to drop it in.

Here are some examples of QM state machine models that are parsed correctly by this Autocoder:

- [Simple.qm](models/TestModels/Simple/Simple.qm)
- [Simple_Composite.qm](models/TestModels/Simple_Composite/Simple_Composite.qm)
- [Cases.qm](models/TestModels/Cases/Cases.qm)
- [Cameo.qm](models/TestModels/Cameo/Cameo.qm)
- [Actions.qm](models/TestModels/Actions/Actions.qm)
- [Complex_Junction.qm](models/TestModels/Complex_Junction/Complex_Junction.qm)
- [Simple_Junction.qm](models/TestModels/Simple_Junction/Simple_Junction.qm)
- [Multiple_Actions.qm](models/TestModels/Multiple_Actions/Multiple_Actions.qm)
- [Arg_Actions.qm](models/TestModels/Arg_Actions/Arg_Actions.qm)
- [Transitions.qm](models/TestModels/Transitions/Transitions.qm)
- [String_Guards.qm](models/TestModels/String_Guards/String_Guards.qm)
- [Simple_Junction.qm](models/TestModels/Simple_Junction/Simple_Junction.qm)

### PlantUML

For using the PlantUML, see the users guide:

[PlantUML_UsersGuide](PlantUML_UsersGuide.adoc)

Here are some examples of PlantUML state machine models that are parsed correctly by this Autocoder:

- [Simple.plantuml](models/TestModels/Simple/Simple.plantuml)
- [Simple_Composite.plantuml](models/TestModels/Simple_Composite/Simple_Composite.plantuml)
- [Cases.plantuml](models/TestModels/Cases/Cases.plantuml)
- [Cameo.plantuml](models/TestModels/Cameo/Cameo.plantuml)
- [Actions.plantuml](models/TestModels/Actions/Actions.plantuml)
- [Complex_Junction.plantuml](models/TestModels/Complex_Junction/Complex_Junction.plantuml)
- [Simple_Junction.plantuml](models/TestModels/Simple_Junction/Simple_Junction.plantuml)
- [Multiple_Actions.plantuml](models/TestModels/Multiple_Actions/Multiple_Actions.plantuml)
- [Arg_Actions.plantuml](models/TestModels/Arg_Actions/Arg_Actions.plantuml)
- [Transitions.plantuml](models/TestModels/Transitions/Transitions.plantuml)
- [String_Guards.plantuml](models/TestModels/String_Guards/String_Guards.plantuml)
- [Simple_Junction.plantuml](models/TestModels/Simple_Junction/Simple_Junction.plantuml)

Diagrams can be generated from PlantUML models:
Example:
For the Blinky model:
```
@startuml

[*] --> Off: /Bsp_Initialize()

state Off {
    Off:Entry: Bsp_LED_TurnOff()
}

state On {
    On:Entry: Bsp_LED_TurnOn()
}

Off --> On : TIMEOUT
On --> Off : TIMEOUT
@enduml
```

Issue the Command:
```bash
python -m plantuml Blinky.plantuml
```
Will generate the following graphic:

![Blinky PlantUML](models/Blinky/BlinkyUML.png)

### MagicDraw Cameo
MagicDraw is not a free tool. If you have a license then you should also have the documentation.
MagicDraw is a complex tool and there are many ways to specify a state machine that looks correct but
will not be parsed correctly by this Autocoder. Here are some example models that do parse correctly:
- models/TestModels/Simple/Simple.xml
- models/TestModels/Simple_Composite/Simple_Composite.xml
- models/TestModels/Cases/Cases.xml
- models/TestModels/Cameo/Cameo.xml
- models/TestModels/Actions/Actions.xml
- models/TestModels/Complex_Junction/Complex_Junction.xml
- models/TestModels/Simple_Junction/Simple_Junction.xml
- models/TestModels/Multiple_Actions/Multiple_Actions.xml
- models/TestModels/Arg_Actions/Arg_Actions.xml
- models/TestModels/Transitions/Transitions.xml
- models/TestModels/String_Guards/String_Guards.xml
- models/TestModels/Simple_Junction/Simple_Junction.xml


## Command Syntax
The Python state-machine Autocoder command syntax:

```
usage: Stars.py [-h] [-backend {c,qf,c++,fprime}] [-model MODEL] [-noImpl] [-noSignals] [-debug] [-smbase]
```

State-machine Autocoder.

| Switch | Argument | Description |
|--------|----------|-------------|
| -h, --help | | show this help message and exit |
| -backend | c, qf, c++, fprime | back-end code to generate |
| -model | MODEL | QM state-machine model file: <model>.qm |
| -noImpl | | Don't generate the Impl files |
| -noSignals | | Don't generate the Signals header file |
| -debug | | prints out the models |
| -smbase | | Generates the component state-machine base class |

## Examples

cd autocoder

### QM Model - C Backend
`./Stars.py -backend c -noImpl -model ../models/Blinky/Blinky.qm`

### PlantUML Model - C++ Backend
`./Stars.py -backend c++ -noImpl -model ../models/Blinky/Blinky.plantuml`

### QM Model - QF Backend
`./Stars.py -backend qf -noImpl -model ../models/Blinky/Blinky.qm`

### PlantUML Model - fprime backend
`./Stars.py -backend fprime -noImpl model ../models/Blinky/Blinky.plantuml`

### Cameo Model - fprime backend
`./Stars.py -backend fprime -noImpl -model ../models/Blinky/Blinky.xml`

### Generate F' state machine base classes and other F' artifacts
`./Stars.py -smbase`

For other examples see:

- [Blinky README](models/Blinky/README.adoc)
- [Device README](models/Device/README.adoc)

## Test Harness

The test harness provides the capability to test a PlantUML state machine model by setting guard states and sending events.
A graphical rendering of the state machine is updated to animate the state machine.

![STARS Interfaces](TestHarness.png)

### Example 

```bash
# Navigate to the debug directory
cd debug

# Copy a PlantUML model
cp ../models/TestModels/Complex_Junction/Complex_Junction.plantuml .

# Launch the test harness
make harness
```

In the interactive Python session:
```python
# Load the model
set_model("Complex_Junction.plantuml")

# Open and view Complex_Junction.png to see the state machine diagram

# Set guard conditions
set_guard("g3", "True")

# Send events to transition the state machine
send_event("Ev1")

# The diagram will update to show the current state highlighted in gold
```

Available commands in the test harness:
- `set_model("<model>.plantuml")` - Load a PlantUML model
- `send_event("<event>")` - Send an event to the state machine
- `set_guard("<guard>", "True"|"False")` - Set a guard condition
- `commands()` - Display available commands

## Wrapping a State Machine in an F Prime Component

This section explains how to integrate a STARS state machine into an F Prime (F´) component using the Simple_Component example from `StarsProj/Simple_Component`.

### Overview

To wrap a state machine model in an F Prime component, you need to:
1. Generate the `.fppi` file from your state machine model using STARS
2. Create an FPP component definition that includes the state machine
3. Implement action handlers and signal triggers in C++
4. Build and test the component

### Step-by-Step Guide

#### 1. Create Your State Machine Model

First, create your state machine model using QM, PlantUML, or Cameo. For this example, we use a simple two-state machine (`Simple.qm`):

```xml
<statechart>
  <initial target="S1"/>
  <state name="S1">
    <entry brief="s1Entry()"/>
    <tran trig="EV1" target="S2"/>
  </state>
  <state name="S2">
    <tran trig="EV1" target="S1"/>
  </state>
</statechart>
```

This defines a state machine with two states (S1 and S2) that toggle on event EV1, with an entry action on S1.

#### 2. Generate the State Machine FPP File

Create an `autocode.sh` script to generate the `.fppi` file:

```bash
#!/bin/bash
../../autocoder/Stars.py -backend fprime -noImpl -model Simple.qm
```

Run the script to generate `Simple_State_Machine.fppi`:

```bash
chmod +x autocode.sh
./autocode.sh
```

The generated `.fppi` file contains the FPP state machine definition:

```fpp
state machine Simple {
  action s1Entry
  signal EV1
  
  initial enter S1
  state S1 {
    entry do { s1Entry }
    on EV1 enter S2
  }
  state S2 {
    on EV1 enter S1
  }
}
```

#### 3. Create the Component FPP Definition

Create `Simple_Component.fpp` to wrap the state machine in an F Prime component:

```fpp
module Components {
  include "Simple_State_Machine.fppi"
  
  @ Component wrapper for Simple state machine
  active component Simple_Component {
    
    # State machine instance
    state machine instance simpleState: Simple 
    
    # Input port to trigger state transitions
    async input port schedIn: Svc.Sched
    
    # Events for state machine actions
    event s1EntryEvent() severity activity high id 0 format "s1Entry Event"
    
    # Standard F Prime ports
    time get port timeCaller
    import Fw.Command
    import Fw.Event
  }
}
```

Key elements:
- **`include "Simple_State_Machine.fppi"`**: Imports the generated state machine definition
- **`state machine instance simpleState: Simple`**: Creates an instance named `simpleState`
- **`event s1EntryEvent()`**: Defines an EVR (Event Report) for the s1Entry action
- **Input/output ports**: Connects the component to the F Prime framework

#### 4. Implement the Component Header

Create `Simple_Component.hpp`:

```cpp
#include "Simple_Component/Simple_ComponentComponentAc.hpp"

namespace Components {

class Simple_Component final : public Simple_ComponentComponentBase {
  public:
    Simple_Component(const char* const compName);
    ~Simple_Component();

  private:
    // Port handler - triggers state transitions
    void schedIn_handler(FwIndexType portNum, U32 context) override;
    
    // State machine action handler
    void Components_Simple_action_s1Entry(
      SmId smId,
      Components_Simple::Signal signal
    ) override;
};

}
```

**Important**: Action handler names follow the pattern `Components_<StateMachineName>_action_<actionName>` and use the signal type `Components_<StateMachineName>::Signal`.

#### 5. Implement the Component Logic

Create `Simple_Component.cpp`:

```cpp
#include "Simple_Component/Simple_Component.hpp"

namespace Components {

Simple_Component::Simple_Component(const char* const compName) 
  : Simple_ComponentComponentBase(compName) {}

Simple_Component::~Simple_Component() {}

// Port handler - sends signal to state machine
void Simple_Component::schedIn_handler(FwIndexType portNum, U32 context) {
  simpleState_sendSignal_EV1();  // Trigger state transition
}

// Action handler - logs event when s1Entry action executes
void Simple_Component::Components_Simple_action_s1Entry(
  SmId smId,
  Components_Simple::Signal signal
) {
  this->log_ACTIVITY_HI_s1EntryEvent();
}

}
```

Key implementation details:
- **Sending signals**: Use `<instanceName>_sendSignal_<SignalName>()` to trigger transitions
- **Logging events**: Use `log_ACTIVITY_HI_<eventName>()` in action handlers
- **State queries**: Use `<instanceName>_getState()` to check current state

#### 6. Create the Build Configuration

Create `CMakeLists.txt`:

```cmake
set(SOURCE_FILES
  "${CMAKE_CURRENT_LIST_DIR}/Simple_Component.fpp"
)

register_fprime_module()

register_fprime_library(
  AUTOCODER_INPUTS
    "${CMAKE_CURRENT_LIST_DIR}/Simple_Component.fpp"
  SOURCES
    "${CMAKE_CURRENT_LIST_DIR}/Simple_Component.cpp"
)
```

#### 7. Build and Test

Build the component:

```bash
cd StarsProj/Simple_Component
fprime-util build
```

Run unit tests:

```bash
fprime-util check
```

### Advanced Features

For more complex examples, see:
- **`Arg_Actions_Component`**: State machine actions with parameters and guard conditions
- **`Complex_Composite_Component`**: Hierarchical state machines with nested composite states

### Common Patterns

**Sending commands to trigger events:**
```fpp
async command SEND_EV1() opcode 0
```

```cpp
void Simple_Component::SEND_EV1_cmdHandler(FwOpcodeType opCode, U32 cmdSeq) {
  simpleState_sendSignal_EV1();
  this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}
```

**Handling guard conditions:**
Guards defined in the model require parameter passing:
```cpp
simpleState_sendSignal_GuardedEvent(guardValue);
```

**State transitions with parameters:**
Actions with parameters receive them through the action handler signature as defined in the generated base class.

### Directory Structure

A complete F Prime state machine component includes:

```
MyComponent/
├── MyModel.qm                    # State machine model
├── autocode.sh                   # Autocoder script
├── MyComponent_State_Machine.fppi # Generated by STARS
├── MyComponent.fpp               # Component definition
├── MyComponent.hpp               # Component header
├── MyComponent.cpp               # Component implementation
├── CMakeLists.txt                # Build configuration
└── test/ut/                      # Unit tests
    ├── MyComponentTester.hpp
    ├── MyComponentTester.cpp
    └── MyComponentTestMain.cpp
```
