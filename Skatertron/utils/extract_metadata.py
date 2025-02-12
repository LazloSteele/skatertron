import os
import subprocess
import json
import tempfile


import subprocess
import tempfile
import json
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os

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
            creation_time = metadata["format"]["tags"].get("creation_time")

        return {"creation_time": creation_time}

    except Exception as e:
        print(f"Error processing file slice: {e}")
        return {"error": str(e)}



if __name__ == "__main__":
    print(json.dumps(get_video_metadata(r"C:\Users\Laurie Steele\Downloads\2023 Aspen-031 Basic 4 Program-Mary Grace Crump.MP4"),indent=2))
