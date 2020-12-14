import csv
from csv import DictWriter
from typing import Any, TextIO, Optional, Sequence, Mapping


class Format:

    def get_column_name(self, data):
        raise NotImplementedError

    @classmethod
    def get_data(cls, data):
        raise NotImplementedError

    @classmethod
    def create_file(cls, *args, **kwargs):
        raise NotImplementedError


class CSVFormat(Format):

    title = 'csv'
    extensions = ('csv',)

    @classmethod
    def get_column_name(cls, steam: TextIO) -> Optional[Sequence[str]]:
        csvreader = csv.DictReader(steam)
        headers = csvreader.fieldnames
        return headers

    @classmethod
    def get_data(cls, steam: TextIO) -> list:
        csvreader = csv.DictReader(steam)
        data_rows = list(csvreader)
        return data_rows

    @classmethod
    def create_file(cls,
                    filename: str,
                    data: list,
                    fieldnames: list,
                    headers: Mapping[str, Any],
                    **kwargs) -> None:
        writer_cls = DictWriter
        with open(filename, 'w') as f:
            writer = writer_cls(f, fieldnames)
            writer.writerow(headers)
            writer.writerows(data)
