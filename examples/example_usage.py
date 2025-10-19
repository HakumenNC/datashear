"""
Example usage of the datashear package
"""

import os
import csv
from datashear import split_csv, CSVSplitter


def create_sample_csv(filename, rows=100):
    """Create a sample CSV file for demonstration"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name', 'Email', 'Age', 'City'])
        for i in range(rows):
            writer.writerow([
                i + 1,
                f'Person{i+1}',
                f'person{i+1}@example.com',
                20 + (i % 50),
                f'City{i % 10}'
            ])
    print(f"Created sample CSV with {rows} rows: {filename}")


def example_split_by_rows():
    """Example: Split CSV by number of rows per file"""
    print("\n=== Example 1: Split by rows ===")
    
    # Create sample data
    create_sample_csv('sample.csv', rows=50)
    
    # Split into files with 20 rows each
    output_files = split_csv(
        'sample.csv',
        rows_per_file=20,
        output_dir='output_rows',
        output_prefix='part'
    )
    
    print(f"\nSplit into {len(output_files)} files:")
    for f in output_files:
        print(f"  - {f}")


def example_split_by_file_count():
    """Example: Split CSV into specific number of files"""
    print("\n=== Example 2: Split into specific number of files ===")
    
    # Create sample data
    create_sample_csv('sample.csv', rows=50)
    
    # Split into exactly 5 files
    output_files = split_csv(
        'sample.csv',
        num_files=5,
        output_dir='output_count',
        output_prefix='chunk'
    )
    
    print(f"\nSplit into {len(output_files)} files:")
    for f in output_files:
        print(f"  - {f}")


def example_using_class():
    """Example: Using the CSVSplitter class directly"""
    print("\n=== Example 3: Using CSVSplitter class ===")
    
    # Create sample data
    create_sample_csv('sample.csv', rows=30)
    
    # Create a splitter instance
    splitter = CSVSplitter(
        'sample.csv',
        output_dir='output_class',
        output_prefix='data'
    )
    
    # Split by rows without including headers
    output_files = splitter.split_by_rows(
        rows_per_file=10,
        include_header=False
    )
    
    print(f"\nSplit into {len(output_files)} files (without headers):")
    for f in output_files:
        print(f"  - {f}")


if __name__ == '__main__':
    # Run all examples
    example_split_by_rows()
    example_split_by_file_count()
    example_using_class()
    
    # Clean up
    print("\n=== Cleaning up ===")
    import shutil
    for dir_name in ['output_rows', 'output_count', 'output_class']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}/")
    
    if os.path.exists('sample.csv'):
        os.remove('sample.csv')
        print("Removed sample.csv")
    
    print("\nDone! Check the examples to see how datashear works.")
