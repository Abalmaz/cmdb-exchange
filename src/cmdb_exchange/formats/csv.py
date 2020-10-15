import csv
from csv import DictReader, DictWriter


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
    def get_data(cls, steam):
        csvreader = csv.reader(steam)
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
    def export_set(cls, filename, data, fieldnames, **kwargs):
        writer_cls = DictWriter
        with open(filename, 'w') as f:
            writer = writer_cls(f, fieldnames)
            writer.writerows(data)
