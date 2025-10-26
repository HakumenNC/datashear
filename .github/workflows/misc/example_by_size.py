"""
Example usage of the by_size method in DataShear.

This script demonstrates how to use the new by_size method to split CSV files
based on file size rather than number of rows.
"""

import os
from datashear import Splitter

def example_by_size():
    """
    Example demonstrating how to use the by_size method.
    """
    print("DataShear by_size Method Example")
    print("=" * 40)
    
    # Define input and output paths
    input_file = "tests/input/MOCK_DATA_SM.csv"
    output_dir = "tests/output"
    
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return
    
    # Show original file info
    original_size = os.path.getsize(input_file)
    print(f"Original file: {input_file}")
    print(f"Original size: {original_size} bytes")
    print()
    
    # Example 1: Split by size with header repetition
    print("Example 1: Split by size (1KB limit) with header repetition")
    print("-" * 60)
    
    splitter1 = Splitter(
        input_file=input_file,
        output_dir=output_dir,
        output_prefix="example1",
        output_sufix="1kb"
    )
    
    splitter1.by_size(size=1024, repeat_header=True)  # 1KB per file
    
    # Show results
    output_files = [f for f in os.listdir(output_dir) if f.startswith("example1_")]
    print(f"Created {len(output_files)} files:")
    for filename in sorted(output_files):
        filepath = os.path.join(output_dir, filename)
        file_size = os.path.getsize(filepath)
        print(f"  {filename}: {file_size} bytes")
    print()
    
    # Example 2: Split by size without header repetition
    print("Example 2: Split by size (800 bytes limit) without header repetition")
    print("-" * 70)
    
    splitter2 = Splitter(
        input_file=input_file,
        output_dir=output_dir,
        output_prefix="example2",
        output_sufix="800b"
    )
    
    splitter2.by_size(size=800, repeat_header=False)  # 800 bytes per file
    
    # Show results
    output_files = [f for f in os.listdir(output_dir) if f.startswith("example2_")]
    print(f"Created {len(output_files)} files:")
    for filename in sorted(output_files):
        filepath = os.path.join(output_dir, filename)
        file_size = os.path.getsize(filepath)
        print(f"  {filename}: {file_size} bytes")
        
        # Show first line to verify header behavior
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            is_header = first_line.startswith('id,first_name')
            print(f"    First line: {'(HEADER)' if is_header else '(DATA)'} {first_line[:50]}...")
    print()
    
    # Example 3: Comparison with by_rows method
    print("Example 3: Comparison with by_rows method")
    print("-" * 45)
    
    splitter3 = Splitter(
        input_file=input_file,
        output_dir=output_dir,
        output_prefix="rows_comparison",
        output_sufix="3rows"
    )
    
    splitter3.by_rows(nb=3, repeat_header=True)  # 3 rows per file
    
    output_files = [f for f in os.listdir(output_dir) if f.startswith("rows_comparison_")]
    print(f"by_rows(3) created {len(output_files)} files:")
    for filename in sorted(output_files):
        filepath = os.path.join(output_dir, filename)
        file_size = os.path.getsize(filepath)
        
        # Count lines
        with open(filepath, 'r', encoding='utf-8') as f:
            line_count = len(f.readlines())
        
        print(f"  {filename}: {file_size} bytes, {line_count} lines")
    
    print("\nComparison Summary:")
    print("- by_size() splits based on file size in bytes")
    print("- by_rows() splits based on number of data rows")
    print("- Both methods support header repetition control")
    print("- by_size() is useful for managing storage quotas or transfer limits")
    print("- by_rows() is useful for processing fixed-size batches")

if __name__ == "__main__":
    example_by_size()