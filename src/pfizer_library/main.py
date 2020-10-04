from pathlib import Path

from src.pfizer_library.constants import EXTENSIONS


class Transfer:
    @staticmethod
    def get_extension(filename=None):
        return Path(filename).suffix[1:]

    @staticmethod
    def load(file=None, schema=None, **kwargs):
        # TODO raise exception if format did not find
        extension = Path(file).suffix[1:]
        fmt = EXTENSIONS[extension]
        data = fmt.import_set(file, schema)
        return data

    @staticmethod
    def export(data, filename=None, schema=None, fieldnames=None, **kwargs):
        extension = Path(filename).suffix[1:]
        fmt = EXTENSIONS[extension]
        csv_file = fmt.export_set(data=data,
                                  filename=filename,
                                  schema=schema,
                                  fieldnames=fieldnames)
        return csv_file
