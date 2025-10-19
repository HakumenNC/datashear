"""
Command-line interface for datashear
"""

import argparse
import sys
from .splitter import split_csv


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Split CSV files into multiple smaller files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split by rows (1000 rows per file)
  datashear input.csv -r 1000
  
  # Split into 5 files
  datashear input.csv -n 5
  
  # Split with custom output directory and prefix
  datashear input.csv -r 1000 -o output/ -p data
  
  # Split without including headers
  datashear input.csv -r 1000 --no-header
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Input CSV file to split"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-r", "--rows",
        type=int,
        dest="rows_per_file",
        help="Number of rows per output file"
    )
    group.add_argument(
        "-n", "--num-files",
        type=int,
        dest="num_files",
        help="Number of output files to create"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Output directory for split files (default: current directory)"
    )
    
    parser.add_argument(
        "-p", "--prefix",
        default="split",
        help="Prefix for output files (default: 'split')"
    )
    
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Do not include header in output files"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    args = parser.parse_args()
    
    try:
        output_files = split_csv(
            input_file=args.input_file,
            rows_per_file=args.rows_per_file,
            num_files=args.num_files,
            output_dir=args.output_dir,
            output_prefix=args.prefix,
            include_header=not args.no_header
        )
        
        print(f"Successfully split CSV into {len(output_files)} files:")
        for file_path in output_files:
            print(f"  - {file_path}")
        
        return 0
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
