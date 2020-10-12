import csv
import fileinput
from contextlib import contextmanager
from csv import DictReader, DictWriter


from src.cmdb_exchange.utils import flatten_data


class CSVFormatReader(DictReader):
    schema = None

    def __next__(self):
        obj = DictReader.__next__(self)
        if self.schema:
            data = self.schema.load(obj)
            obj = data
        return obj

    def next(self):
        if not hasattr(DictReader, "__next__"):
            DictReader.__next__ = DictReader.next
        return self.__next__()

    @classmethod
    def import_from_schema(cls, schema):
        return type(
            'CSVFormatReader',
            (cls, object),
            {"schema": schema}
        )


class CSVFormat:
    title = 'csv'
    extensions = ('csv',)

    @classmethod
    def get_column_name(cls, filename):
        with open(filename) as f:
            d_reader = csv.DictReader(f)
            headers = d_reader.fieldnames
        return headers

    @classmethod
    def get_data(cls, filename):
        with open(filename) as f:
            csvreader = csv.reader(f)
            parsed_csv = list(csvreader)
            data_rows = parsed_csv[1:]  # discard column names
        return data_rows

    @classmethod
    def import_set(cls, filename, schema=None, **kwargs):
        dset = []
        with open(filename) as f:
            if schema:
                reader = CSVFormatReader.import_from_schema(schema)
                rows = reader(f, **kwargs)
            else:
                rows = CSVFormatReader(f, **kwargs)
            for row in rows:
                dset.append(row)
        return dset

    @classmethod
    def export_set(cls, data, filename, many=True,
                   schema=None, fieldnames=None, **kwargs):
        writer_cls = DictWriter
        if schema:
            serialized_data = schema.dump(data, many=many)
            data = serialized_data
        with open(filename, 'w') as f:
            flatt_data = flatten_data(data)
            if fieldnames is None:
                fieldnames = flatt_data[0].keys()
            writer = writer_cls(f, fieldnames)
            writer.writerows(flatt_data)

    @contextmanager
    def open(self, filepath, mode='r', newline=''):
        f = fileinput.input(files=filepath, openhook=fileinput.hook_encoded("utf-8-sig"))
        try:
            yield f
        finally:
            f.close()
