# STARS Debug Directory Makefile
# Provides targets for autocoding, building, and running state machine models
# Usage: make <target> MODEL=<path/to/model>

MAKEFLAGS += --no-print-directory

# Paths
PYTHON = /home/watney/visar-venv/bin/python3
AUTOCODER = $(PYTHON) ../../autocoder/Stars.py
QHSM_DIR = ../../QHsm

# Default model (can be overridden with MODEL=<path>)
MODEL ?= 

# Extract model base name without extension
MODEL_BASE = $(basename $(notdir $(MODEL)))

# Help target
.PHONY: help
help:
	@echo "STARS Debug Directory - Available Targets:"
	@echo ""
	@echo "Autocoding:"
	@echo "  make autocode-c MODEL=<path>      - Run autocoder with C backend"
	@echo "  make autocode-cpp MODEL=<path>    - Run autocoder with C++ backend"
	@echo "  make autocode-qf MODEL=<path>     - Run autocoder with QF backend"
	@echo "  make autocode-fprime MODEL=<path> - Run autocoder with F' backend"
	@echo ""
	@echo "Building:"
	@echo "  make build-c                      - Compile C backend code"
	@echo "  make build-cpp                    - Compile C++ backend code"
	@echo "  make build-qf                     - Compile QF backend code"
	@echo ""
	@echo "Running:"
	@echo "  make run-c                        - Execute C backend test"
	@echo "  make run-cpp                      - Execute C++ backend test"
	@echo "  make run-qf                       - Execute QF backend test"
	@echo ""
	@echo "Complete Workflows:"
	@echo "  make all-c MODEL=<path>           - autocode-c + build-c + run-c"
	@echo "  make all-cpp MODEL=<path>         - autocode-cpp + build-cpp + run-cpp"
	@echo "  make all-qf MODEL=<path>          - autocode-qf + build-qf + run-qf"
	@echo ""
	@echo "Test Harness:"
	@echo "  make harness                      - Launch test harness (PlantUML only)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean                        - Remove all generated files"
	@echo "  make clean-c                      - Clean C backend directory"
	@echo "  make clean-cpp                    - Clean C++ backend directory"
	@echo "  make clean-qf                     - Clean QF backend directory"
	@echo "  make clean-fprime                 - Clean F' backend directory"
	@echo ""
	@echo "Example:"
	@echo "  make all-c MODEL=../models/TestModels/Simple/Simple.qm"

# ============================================================================
# Autocoding Targets
# ============================================================================

.PHONY: autocode-c
autocode-c:
	@if [ -z "$(MODEL)" ]; then \
		echo "Error: MODEL not specified. Usage: make autocode-c MODEL=<path>"; \
		exit 1; \
	fi
	@echo "=== Running STARS Autocoder (C Backend) ==="
	@echo "Model: $(MODEL)"
	@echo "Output: c/"
	@echo ""
	cd c && $(AUTOCODER) -backend c -model ../$(MODEL)
	@echo ""
	@echo "=== Autocoding Complete ==="

.PHONY: autocode-cpp
autocode-cpp:
	@if [ -z "$(MODEL)" ]; then \
		echo "Error: MODEL not specified. Usage: make autocode-cpp MODEL=<path>"; \
		exit 1; \
	fi
	@echo "=== Running STARS Autocoder (C++ Backend) ==="
	@echo "Model: $(MODEL)"
	@echo "Output: cpp/"
	@echo ""
	cd cpp && $(AUTOCODER) -backend c++ -model ../$(MODEL)
	@echo ""
	@echo "=== Autocoding Complete ==="

.PHONY: autocode-qf
autocode-qf:
	@if [ -z "$(MODEL)" ]; then \
		echo "Error: MODEL not specified. Usage: make autocode-qf MODEL=<path>"; \
		exit 1; \
	fi
	@echo "=== Running STARS Autocoder (QF Backend) ==="
	@echo "Model: $(MODEL)"
	@echo "Output: qf/"
	@echo ""
	cd qf && $(AUTOCODER) -backend qf -model ../$(MODEL)
	@echo ""
	@echo "=== Autocoding Complete ==="

.PHONY: autocode-fprime
autocode-fprime:
	@if [ -z "$(MODEL)" ]; then \
		echo "Error: MODEL not specified. Usage: make autocode-fprime MODEL=<path>"; \
		exit 1; \
	fi
	@echo "=== Running STARS Autocoder (F' Backend) ==="
	@echo "Model: $(MODEL)"
	@echo "Output: fprime/"
	@echo ""
	cd fprime && $(AUTOCODER) -backend fprime -model ../$(MODEL)
	@echo ""
	@echo "=== Autocoding Complete ==="
	@echo "Note: F' backend generates .fppi files, not executables"

# ============================================================================
# Building Targets
# ============================================================================

.PHONY: build-c
build-c:
	@echo "=== Building C Backend ==="
	@if [ ! -f "c/$(MODEL_BASE).c" ]; then \
		echo "Error: No generated code found in c/. Run 'make autocode-c MODEL=<path>' first."; \
		exit 1; \
	fi
	@echo "Compiling C files..."
	cd c && gcc -c -Wall $(MODEL_BASE).c -o $(MODEL_BASE).o
	cd c && gcc -c -Wall $(MODEL_BASE)Impl.c -o $(MODEL_BASE)Impl.o
	cd c && gcc -c -Wall testDrv.c -o testDrv.o
	cd c && gcc -c -Wall sendEvent.c -o sendEvent.o
	@echo "Linking executable..."
	cd c && gcc -Wall main.c $(MODEL_BASE).o $(MODEL_BASE)Impl.o testDrv.o sendEvent.o -o test
	@echo "=== Build Complete: c/test ==="

