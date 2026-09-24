# Simple Data Preparation Notebooks

This is a collection of simple browser based computational notebooks for performing some common data transformation and preparation tasks. These are primarily aimed at addressing some common data challenges, where the tools you might want to use require a different format to the data/materials you currently have.

These tools aim to have a simple user interface and basic configuration options to handle the most common problems, but certainly won't be able to address every need. They all run entirely in your browser: your data is never transferred outside your own computer. The complete source code for each tool is included and published under an open source licence, so you are welcome to inspect, modify, customise, or learn from as you so desire (however we do hope that the basic options covered are enough for most people).

The specific tools included are:

- [The Word Transcript Tabulator notebook](word_transcript_tabulator.ipynb). Takes a set of interview transcripts in Microsoft Word format (`docx` format only), and converts them into a structured Excel spreadsheet (`xlsx` format).
- [The Spreadsheet to Plaintext notebook](spreadsheet_to_plaintext.ipynb). Upload a structured Excel spreadsheet (`xlsx` format), and choose which columns to pull out into separate text files.
- [The Document Text Extractor notebook](document_text_extractor.ipynb). Takes a set of PDF and Word documents (`docx` format), and pulls out the text into either a set of plaintext files, or a structured format like a spreadsheet. This tool does not perform optical character recognition (OCR), but can work with the outputs of tools like [Scribe OCR](https://scribeocr.com/) (also runs in your browser).


## Citation

These tools have been built by Sam Hames as part of the Language Data Commons of Australia (LDaCA) research infrastructure project. If you use these tools, please cite them. 

An example citation is:

Hames, S. (2026). Simple Language Data Preparation Tools. https://doi.org/10.5281/zenodo.20606858


## Contact and Support

You can reach out to the LDaCA project via the [contact information on our website](https://www.ldaca.edu.au/contact/). If you run into issues or problems with these tools, please raise an issue [on the GitHub repository](https://github.com/Australian-Text-Analytics-Platform/simple-language-data-prep-tools/issues).


## Acknowledgment

The Language Data Commons of Australia (LDaCA) is a co-investment partnership with the Australian Research Data Commons (ARDC) through the HASS and Indigenous Research Data Commons (DOI: 10.3565/kq2v-9g52). The ARDC is enabled by the Australian Government’s National Collaborative Research Infrastructure Strategy (NCRIS).