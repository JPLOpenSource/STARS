#!/usr/bin/env python3
"""
Pytest-based tests for STARS autocoder.
Tests multiple models, input formats, and backends.
"""

import pytest
import difflib
from pathlib import Path
from .utils import (
    run_autocoder,
    build_c_backend,
    build_cpp_backend,
    build_qf_backend,
    run_test_executable,
    validate_fpp_file
)


def generate_test_ids(models, input_formats, backends):
    """Generate readable test IDs for parameterized tests."""
    test_ids = []
    for model_name, model_config in models.items():
        for input_format in input_formats:
            for backend in backends:
                test_ids.append(f"{model_name}-{input_format}-{backend}")
    return test_ids


def pytest_generate_tests(metafunc):
    """Generate parameterized test cases from config."""
    if 'model_name' in metafunc.fixturenames:
        # Load test config
        import yaml
        config_file = Path(__file__).parent / "test_config.yaml"
        with open(config_file) as f:
            config = yaml.safe_load(f)
        
        # Generate all test combinations
        test_cases = []
        test_ids = []
        
        for model_name, model_config in config['models'].items():
            input_formats = list(model_config['inputs'].keys())
            backends = model_config['backends']
            
            for input_format in input_formats:
                for backend in backends:
                    test_cases.append((model_name, input_format, backend))
                    test_ids.append(f"{model_name}-{input_format}-{backend}")
        
        metafunc.parametrize(
            "model_name,input_format,backend",
            test_cases,
            ids=test_ids
        )


def test_autocoder(model_name, input_format, backend, test_config, base_dir, tmp_path, update_golden, qhsm_library):
    """
    Test autocoder for a specific model/input/backend combination.
    
    Test flow:
    1. Run Stars.py autocoder to generate code
    2. For C/C++/QF: compile and run executable, capture stdout
    3. For Fprime: read generated .fppi file
    4. Compare output with golden file
    5. Optionally update golden file if --update-golden flag is set
    
    Args:
        qhsm_library: Ensures libqhsm.a is built before QF backend tests
    """
    # Get test configuration
    model_config = test_config['models'][model_name]
    
    # Process template variables
    def substitute_vars(value):
        if isinstance(value, str):
            return value.replace("${model_name}", model_name)
        return value
    
    # Get model file with variable substitution
    model_file = substitute_vars(model_config['inputs'][input_format])
    model_path = test_config['models_dir'] / model_name / model_file
    test_driver_path = test_config['models_dir'] / model_name / model_config['test_driver']
    
    # Handle format-specific golden files (for fprime backend)
    if isinstance(model_config['golden'][backend], dict):
        # Format-specific golden file
        golden_file_rel = substitute_vars(model_config['golden'][backend][input_format])
    else:
        # Single golden file for all formats
        golden_file_rel = substitute_vars(model_config['golden'][backend])
        
    golden_file = test_config['golden_dir'] / golden_file_rel
    
    # Get model base name (e.g., "Simple" from "Simple.qm")
    model_base = Path(model_file).stem
    
    # Step 1: Copy testDrv.txt to parent of tmp_path so autocoder can find it
    # The autocoder looks for ../testDrv.txt relative to output_dir
    import shutil
    test_drv_dest = tmp_path.parent / "testDrv.txt"
    if test_driver_path.exists():
        shutil.copy(test_driver_path, test_drv_dest)
    
    # Step 2: Run autocoder (generates .c/.h or .cpp/.hpp or .fpp files)
    print(f"\n{'='*60}")
    print(f"Testing: {model_name} / {input_format} / {backend}")
    print(f"{'='*60}")
    print(f"Running autocoder: {model_path}")
    
    result = run_autocoder(
        model_file=model_path,
        backend=backend,
        output_dir=tmp_path,
        base_dir=base_dir
    )
    
    if result.returncode != 0:
        pytest.fail(f"Autocoder failed:\nstdout: {result.stdout}\nstderr: {result.stderr}")
    
    # Step 3: Build and run (for C/C++/QF) or just read output (for Fprime)
    if backend == 'c':
        print("Building C executable...")
        build_c_backend(tmp_path, model_base, base_dir)
        print("Running test executable...")
        output = run_test_executable(tmp_path)
        
    elif backend == 'c++':
        print("Building C++ executable...")
        build_cpp_backend(tmp_path, model_base, base_dir)
        print("Running test executable...")
        output = run_test_executable(tmp_path)
        
    elif backend == 'qf':
        print("Building QF executable...")
        build_qf_backend(tmp_path, model_base, base_dir, qhsm_library)
        print("Running test executable...")
        output = run_test_executable(tmp_path)
        
    elif backend == 'fprime':
        print("Reading generated FPP file...")
        output_file = tmp_path / f"{model_base}_State_Machine.fppi"
        if not output_file.exists():
            pytest.fail(f"Fprime output file not found: {output_file}")
        
        # Validate FPP syntax with fpp-check
        print("Running fpp-check...")
        try:
            validate_fpp_file(output_file)
        except RuntimeError as e:
            pytest.fail(str(e))
        
        output = output_file.read_text()
    
    else:
        pytest.fail(f"Unknown backend: {backend}")
    
    # Step 3: Handle golden file update or comparison
    if update_golden:
        # Update mode: write output to golden file
        print(f"Updating golden file: {golden_file}")
        golden_file.parent.mkdir(parents=True, exist_ok=True)
        golden_file.write_text(output)
        pytest.skip(f"Golden file updated: {golden_file}")
    else:
        # Test mode: compare with golden file
        if not golden_file.exists():
            pytest.fail(
                f"Golden file not found: {golden_file}\n"
                f"Run with --update-golden to create it.\n"
                f"Actual output:\n{output}"
            )
        
        expected = golden_file.read_text()
        
        if output != expected:
            # Generate a detailed diff
            diff = '\n'.join(difflib.unified_diff(
                expected.splitlines(keepends=True),
                output.splitlines(keepends=True),
                fromfile=f'expected ({golden_file.name})',
                tofile='actual',
                lineterm=''
            ))
            
            pytest.fail(
                f"\nOutput mismatch for {model_name}/{input_format}/{backend}\n"
                f"Golden file: {golden_file}\n"
                f"\nDiff:\n{diff}\n"
                f"\nRun with --update-golden -k '{model_name} and {backend}' to update if this is expected."
            )
        
        print(f"✓ Output matches golden file")
