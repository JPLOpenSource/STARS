# STARS Pytest Testing Framework

This is a prototype pytest-based testing framework for the STARS autocoder, currently supporting the `simple` model.

## Quick Start

```bash
# Run all tests (12 combinations for simple model)
cd /home/watney/STARS/models/TestModels
source /home/watney/visar-venv/bin/activate
pytest -v

# Results: 12 passed in 4.00s
# (No need to specify tests/ - pytest.ini has testpaths = tests)
```

## What Was Created

```
models/TestModels/
├── pytest.ini                   # Pytest configuration
├── tests/
│   ├── __init__.py
│   ├── test_config.yaml         # Test metadata (easy to add new models)
│   ├── conftest.py              # Pytest fixtures and custom options
│   ├── utils.py                 # Build functions (replaces Makefile logic)
│   └── test_autocoder.py        # Main test file (~165 lines)
└── golden/
    └── simple/
        ├── c.txt                # Golden file for C backend
        ├── cpp.txt              # Golden file for C++ backend
        ├── qf.txt               # Golden file for QF backend
        └── fprime.fppi          # Golden file for Fprime backend
```

## Key Features

### 1. Filter by Model
```bash
pytest -k simple
```

### 2. Filter by Backend
```bash
# Test only C backend
pytest -k c

# Test only Fprime backend
pytest -k fprime
```

### 3. Filter by Input Format
```bash
# Test only QM input
pytest -k qm

# Test only PlantUML input
pytest -k plantuml
```

### 4. Combine Filters
```bash
# Test simple model with C backend
pytest -k "simple and c"

# Test QM input with Fprime backend
pytest -k "qm and fprime"
```

### 5. Run in Parallel (if pytest-xdist installed)
```bash
# Run with 4 parallel workers
pytest -n 4
```

### 6. Update Golden Files
```bash
# Update specific golden file after verifying change is correct
pytest -k "simple and c" --update-golden

# Update all golden files (use carefully!)
pytest --update-golden
```

### 7. Verbose Output
```bash
# Show detailed test output
pytest -vv

# Show stdout even for passing tests
pytest -s
```

## How It Works

Each test:
1. **Runs autocoder** via subprocess (replaces `make autocode`)
2. **Compiles code** via subprocess.run(["gcc", ...]) (replaces `make build`)
3. **Runs executable** and captures stdout (replaces `make run`)
4. **Compares with golden file** using Python difflib

**No Makefiles needed!** The gcc commands are in Python functions in `tests/utils.py`.

## Adding a New Model

To add a new model (e.g., "actions"), just:

1. **Add entry to test_config.yaml:**
```yaml
models:
  simple:
    # ... existing config ...
  
  actions:  # New model
    inputs:
      qm: Actions.qm
      plantuml: Actions.plantuml
      cameo: Actions.xml
    backends: [c, c++, qf, fprime]
    test_driver: testDrv.txt
    golden:
      c: actions/c.txt
      c++: actions/cpp.txt
      qf: actions/qf.txt
      fprime: actions/fprime.fppi
```

2. **Generate golden files:**
```bash
pytest -k actions --update-golden
```

3. **Done!** You now have 12 new tests.

No directories to create, no Makefiles to write.

## Comparison: Old vs New

### Old Way (Make-based)
- **Files:** 13 Makefiles per model (156 total for 12 models)
- **Adding model:** Create 12 directories, write 13 Makefiles (~20 minutes)
- **Running tests:** `make ut` (sequential, ~5 minutes)
- **Updating golden:** Manually copy files
- **Filtering:** Not possible, must run all or edit Makefile

### New Way (Pytest-based)
- **Files:** 5 Python files total, 1 YAML config
- **Adding model:** Add 10 lines to YAML (~2 minutes)
- **Running tests:** `pytest` (parallel-capable, ~4 seconds)
- **Updating golden:** `pytest --update-golden -k model_name`
- **Filtering:** `pytest -k "model and backend"` (built-in)

## Next Steps

To expand this to all models:
1. Copy golden files from `models/*/goldy*.txt` to `golden/*/`
2. Add each model to `test_config.yaml` (10 lines per model)
3. Run `pytest` to verify all tests pass

That's it! No more Makefile management.
