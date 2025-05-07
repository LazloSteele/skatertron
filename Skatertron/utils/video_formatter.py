import os
import tempfile
import subprocess


class VideoFormatter:
    @staticmethod
    def format_video(temp_path: str) -> str:
        """
        Synchronously processes a .mov video file, removes its audio, and remuxes it to .mp4 without re-encoding.

        :param temp_path: Path to the input video file.
        :return: Path to the processed video file (.mp4) or an error message.
        """
        try:
            # Ensure input file exists
            if not os.path.exists(temp_path) or os.stat(temp_path).st_size == 0:
                raise ValueError(f"Input video file is missing or empty: {temp_path}")

            # Create a temporary output file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", dir=r"S:\2025 Omaha Winterfest\tmp") as output_file:
                output_filepath = output_file.name

            # Run FFmpeg synchronously
            result = subprocess.run(
                ["ffmpeg", "-i", temp_path, "-c:v", "copy", "-an", output_filepath],
                text=True, check=True
            )

            # Check if FFmpeg executed successfully
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg failed: {result.stderr}")

            # Check if output file was created successfully
            if not os.path.exists(output_filepath) or os.stat(output_filepath).st_size == 0:
                raise RuntimeError("FFmpeg did not generate a valid output file.")

            return output_filepath

        except Exception as e:
            print(f"Error processing file: {e}")
            return None

        finally:
            # Clean up input file if necessary
            if os.path.exists(temp_path):
                os.remove(temp_path)
