# Project Chimera: Test Suite

## Overview

This directory contains the test suite for Project Chimera, following Test-Driven Development (TDD) principles. These tests are designed to **FAIL initially** - they define the "empty slots" that AI agents must fill during implementation.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared pytest configuration
├── test_trend_fetcher.py    # Trend fetcher API contract tests
├── test_skills_interface.py # Skills interface contract tests
└── README.md               # This file
```

## Test Philosophy

### 1. **Tests Define Requirements**
Each test corresponds to a requirement from the specifications:
- `technical.md` - API contracts and data structures
- `skills/README.md` - Skill input/output contracts
- `functional.md` - User stories and acceptance criteria

### 2. **Failing Tests are Success**
Initially, tests should fail because:
- They verify interfaces that don't exist yet
- They validate data structures not implemented
- They check behavior not yet coded

### 3. **Test Categories**

#### **Contract Tests**
- Validate API request/response structures
- Check data model compliance
- Verify input validation

#### **Interface Tests**
- Ensure skill methods have correct signatures
- Check module exports and imports
- Validate error handling patterns

#### **Integration Tests** (Future)
- Test component interactions
- Verify end-to-end workflows
- Check system performance

## Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_trend_fetcher.py

# Run with verbose output
pytest tests/ -v

# Run with coverage reporting
pytest tests/ --cov=.
```

### Expected Initial Results
When you first run these tests, you should see:
- **Many FAILING tests** - This is correct and expected
- **Some SKIPPED tests** - Where dependencies don't exist
- **Few PASSING tests** - Only contract validation tests

### Test Markers
```bash
# Run only integration tests
pytest tests/ -m integration

# Run all except slow tests
pytest tests/ -m "not slow"

# List all markers
pytest --markers
```

## Test Development Guidelines

### Writing New Tests
1. **Reference Specifications:** Each test must trace to a spec requirement
2. **Define Expected Behavior:** Tests should specify WHAT, not HOW
3. **Include Examples:** Use examples from specifications
4. **Add Documentation:** Explain what requirement is being tested

### Test Naming Convention
```
test_[component]_[behavior]_[condition]
Example: test_trend_fetcher_response_structure_valid_input
```

### Test Data Management
- Use fixtures for shared test data
- Reference examples from specifications
- Keep test data realistic but minimal

## Test Implementation Status

### Currently Testing:
✅ **API Contracts** (from `technical.md`)
- Trend research request/response structures
- Error response formats
- Data type validation

✅ **Skill Interfaces** (from `skills/README.md`)
- Module structure and exports
- Method signatures
- Input/output contracts

### To Be Tested:
- Agent communication protocols
- Database schema compliance
- Performance requirements
- Security validations

## Dependencies

### Required Packages
```toml
# pyproject.toml test dependencies
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
pytest-cov = "^4.1.0"
```

### Environment Setup
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Or using uv
uv add --dev pytest pytest-asyncio pytest-cov
```

## Continuous Integration

Tests are automatically run on:
- Every git commit (pre-commit hook)
- Every pull request (GitHub Actions)
- Nightly builds (scheduled runs)

## Troubleshooting

### Common Issues

1. **Import Errors:**
   ```bash
   # Add project to Python path
   export PYTHONPATH="$PYTHONPATH:$(pwd)"
   ```

2. **Async Test Failures:**
   ```bash
   # Ensure pytest-asyncio is installed
   pip install pytest-asyncio
   ```

3. **Test Discovery Issues:**
   ```bash
   # Run pytest from project root
   cd /path/to/project-chimera
   pytest tests/
   ```

### Debugging Tests
```python
# Add debug prints
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pytest debug flag
pytest tests/ -v --tb=short

# Run specific test with debug
pytest tests/test_trend_fetcher.py::TestTrendFetcher::test_specific -v
```

