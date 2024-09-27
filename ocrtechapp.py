import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Set the path for Tesseract executable if needed
# Uncomment the line below if you have a custom installation of Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust if necessary

def extract_images_and_ocr(pdf_file):
    """
    Extract images from a PDF and apply OCR to detect text.
    
    :param pdf_file: The uploaded PDF file.
    :return: A dictionary with page numbers and extracted text.
    """
    pdf_document = fitz.open(pdf_file)
    page_ocr_data = {}

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        # Extract images on the page
        images = page.get_images(full=True)

        # Initialize list to store OCR results
        extracted_texts = []

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # Convert the image bytes to a PIL image for OCR
            image = Image.open(io.BytesIO(image_bytes))

            # Use OCR to extract text from the image
            ocr_result = pytesseract.image_to_string(image)
            extracted_texts.append(ocr_result.strip())

        # Store results if there are images
        if images:
            page_ocr_data[page_number + 1] = extracted_texts

    pdf_document.close()
    return page_ocr_data

# Streamlit app
st.title("OCR Image Detector in PDF")
st.write("Upload a PDF file to detect images and extract text using OCR.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Show a spinner while processing
    with st.spinner("Extracting images and applying OCR..."):
        ocr_results = extract_images_and_ocr(uploaded_file)

    # Output the result
    if ocr_results:
        st.success("OCR results extracted from images:")
        for page_number, texts in ocr_results.items():
            st.subheader(f"Page {page_number}")
            for text in texts:
                st.write(text or "No text detected")
    else:
        st.warning("No images found in the PDF or no text detected.")
