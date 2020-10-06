from pathlib import Path

from src.pfizer_library.constants import EXTENSIONS
from src.pfizer_library.exceptions import UnsupportedFormat


def get_extension(filename=None):
    extension = Path(filename).suffix[1:]
    try:
        fmt = EXTENSIONS[extension]
    except KeyError:
        raise UnsupportedFormat(f'Format {extension} '
                                f'cannot be exported.')
    return fmt


class Transfer:
    @staticmethod
    def load(filename=None, schema=None, **kwargs):
        fmt = get_extension(filename)
        return fmt.import_set(filename=filename, schema=schema)

    @staticmethod
    def export(data, filename=None, schema=None,
               fieldnames=None, many=True, **kwargs):
        fmt = get_extension(filename)

        return fmt.export_set(data=data,
                              filename=filename,
                              schema=schema,
                              fieldnames=fieldnames,
                              many=many)
