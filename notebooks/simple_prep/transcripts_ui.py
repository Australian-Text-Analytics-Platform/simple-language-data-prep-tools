"""
Ipywidgets based user interface for the transcript tidying process.

"""

from io import BytesIO
import pathlib
import re

import ipywidgets as widgets
from IPython.display import HTML

from .tidy_transcripts import TidyTranscripts
from .widget_layouts import full_width_layout, selector_layout, description_style

process_output = widgets.Output()

zip_upload = widgets.FileUpload(
    accept=".zip",
    description="Upload transcripts (zip file containing .docx files)",
    layout=full_width_layout,
)
xlsx_upload = widgets.FileUpload(
    accept=".xlsx",
    description="(Optional): Upload a matched spreadsheet with extra information to merge in (.xlsx)",
    layout=full_width_layout,
)
run_button = widgets.Button(
    description="Generate spreadsheet", layout=full_width_layout
)

speaker_separator = widgets.Dropdown(
    options=[
        (r":\t (colon-tab)", ":\t"),
        (r": (colon-space)", ": "),
        (r":\s+ (colon-any whitespace)", r":\s+"),
    ],
    value=":\t",
    description="Speaker separator:",
    layout=selector_layout,
    style=description_style,
)

fill_with_previous_speaker = widgets.Checkbox(
    description="Assign previous speaker when no speaker identified",
    value=False,
    layout=selector_layout,
)


def allow_generating_after_upload(change):
    process_output.clear_output()
    with process_output:
        display(xlsx_upload)
        display(run_button)
        display(speaker_separator)
        display(fill_with_previous_speaker)


zip_upload.observe(allow_generating_after_upload, names=["value"])


def run_process(button):
    with process_output:
        display(HTML("Processing your transcripts"))

        spreadsheet = None
        if xlsx_upload.value:
            spreadsheet = bytes(xlsx_upload.value[0].content)

        transcripts = TidyTranscripts.from_zip(
            BytesIO(zip_upload.value[0].content),
            split_speaker_on=speaker_separator.value,
            fill_missing_speaker_with_previous_speaker=fill_with_previous_speaker.value,
            spreadsheet_bytes=spreadsheet,
        )
        generated_transcript = transcripts.as_xlsx()

        pathlib.Path("outputs").mkdir(exist_ok=True)
        generated_transcript.save("outputs/combined_transcripts.xlsx")

        display(
            HTML(
                '<a href="outputs/combined_transcripts.xlsx" download="combined_transcripts.xlsx">'
                "Download your combined transcripts"
                "</a>"
            )
        )


run_button.on_click(run_process)

ui = widgets.VBox(
    [zip_upload, process_output],
)
