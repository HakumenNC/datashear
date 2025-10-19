# Examples

This directory contains example scripts demonstrating how to use the datashear package.

## Running the Examples

First, make sure you have installed the datashear package:

```bash
pip install datashear
```

Or if you're working from the source:

```bash
cd ..
pip install -e .
```

Then run the example script:

```bash
python example_usage.py
```

## What the Examples Demonstrate

The `example_usage.py` script shows three different ways to use datashear:

1. **Split by rows**: Splitting a CSV file into multiple files with a specific number of rows per file
2. **Split by file count**: Splitting a CSV file into a specific number of files
3. **Using the class directly**: Using the `CSVSplitter` class for more control over the splitting process

Each example creates sample CSV data, performs the split, and cleans up afterwards.
