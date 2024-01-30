import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import plotly.express as px
import cv2
import numpy as np

#import helpers.opencv as opencv

st.title("Simple Image Text Extractor")

# Create an empty DataFrame
df = pd.DataFrame(columns=['Time', 'KW', 'KW_num'])

# Upload multiple images through Streamlit
uploaded_files = st.file_uploader("Choose multiple images...", type=["jpg", "png"], accept_multiple_files=False)

if uploaded_files:

    st.warning("Not activated yet - Check the boxes below to apply preprocessing to the image.")
    cGrayscale = st.checkbox(label="Grayscale", value=True)
    cDenoising = st.checkbox(label="Denoising", value=False)
    cDenoisingStrength = st.slider(label="Denoising Strength", min_value=1, max_value=40, value=10, step=1)
    cThresholding = st.checkbox(label="Thresholding", value=False)
    cThresholdLevel = st.slider(label="Threshold Level", min_value=0, max_value=255, value=128, step=1)
    cRotate90 = st.checkbox(label="Rotate in 90° steps", value=False)
    angle90 = st.slider("Rotate rectangular [Degree]", min_value=0, max_value=270, value=0, step=90)
    cRotateFree = st.checkbox(label="Rotate in free degrees", value=False)
    angle = st.slider("Rotate freely [Degree]", min_value=-180, max_value=180, value=0, step=1)

    _="""  
    try:
        # convert uploaded file to numpy array
         image = opencv.load_image(uploaded_files)
    except Exception as e:
        st.error("Exception during Image Conversion")
        st.error(f"Error Message: {e}")
        st.stop()


        try:
            if cGrayscale:
                image = opencv.grayscale(image)
            if cDenoising:
                image = opencv.denoising(image, strength=cDenoisingStrength)
            if cThresholding:
                image = opencv.thresholding(image, threshold=cThresholdLevel)
            if cRotate90:
                # convert angle to opencv2 enum
                angle90 = constants.angles.get(angle90, None)
                image = opencv.rotate90(image, rotate=angle90)
            if cRotateFree:
                image = opencv.rotate_scipy(image, angle=angle, reshape=True)
            # TODO: add crop functions here
            # if cCrop:
            #     pass
            image = opencv.convert_to_rgb(image)
        except Exception as e:
            st.error(f"Exception during Image Preprocessing (Probably you selected Threshold on a color image?): {e}")
            st.stop()
        """
  


    

    
    textselection = st.toggle("Extract certain text and make a table bitte")
    if textselection:
        number = st.number_input("Insert a line number", value=10, placeholder="Line nr..")
    
    st.subheader("Uploaded Images:")
    for uploaded_file in uploaded_files:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption=f'Uploaded Image - {uploaded_file.name}', use_column_width=True)

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(image)

        if textselection:
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

        if textselection:
            # Display the DataFrame
            st.subheader("DataFrame:")
            st.dataframe(df)
            
            chartCreate = st.checkbox("Draw line chart")
            if chartCreate:
                # Line chart with time on the x-axis and KW_num on the y-axis
                fig = px.line(df, x='Time', y='KW_num', title='KW_num Over Time', labels={'KW_num': 'KW'})
                st.plotly_chart(fig)
