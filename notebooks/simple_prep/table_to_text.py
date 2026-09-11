import collections
import io
import pathlib
import time
import zipfile

from IPython.display import HTML
from openpyxl import load_workbook
import ipywidgets as widgets


def generate_zip(button):
    with process_output:
        try:
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

            # Count rows first to have a proper progress bar
            n_rows = sum(1 for _ in ws.values) - 1  # account for header row.

            progress_bar = widgets.IntProgress(
                value=1,
                min=1,
                max=n_rows,
                description="Processing Rows:",
                bar_style="info",
                orientation="horizontal",
                style=description_style,
                layout=full_width_layout,
            )

            display(progress_bar)

            last_progress_update = time.monotonic()
            next_progress_report = 9
            report_delta = 10

            with zipfile.ZipFile(output_zip, "w") as z:

                rows = enumerate(ws.values)

                # Skip the header
                next(rows)

                for i, row in rows:

                    # i + 2 as the name because we want it to be an Excel row number,
                    # which starts at 1, and we have a header.
                    z.writestr(f"data/{i + 2}.txt", row[col_idx] or "")

                    # Rate limit progress bar updates, adaptively
                    if i == next_progress_report:
                        progress_bar.value = i + 1

                        current_time = time.monotonic()

                        if current_time - last_progress_update < 0.5:
                            report_delta *= 2

                        next_progress_report += report_delta
                        last_progress_update = current_time

            progress_bar.value = n_rows

            display(
                HTML(
                    f'<a href="{output_zip}" download="{output_name.value}">'
                    "Download your zip file</a>"
                )
            )
        except Exception as e:
            display(e)
            display("Sorry, something went wrong. The error details are above.")
            raise


def update_sheet_names(change):
    """Update sheet names when a new file is uploaded."""

    header_row_options = collections.defaultdict(dict)

    spreadsheet = load_workbook(io.BytesIO(change.new[0].content))
    sheets = spreadsheet.sheetnames
    sheet_selector.options = sheets
    spreadsheet_upload.spreadsheet = spreadsheet

    # If there's only one sheet just choose that.
    if len(sheets) == 1:
        sheet_selector.value = sheets[0]


def update_header_rows(change):
    """Update header row chooser when the sheet changes."""

    sheet = spreadsheet_upload.spreadsheet[change.new]

    header_options = []

    # Extract potential header rows until we have at least 10 options.
    for i, row in enumerate(sheet.iter_rows(values_only=True)):
        cols = [str(col) for col in row if col]

        # Don't mark rows with nothing in them as headers
        if cols:
            row_number = i + 1
            display = f"{row_number}: {' '.join(cols)}"
            header_options.append((display, row_number))

        # Go until we have 10 header candidates, or we reach the end of the sheet.
        if len(header_options) >= 10:
            break

    header_row_selector.options = header_options

    if header_options:
        header_row_selector.value = header_options[0][1]


def update_column_names(change):
    """
    Update column names when a new header row is chosen.

    """
    sheet = spreadsheet_upload.spreadsheet[sheet_selector.value]
    header = list(
        sheet.iter_rows(
            min_row=header_row_selector.value,
            max_row=header_row_selector.value,
            values_only=True,
        )
    )[0]
    text_column_selector.options = [str(col) for col in header if col]


full_width_layout = widgets.Layout(width="95%", height="2lh")
selector_layout = widgets.Layout(width="95%")

# Make sure the descriptions aren't truncated and are aligned.
description_style = {"description_width": "25%"}
process_output = widgets.Output()
spreadsheet_upload = widgets.FileUpload(
    accept=".xlsx",
    description="Upload your spreadsheet (.xlsx)",
    layout=full_width_layout,
    style=description_style,
)
sheet_selector = widgets.Select(
    options=[],
    description="Sheet:",
    style=description_style,
    layout=selector_layout,
)

header_row_selector = widgets.Dropdown(
    options=[],
    description="Header Row:",
    style=description_style,
    layout=selector_layout,
)

text_column_selector = widgets.Select(
    options=[],
    description="Text column:",
    style=description_style,
    layout=selector_layout,
)

name_column_selector = widgets.Select(
    options=[],
    description="Filename columns:",
    style=description_style,
    layout=selector_layout,
)


run_button = widgets.Button(description="Generate text files", layout=full_width_layout)

output_name = widgets.Text(
    "extracted.zip",
    description="Zip filename:",
    style=description_style,
    layout=selector_layout,
)

run_button.on_click(generate_zip)

spreadsheet_upload.observe(update_sheet_names, names=["value"])
sheet_selector.observe(update_header_rows, names=["value"])
header_row_selector.observe(update_column_names, names=["value"])

ui = widgets.VBox(
    [
        spreadsheet_upload,
        sheet_selector,
        header_row_selector,
        text_column_selector,
        name_column_selector,
        output_name,
        run_button,
        process_output,
    ]
)
