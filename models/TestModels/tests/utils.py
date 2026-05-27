#!/usr/bin/env python3
"""
Utility functions for STARS testing.
Contains build functions that replace Makefile logic.
"""

import subprocess
from pathlib import Path


def run_autocoder(model_file, backend, output_dir,  base_dir=None):
    """
    Run Stars.py autocoder.
    Equivalent to 'autocode' target in Makefiles.
    
    Args:
        model_file: Path to model file (.qm, .plantuml, or .xml)
        backend: Backend type (c, cpp, qf, fprime)
        output_dir: Directory to generate code into
        base_dir: Base directory (defaults to STARS root)
    
    Returns:
        CompletedProcess object
    """
    if base_dir is None:
        # utils.py -> tests/ -> TestModels/ -> models/ -> STARS/
        base_dir = Path(__file__).parent.parent.parent.parent
    
    autocoder = base_dir / "autocoder" / "Stars.py"
    
    cmd = [str(autocoder), "-backend", backend, "-model", str(model_file)]
    
    result = subprocess.run(
        cmd,
        cwd=output_dir,
        capture_output=True,
        text=True
    )
    
    return result


def build_c_backend(tmp_path, model_base, base_dir):
    """
    Build C backend executable.
    Equivalent to Common_C_Makefile build target.
    
    Args:
        tmp_path: Temporary directory containing generated code
        model_base: Base name of model (e.g., "Simple")
        base_dir: Base directory for includes
    
    Raises:
        RuntimeError: If compilation or linking fails
    """
    # Compile all .c files to .o files
    gcc_compile = [
        ["gcc", "-c", "-Wall", f"{model_base}.c", "-o", f"{model_base}.o"],
        ["gcc", "-c", "-Wall", f"{model_base}Impl.c", "-o", f"{model_base}Impl.o"],
        ["gcc", "-c", "-Wall", "testDrv.c", "-o", "testDrv.o"],
        ["gcc", "-c", "-Wall", "sendEvent.c", "-o", "sendEvent.o"],
    ]
    
    for cmd in gcc_compile:
        result = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Compilation failed: {' '.join(cmd)}\n{result.stderr}")
    
    # Link into executable
    link_cmd = [
        "gcc", "-Wall", "main.c",
        f"{model_base}.o", f"{model_base}Impl.o",
        "testDrv.o", "sendEvent.o", "-o", "test"
    ]
    result = subprocess.run(link_cmd, cwd=tmp_path, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Linking failed: {' '.join(link_cmd)}\n{result.stderr}")


def build_cpp_backend(tmp_path, model_base, base_dir):
    """
    Build C++ backend executable.
    Equivalent to Common_CPP_Makefile build target.
    
    Args:
        tmp_path: Temporary directory containing generated code
        model_base: Base name of model (e.g., "Simple")
        base_dir: Base directory for includes
    
    Raises:
        RuntimeError: If compilation or linking fails
    """
    # Compile all .cpp files to .o files
    gcc_compile = [
        ["gcc", "-c", "-Wall", f"{model_base}.cpp", "-o", f"{model_base}.o"],
        ["gcc", "-c", "-Wall", f"{model_base}Impl.cpp", "-o", f"{model_base}Impl.o"],
        ["gcc", "-c", "-Wall", "testDrv.cpp", "-o", "testDrv.o"],
        ["gcc", "-c", "-Wall", "sendEvent.cpp", "-o", "sendEvent.o"],
    ]
    
    for cmd in gcc_compile:
        result = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Compilation failed: {' '.join(cmd)}\n{result.stderr}")
    
    # Link into executable
    link_cmd = [
        "gcc", "-Wall", "main.cpp",
        f"{model_base}.o", f"{model_base}Impl.o",
        "testDrv.o", "sendEvent.o", "-o", "test"
    ]
    result = subprocess.run(link_cmd, cwd=tmp_path, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Linking failed: {' '.join(link_cmd)}\n{result.stderr}")


def build_qf_backend(tmp_path, model_base, base_dir, qhsm_library):
    """
    Build QF backend executable.
    Equivalent to Common_QF_Makefile build target.
    
    Args:
        tmp_path: Temporary directory containing generated code
        model_base: Base name of model (e.g., "Simple")
        base_dir: Base directory for includes
        qhsm_library: Path to libqhsm.a (ensures library is built)
    
    Raises:
        RuntimeError: If compilation or linking fails
    """
    qhsm_dir = base_dir / "QHsm"
    include_dirs = ["-I.", f"-I{qhsm_dir}"]
    
    # Compile with QHsm includes
    gcc_compile = [
        ["gcc", "-c", "-Wall"] + include_dirs + [f"{model_base}.c", "-o", f"{model_base}.o"],
        ["gcc", "-c", "-Wall"] + include_dirs + [f"{model_base}Impl.c", "-o", f"{model_base}Impl.o"],
        ["gcc", "-c", "-Wall"] + include_dirs + ["main.c", "-o", "main.o"],
        ["gcc", "-c", "-Wall"] + include_dirs + ["testDrv.c", "-o", "testDrv.o"],
        ["gcc", "-c", "-Wall"] + include_dirs + ["sendEvent.c", "-o", "sendEvent.o"],
    ]
    
    for cmd in gcc_compile:
        result = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Compilation failed: {' '.join(cmd)}\n{result.stderr}")
    
    # Link with QHsm library
    link_cmd = [
        "gcc", "-o", "test",
        f"{model_base}.o", f"{model_base}Impl.o",
        "main.o", "testDrv.o", "sendEvent.o",
        f"-L{qhsm_dir}", "-lqhsm"
    ]
    result = subprocess.run(link_cmd, cwd=tmp_path, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Linking failed: {' '.join(link_cmd)}\n{result.stderr}")


def run_test_executable(tmp_path):
    """
    Run the compiled test executable and capture output.
    Equivalent to running './test' in Makefile.
    
    Args:
        tmp_path: Directory containing the test executable
    
    Returns:
        stdout from the test executable
    """
    result = subprocess.run(
        ["./test"],
        cwd=tmp_path,
        capture_output=True,
        text=True
    )
    return result.stdout


def validate_fpp_file(fppi_file):
    """
    Run fpp-check on a generated .fppi file to validate syntax.
    
    Args:
        fppi_file: Path to the .fppi file to check
    
    Raises:
        RuntimeError: If fpp-check fails with validation errors
    """
    result = subprocess.run(
        ["fpp-check", str(fppi_file)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise RuntimeError(
            f"fpp-check validation failed for {fppi_file.name}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )
    
    print(f"✓ fpp-check passed for {fppi_file.name}")
