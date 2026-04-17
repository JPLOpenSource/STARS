# STARS Pytest Testing Framework

## Introduction

The STARS (State Autocoding for Real-time Systems) Pytest Testing Framework provides a robust, efficient way to test the STARS autocoder across multiple models, input formats, and backend code generators. This framework replaces the traditional Makefile-based approach with a more flexible, maintainable pytest solution.

This document serves as a comprehensive guide for both users who want to run tests and developers who need to extend the framework with new models or features.

## Overview

STARS transforms state-machine models into efficient code for embedded real-time applications. The testing framework validates that:

1. The autocoder correctly processes different input formats (QM, PlantUML, Cameo)
2. The generated code compiles successfully for different backends (C, C++, QF, F´)
3. The compiled code produces expected outputs when executed

## For Users: Running Tests

### Quick Start

```bash
# Navigate to the project root directory
cd STARS

# Install dependencies if needed
pip install -r requirements.txt

# Navigate to the TestModels directory
cd models/TestModels

# Run all tests
pytest -v

# Expected output: Tests passed (multiple combinations across models)
```

**Dependencies:** The testing framework requires the following Python packages (specified in requirements.txt):
- anytree
- Cheetah3
- lxml
- pyparsing
- plantuml
- pydantic
- pytest (for running the tests)

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

# Test only F´ (fprime) backend
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

# Test QM input with F´ backend
pytest -k "qm and fprime"

# Test Transitions model with PlantUML input and C++ backend
pytest -k "transitions and plantuml and c++"
```

### Advanced Options

#### Run Tests in Parallel
```bash
# Run with 4 parallel workers (requires pytest-xdist)
pytest -n 4
```

#### Verbose Output
```bash
# Show detailed test output
pytest -vv

# Show stdout even for passing tests
pytest -s
```

## For Developers: Framework Structure

### Directory Structure

```
models/TestModels/
├── pytest.ini                   # Pytest configuration and markers
├── tests/
│   ├── __init__.py
│   ├── test_config.yaml         # Test configuration (models, inputs, backends)
│   ├── conftest.py              # Pytest fixtures and custom options
│   ├── utils.py                 # Build functions (replaces Makefile logic)
│   └── test_autocoder.py        # Main test implementation
└── golden/
    └── model_name/              # One directory per model
        ├── c.txt                # Golden file for C backend
        ├── cpp.txt              # Golden file for C++ backend
        ├── qf.txt               # Golden file for QF backend
        └── fprime.fppi          # Golden file for F´ backend
```

### How Tests Work

Each test follows this process:

1. **Configuration**: Reads test parameters from `test_config.yaml`
2. **Autocoding**: Runs STARS autocoder on the model file via subprocess
3. **Compilation**: For C/C++/QF backends, compiles the generated code
4. **Execution**: Runs the compiled executable and captures output
5. **Verification**: Compares output with golden file using Python's difflib

### Golden Files

Golden files contain the expected output for each test combination. They serve as the reference for validating test results.

#### Updating Golden Files

```bash
# Update golden file for a specific test
pytest -k "simple and c" --update-golden

# Update all golden files (use carefully!)
pytest --update-golden
```

## Adding a New Model

To add a new model for testing:

1. **Add entry to test_config.yaml:**
```yaml
models:
  # Existing models...
  
  new_model_name:  # Your new model
    inputs:
      qm: NewModel.qm
      plantuml: NewModel.plantuml
      cameo: NewModel.xml
    backends: [c, c++, qf, fprime]
    test_driver: testDrv.txt
    golden:
      c: new_model_name/c.txt
      c++: new_model_name/cpp.txt
      qf: new_model_name/qf.txt
      fprime: new_model_name/fprime.fppi
```

2. **Generate golden files:**
```bash
pytest -k new_model_name --update-golden
```

3. **Done!** You now have new tests for your model.

No directories to create, no Makefiles to write.
