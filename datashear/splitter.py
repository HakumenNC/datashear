"""
Core CSV splitting functionality
"""

import csv
import os
from typing import Optional, Union


class CSVSplitter:
    """
    A class to split CSV files into multiple smaller files.
    
    Args:
        input_file: Path to the input CSV file
        output_dir: Directory where split files will be saved (default: current directory)
        output_prefix: Prefix for output files (default: 'split')
    """
    
    def __init__(
        self,
        input_file: str,
        output_dir: str = ".",
        output_prefix: str = "split"
    ):
        self.input_file = input_file
        self.output_dir = output_dir
        self.output_prefix = output_prefix
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def split_by_rows(
        self,
        rows_per_file: int,
        include_header: bool = True
    ) -> list:
        """
        Split CSV file by number of rows.
        
        Args:
            rows_per_file: Number of data rows per output file
            include_header: Whether to include header in each output file
            
        Returns:
            List of created output file paths
        """
        if rows_per_file <= 0:
            raise ValueError("rows_per_file must be positive")
        
        output_files = []
        
        with open(self.input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            
            # Read header
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError("CSV file is empty")
            
            file_num = 1
            row_count = 0
            current_writer = None
            current_file = None
            
            for row in reader:
                if row_count == 0:
                    # Close previous file if exists
                    if current_file:
                        current_file.close()
                    
                    # Open new file
                    output_path = os.path.join(
                        self.output_dir,
                        f"{self.output_prefix}_{file_num}.csv"
                    )
                    current_file = open(output_path, 'w', newline='', encoding='utf-8')
                    current_writer = csv.writer(current_file)
                    
                    # Write header if needed
                    if include_header:
                        current_writer.writerow(header)
                    
                    output_files.append(output_path)
                    file_num += 1
                
                current_writer.writerow(row)
                row_count += 1
                
                if row_count >= rows_per_file:
                    row_count = 0
            
            # Close last file
            if current_file:
                current_file.close()
        
        return output_files
    
    def split_by_file_count(
        self,
        num_files: int,
        include_header: bool = True
    ) -> list:
        """
        Split CSV file into a specific number of files.
        
        Args:
            num_files: Number of output files to create
            include_header: Whether to include header in each output file
            
        Returns:
            List of created output file paths
        """
        if num_files <= 0:
            raise ValueError("num_files must be positive")
        
        # First, count total rows
        with open(self.input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            try:
                header = next(reader)
            except StopIteration:
                raise ValueError("CSV file is empty")
            
            total_rows = sum(1 for _ in reader)
        
        if total_rows == 0:
            raise ValueError("CSV file has no data rows")
        
        # Calculate rows per file
        rows_per_file = (total_rows + num_files - 1) // num_files  # Ceiling division
        
        return self.split_by_rows(rows_per_file, include_header)


def split_csv(
    input_file: str,
    rows_per_file: Optional[int] = None,
    num_files: Optional[int] = None,
    output_dir: str = ".",
    output_prefix: str = "split",
    include_header: bool = True
) -> list:
    """
    Convenience function to split a CSV file.
    
    Args:
        input_file: Path to the input CSV file
        rows_per_file: Number of data rows per output file (mutually exclusive with num_files)
        num_files: Number of output files to create (mutually exclusive with rows_per_file)
        output_dir: Directory where split files will be saved
        output_prefix: Prefix for output files
        include_header: Whether to include header in each output file
        
    Returns:
        List of created output file paths
        
    Raises:
        ValueError: If neither or both splitting criteria are provided
    """
    if rows_per_file is None and num_files is None:
        raise ValueError("Either rows_per_file or num_files must be specified")
    
    if rows_per_file is not None and num_files is not None:
        raise ValueError("Cannot specify both rows_per_file and num_files")
    
    splitter = CSVSplitter(input_file, output_dir, output_prefix)
    
    if rows_per_file is not None:
        return splitter.split_by_rows(rows_per_file, include_header)
    else:
        return splitter.split_by_file_count(num_files, include_header)
