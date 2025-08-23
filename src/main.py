from src.scientific_pdf_loader.pdf_reader import TobisPDF, get_pdf_pages

if '__main__' == __name__:
    pancreas_ll_pdf = TobisPDF(
        pdf_path="../data/LL_Pankreaskarzinom_Langversion_3.1.pdf",
        title="S3-Leitlinie Exokrines Pankreaskarzinom",
        release_date="September 2024",
        roi_text=(147, 94, 440, 675),
        roi_pg_number=('515', '36', '44', '40'),
        )

    pancreas_ll_pdf_page = pancreas_ll_pdf.extract(list(pancreas_ll_pdf.pages)[21])

    print(pancreas_ll_pdf_page.page_number, "is an ", type(pancreas_ll_pdf_page.page_number))
    print(pancreas_ll_pdf_page.page_content)

