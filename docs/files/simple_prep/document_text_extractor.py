"""
Handle the extraction of text from a set of PDF and Word (.docx) documents.

"""

from urllib.parse import quote
from zipfile import ZipFile
import collections
import io
import math
import pathlib
import time

from IPython.display import HTML
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from openpyxl import Workbook
from pypdf import PdfReader
import ipywidgets as widgets

from . import version
from .widget_layouts import full_width_layout, selector_layout, description_style


def extract_pages_pdf(file):
    """Extract the text from each page in the PDF, one at a time."""

    reader = PdfReader(file, strict=False)

    for page in reader.pages:
        page_text = "".join(page.extract_text())
        # yes this happens in real PDFs...
        # And needs to be handled because it's not valid in a string for .xlsx format.
        page_text = page_text.replace("\x00", "")

        yield ("page", page.page_number, None, page_text)


def _extract_doc_table_contents(table):
    """Extract contents of a docx table, accounting for nesting of tables."""
    for row in table.rows:
        for cell in row.cells:
            yield cell.text.strip()

            for subtable in cell.tables:
                yield from _extract_doc_table_contents(table)

        yield "\n"


def extract_paragraphs_docx(file):
    """Extract the text from the docx file, one paragraph at a time."""

    doc = Document(file)

    for sequence_number, item in enumerate(doc.iter_inner_content()):
        if isinstance(item, Paragraph):
            # Skip blank paragraphs.
            if item.text.strip():
                yield ("paragraph", sequence_number, item.style.name, item.text.strip())

        elif isinstance(item, Table):
            yield (
                "table",
                sequence_number,
                None,
                " ".join(_extract_doc_table_contents(item)),
            )

        else:
            raise ValueError(f"I don't know what to do with {item}.")


def iterate_files_text(doc_zip):
    """Generator of files in the zip and their associated text content."""

    with ZipFile(doc_zip) as zipf:
        valid_files = [
            f for f in zipf.namelist() if f.lower().endswith((".docx", ".pdf"))
        ]

        progress_bar = widgets.IntProgress(
            value=1,
            min=1,
            max=len(valid_files),
            description="Processing Files:",
            bar_style="info",
            orientation="horizontal",
            style=description_style,
            layout=full_width_layout,
        )

        display(progress_bar)

        for zippath in valid_files:
            with zipf.open(zippath, "r") as f:
                if zippath.lower().endswith(".docx"):
                    yield zippath, extract_paragraphs_docx(f)

                elif zippath.lower().endswith(".pdf"):
                    yield zippath, extract_pages_pdf(f)

            progress_bar.value += 1


def prepare_plaintext(doc_zip, output_filename, encoding):
    """Prepare the plaintext extract, merging all the text from each document together."""

    with ZipFile(output_filename, "w") as z:
        for filepath, text in iterate_files_text(doc_zip):
            z.writestr(
                filepath + ".txt", ("\n\n".join(t[0] for t in text)).encode(encoding)
            )


def prepare_spreadsheet(doc_zip, output_filename):
    """Prepare a spreadsheet of text data from the given files."""

    wb = Workbook()
    wb.remove(wb["Sheet"])

    wb.create_sheet("document_text")

    ws = wb["document_text"]

    ws.append(["source_file", "unit_type", "sequence_number", "style", "text"])

    for filepath, text in iterate_files_text(doc_zip):
        for t in text:
            ws.append([filepath, *t])

    wb.save(output_filename)


def run_process(button):
    """Run the process, dispatching to the right function based on what's selected."""

    process_output.clear_output()

    with process_output:
        try:
            mode = extraction_mode.value
            output = output_name.value

            uploaded = io.BytesIO(zip_upload.value[0].content)

            # Make sure the filename is right
            if mode == "docs" and not output.endswith(".zip"):
                output += ".zip"

            elif mode == "parts" and not output.endswith(".xlsx"):
                output += ".xlsx"

            folder = pathlib.Path("outputs")
            folder.mkdir(exist_ok=True)
            download_location = folder / output

            if mode == "docs":
                prepare_plaintext(uploaded, download_location, output_encoding.value)
            elif mode == "parts":
                prepare_spreadsheet(uploaded, download_location)

            display(
                HTML(
                    f'<a href="{download_location}" download="{output}">'
                    "Download your file</a>"
                )
            )

        except Exception as e:
            display(e)
            print("Something went wrong that we didn't know how to handle")


process_output = widgets.Output()

zip_upload = widgets.FileUpload(
    accept=".zip",
    description="Upload your documents (zip file containing .docx and .pdf files)",
    layout=full_width_layout,
)

output_name = widgets.Text(
    "extracted_text",
    description="Output filename:",
    style=description_style,
    layout=selector_layout,
)

run_button = widgets.Button(
    description="Extract text from documents", layout=full_width_layout
)

run_button.on_click(run_process)

extraction_mode = widgets.Dropdown(
    value="parts",
    options=[
        ("Extract whole documents into text files", "docs"),
        (
            "Extract paragraphs (word), pages (pdf) from documents into a spreadsheet",
            "parts",
        ),
    ],
    description="Text extraction mode:",
    layout=selector_layout,
    style=description_style,
)

output_encoding = widgets.Dropdown(
    options=[
        "utf_32",
        "utf_32_be",
        "utf_32_le",
        "utf_16",
        "utf_16_be",
        "utf_16_le",
        "utf_7",
        "utf_8",
        "utf_8_sig",
    ],
    value="utf_8",
    description="Text Encoding (text files only):",
    style=description_style,
    layout=selector_layout,
)


ui = widgets.VBox(
    [
        zip_upload,
        extraction_mode,
        output_encoding,
        output_name,
        run_button,
        process_output,
    ]
)
