from moviepy import VideoFileClip, vfx
import tempfile


class VideoFormatter(object):
    @staticmethod
    def format_video(temp_path):
        try:
            clip = VideoFileClip(temp_path)

            if not clip:
                raise ValueError("Failed to load video. The video clip is None.")

            print(f'\n\n\n{type(clip)}\n\n\n')

            processed_clip = clip.with_effects(
                [
                    vfx.FadeIn(1.5),
                    vfx.FadeOut(1.5),
                ]
            ).without_audio()

            output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            output_filepath = output_file.name

            print(f"\n\n\nProcessed video will be saved to: {output_filepath}\n\n\n")

            processed_clip.write_videofile(output_filepath)

            clip.close()

            # Return the processed video filepath as a response
            return output_filepath

        except Exception as e:
            print(f"Error processing file: {e}")
            return {"error": str(e)}
