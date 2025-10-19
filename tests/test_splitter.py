"""
Tests for the CSV splitter functionality
"""

import os
import csv
import tempfile
import shutil
import unittest
from datashear.splitter import CSVSplitter, split_csv


class TestCSVSplitter(unittest.TestCase):
    """Test cases for CSVSplitter class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, "test_input.csv")
        self.output_dir = os.path.join(self.test_dir, "output")
        
        # Create a sample CSV file
        with open(self.input_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Age', 'City'])
            for i in range(10):
                writer.writerow([f'Person{i}', 20 + i, f'City{i}'])
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_init_creates_output_dir(self):
        """Test that CSVSplitter creates output directory if it doesn't exist"""
        splitter = CSVSplitter(self.input_file, self.output_dir)
        self.assertTrue(os.path.exists(self.output_dir))
    
    def test_init_raises_on_missing_file(self):
        """Test that CSVSplitter raises error for missing input file"""
        with self.assertRaises(FileNotFoundError):
            CSVSplitter("nonexistent.csv")
    
    def test_split_by_rows(self):
        """Test splitting by number of rows"""
        splitter = CSVSplitter(self.input_file, self.output_dir)
        output_files = splitter.split_by_rows(3)
        
        # Should create 4 files (3+3+3+1 rows)
        self.assertEqual(len(output_files), 4)
        
        # Check first file
        with open(output_files[0], 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 4)  # header + 3 data rows
            self.assertEqual(rows[0], ['Name', 'Age', 'City'])
            self.assertEqual(rows[1][0], 'Person0')
    
    def test_split_by_rows_without_header(self):
        """Test splitting without including headers"""
        splitter = CSVSplitter(self.input_file, self.output_dir)
        output_files = splitter.split_by_rows(3, include_header=False)
        
        # Check first file has no header
        with open(output_files[0], 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)  # Only data rows
            self.assertEqual(rows[0][0], 'Person0')
    
    def test_split_by_file_count(self):
        """Test splitting into specific number of files"""
        splitter = CSVSplitter(self.input_file, self.output_dir)
        output_files = splitter.split_by_file_count(3)
        
        # Should create exactly 3 files
        self.assertEqual(len(output_files), 3)
        
        # Check that all data is present
        total_rows = 0
        for file_path in output_files:
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                total_rows += len(rows) - 1  # Exclude header
        
        self.assertEqual(total_rows, 10)  # All 10 data rows
    
    def test_split_by_rows_invalid_value(self):
        """Test that invalid rows_per_file raises ValueError"""
        splitter = CSVSplitter(self.input_file, self.output_dir)
        with self.assertRaises(ValueError):
            splitter.split_by_rows(0)
        with self.assertRaises(ValueError):
            splitter.split_by_rows(-1)
    
    def test_split_by_file_count_invalid_value(self):
        """Test that invalid num_files raises ValueError"""
        splitter = CSVSplitter(self.input_file, self.output_dir)
        with self.assertRaises(ValueError):
            splitter.split_by_file_count(0)
        with self.assertRaises(ValueError):
            splitter.split_by_file_count(-1)
    
    def test_empty_csv_file(self):
        """Test handling of empty CSV file"""
        empty_file = os.path.join(self.test_dir, "empty.csv")
        with open(empty_file, 'w', newline='', encoding='utf-8') as f:
            pass  # Create empty file
        
        splitter = CSVSplitter(empty_file, self.output_dir)
        with self.assertRaises(ValueError):
            splitter.split_by_rows(3)


class TestSplitCSVFunction(unittest.TestCase):
    """Test cases for split_csv convenience function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, "test_input.csv")
        self.output_dir = os.path.join(self.test_dir, "output")
        
        # Create a sample CSV file
        with open(self.input_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Age', 'City'])
            for i in range(10):
                writer.writerow([f'Person{i}', 20 + i, f'City{i}'])
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir)
    
    def test_split_csv_with_rows_per_file(self):
        """Test split_csv function with rows_per_file parameter"""
        output_files = split_csv(
            self.input_file,
            rows_per_file=4,
            output_dir=self.output_dir
        )
        self.assertEqual(len(output_files), 3)  # 4+4+2 rows
    
    def test_split_csv_with_num_files(self):
        """Test split_csv function with num_files parameter"""
        output_files = split_csv(
            self.input_file,
            num_files=2,
            output_dir=self.output_dir
        )
        self.assertEqual(len(output_files), 2)
    
    def test_split_csv_no_params_raises_error(self):
        """Test that split_csv raises error when no splitting criteria provided"""
        with self.assertRaises(ValueError):
            split_csv(self.input_file, output_dir=self.output_dir)
    
    def test_split_csv_both_params_raises_error(self):
        """Test that split_csv raises error when both splitting criteria provided"""
        with self.assertRaises(ValueError):
            split_csv(
                self.input_file,
                rows_per_file=3,
                num_files=2,
                output_dir=self.output_dir
            )
    
    def test_split_csv_custom_prefix(self):
        """Test split_csv function with custom output prefix"""
        output_files = split_csv(
            self.input_file,
            rows_per_file=5,
            output_dir=self.output_dir,
            output_prefix="custom"
        )
        
        # Check that files have custom prefix
        for file_path in output_files:
            self.assertTrue(os.path.basename(file_path).startswith("custom_"))


if __name__ == '__main__':
    unittest.main()
