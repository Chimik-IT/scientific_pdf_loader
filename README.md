# scientific-pdf-loader

A configurable PDF text and image extractor for scientific documents, designed as a preprocessing step for LLM and RAG pipelines.

Extracts structured text and embedded images from PDFs using **region-of-interest (ROI) coordinates**, making it robust to complex scientific layouts where simple full-page extraction picks up headers, footers, and page numbers as noise.

## Features

- **ROI-based text extraction** — define bounding box coordinates to target only the content area of each page
- **Logical page number detection** — reads the printed page number from a configurable ROI, decoupling it from the physical PDF page index
- **Image extraction** — extracts all embedded images per page, saved to disk
- **YAML-driven batch configuration** — describe a collection of documents (path, title, author, date, ROIs) in a single config file
- **Structured output** — Pydantic models per page; batch export to Excel

## Use case

Built to prepare scientific literature for downstream LLM processing. Each document is loaded into a structured representation (`TobiasPage`) containing metadata and page content, ready to be passed to a retrieval or question-answering pipeline.

## Installation

```bash
poetry install
```

Requires Python 3.11+.

## Configuration

Coordinates are specified in **PDF points** (1 pt = 1/72 inch). Use a tool like [PyMuPDF's page.get_text("blocks")](https://pymupdf.readthedocs.io/en/latest/page.html) or a PDF viewer with point rulers to determine the correct values for your documents.

Describe your documents in a YAML file:

```yaml
cases:
  - file_path: /path/to/document.pdf
    title: "Example Paper"
    author: "Author Name"
    release_date: "2024-01"
    page_rect: [x, y, width, height]        # ROI for text content, in PDF points
    page_number_rect: [x, y, width, height]  # ROI for printed page number, in PDF points
```

## Usage

```python
from scientific_pdf_loader.pdf_reader import TobisPDF

pdf = TobisPDF(
    pdf_path="document.pdf",
    title="Example Paper",
    roi_text=(50, 80, 500, 700),      # in PDF points
    roi_pg_number=(500, 760, 40, 20), # in PDF points
)

pages = [pdf.extract_text(page) for page in pdf.pages]
```

## Dependencies

- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF parsing and image extraction
- [Pydantic](https://docs.pydantic.dev/) — structured page model
- [pandas](https://pandas.pydata.org/) + openpyxl — Excel export
- PyYAML — batch configuration

## License

GPL-2.0
