import io
import pathlib
import zipfile

from openpyxl import load_workbook
import ipywidgets
from IPython.display import HTML

def generate_zip(button):
    with process_output:
        try:
            print('generating plaintext files')
            output_path = pathlib.Path("outputs")
            output_path.mkdir(exist_ok=True)

            if not output_name.value.endswith(".zip"):
                output_name.value += ".zip"

            output_zip = output_path / output_name.value
            sheet = sheet_selector.value
            column = column_selector.value

            ws = spreadsheet_upload.spreadsheet[sheet]
            header = list(ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]
            col_idx = header.index(column)

            with zipfile.ZipFile(output_zip, 'w') as z:

                rows = enumerate(ws.values)

                # Skip the header
                next(rows)

                for i, row in rows:
                    z.writestr(f"data/{i + 1}.txt", row[col_idx] or "")

            display(
                HTML(
                    f'<a href="{output_zip}" download="{output_name.value}">Download your zip file</a>'
                )
            )
        except Exception as e:
            print(e)
            raise

def update_sheet_names(change):
    spreadsheet = load_workbook(io.BytesIO(change.new[0].content))
    sheets = spreadsheet.sheetnames
    sheet_selector.options = sheets
    spreadsheet_upload.spreadsheet = spreadsheet

    # If there's only one sheet just choose that.
    if len(sheets) == 1:
        sheet_selector.value = sheets[0]

def update_column_names(change):

    sheet = spreadsheet_upload.spreadsheet[change.new]
    header = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))[0]
    column_selector.options = [col for col in header if isinstance(col, str) and col]

width_layout = ipywidgets.Layout(width='90%', height='2lh')
process_output = ipywidgets.Output()
spreadsheet_upload = ipywidgets.FileUpload(
    accept='.xlsx',
    description="Upload your spreadsheet (.xlsx)",
    layout=width_layout
)
sheet_selector = ipywidgets.Select(
    options=[], description="Choose sheet:",
    style = {'description_width': 'initial'},
    layout=width_layout
)
column_selector = ipywidgets.Select(
    options=[], description="Choose columns:",
    style = {'description_width': 'initial'},
    layout=width_layout
)
run_button = ipywidgets.Button(
    description="Generate text files",
    layout=width_layout
)

output_name = ipywidgets.Text("extracted.zip", description='Zip file name:')

run_button.on_click(generate_zip)

spreadsheet_upload.observe(update_sheet_names, names=['value'])
sheet_selector.observe(update_column_names, names=['value'])

ui = ipywidgets.VBox(
    [
        spreadsheet_upload,
        sheet_selector,
        column_selector,
        output_name,
        run_button,
        process_output,
    ]
)