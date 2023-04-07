import streamlit as st
import pandas as pd
import tabula
import io
import numpy as np
import subprocess

st.set_page_config(layout="centered",
                   page_title="RCV PDF Demo", page_icon="📄")


@st.cache_resource
def download_en_core_web_sm():
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])


download_en_core_web_sm()
nlp = spacy.load("en_core_web_sm")


def pdf(file):
    import os
    from serpapi import GoogleSearch
    import pandas as pd
    import spacy
    import pdfx

    word_list = ["led", "wall", "floor",
                 "sign", "pendant", "light", "steplight"]
    ADP_list = ["in", "on", "at"]

    pdf = pdfx.PDFx(os.path.join(os.getcwd(), 'test.pdf'))
    text = pdf.get_text()

    text_block = text.split("\n\n")
    block_list = []
    for textblock in text_block:
        doc = nlp(textblock)
        cols = ("text", "lemma", "POS", "explain", "stopword")
        rows = []
        keep = False
        legit = False
        for t in doc:
            if t.text.lower() in word_list:
                keep = True
            if t.text.lower() in ADP_list:
                legit = True
        if keep and legit:
            block_list.append(doc.text)

    search_list = []
    for i in block_list:
        wordlist = i.split("\n")
        to_search = ""
        for j in wordlist:
            to_search = to_search + j + " "
        search_list.append(to_search.strip())

    price_list = []
    price_holder = 0
    for i in search_list:
        price_list.append(price_holder)
        price_holder += 1

    return_dict = {}
    for i in range(len(search_list)):
        return_dict[search_list[i]] = price_list[i]

    return return_dict


st.title("RCV PDF Demo")

uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])

if uploaded_file is not None:
    data = pdf(uploaded_file)
    df = pd.DataFrame(list(data.items()), columns=['Product', 'Price'])

    if data is not None:
        st.subheader("Extracted Data:")
        st.table(df)

        # Display the download button
        csv_file = df.to_csv(sep=",", index=False,
                             line_terminator='\n', encoding='utf-8')
        st.download_button("Download as CSV", csv_file,
                           file_name="ProductPriceList.csv", mime="text/csv")
    else:
        st.error(
            "Could not extract PRODUCT DESCRIPTION and BASIS OF DESIGN MANUFACTURER from the PDF.")
else:
    st.info("Please upload a PDF file.")