.PHONY: build-cpp
build-cpp:
	@echo "=== Building C++ Backend ==="
	@if [ ! -f "cpp/$(MODEL_BASE).cpp" ]; then \
		echo "Error: No generated code found in cpp/. Run 'make autocode-cpp MODEL=<path>' first."; \
		exit 1; \
	fi
	@echo "Compiling C++ files..."
	cd cpp && gcc -c -Wall $(MODEL_BASE).cpp -o $(MODEL_BASE).o
	cd cpp && gcc -c -Wall $(MODEL_BASE)Impl.cpp -o $(MODEL_BASE)Impl.o
	cd cpp && gcc -c -Wall testDrv.cpp -o testDrv.o
	cd cpp && gcc -c -Wall sendEvent.cpp -o sendEvent.o
	@echo "Linking executable..."
	cd cpp && gcc -Wall main.cpp $(MODEL_BASE).o $(MODEL_BASE)Impl.o testDrv.o sendEvent.o -o test
	@echo "=== Build Complete: cpp/test ==="

.PHONY: build-qf
build-qf:
	@echo "=== Building QF Backend ==="
	@if [ ! -f "qf/$(MODEL_BASE).c" ]; then \
		echo "Error: No generated code found in qf/. Run 'make autocode-qf MODEL=<path>' first."; \
		exit 1; \
	fi
	@echo "Compiling QF files with QHsm includes..."
	cd qf && gcc -c -Wall -I. -I$(QHSM_DIR) $(MODEL_BASE).c -o $(MODEL_BASE).o
	cd qf && gcc -c -Wall -I. -I$(QHSM_DIR) $(MODEL_BASE)Impl.c -o $(MODEL_BASE)Impl.o
	cd qf && gcc -c -Wall -I. -I$(QHSM_DIR) main.c -o main.o
	cd qf && gcc -c -Wall -I. -I$(QHSM_DIR) testDrv.c -o testDrv.o
	cd qf && gcc -c -Wall -I. -I$(QHSM_DIR) sendEvent.c -o sendEvent.o
	@echo "Linking with QHsm library..."
	cd qf && gcc -o test $(MODEL_BASE).o $(MODEL_BASE)Impl.o main.o testDrv.o sendEvent.o -L$(QHSM_DIR) -lqhsm
	@echo "=== Build Complete: qf/test ==="

# ============================================================================
# Running Targets
# ============================================================================

.PHONY: run-c
run-c:
	@if [ ! -f "c/test" ]; then \
		echo "Error: Executable not found. Run 'make build-c' first."; \
		exit 1; \
	fi
	@echo "=== Running C Backend Test ==="
	@echo ""
	cd c && ./test
	@echo ""
	@echo "=== Test Complete ==="

.PHONY: run-cpp
run-cpp:
	@if [ ! -f "cpp/test" ]; then \
		echo "Error: Executable not found. Run 'make build-cpp' first."; \
		exit 1; \
	fi
	@echo "=== Running C++ Backend Test ==="
	@echo ""
	cd cpp && ./test
	@echo ""
	@echo "=== Test Complete ==="

.PHONY: run-qf
run-qf:
	@if [ ! -f "qf/test" ]; then \
		echo "Error: Executable not found. Run 'make build-qf' first."; \
		exit 1; \
	fi
	@echo "=== Running QF Backend Test ==="
	@echo ""
	cd qf && ./test
	@echo ""
	@echo "=== Test Complete ==="

# ============================================================================
# Complete Workflow Targets
# ============================================================================

.PHONY: all-c
all-c: autocode-c build-c run-c

.PHONY: all-cpp
all-cpp: autocode-cpp build-cpp run-cpp

.PHONY: all-qf
all-qf: autocode-qf build-qf run-qf

# ============================================================================
# Test Harness Target
# ============================================================================

.PHONY: harness
harness:
	@if [ ! -f "test_harness.py" ]; then \
		echo "Error: test_harness.py not found in debug directory."; \
		exit 1; \
	fi
	@echo "=== Launching Test Harness ==="
	@echo "Copy a PlantUML model to this directory first."
	@echo "In Python, use: set_model('<model>.plantuml')"
	@echo ""
	$(PYTHON) -i test_harness.py

# ============================================================================
# Clean Targets
# ============================================================================

.PHONY: clean-c
clean-c:
	@echo "Cleaning C backend directory..."
	rm -f c/*.o c/*.c c/*.h c/test c/*.png

.PHONY: clean-cpp
clean-cpp:
	@echo "Cleaning C++ backend directory..."
	rm -f cpp/*.o cpp/*.cpp cpp/*.hpp cpp/test cpp/*.png

.PHONY: clean-qf
clean-qf:
	@echo "Cleaning QF backend directory..."
	rm -f qf/*.o qf/*.c qf/*.h qf/test qf/*.png

.PHONY: clean-fprime
clean-fprime:
	@echo "Cleaning F' backend directory..."
	rm -f fprime/*.cpp fprime/*.hpp fprime/*.fppi fprime/*.xml fprime/*.png

.PHONY: clean
clean: clean-c clean-cpp clean-qf clean-fprime
	@echo "Cleaning test harness files..."
	rm -f test.json *.png
	@echo "=== All Clean ==="
