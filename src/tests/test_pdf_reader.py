from typing import Iterable

import pytest
from pymupdf import Page

from scientific_pdf_loader.pdf_reader import (TobisPDF, get_pdf_pages,
                                              points_from_coordinates, TobiasPage)

@pytest.fixture(scope="module")
def offset():
    return 30, 200

@pytest.fixture(scope="module")
def text_coordinates():
    return 147, 94, 440, 675

@pytest.fixture(scope="module")
def page_number_coordinates():
    return '515', '36', '44', '40'

@pytest.fixture(scope="module")
def pdf_file():
    return "data/LL_Pankreaskarzinom_Langversion_3.1.pdf"

@pytest.fixture(scope="module")
def test_tobis_pdf_without_offset(pdf_file_path, page_number_coordinates, text_coordinates):
    return TobisPDF(pdf_path=pdf_file,
                    title="My Test PDF",
                    roi_text=text_coordinates,
                    roi_pg_number=page_number_coordinates,
                    )

@pytest.fixture(scope="module")
def test_tobias_pdf_with_offset(pdf_file_path, page_number_coordinates, text_coordinates, offset):
    return TobisPDF(pdf_path=pdf_file,
                    page_offset=offset,
                    title="My Test PDF",
                    roi_text=text_coordinates,
                    roi_pg_number=page_number_coordinates,
                    )

@pytest.fixture(scope="module")
def pdf_pages(pdf_file):
    return list(get_pdf_pages(pdf_path=pdf_file))


@pytest.fixture(scope="module")
def test_pdf_page(pdf_pages):
    return pdf_pages[21]

def test_points_from_coordinates_with_strings_for_points(text_coordinates):
    assert points_from_coordinates(
        coordinates=text_coordinates) == (147, 94, 147 + 440, 94 + 675)

def test_points_from_coordinates_normal_usage(page_number_coordinates):
    assert points_from_coordinates(
        coordinates=page_number_coordinates) == (515, 36, 515 + 44, 36 + 40)

def test_creation_of_TobisPDF(test_tobis_pdf_without_offset):

    assert test_tobis_pdf_without_offset.title == "My Test PDF"
    assert isinstance(test_tobis_pdf_without_offset.pages, Iterable)
    assert test_tobis_pdf_without_offset.roi_pg_number == (515, 36, 515 + 44, 36 + 40)
    assert test_tobis_pdf_without_offset.roi_text == (147, 94, 147 + 440, 94 + 675)

def test_get_pdf_pages(pdf_file):

    pdf_pages = list(get_pdf_pages(pdf_path=pdf_file))

    assert isinstance(pdf_pages, Iterable)
    assert isinstance(pdf_pages[0], Page)

def test_page_extraction(test_tobis_pdf_without_offset, test_tobias_pdf_with_offset,test_pdf_page):
    test_page = test_tobis_pdf_without_offset.extract(test_pdf_page)

    assert isinstance(test_page.page_content, str)
    assert isinstance(test_page.page_number, int)

def test_page_number_extraction(test_pdf_page, test_tobis_pdf_without_offset,
                                test_tobias_pdf_with_offset):

    test_text_wo_offset = test_tobis_pdf_without_offset.extract(test_pdf_page)
    test_text_with_offset = test_tobias_pdf_with_offset.extract(test_pdf_page)
    # no offset
    assert isinstance(test_text_wo_offset.page_number, int)
    assert isinstance(test_text_wo_offset.page_content, str)
    assert test_text_wo_offset.page_number == 22
    assert isinstance(test_text_wo_offset, TobiasPage)
    assert test_text_wo_offset.title == "My Test PDF"

    # with offset
    assert test_text_with_offset is None
