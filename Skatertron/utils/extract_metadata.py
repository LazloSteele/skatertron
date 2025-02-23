import subprocess
import tempfile
import json
from fastapi import APIRouter, UploadFile, File
import os

from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta, timezone

router = APIRouter()


# Function to extract video metadata from the file contents (file slice)
async def get_video_metadata(file_contents):
    try:
        # Create a temporary file to save the file contents
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_contents)  # Write the file slice to the temporary file
            temp_file.flush()  # Ensure content is fully written
            temp_file_path = temp_file.name

        # Use ffprobe to extract metadata from the temporary file
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", temp_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        # Check for errors in ffprobe's stderr output
        if result.stderr:
            error_message = result.stderr.decode('utf-8', errors='ignore')
            print(f"ffprobe error: {error_message}")
            os.remove(temp_file_path)  # Clean up the temporary file
            return {"error": "Failed to extract metadata"}

        # Decode ffprobe's stdout (metadata) from bytes to a string
        metadata = result.stdout.decode('utf-8', errors='ignore')

        # Parse the metadata into a JSON object
        try:
            metadata = json.loads(metadata)
        except json.JSONDecodeError:
            print("Error decoding ffprobe metadata")
            metadata = {}

        # Clean up the temporary file
        os.remove(temp_file_path)

        # Check for creation time in the metadata and return it
        creation_time = None
        if "format" in metadata and "tags" in metadata["format"]:
            creation_time = (datetime.fromisoformat(metadata["format"]["tags"].get("creation_time")
                                                    .replace("Z", "+00:00")).strftime('%Y-%m-%d %H:%M:%S UTC'))

        return {"creation_time": creation_time}

    except Exception as e:
        print(f"Error processing file slice: {e}")
        return {"error": str(e)}


async def get_image_metadata(file_contents):
    print("YES MARKED AS IMAGE!")
    try:
        # Use PIL (Pillow) to extract EXIF metadata from image files
        image = Image.open(BytesIO(file_contents))
        creation_time = None

        if image.format in ["JPEG", "MPO"]:
            # Extract EXIF data
            exif_data = image._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    # Look for DateTimeOriginal in EXIF data
                    if tag == 36867:  # DateTimeOriginal tag
                        print("YES FOUND EXIF")
                        creation_time = datetime.strptime(value, "%Y:%m:%d %H:%M:%S") - timedelta(hours = 6, minutes=11)
                        creation_time = creation_time.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
                        break

        if not creation_time:
            # If no EXIF data, return the file's last-modified time or current time
            creation_time = datetime.utcnow().isoformat()

        return {"creation_time": creation_time}

    except Exception as e:
        print(f"Error extracting image metadata: {e}")
        return {"error": str(e)}
