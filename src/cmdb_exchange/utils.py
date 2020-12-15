import glob
import os


def concatenate_path(path: str, filename: str) -> str:
    if not os.path.isdir(path):
        raise OSError(f"Given path {path} is not a directory")
    return os.path.join(path, filename)


def get_file_by_name_pattern(path: str, pattern: str) -> str:
    path = concatenate_path(path, pattern)
    file = glob.glob(path)
    if not file:
        raise OSError("File not found")
    elif len(file) > 1:
        raise OSError("More than one file was found")
    else:
        return file[0]
