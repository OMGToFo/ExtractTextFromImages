import streamlit as st
from PIL import Image
import pytesseract

st.title("Multiple Image Text Extractor")

# Upload multiple images through Streamlit
uploaded_files = st.file_uploader("Choose multiple images...", type=["jpg", "png"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("Uploaded Images:")
    for uploaded_file in uploaded_files:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Uploaded Image - {uploaded_file.name}', use_column_width=True)

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(image)

        # Specify the position where the relevant text should be placed
        position = (100, 100)  # Replace with your desired position coordinates

        # Create an image with text placed at the specified position
        image_with_text = Image.new('RGB', image.size)
        image_with_text.paste(image, (0, 0))
        st.image(image_with_text, caption=f'Image with Extracted Text - {uploaded_file.name}', use_column_width=True)

        # Display the extracted text
        st.subheader(f"Extracted Text from {uploaded_file.name}:")
        st.text(text)
