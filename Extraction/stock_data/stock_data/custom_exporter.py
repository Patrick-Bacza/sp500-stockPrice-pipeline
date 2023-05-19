from scrapy.exporters import CsvItemExporter

class CustomCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = '|'  # Set the desired delimiter
        super().__init__(*args, **kwargs)