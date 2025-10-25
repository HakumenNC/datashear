"""
Tests for the by_rows method of the Splitter class.
"""

import pytest
import os
import csv
import tempfile
import shutil
from pathlib import Path

from datashear.core import Splitter


class TestSplitterByRows:
    """Test cases for Splitter.by_rows method."""


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
        
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Tests
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    def test_by_rows_basic_functionality(self):
        """
        Test basic splitting functionality.
        """
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_rows(3)

        output_files = self.count_files()
        nb_output_files_expected = 4
        assert output_files == nb_output_files_expected + 1 # adding input file
    
    def test_by_rows_with_header_repetition(self):
        """
        Test that headers are repeated when repeat_header=True.
        """
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_rows(3, repeat_header=True)

        first_file = os.path.join(self.test_dir, "sample_1.csv" )
        rows = self.read_csv_file(first_file)
        
        # first row should be header
        assert rows[0] == self.header
        # should have header + 3 data rows = 4 total rows
        assert len(rows) == 4
    
    def test_by_rows_without_header_repetition(self):
        """
        Test splitting without header repetition.
        """
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_rows(3, repeat_header=False)
        
        first_file = os.path.join(self.test_dir,"sample_1.csv")
        rows = self.read_csv_file(first_file)
        
        # first row should be data, not header
        assert rows[0] == ['1', 'Person_1', '21', 'City_1']
        # should have only 3 data rows
        assert len(rows) == 3
    
    def test_by_rows_custom_output_parameters(self):
        """Test with custom output prefix and suffix."""
        splitter = Splitter(
            self.sample_csv, 
            self.test_dir, 
            output_prefix="chunk",
            output_sufix="data"
        )
        splitter.by_rows(5)
        
        # Check that files are created with correct naming
        expected_file = os.path.join(self.test_dir, "chunk_sample_data_1.csv")
        assert os.path.exists(expected_file)
    
    def test_by_rows_single_row_per_file(self):
        """Test splitting with 1 row per file."""
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_rows(1)
        
        # Should create 10 files (one for each data row)
        output_files = self.count_files()
        nb_output_files_expected = 10
        assert output_files == nb_output_files_expected + 1 # adding input file
    
    def test_by_rows_larger_than_file(self):
        """Test when rows per file is larger than total rows."""
        self.create_sample_csv(5)  # Create file with only 5 data rows
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_rows(10)  # Request 10 rows per file
        
        # Should create only 1 file
        output_files = self.count_files()
        nb_output_files_expected = 1
        assert output_files == nb_output_files_expected + 1 # adding input file
        
        # File should contain all data
        output_file = os.path.join(self.test_dir, "sample_1.csv")
        rows = self.read_csv_file(output_file)
        assert len(rows) == 6  # header + 5 data rows
    
    def test_by_rows_invalid_parameters(self):
        """Test error handling for invalid parameters."""
        splitter = Splitter(self.sample_csv, self.test_dir)
        
        # Test zero rows
        with pytest.raises(ValueError, match="rows per file must be greater than 0"):
            splitter.by_rows(0)
        
        # Test negative rows
        with pytest.raises(ValueError, match="rows per file must be greater than 0"):
            splitter.by_rows(-5)
    
    def test_by_rows_empty_csv(self):
        """Test handling of empty CSV file."""
        empty_csv = os.path.join(self.test_dir, "empty.csv")
        
        # Create empty CSV
        with open(empty_csv, 'w', encoding='utf-8') as f:
            pass
        
        splitter = Splitter(empty_csv, self.test_dir)
        
        with pytest.raises(ValueError, match="CSV file is empty"):
            splitter.by_rows(3)
    
  
    def test_by_rows_file_content_accuracy(self):
        """Test that file contents are accurate and complete."""
        self.create_sample_csv(7)  # Create 7 data rows
        splitter = Splitter(self.sample_csv, self.test_dir)
        splitter.by_rows(3)
        
        # Read all output files and verify content
        all_data_rows = []
        
        for i in range(1, 4):  # Should have 3 files
            file_path = os.path.join(self.test_dir, f"sample_{i}.csv")
            if os.path.exists(file_path):
                rows = self.read_csv_file(file_path)
                # Skip header if present
                data_rows = rows[1:] if rows[0] == ['ID', 'Name', 'Age', 'City'] else rows
                all_data_rows.extend(data_rows)
        
        # Should have all 7 original data rows
        assert len(all_data_rows) == 7
        
        # Verify first and last rows
        assert all_data_rows[0] == ['1', 'Person_1', '21', 'City_1']
        assert all_data_rows[-1] == ['7', 'Person_7', '27', 'City_2']
    
    def test_by_rows_nonexistent_input_file(self):
        """Test error handling for nonexistent input file."""
        with pytest.raises(FileNotFoundError):
            Splitter("nonexistent.csv", self.test_dir)
    
    def test_by_rows_creates_output_directory(self):
        """Test that output directory is created if it doesn't exist."""
        new_output_dir = os.path.join(self.test_dir, "new_output")
        splitter = Splitter(self.sample_csv, new_output_dir)
        
        # Directory should be created during initialization
        assert os.path.exists(new_output_dir)
    
    def test_by_rows_memory_efficiency(self):
        """Test memory efficiency with larger file (integration test)."""
        # Create a larger CSV for memory testing
        large_csv = os.path.join(self.test_dir, "large.csv")
        self.create_large_csv(large_csv, 1000)  # 1000 rows
        
        splitter = Splitter(large_csv, self.test_dir, output_prefix="large")
        splitter.by_rows(100)
        
        # Should create 10 files
        large_files = len([f for f in os.listdir(self.test_dir) if f.startswith("large")])
        nb_output_files_expected = 10
        assert large_files == nb_output_files_expected + 1 # adding input file
    
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


if __name__ == "__main__":
    pytest.main([__file__])