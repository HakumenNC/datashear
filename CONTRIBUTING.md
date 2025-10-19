# Contributing to datashear

Thank you for your interest in contributing to datashear!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/HakumenNC/datashear.git
cd datashear
```

2. Install in development mode:
```bash
pip install -e .
```

3. Run the tests:
```bash
python -m unittest discover tests/
```

## Running Tests

To run all tests:
```bash
python -m unittest discover tests/ -v
```

To run a specific test file:
```bash
python -m unittest tests.test_splitter
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and single-purpose

## Adding New Features

1. Create a new branch for your feature
2. Write tests for your feature first (TDD approach)
3. Implement the feature
4. Ensure all tests pass
5. Update documentation if needed
6. Submit a pull request

## Testing Your Changes

Before submitting a pull request, please:

1. Run all unit tests and ensure they pass
2. Test the CLI interface manually
3. Test the Python API manually
4. Add new tests for any new functionality
5. Update the README if you've added new features

## Example Test

Here's a basic example of how to test your changes:

```python
import unittest
from datashear import split_csv

class TestMyFeature(unittest.TestCase):
    def test_something(self):
        # Your test code here
        pass
```

## Questions?

If you have any questions, please open an issue on GitHub.
