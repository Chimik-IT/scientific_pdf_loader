from typing import Optional, Iterable

import pymupdf
from pydantic import BaseModel
from pymupdf import Page


def points_from_coordinates(coordinates: tuple[int, int, int,int]) -> tuple[int, int, int,int]:
    point_x, point_y, width, height = coordinates
    return int(point_x), int(point_y), int(point_x) + int(width), int(point_y) + int(height)

class TobiasPage(BaseModel):
    """
    Holds the information of the loaded PDF file
    """
    title: str
    release_date: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_content: str
    page_number: int

class TobisPDF:
    """
    Class that holds the information to load and extract text from a pdf file.
    """

    def __init__(self, pdf_path: str,title: str,roi_text: tuple[int, int, int, int],
                 roi_pg_number: tuple[int, int, int, int],
                 page_offset: tuple[int, int] = (None, None),
                 release_date: str = None, author: str = None, publisher: str = None) -> None:
        self.pages = get_pdf_pages(pdf_path)
        self.page_count = len(list(get_pdf_pages(pdf_path)))
        self.title = title
        self.roi_text: tuple[int, int, int, int] = points_from_coordinates(roi_text)
        self.roi_pg_number: tuple[int, int, int, int] = points_from_coordinates(roi_pg_number)
        self.page_offset = page_offset
        self.release_date = release_date
        self.author = author
        self.publisher = publisher

    def extract(self, page: Page) -> TobiasPage | None:
        """
        creates an instance of TobiasPage. containing metadata and context of the page
        :param page: pymupdf page
        :return: instance of TobiasPage
        """
        start, stop = self.page_offset
        if start is None:
            start = 0
        if stop is None:
            stop = self.page_count
        if start <= get_roi_from_page(page, self.roi_pg_number) <= stop:
            return TobiasPage(
                title=self.title,
                release_date=self.release_date,
                author=self.author,
                publisher=self.publisher,
                page_content=get_roi_from_page(page, self.roi_text),
                page_number=get_roi_from_page(page, self.roi_pg_number),
            )
        return None


def get_pdf_pages(pdf_path: str) -> Iterable:
    """
    Load pages of the pdf file
    :return: pages of the pdf file as an iterable
    """
    pdf_doc = pymupdf.open(pdf_path)
    return pdf_doc.pages()


def get_roi_from_page(page: Page, coordinates: tuple[int, int, int, int]) -> str | int:
    """
    extracts the text from the page of the PDF file
    :param coordinates: tuple of ints describing ROI in Page
    :param page: pdf page
    :return: text of the page
    """
    page_rect = pymupdf.Rect(*coordinates)
    page_text = page.get_textbox(page_rect)
    try:
        roi_content = int(page_text)
        return roi_content
    except ValueError:
        return page_text
