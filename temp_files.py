import os
import zipfile
import tempfile
import streamlit as st
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Create a temporary directory to store files
temp_dir = tempfile.TemporaryDirectory()

def createqr(data):
    new_data = data
    #new_data = data.replace(rmdata, '') 
    # Create a QR code object with a larger size and higher error correction
    qr = qrcode.QRCode(version=3, box_size=20, border=4, error_correction=qrcode.constants.ERROR_CORRECT_H)

    # Define the data to be encoded in the QR code


    # Add the data to the QR code object
    qr.add_data(data)

    # Make the QR code
    qr.make(fit=True)

    # Create an image from the QR code with a black fill color and white background
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to a format Pillow can work with (RGBA)
    qr_img = qr_img.convert("RGBA")

    # Define the font and size for the text overlay
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # You can adjust the font and size as needed
    except IOError:
        # Fallback in case the font is not available
        font = ImageFont.load_default()

    # Get the dimensions of the QR code image
    qr_width, qr_height = qr_img.size

    # Create a new image with extra space for the text
    final_img_height = qr_height + 100  # Add space for text (100px)
    final_img = Image.new('RGB', (qr_width, final_img_height), color="white")

    # Paste the QR code onto the new image
    final_img.paste(qr_img, (0, 0))

    # Prepare the text to be drawn under the QR code
    draw = ImageDraw.Draw(final_img)

    # Get the bounding box of the text
    bbox = draw.textbbox((0, 0), new_data, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate the position to center the text
    text_position = ((qr_width - text_width) // 2, qr_height + 10)

    # Draw the text onto the final image
    draw.text(text_position, new_data, font=font, fill="black")

    #renamed path folder to 2
    path_folder = temp_dir.name
    name_image = os.path.join(path_folder, new_data + ".png")
    with open(name_image, "wb") as f:
        final_img.save(name_image)
        f.write(name_image.read())

    # Save the final image

    print(name_image)
    # Optionally display the final image
    #final_img.show()







# File upload section
# st.header("Upload PNG Files")
# uploaded_files = st.file_uploader("Upload PNG files", type=["png"], accept_multiple_files=True)

# # Save uploaded files to the temporary folder
# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         file_path = os.path.join(temp_dir.name, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.read())
#     st.success(f"Uploaded {len(uploaded_files)} file(s) successfully!")

# Show the list of files
files_in_temp = os.listdir(temp_dir.name)
if files_in_temp:
    st.write("Files in temporary folder:")
    for file in files_in_temp:
        st.write(f"- {file}")

# Download the folder as a ZIP
if st.button("Download Folder as ZIP"):
    # Create a ZIP file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_name in files_in_temp:
            file_path = os.path.join(temp_dir.name, file_name)
            zipf.write(file_path, arcname=file_name)
    zip_buffer.seek(0)

    # Provide download link for the ZIP file
    st.download_button(
        label="Download ZIP",
        data=zip_buffer,
        file_name="images.zip",
        mime="application/zip",
    )

# Cleanup the temporary folder on app exit
st.sidebar.write("Temporary files will be deleted automatically when the app closes.")






url = "https://docs.google.com/spreadsheets/d/1qZJXuGy6IRGw2WZuW2mtC1tiDJba6mQyEDuLQgsCrPY/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, usecols=[0])
st.dataframe(data)

column_1 = data.iloc[:, 0] 
names_list = data["Name"].tolist()
with pd.option_context('display.max_rows', None):
    # new_data = str(data)
    # print(new_data)
    for name in names_list:
        createqr(name)

