import streamlit as st
import cv2
from PIL import Image
import os


template_path = 'Certificate.png'
font = cv2.FONT_HERSHEY_COMPLEX
font_size = 2
font_color = (0,0,0)


# Coordinates on the certificate where
# will be printing the name (set
# according to your own template)
coordinate_y_adjustment = 25
coordinate_x_adjustment = 5

st.title("Certificate Center")
name = st.text_input('Enter your name')
submit = st.button("Submit")
if submit:
    if name=="":
        st.error("Please enter your Name")
    else:
        certi_name = name
        #certi_name = input("Enter your name:")

        # read the certificate template
        img = cv2.imread(template_path)
                                            

        # get the size of the name to be printed
        text_size = cv2.getTextSize(certi_name, font, font_size, 5)[0]     

        # get the (x,y) coordinates where the
        # name is to written on the template
        # The function cv.putText accepts only
        # integer arguments so convert it into 'int'.
        text_x = (img.shape[1] - text_size[0]) / 2 + coordinate_x_adjustment 
        text_y = (img.shape[0] + text_size[1]) / 2 - coordinate_y_adjustment
        text_x = int(text_x)
        text_y = int(text_y)
        cv2.putText(img, certi_name,
                (text_x ,text_y ), 
                font,
                font_size,
                font_color, 5)

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

