from pathlib import Path

from src.pfizer_library.constants import EXTENSIONS


class Transfer:
    @staticmethod
    def load(file=None, schema=None, **kwargs):
        # TODO raise exception if format did not find
        extension = Path(file).suffix[1:]
        fmt = EXTENSIONS[extension]
        data = fmt.import_set(file, schema)
        return data

    @staticmethod
    def export(data, filename=None, schema=None, **kwargs):
        extension = Path(filename).suffix[1:]
        fmt = EXTENSIONS[extension]
        csv_file = fmt.export_set(data=data, filename=filename, schema=schema)
        return csv_file
