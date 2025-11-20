from typing import Optional, Iterable, Any

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
        self.pdf_path = pdf_path
        self.pages = get_pdf_pages(pdf_path)
        self.doc = pymupdf.open(pdf_path)
        self.page_count = len(list(get_pdf_pages(pdf_path)))
        self.title = title
        self.roi_text: tuple[int, int, int, int] = points_from_coordinates(roi_text)
        self.roi_pg_number: tuple[int, int, int, int] = points_from_coordinates(roi_pg_number)
        self.page_offset = page_offset
        self.release_date = release_date
        self.author = author
        self.publisher = publisher

    def extract_text(self, page: Page) -> TobiasPage | None:
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
        if get_page_number_from_page(page, self.roi_pg_number) in range(start, stop+1):
            return TobiasPage(
                title=self.title,
                release_date=self.release_date,
                author=self.author,
                publisher=self.publisher,
                page_content=get_text_from_page(page, self.roi_text),
                page_number=get_page_number_from_page(page, self.roi_pg_number),
            )
        return None

    def extract_image(self, page: Page) -> list[Any] | None:
        """
        creates an instance of tkinter.Image
        """
        start, stop = self.page_offset
        if start is None:
            start = 0
        if stop is None:
            stop = self.page_count
        if get_page_number_from_page(page, self.roi_pg_number) in range(start, stop + 1):
            image_ref = [img[0] for img in page.get_images()]
            images = [self.doc.extract_image(img_ref) for img_ref in image_ref]
            return images

        return None

def get_pdf_pages(pdf_path: str) -> Iterable:
    """
    Load pages of the pdf file
    :return: pages of the pdf file as an iterable
    """
    pdf_doc = pymupdf.open(pdf_path)
    return list(pdf_doc.pages())


def get_text_from_page(page: Page, text_coordinates: tuple[int, int, int, int]) -> str:
    """
    extracts the text from the page of the PDF file
    :param text_coordinates: tuple of ints describing ROI in Page
    :param page: pdf page
    :return: text of the page
    """
    page_rect = pymupdf.Rect(*text_coordinates)
    page_text = page.get_textbox(page_rect)
    return page_text

def get_page_number_from_page(page: Page, page_number_coordinates: tuple[int, int, int, int]) -> int | None:
    """
    extracts the text from the page of the PDF file
    :param page_number_coordinates: tuple of ints describing ROI in Page
    :param page: pdf page
    :return: text of the page
    """
    page_rect = pymupdf.Rect(*page_number_coordinates)
    page_text = page.get_textbox(page_rect)
    try:
        return int(page_text)
    except ValueError:
        return page.number