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
pytest -k simple

# Test only the Complex_Junction model
pytest -k complex_junction
```

#### Filter by Backend
```bash
# Test only C backend
pytest -k c

# Test only F' (fprime) backend
pytest -k fprime
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
pytest -k "simple and c"

# Test QM input with F' backend
pytest -k "qm and fprime"

# Test Transitions model with PlantUML input and C++ backend
pytest -k "transitions and plantuml and c++"
```

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
i.e. Open up [Simple.qm](models/TestModels/simple/Simple.qm) and just rename the model.

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

- [Simple.qm](models/TestModels/simple/Simple.qm)
- [Simple_Composite.qm](models/TestModels/simple_composite/Simple_Composite.qm)
- [Cases.qm](models/TestModels/cases/Cases.qm)
- [Cameo.qm](models/TestModels/Cameo/Cameo.qm)
- [Actions.qm](models/TestModels/actions/Actions.qm)
- [Complex_Junction.qm](models/TestModels/complex_junction/Complex_Junction.qm)
- [Simple_Junction.qm](models/TestModels/simple_junction/Simple_Junction.qm)
- [Multiple_Actions.qm](models/TestModels/multiple_actions/Multiple_Actions.qm)
- [Arg_Actions.qm](models/TestModels/arg_actions/Arg_Actions.qm)
- [Transitions.qm](models/TestModels/transitions/Transitions.qm)
- [String_Guards.qm](models/TestModels/string_guards/String_Guards.qm)
- [Simple_Junction.qm](models/TestModels/simple_junction/Simple_Junction.qm)

### PlantUML

For using the PlantUML, see the users guide:

[PlantUML_UsersGuide](PlantUML_UsersGuide.adoc)

Here are some examples of PlantUML state machine models that are parsed correctly by this Autocoder:

- [Simple.plantuml](models/TestModels/simple/Simple.plantuml)
- [Simple_Composite.plantuml](models/TestModels/simple_composite/Simple_Composite.plantuml)
- [Cases.plantuml](models/TestModels/cases/Cases.plantuml)
- [Cameo.plantuml](models/TestModels/Cameo/Cameo.plantuml)
- [Actions.plantuml](models/TestModels/actions/Actions.plantuml)
- [Complex_Junction.plantuml](models/TestModels/complex_junction/Complex_Junction.plantuml)
- [Simple_Junction.plantuml](models/TestModels/simple_junction/Simple_Junction.plantuml)
- [Multiple_Actions.plantuml](models/TestModels/multiple_actions/Multiple_Actions.plantuml)
- [Arg_Actions.plantuml](models/TestModels/arg_actions/Arg_Actions.plantuml)
- [Transitions.plantuml](models/TestModels/transitions/Transitions.plantuml)
- [String_Guards.plantuml](models/TestModels/string_guards/String_Guards.plantuml)
- [Simple_Junction.plantuml](models/TestModels/simple_junction/Simple_Junction.plantuml)

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
- models/TestModels/simple/Simple.xml
- models/TestModels/simple_composite/Simple_Composite.xml
- models/TestModels/cases/Cases.xml
- models/TestModels/Cameo/Cameo.xml
- models/TestModels/actions/Actions.xml
- models/TestModels/complex_junction/Complex_Junction.xml
- models/TestModels/simple_junction/Simple_Junction.xml
- models/TestModels/multiple_actions/Multiple_Actions.xml
- models/TestModels/arg_actions/Arg_Actions.xml
- models/TestModels/transitions/Transitions.xml
- models/TestModels/string_guards/String_Guards.xml
- models/TestModels/simple_junction/Simple_Junction.xml


## Command Syntax
The Python state-machine Autocoder command syntax:

```
usage: Stars.py [-h] [-backend {c,qf,c++,fprime}] [-model MODEL] [-noImpl] [-noSignals] [-namespace NAMESPACE] [-debug] [-smbase]
```

State-machine Autocoder.

| Switch | Argument | Description |
|--------|----------|-------------|
| -h, --help | | show this help message and exit |
| -backend | c, qf, c++, fprime | back-end code to generate |
| -model | MODEL | QM state-machine model file: <model>.qm |
| -noImpl | | Don't generate the Impl files |
| -noSignals | | Don't generate the Signals header file |
| -namespace | NAMESPACE | Fprime namespace |
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
`./Stars.py -backend fprime -noImpl -namespace BLINKY -model ../models/Blinky/Blinky.plantuml`

### Cameo Model - fprime backend
`./Stars.py -backend fprime -noImpl -namespace BLINKY -model ../models/Blinky/Blinky.xml`

### Generate F' state machine base classes and other F' artifacts
`./Stars.py -smbase`

For other examples see:

- [Blinky README](models/Blinky/README.adoc)
- [Device README](models/Device/README.adoc)

## Test Harness

The test harness provides the capability to test a state machine model by setting guard states and sending events.
A graphical rendering of the state machine is updated to animate the state machine.

![STARS Interfaces](TestHarness.png)

### Example 

- `cd testharness`
- `cp ../models/TestModels/complex_junction/Complex_Junction.plantuml .`
- `ipython`
- `%run test_harness.py`
- `set_model("Complex_Junction.plantuml")`
  (Open and view `Complex_Junction.png`)
- `set_guard("g3", "True")`
- `send_event("Ev1")`
