# STARS Debug Directory

This directory provides a development and debugging environment for testing the STARS autocoder with individual state machine models.

## Purpose

The debug directory allows you to:
- Run models through the STARS autocoder and see all output
- Build and execute generated code for different backends
- Test PlantUML models with the interactive test harness
- Debug autocoder issues in an isolated environment

## Directory Structure

```
debug/
├── Makefile              # Main Makefile with all targets
├── testDrv.txt           # Customizable test driver (event sequences)
├── test_harness.py       # Test harness for PlantUML models
├── c/                    # C backend output
├── cpp/                  # C++ backend output
├── qf/                   # QF backend output
└── fprime/               # F' backend output
```

## Quick Start

### 1. Copy a Model and Test Driver
```bash
cd debug
cp ../models/TestModels/Simple/Simple.qm .
cp ../models/TestModels/Simple/testDrv.txt .
```

**Important:** Always copy the `testDrv.txt` file from the model directory. This file defines the event sequences for testing and must match the events in your model.

### 2. Run Complete Workflow
```bash
make all-c MODEL=Simple.qm
```

This will autocode, build, and run the model in one command.

## Available Make Targets

### Autocoding
Run the STARS autocoder on a model:
```bash
make autocode-c MODEL=<path>      # C backend
make autocode-cpp MODEL=<path>    # C++ backend
make autocode-qf MODEL=<path>     # QF backend
make autocode-fprime MODEL=<path> # F' backend
```

### Building
Compile the generated code:
```bash
make build-c      # Build C backend
make build-cpp    # Build C++ backend
make build-qf     # Build QF backend
```

### Running
Execute the compiled test:
```bash
make run-c        # Run C backend test
make run-cpp      # Run C++ backend test
make run-qf       # Run QF backend test
```

### Complete Workflows
Run autocode + build + run in one command:
```bash
make all-c MODEL=<path>
make all-cpp MODEL=<path>
make all-qf MODEL=<path>
```

### Test Harness
Launch the interactive test harness (PlantUML models only):
```bash
make harness
```

In ipython:
```python
set_model("Simple.plantuml")
send_event("EV1")
set_guard("g1", "True")
```

### Cleaning
Remove generated files:
```bash
make clean          # Clean all backends
make clean-c        # Clean C backend only
make clean-cpp      # Clean C++ backend only
make clean-qf       # Clean QF backend only
make clean-fprime   # Clean F' backend only
```

## Usage Examples

### Example 1: Test C Backend with QM Model
```bash
cd debug
cp ../models/TestModels/Simple/Simple.qm .
cp ../models/TestModels/Simple/testDrv.txt .
make all-c MODEL=Simple.qm
```

### Example 2: Debug Autocoder Output
```bash
cd debug
cp ../models/TestModels/Complex_Junction/Complex_Junction.plantuml .
cp ../models/TestModels/Complex_Junction/testDrv.txt .
make autocode-cpp MODEL=Complex_Junction.plantuml
# Review generated code in cpp/ directory
# Modify model if needed
make autocode-cpp MODEL=Complex_Junction.plantuml
```

### Example 3: Test Multiple Backends
```bash
cd debug
cp ../models/TestModels/Actions/Actions.qm .
cp ../models/TestModels/Actions/testDrv.txt .
make autocode-c MODEL=Actions.qm
make autocode-cpp MODEL=Actions.qm
make autocode-qf MODEL=Actions.qm
make build-c
make build-cpp
make build-qf
make run-c
make run-cpp
make run-qf
```

### Example 4: Custom Test Driver
```bash
cd debug
cp ../models/TestModels/Transitions/Transitions.qm .
cp ../models/TestModels/Transitions/testDrv.txt .
# Edit testDrv.txt with your custom event sequence:
# EV1
# EV2
# EV1
make all-c MODEL=Transitions.qm
```

### Example 5: PlantUML Test Harness
```bash
cd debug
cp ../models/TestModels/Simple_Junction/Simple_Junction.plantuml .
make harness
```

In ipython:
```python
set_model("Simple_Junction.plantuml")
# View Simple_Junction.png
send_event("EV1")
set_guard("g1", "True")
send_event("EV2")
```

### Example 6: F' Backend
```bash
cd debug
cp ../models/TestModels/Simple/Simple.qm .
cp ../models/TestModels/Simple/testDrv.txt .
make autocode-fprime MODEL=Simple.qm
# Check fprime/ directory for generated .fppi files
ls -l fprime/
```

## Test Driver File (testDrv.txt)

The `testDrv.txt` file defines the sequence of events to send to the state machine during testing. Edit this file to customize your test scenarios.

Format:
```
EV1
EV2
// This is a comment
EV3
```

The autocoder reads this file and generates:
- `testDrv.c/cpp` - Test driver implementation
- `main.c/cpp` - Main program
- `sendEvent.c/cpp` - Event sending functions

## Backends

### C Backend
- Generates C code with switch-based state machine
- Compiles with gcc
- Executable: `c/test`

### C++ Backend
- Generates C++ code with switch-based state machine
- Compiles with gcc
- Executable: `cpp/test`

### QF Backend
- Generates C code using Quantum Framework
- Requires QHsm library (in `../QHsm/`)
- Compiles with QHsm includes and links with libqhsm
- Executable: `qf/test`

### F' Backend
- Generates F' component code
- Creates .fppi files (F' port interface)
- No executable (F' uses different build system)

## Troubleshooting

### Model not found
Make sure to copy the model file to the debug directory or provide the full path:
```bash
make all-c MODEL=../models/TestModels/Simple/Simple.qm
```

### Build errors
Check that:
1. The autocoder ran successfully
2. The generated code is in the correct backend directory
3. For QF backend, the QHsm library is built (`cd ../QHsm && make`)

### Test harness not working
The test harness only works with PlantUML models. Make sure:
1. You have a .plantuml file in the debug directory
2. You have the required Python packages: `pydantic`, `plantuml`

## Help

Run `make help` or just `make` to see all available targets:
```bash
make help
```
