# datashear

A Python package that allows you to split CSV files into multiple smaller files.

## Features

- Split CSV files by number of rows per file
- Split CSV files into a specific number of files
- Optionally include or exclude headers in output files
- Command-line interface for easy usage
- Python API for programmatic usage

## Installation

```bash
pip install datashear
```

Or install from source:

```bash
git clone https://github.com/HakumenNC/datashear.git
cd datashear
pip install -e .
```

## Usage

### Command Line Interface

Split a CSV file by number of rows:

```bash
datashear input.csv -r 1000
```

Split a CSV file into a specific number of files:

```bash
datashear input.csv -n 5
```

Specify output directory and prefix:

```bash
datashear input.csv -r 1000 -o output/ -p data
```

Split without including headers:

```bash
datashear input.csv -r 1000 --no-header
```

### Python API

```python
from datashear import split_csv, CSVSplitter

# Using the convenience function
output_files = split_csv(
    'input.csv',
    rows_per_file=1000,
    output_dir='output',
    output_prefix='split'
)

# Using the CSVSplitter class
splitter = CSVSplitter('input.csv', output_dir='output', output_prefix='data')

# Split by rows
output_files = splitter.split_by_rows(rows_per_file=1000, include_header=True)

# Split by file count
output_files = splitter.split_by_file_count(num_files=5, include_header=True)
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

Or using unittest:

```bash
python -m unittest discover tests/
```

## License

MIT License - see LICENSE file for details
