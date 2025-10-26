"""
Test script to verify the by_size method works correctly.
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from datashear.core import Splitter

def test_by_size():
    """Test the by_size method with sample data."""
    
    # Chemin vers le fichier de test
    input_file = os.path.join(os.path.dirname(__file__), 'input/MOCK_DATA_M.csv')
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    
    # Get original file size
    original_size = os.path.getsize(input_file)
    print(f"Original file size: {original_size} bytes")

    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Nettoyer le répertoire de sortie
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Test with different sizes
    test_sizes = [
        original_size // 4,  # Quarter size
        original_size // 2,  # Half size  
        original_size * 2    # Double size (should create only one file)
    ]
    
    for i, target_size in enumerate(test_sizes, 1):
        print(f"\nTest {i}: Target size = {target_size} bytes")
        
        # Create splitter
        splitter = Splitter(
            input_file, 
            output_dir, 
            output_prefix=f"size_test_{i}",
            output_sufix="by_size"
        )
        
        try:
            # Split by size
            splitter.by_size(target_size, repeat_header=True)
            
            # Count output files
            output_files = [f for f in os.listdir(output_dir) 
                          if f.startswith(f"size_test_{i}_")]
            print(f"Created {len(output_files)} files")
            
            # Show file sizes
            for filename in sorted(output_files):
                filepath = os.path.join(output_dir, filename)
                file_size = os.path.getsize(filepath)
                print(f"  {filename}: {file_size} bytes")
                
        except Exception as e:
            print(f"Error in test {i}: {e}")

if __name__ == "__main__":
    test_by_size()