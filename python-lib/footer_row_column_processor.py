import numpy


class ColumnProcessor():
    stack = []
    end_result = None
    column_name = None

    def __init__(self, column_name, operation, separator=None):
        self.column_name = column_name
        self.operation = operation
        if self.operation == "concatenate":
            self.end_result = ""
            if separator:
                self.separator = str(separator)
            else:
                self.separator = ""
        elif self.operation == "total":
            self.end_result = 0.

    def ingest(self, value):
        if self.operation == "concatenate":
            self.end_result = self.end_result + self.separator + value
        elif self.operation == "total":
            if value is not None and not numpy.isnan(value):
                self.end_result = self.end_result + float(value)

    def compute(self):
        if self.operation in ["concatenate", "total"]:
            return self.end_result

    def get_column_name(self):
        return self.column_name
