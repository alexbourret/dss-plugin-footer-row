import dataiku
import pandas
import json

from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config
from footer_row_column_processor import ColumnProcessor

input_A_names = get_input_names_for_role('input_A_role')
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

output_A_names = get_output_names_for_role('main_output')

output = dataiku.Dataset(output_A_names[0])
input_dataframe = input_A_datasets[0].get_dataframe()

config = get_recipe_config()
columns_to_process = config.get("columns", [])
processors = []

for column_to_process in columns_to_process:
    column_name = column_to_process.get("column")
    column_operation = column_to_process.get("operation")
    processors.append(ColumnProcessor(column_name, column_operation))
output = dataiku.Dataset(output_A_names[0])

first_dataframe = True
with output.get_writer() as writer:
    unnested_items_rows = []
    for index, input_parameters_row in input_dataframe.iterrows():
        row = input_parameters_row.to_dict()
        for column_to_process, processor in zip(columns_to_process, processors):
            column_name = column_to_process.get("column")
            value = row.get(column_name, "")
            processor.ingest(value)
    output_row = {}
    for processor in processors:
        output_row[processor.get_column_name()] = processor.compute()
    unnested_items_rows = [output_row]
    unnested_items_rows = pandas.DataFrame(unnested_items_rows)
    output.write_schema_from_dataframe(unnested_items_rows)
    if not unnested_items_rows.empty:
        writer.write_dataframe(unnested_items_rows)
