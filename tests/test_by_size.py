"""
Tests for the by_size method of the Splitter class.
"""

import pytest
import os
import csv
import tempfile
import shutil
from pathlib import Path

from datashear.core import Splitter


class TestSplitterBySize:

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Utils
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    def setup_method(self):
        """
        Set up test fixtures before each test method.
        """
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.sample_csv = os.path.join(self.test_dir, "sample.csv")

        # header
        self.header = ['ID', 'Name', 'Age', 'City']
        
        # Create a sample CSV file
        self.create_sample_csv()
    
    def teardown_method(self):
        """
        Clean up after each test method.
        """
        # Remove temporary directory and all its contents
        shutil.rmtree(self.test_dir)
    
    def create_sample_csv(self, rows=10):
        """
        Create a sample CSV file for testing.
        """
        with open(self.sample_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            for i in range(1, rows + 1):
                writer.writerow([i, f'Person_{i}', 20 + (i % 50), f'City_{i % 5}'])
    
    def count_files(self, prefix="", sufix=""):
        """
        Count files in test directory with given prefix.
        """
        return len([f for f in os.listdir(self.test_dir) if f.startswith(prefix)])
    
    def read_csv_file(self, filepath):
        """
        Read CSV file and return rows as list.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return list(reader)
        
    def create_large_csv(self, filepath, num_rows):
        """Create a larger CSV file for testing."""
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Age', 'City', 'Country', 'Salary'])
            for i in range(1, num_rows + 1):
                writer.writerow([
                    i, 
                    f'Person_{i}', 
                    20 + (i % 50), 
                    f'City_{i % 10}',
                    f'Country_{i % 5}',
                    30000 + (i * 100)
                ])

    def get_file_size(self, filepath):
        """Get file size in bytes."""
        return os.path.getsize(filepath)
        
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Tests
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    def test_by_size_basic_functionality(self):
        """
        Test basic splitting functionality by size.
        """
        # Get original file size
        original_size = self.get_file_size(self.sample_csv)
        
        # Split by half the original size
        target_size = original_size // 2
        
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_size(target_size)

        # Should create at least 2 files
        output_files = self.count_files("sample_")
        assert output_files >= 2
    
    def test_by_size_with_header_repetition(self):
        """
        Test that headers are repeated in each output file when repeat_header=True.
        """
        original_size = self.get_file_size(self.sample_csv)
        target_size = original_size // 3
        
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_size(target_size, repeat_header=True)

        # Check that all output files have headers
        output_files = [f for f in os.listdir(self.test_dir) if f.startswith("sample_")]
        
        for filename in output_files:
            filepath = os.path.join(self.test_dir, filename)
            rows = self.read_csv_file(filepath)
            assert len(rows) > 0, f"File {filename} should not be empty"
            assert rows[0] == self.header, f"File {filename} should have header as first row"
    
    def test_by_size_without_header_repetition(self):
        """
        Test that headers are not repeated when repeat_header=False.
        """
        original_size = self.get_file_size(self.sample_csv)
        target_size = original_size // 3
        
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_size(target_size, repeat_header=False)

        # Check that only the first output file has header
        output_files = sorted([f for f in os.listdir(self.test_dir) if f.startswith("sample_")])
        
        for i, filename in enumerate(output_files):
            filepath = os.path.join(self.test_dir, filename)
            rows = self.read_csv_file(filepath)
            assert len(rows) > 0, f"File {filename} should not be empty"
            
            if i == 0:
                # First file should have header
                assert rows[0] == self.header, f"First file {filename} should have header"
            else:
                # Other files should not have header
                assert rows[0] != self.header, f"File {filename} should not have header"
    
    def test_by_size_very_small_size(self):
        """
        Test splitting with very small size (one row per file).
        """
        # Use a very small size that forces one row per file
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_size(50)  # Very small size

        # Should create multiple files
        output_files = self.count_files("sample_")
        assert output_files > 1
    
    def test_by_size_very_large_size(self):
        """
        Test splitting with size larger than the input file.
        """
        original_size = self.get_file_size(self.sample_csv)
        
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_size(original_size * 2)  # Much larger than original

        # Should create only one output file
        output_files = self.count_files("sample_")
        assert output_files == 1
    
    def test_by_size_zero_size(self):
        """
        Test that zero size raises ValueError.
        """
        splitter = Splitter(self.sample_csv, self.test_dir)
        
        with pytest.raises(ValueError, match="size per file must be greater than 0"):
            splitter.by_size(0)
    
    def test_by_size_negative_size(self):
        """
        Test that negative size raises ValueError.
        """
        splitter = Splitter(self.sample_csv, self.test_dir)
        
        with pytest.raises(ValueError, match="size per file must be greater than 0"):
            splitter.by_size(-100)
    
    def test_by_size_empty_file(self):
        """
        Test handling of empty CSV file.
        """
        empty_csv = os.path.join(self.test_dir, "empty.csv")
        
        # Create empty file
        with open(empty_csv, 'w', encoding='utf-8') as file:
            pass
        
        splitter = Splitter(empty_csv, self.test_dir)
        
        with pytest.raises(ValueError, match="CSV file is empty"):
            splitter.by_size(1000)
    
    def test_by_size_with_custom_prefix_suffix(self):
        """
        Test splitting with custom prefix and suffix.
        """
        original_size = self.get_file_size(self.sample_csv)
        target_size = original_size // 2
        
        splitter = Splitter(
            self.sample_csv, 
            self.test_dir, 
            output_prefix="prefix", 
            output_sufix="suffix"
        )
        splitter.by_size(target_size)

        # Check that files have correct naming
        output_files = [f for f in os.listdir(self.test_dir) if f.startswith("prefix_")]
        assert len(output_files) > 0
        
        for filename in output_files:
            assert "prefix_" in filename
            assert "suffix_" in filename
    
    def test_by_size_file_sizes_respect_limit(self):
        """
        Test that output files respect the size limit (approximately).
        """
        # Create a larger file for this test
        large_csv = os.path.join(self.test_dir, "large.csv")
        self.create_large_csv(large_csv, 100)
        
        target_size = 1000  # 1KB limit
        
        splitter = Splitter(large_csv, self.test_dir)
        splitter.by_size(target_size)

        # Check output file sizes (allowing some tolerance for headers and encoding)
        output_files = [f for f in os.listdir(self.test_dir) if f.startswith("large_")]
        
        for filename in output_files[:-1]:  # All files except the last one
            filepath = os.path.join(self.test_dir, filename)
            file_size = self.get_file_size(filepath)
            # Allow some tolerance (headers might make files slightly larger)
            assert file_size <= target_size * 1.5, f"File {filename} size {file_size} exceeds limit {target_size}"
    
    def test_by_size_data_integrity(self):
        """
        Test that all original data is preserved across split files.
        """
        original_size = self.get_file_size(self.sample_csv)
        target_size = original_size // 3
        
        # Read original data
        original_rows = self.read_csv_file(self.sample_csv)
        original_data = original_rows[1:]  # Exclude header
        
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_size(target_size, repeat_header=True)

        # Collect all data from output files
        output_files = sorted([f for f in os.listdir(self.test_dir) if f.startswith("sample_")])
        collected_data = []
        
        for filename in output_files:
            filepath = os.path.join(self.test_dir, filename)
            rows = self.read_csv_file(filepath)
            # Skip header row
            data_rows = rows[1:] if rows[0] == self.header else rows
            collected_data.extend(data_rows)
        
        # Compare original and collected data
        assert len(collected_data) == len(original_data), "Data count mismatch"
        assert collected_data == original_data, "Data content mismatch"