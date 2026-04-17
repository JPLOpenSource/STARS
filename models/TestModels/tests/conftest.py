#!/usr/bin/env python3
"""
Pytest configuration and fixtures for STARS testing.
"""

import pytest
import yaml
from pathlib import Path


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Update golden files with new test output"
    )


@pytest.fixture(scope="session")
def test_config():
    """Load test configuration from YAML file."""
    config_file = Path(__file__).parent / "test_config.yaml"
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Convert relative paths to absolute
    base = Path(__file__).parent.parent
    config['base_dir'] = base / config['base_dir']
    config['models_dir'] = base / config['models_dir']
    config['golden_dir'] = base / config['golden_dir']
    
    return config


@pytest.fixture
def update_golden(request):
    """Fixture that indicates if golden files should be updated."""
    return request.config.getoption("--update-golden")


@pytest.fixture(scope="session")
def base_dir():
    """Get the STARS base directory."""
    # conftest.py -> tests/ -> TestModels/ -> models/ -> STARS/
    return Path(__file__).parent.parent.parent.parent


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "model(name): mark test with model name"
    )
    config.addinivalue_line(
        "markers", "backend(name): mark test with backend name"
    )
    config.addinivalue_line(
        "markers", "input_format(name): mark test with input format"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically add markers based on test parameters."""
    for item in items:
        # Add markers based on test parameters
        if hasattr(item, 'callspec'):
            params = item.callspec.params
            
            if 'model_name' in params:
                item.add_marker(pytest.mark.model(params['model_name']))
                # Also add a marker with the model name itself
                item.add_marker(getattr(pytest.mark, params['model_name']))
            
            if 'backend' in params:
                item.add_marker(pytest.mark.backend(params['backend']))
                # Also add a marker with the backend name itself (if valid identifier)
                backend = params['backend']
                if backend.replace('_', '').isalnum():
                    item.add_marker(getattr(pytest.mark, backend))
            
            if 'input_format' in params:
                item.add_marker(pytest.mark.input_format(params['input_format']))
