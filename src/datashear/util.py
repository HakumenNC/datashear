import psutil
import os

class Util:

    @staticmethod
    def show_memory_usage():
        process = psutil.Process(os.getpid())
        memory = process.memory_info().rss / 1024 / 1024
        print(f"Memory usage: {memory:.1f} MB")

    @staticmethod
    def get_output_filename(
      input_filename: str,
      index: int = 1,
      prefix: str = "",
      base: str = "",
      sufix: str = "",
      extension: str = ""
    ):
        filename = os.path.splitext(os.path.basename(input_filename))[0]
        extension = os.path.splitext(input_filename)[1]

        parts = []
        if prefix != "": parts.append(prefix)
        if base != "": parts.append(base)
        else: parts.append(filename)
        if sufix != "": parts.append(sufix)
        parts.append(str(index))

        return "_".join(parts) + extension

