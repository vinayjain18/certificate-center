import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os
import uuid
import re
import tempfile

# Constants
FONT_COLOR = (0, 0, 0)
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
MAX_NAME_LENGTH = 100
MAX_COORDINATE_VALUE = 5000
MIN_COORDINATE_VALUE = -5000

# Font mapping dictionary
FONT_MAP = {
    "Normal size sans-serif font": cv2.FONT_HERSHEY_SIMPLEX,
    "Small size sans-serif font": cv2.FONT_HERSHEY_PLAIN,
    "Complex size sans-serif font": cv2.FONT_HERSHEY_DUPLEX,
    "Normal size serif font": cv2.FONT_HERSHEY_COMPLEX,
    "Complex size serif font": cv2.FONT_HERSHEY_TRIPLEX,
    "Small size serif font": cv2.FONT_HERSHEY_COMPLEX_SMALL,
    "Hand-writing style font": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    "Complex Hand-writing style font": cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
}


def load_logo():
    """Load the application logo safely."""
    logo_path = os.path.join(os.path.dirname(__file__), 'certification.png')
    if os.path.exists(logo_path):
        return Image.open(logo_path)
    return None


def sanitize_filename(name):
    """Remove special characters from filename to prevent path traversal."""
    # Remove any path separators and special characters
    sanitized = re.sub(r'[^\w\s-]', '', name)
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    return sanitized.strip('_')[:50]  # Limit length


def validate_name(name):
    """Validate the name input."""
    if not name or name.strip() == "":
        return False, "Please enter your name."
    if len(name) > MAX_NAME_LENGTH:
        return False, f"Name is too long. Maximum {MAX_NAME_LENGTH} characters allowed."
    return True, ""


def validate_coordinates(x_coord, y_coord):
    """Validate coordinate inputs are within bounds."""
    if x_coord < MIN_COORDINATE_VALUE or x_coord > MAX_COORDINATE_VALUE:
        return False, f"X-coordinate must be between {MIN_COORDINATE_VALUE} and {MAX_COORDINATE_VALUE}."
    if y_coord < MIN_COORDINATE_VALUE or y_coord > MAX_COORDINATE_VALUE:
        return False, f"Y-coordinate must be between {MIN_COORDINATE_VALUE} and {MAX_COORDINATE_VALUE}."
    return True, ""


def validate_file(uploaded_file):
    """Validate the uploaded file."""
    if uploaded_file is None:
        return False, "Please upload a certificate template.", None

    bytes_value = uploaded_file.read()

    # Check file size
    if len(bytes_value) > MAX_FILE_SIZE_BYTES:
        return False, f"File is too large. Maximum size is {MAX_FILE_SIZE_MB}MB.", None

    if len(bytes_value) == 0:
        return False, "The uploaded file is empty.", None

    return True, "", bytes_value


def decode_image(bytes_value):
    """Decode image bytes and validate the result."""
    try:
        img_array = np.array(bytearray(bytes_value), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)

        if img is None:
            return None, "Failed to decode image. Please upload a valid PNG or JPG file."

        # Check if image has valid dimensions
        if img.shape[0] == 0 or img.shape[1] == 0:
            return None, "Invalid image dimensions."

        return img, ""
    except Exception as e:
        return None, f"Error processing image: {str(e)}"


def generate_certificate(img, name, font, font_size, font_multiplier, x_adjustment, y_adjustment):
    """Generate certificate with the name overlay."""
    try:
        # Get the size of the name to be printed
        text_size = cv2.getTextSize(name, font, font_size, font_multiplier)[0]

        # Get the (x,y) coordinates where the name is to written on the template
        text_x = int((img.shape[1] - text_size[0]) / 2 + x_adjustment)
        text_y = int((img.shape[0] + text_size[1]) / 2 - y_adjustment)

        # Create a copy to avoid modifying original
        img_copy = img.copy()

        cv2.putText(
            img_copy,
            name,
            (text_x, text_y),
            font,
            font_size,
            FONT_COLOR,
            font_multiplier
        )

        return img_copy, ""
    except Exception as e:
        return None, f"Error generating certificate: {str(e)}"


def save_certificate(img, temp_path):
    """Save certificate to a temporary file."""
    try:
        success = cv2.imwrite(temp_path, img)
        if not success:
            return False, "Failed to save certificate image."
        return True, ""
    except Exception as e:
        return False, f"Error saving certificate: {str(e)}"


def cleanup_temp_file(file_path):
    """Safely remove temporary file."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass  # Ignore cleanup errors


# Main Application
logo = load_logo()
st.set_page_config("Certificate Center", logo)

st.title("Certificate Center")

name = st.text_input('Enter your name', max_chars=MAX_NAME_LENGTH)

font_f = st.selectbox(
    "Select Font:",
    tuple(FONT_MAP.keys())
)

font_size = st.selectbox(
    "Select Font size:",
    (0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7)
)

font_multiplier = st.select_slider(
    "Select the intensity/thickness:",
    options=[1, 2, 3, 4, 5]
)

# Coordinates on the certificate where will be printing the name
# (set according to your own template)
coordinate_x_adjustment = st.number_input(
    "Enter X-coordinate position of your text",
    min_value=float(MIN_COORDINATE_VALUE),
    max_value=float(MAX_COORDINATE_VALUE),
    value=0.0
)
coordinate_y_adjustment = st.number_input(
    "Enter Y-coordinate position of your text",
    min_value=float(MIN_COORDINATE_VALUE),
    max_value=float(MAX_COORDINATE_VALUE),
    value=0.0
)

# Upload file here
uploaded_file = st.file_uploader("Upload file:", ['png', 'jpg'])

submit = st.button("Submit")

if submit:
    temp_path = None

    try:
        # Validate name
        is_valid, error_msg = validate_name(name)
        if not is_valid:
            st.error(error_msg)
            st.stop()

        # Validate coordinates
        is_valid, error_msg = validate_coordinates(coordinate_x_adjustment, coordinate_y_adjustment)
        if not is_valid:
            st.error(error_msg)
            st.stop()

        # Validate and read file
        is_valid, error_msg, bytes_value = validate_file(uploaded_file)
        if not is_valid:
            st.error(error_msg)
            st.stop()

        # Decode image
        img, error_msg = decode_image(bytes_value)
        if img is None:
            st.error(error_msg)
            st.stop()

        # Get font from mapping
        font = FONT_MAP[font_f]

        # Generate certificate
        result_img, error_msg = generate_certificate(
            img, name, font, font_size, font_multiplier,
            coordinate_x_adjustment, coordinate_y_adjustment
        )
        if result_img is None:
            st.error(error_msg)
            st.stop()

        # Generate unique temporary file path to prevent race conditions
        unique_id = uuid.uuid4().hex
        temp_path = os.path.join(tempfile.gettempdir(), f"certificate_{unique_id}.png")

        # Save the certificate
        success, error_msg = save_certificate(result_img, temp_path)
        if not success:
            st.error(error_msg)
            st.stop()

        # Display the certificate
        image = Image.open(temp_path)
        st.image(image)

        # Prepare download with sanitized filename
        safe_name = sanitize_filename(name)
        download_filename = f"{safe_name}_certificate.png" if safe_name else "certificate.png"

        with open(temp_path, "rb") as file:
            st.download_button(
                label="Download Certificate",
                data=file,
                file_name=download_filename,
                mime="image/png"
            )

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

    finally:
        # Always cleanup temporary file
        cleanup_temp_file(temp_path)
