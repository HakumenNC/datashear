# DataShear

[![codecov](https://codecov.io/github/HakumenNC/datashear/branch/main/graph/badge.svg?token=0JW393HPAY)](https://codecov.io/github/HakumenNC/datashear)
![PyPI - Version](https://img.shields.io/pypi/v/datashear)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datashear)


A Python package that allows you to split CSV files

## Installation

```bash
pip install datashear
```

## Usage

```py
from datashear import Splitter

# Split by number of rows
splitter = Splitter("large_file.csv", output_dir="output")
splitter.by_rows(1000)  # 1000 rows per file

# Split by file size  
splitter.by_size(1024*1024)  # 1MB per file
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/HakumenNC/datashear.git
cd datashear
```

2. Install in development mode:
```bash
pip install -e ".[dev]"
```

## Testing

> Writing tests means you don’t trust your code.

Running test with [`pytest`](https://docs.pytest.org/en/stable)

```bash
pytest
```

```bash
pytest --cov=src --cov-report=xml
```

### Go further

#### pytest

> The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.

https://docs.pytest.org/en/stable

- [Method and function level setup/teardown](https://docs.pytest.org/en/stable/how-to/xunit_setup.html#method-and-function-level-setup-teardown)
- [Asserting with the assert statement](https://docs.pytest.org/en/stable/how-to/assert.html)
- [Assertions about expected exceptions](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions)

#### Codecov

> Codecov doesn’t just measure code coverage—it helps you improve code quality at every step.

https://about.codecov.io

- https://github.com/codecov/codecov-action

## Building

Build the package:
```bash
python -m build
```

## Publish

Publishing with [`twine`](https://github.com/pypa/twine) via [`github-actions`](https://github.com/features/actions) on release

## License

MIT License - see LICENSE file for details.
