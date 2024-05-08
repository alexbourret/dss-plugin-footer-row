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

    def ingest(self, value):
        if self.operation == "concatenate":
            self.end_result = self.end_result + self.separator + value

    def compute(self):
        if self.operation == "concatenate":
            return self.end_result

    def get_column_name(self):
        return self.column_name
