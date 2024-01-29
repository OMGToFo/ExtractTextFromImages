import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd

st.title("Simple Multiple Image Text Extractor")

# Create an empty DataFrame
df = pd.DataFrame(columns=['Time', 'KW', 'KW_num'])

# Upload multiple images through Streamlit
uploaded_files = st.file_uploader("Choose multiple images...", type=["jpg", "png"], accept_multiple_files=True)

if uploaded_files:

    number = st.number_input("Insert a line number", value=10, placeholder="Line nr..")
    
    st.subheader("Uploaded Images:")
    for uploaded_file in uploaded_files:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Uploaded Image - {uploaded_file.name}', use_column_width=True)

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(image)

        # Extract relevant information
        time_info = text[:5]  # Extract the first 5 characters for time
        kw_info = text.splitlines()[number]  # Extract the 9th line for kW

       # Extract the first two numbers from 'KW' and convert to integer
        kw_num = int(''.join(filter(str.isdigit, kw_info[:2])))

        # Add values to the DataFrame using loc
        df.loc[df.shape[0]] = {'Time': time_info, 'KW': kw_info, 'KW_num': kw_num}

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
