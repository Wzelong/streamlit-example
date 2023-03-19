import streamlit as st
import pandas as pd
import tabula
import io
import numpy as np

st.set_page_config(layout="centered",
                   page_title="RCV PDF Extractor", page_icon="📄")


def extract_data_from_pdf(file):
    tables = tabula.read_pdf(file, pages="all")
    tables[0].columns = tables[0].iloc[1]
    tables[0] = tables[0][2:]
    return tables


def extract_product_description_and_basis_of_design_manufacturer(tables):
    for table in tables:
        if "PRODUCT DESCRIPTION" in table.columns and "BASIS OF DESIGN MANUFACTURER" in table.columns:
            product_description = table["PRODUCT DESCRIPTION"].fillna(
                "N/A").tolist()
            basis_of_design_manufacturer = table["BASIS OF DESIGN MANUFACTURER"].fillna(
                "N/A").tolist()

            # Create a DataFrame with the extracted columns
            data = pd.DataFrame({"PRODUCT DESCRIPTION": product_description,
                                "BASIS OF DESIGN MANUFACTURER": basis_of_design_manufacturer})
            return data

    return None


st.title("RCV PDF Extractor")

uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

if uploaded_file is not None:
    with st.spinner("Extracting data from the PDF..."):
        pdf_data = io.BytesIO(uploaded_file.read())
        tables = extract_data_from_pdf(pdf_data)
        data = extract_product_description_and_basis_of_design_manufacturer(
            tables)

    if data is not None:
        # Generate random prices ranging from 20 to 200, with the same length as the extracted data
        random_prices = np.random.randint(20, 201, len(data))

        # Add the generated prices as the third column
        data["Price(US Dollar)"] = random_prices

        st.subheader("Extracted Data:")
        st.write(data)

        # Display the download button
        data = data.replace({r'\n': ' '}, regex=True)
        csv_file = data.to_csv(sep=",", index=False,
                               line_terminator='\n', encoding='utf-8')
        st.download_button("Download as CSV", csv_file,
                           file_name="data.csv", mime="text/csv")
    else:
        st.error(
            "Could not extract PRODUCT DESCRIPTION and BASIS OF DESIGN MANUFACTURER from the PDF.")
else:
    st.info("Please upload a PDF file.")
