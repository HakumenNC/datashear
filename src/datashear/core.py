import os
import csv
from .util import Util


class Splitter:
    
    def __init__(
            self,
            input_file: str,
            output_dir: str = ".",
            output_base_filename: str = "",
            output_prefix: str = "",
            output_sufix: str = "part"
    ):
        self.input_file = input_file
        self.output_dir = output_dir
        self.output_base_filename = output_base_filename
        self.output_prefix = output_prefix
        self.output_sufix = output_sufix

        # File not found
        if not os.path.exists(input_file): raise FileNotFoundError(f"Input file not found: {input_file}")
        # Create folder if not exists
        if not os.path.exists(output_dir): os.makedirs(output_dir)

    def by_rows(self, nb: int, repeat_header: bool = True ):
        if nb <= 0: raise ValueError("rows per file must be greater than 0")

        with open(self.input_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

            try: header = next(reader)
            except: raise ValueError('CSV file is empty')

            output_index = 1
            row_count = 0
            current_file = None
            current_writer = None

            try:
                for row in reader:
                    if row_count == 0:
                        if current_file: current_file.close()

                        output_filename = Util.get_output_filename(
                            self.input_file,
                            output_index,
                            self.output_prefix,
                            self.output_base_filename,
                            self.output_sufix
                        )

                        output_path = os.path.join(self.output_dir, output_filename)
                        current_file = open(output_path, 'w', newline='', encoding='utf-8')
                        current_writer = csv.writer(current_file)

                        if repeat_header: current_writer.writerow(header)

                    current_writer.writerow(row)
                    row_count += 1               

                    if row_count >= nb:
                        Util.show_memory_usage()
                        row_count = 0
                        output_index += 1
                        current_file.close()
                        current_file = None
                
            finally:
                if current_file:
                    current_file.close()
                    current_file = None