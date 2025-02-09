import os
import zipfile
import tempfile
import streamlit as st
from io import BytesIO
import shutil


# Temporary directory for uploaded files
temp_dir = tempfile.mkdtemp()

def zip_files(file_paths, zip_name="files.zip"):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_paths:
            zipf.write(file, os.path.basename(file))
    return zip_name

# Streamlit UI
st.title("PNG File Upload and Zip Generator")

# Upload PNG files
uploaded_files = st.file_uploader("Upload PNG files", type=["png"], accept_multiple_files=True)

# Save uploaded files to temporary directory
if uploaded_files:
    for uploaded_file in uploaded_files:
        with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

    st.success("Files uploaded successfully!")

# Allow user to download all uploaded PNGs as a ZIP file
if st.button("Download ZIP of Uploaded Files"):
    # Collect paths of all uploaded files
    file_paths = [os.path.join(temp_dir, file.name) for file in uploaded_files]
    
    # Create a zip file
    zip_file_name = "uploaded_files.zip"
    zip_file = zip_files(file_paths, zip_file_name)

    # Provide the zip file for download
    with open(zip_file, "rb") as f:
        st.download_button(
            label="Download ZIP",
            data=f,
            file_name=zip_file_name,
            mime="application/zip"
        )

    # Optionally clean up the temporary files
    shutil.rmtree(temp_dir)
