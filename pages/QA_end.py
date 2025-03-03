import streamlit as st
from fpdf import FPDF

st.title("Your answer are saved")
st.subheader("Our team will contact you shortly")
st.subheader("Have a nice day!")


def txt_to_pdf(txt_file, pdf_file):
    # Create instance of FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Read text file
    with open(txt_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Add text to the PDF, specifying the encoding
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text.encode("latin-1", "replace").decode("latin-1"))

    # Save the PDF
    pdf.output(pdf_file)


# Define path of the files
txt_file = 'report.txt'
pdf_file = 'report.pdf'

# Exit button
if st.button("Exit"):
    txt_to_pdf(txt_file, pdf_file)
    st.stop()