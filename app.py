import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os


logo = Image.open('certification.png')
font_color = (0,0,0)


st.set_page_config("Certificate Center", logo)

st.title("Certificate Center")

name = st.text_input('Enter your name')

font_f = st.selectbox(
    "Select Font:",
    ("Normal size sans-serif font", 
    "Small size sans-serif font", 
    "Complex size sans-serif font",
    "Normal size serif font",
    "Complex size serif font",
    "Small size serif font",
    "Hand-writing style font",
    "Complex Hand-writing style font",
    )
)

font_size = st.selectbox(
    "Select Font size:",
    (0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7)
)

font_multiplier = st.select_slider(
    "Select the number:",
    options=[1, 2, 3, 4, 5]
)

# Coordinates on the certificate where will be printing the name 
# (set according to your own template)
coordinate_x_adjustment = st.number_input("Enter X-coordinate position of your text")
coordinate_y_adjustment = st.number_input("Enter Y-coordinate position of your text")

#upload file here
uploaded_file = st.file_uploader("Upload file:", ['png', 'jpg'])



submit = st.button("Submit")
if submit:
    if name=="" or uploaded_file is None:
        st.error("Please enter your Name/ Upload Sample certificate")
    else:
        if font_f == "Normal size sans-serif font":
            font = cv2.FONT_HERSHEY_SIMPLEX
        elif font_f == "Small size sans-serif font":
            font = cv2.FONT_HERSHEY_PLAIN
        elif font_f == "Complex size sans-serif font":
            font = cv2.FONT_HERSHEY_DUPLEX
        elif font_f == "Normal size serif font":
            font = cv2.FONT_HERSHEY_COMPLEX
        elif font_f == "Complex size serif font":
            font = cv2.FONT_HERSHEY_TRIPLEX
        elif font_f == "Small size serif font":
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        elif font_f == "Hand-writing style font":
            font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        elif font_f == "Complex Hand-writing style font":
            font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        else:
            st.write("Invalid input. Try again")
        

        certi_name = name

        #read the data from the file uploaded and convert it into array using numpy
        bytes_value = uploaded_file.read()
        img_array = np.array(bytearray(bytes_value), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
                                            

        # get the size of the name to be printed
        text_size = cv2.getTextSize(certi_name, font, font_size, font_multiplier)[0]     

        # get the (x,y) coordinates where the name is to written on the template
        # The function cv.putText accepts only integer arguments so convert it into 'int'.
        text_x = (img.shape[1] - text_size[0]) / 2 + coordinate_x_adjustment 
        text_y = (img.shape[0] + text_size[1]) / 2 - coordinate_y_adjustment
        text_x = int(text_x)
        text_y = int(text_y)
        cv2.putText(img, certi_name,
                (text_x ,text_y ), 
                font,
                font_size,
                font_color, font_multiplier)

        # Output path along with the name of the
        # certificate generated
        certi_path ='certi' + '.png'
        
        # Save the certificate                      
        cv2.imwrite(certi_path, img)

        st.write("")
        image = Image.open('certi.png')
        st.image(image)

        with open("certi.png", "rb") as file:
            btn = st.download_button(
                    label="Download Certificate",
                    data=file,
                    file_name = name+"_certificate.png",
                    mime="image/png"
                )

        os.remove("certi.png")
