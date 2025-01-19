import subprocess
import json


async def get_video_metadata(file_path):
    # Run ffprobe command to extract metadata
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )

    metadata = json.loads(result.stdout)

    return metadata


if __name__ == "__main__":
    print(json.dumps(get_video_metadata(r"C:\Users\Laurie Steele\Downloads\2023 Aspen-031 Basic 4 Program-Mary Grace Crump.MP4"),indent=2))
