from scientific_pdf_loader.pdf_reader import TobisPDF
import pandas as pd

if '__main__' == __name__:
    hepatocell_carcinoma_pdf = TobisPDF(
        pdf_path="../data/2025-06_S3_Diagnostik-Therapie-Hepatozellulaeres-Karzinom-biliaere-Karzinome.pdf",
        title="S3-Leitlinie Diagnostik und Therapie ddes Hepatozellulären Karzinoms und biliärer Karzinome",
        release_date="Juni 2025",
        roi_pg_number=(507, 27, 66, 43),
        roi_text=(73, 85, 514, 678),
        page_offset=(26, 210)
        )

    pages = list(filter(lambda x: x is not None, [hepatocell_carcinoma_pdf.extract(page) for page in hepatocell_carcinoma_pdf.pages]))

    pages_for_df = [page.__dict__ for page in pages]
    df = pd.DataFrame.from_records(pages_for_df)
    df.to_csv("../data/hepatocell_carcinoma_pdf.csv", index=False)