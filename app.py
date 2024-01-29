import streamlit as st
from PIL import Image
import pytesseract

st.title("Image Text Extractor")



# Image upload
uploaded_file = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image)

    # Specify the position where the relevant text should be placed
    position = (100, 100)  # Replace with your desired position coordinates

    # Create an image with text placed at the specified position
    image_with_text = Image.new('RGB', image.size)
    image_with_text.paste(image, (0, 0))
    st.image(image_with_text)

    # Display the extracted text
    st.subheader("Extracted Text:")
    st.text(text)
