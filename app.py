import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd

st.title("Multiple Image Text Extractor and DataFrame")

# Create an empty DataFrame
df = pd.DataFrame(columns=['Time', 'KW'])

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

        # Extract relevant information
        time_info = text[:5]  # Extract the first 5 characters for time
        kw_info = text.splitlines()[8]  # Extract the 9th line for kW

        # Add values to the DataFrame using loc
        df.loc[df.shape[0]] = {'Time': time_info, 'KW': kw_info}

        # Specify the position where the relevant text should be placed
        #position = (100, 100)  # Replace with your desired position coordinates

        # Create an image with text placed at the specified position
        #image_with_text = Image.new('RGB', image.size)
        #image_with_text.paste(image, (0, 0))
        #st.image(image_with_text, caption=f'Image with Extracted Text - {uploaded_file.name}', use_column_width=True)

        # Display the extracted text
        st.subheader(f"Extracted Text from {uploaded_file.name}:")
        st.text(text)

# Display the DataFrame
st.subheader("DataFrame:")
st.dataframe(df)
