import sys
import os
import subprocess
from PIL import Image

# Get the track file path from parameters
thumbnail_file_path = sys.argv[1]
thumbnail_dir_path = os.path.dirname(sys.argv[1])

# Read the track file
print("Reading file: " + thumbnail_file_path)
with open(thumbnail_file_path, 'rb') as thumbnail_file:
    thumbnail_content = thumbnail_file.read()

# Find the start of the image
image_start_bytes = b'\x49\x49\xbc\x01'
image_start_index = thumbnail_content.find(image_start_bytes)

# Given file included a jxr image
if image_start_index >= 0:
    # Get the image data from the thumbnail file
    thumbnail_image_data = thumbnail_content[image_start_index:]

    # Create temporary image file that will be converted from jxr to bmp for PIL
    print("Creating temporary image files")
    thumbnail_temp_jxr_path = os.path.join(thumbnail_dir_path, 'thumbnail.jxr')
    with open(thumbnail_temp_jxr_path, 'wb') as thumbnail_temp_file:
        thumbnail_temp_file.write(thumbnail_image_data)

    # Convert the image file with jxrlib
    print("Converting image")
    thumbnail_temp_bmp_path = os.path.join(thumbnail_dir_path, 'thumbnail.bmp')
    subprocess.call(["JXRDecApp.exe", '-i', thumbnail_temp_jxr_path,
                     '-o', thumbnail_temp_bmp_path])

    # Open the image with PIL
    thumbnail_image = Image.open(thumbnail_temp_bmp_path)
    # Mirror the image horizontally
    mirrored_thumbnail_image = thumbnail_image.transpose(Image.FLIP_TOP_BOTTOM)
    # Save image as jpg
    print("Saving image")
    mirrored_thumbnail_image.save(os.path.join(thumbnail_dir_path, 'thumbnail.jpg'))

    # Delete temp files
    print("Deleting temporary image files")
    os.remove(thumbnail_temp_jxr_path)
    os.remove(thumbnail_temp_bmp_path)

else:
    print("No image found")
