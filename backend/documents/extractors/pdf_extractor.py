import pdfplumber
import pandas as pd


def extract_pdf_to_dataframe(uploaded_file):
    """
    Extract tables from PDF and return a pandas DataFrame.
    Raises ValueError if no usable table is found.
    """
    tables = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables:
                if table and len(table) > 1:
                    tables.append(table)

    if not tables:
        raise ValueError(
            "No structured tables found in PDF. "
            "Unable to compute values from this document."
        )

    # Take the largest table (most columns)
    main_table = max(tables, key=lambda t: len(t[0]))

    headers = main_table[0]
    rows = main_table[1:]

    df = pd.DataFrame(rows, columns=headers)

    # Clean column names
    df.columns = [str(c).strip().lower() for c in df.columns]

    return df
