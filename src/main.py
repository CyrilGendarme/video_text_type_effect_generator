"""
Main module for text animation video generation
"""
from .text_animator import TextAnimator, TextStyle, AnimationMode
from .video_processor import VideoProcessor
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextVideoGenerator:
    """High-level interface for generating videos with animated text overlays"""

    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        """
        Initialize the generator.

        Args:
            ffmpeg_path: Path to FFmpeg executable
        """
        self.animator = TextAnimator()
        self.processor = VideoProcessor(ffmpeg_path)

    def add_typewriter_text(
        self,
        text: str,
        start_time: float,
        typing_speed: float = 80,
        style: TextStyle = None,
        position=(0, 0),
    ) -> float:
        """Add typewriter effect text and return end time"""
        if style is None:
            style = TextStyle()
        return self.animator.add_typewriter_text(
            text, start_time, typing_speed, style=style, position=position
        )

    def add_reveal_text(
        self,
        text: str,
        start_time: float,
        style: TextStyle = None,
        position=(0, 0),
    ) -> float:
        """Add reveal effect text and return end time"""
        if style is None:
            style = TextStyle()
        return self.animator.add_reveal_text(text, start_time, style=style, position=position)

    def add_fade_in_text(
        self,
        text: str,
        start_time: float,
        duration: float = 1.0,
        style: TextStyle = None,
        position=(0, 0),
    ) -> float:
        """Add fade-in effect text and return end time"""
        if style is None:
            style = TextStyle()
        return self.animator.add_fade_in_text(
            text, start_time, duration, style=style, position=position
        )

    def generate_video(
        self,
        input_video: str,
        output_video: str,
        ass_file: str = None,
        font_dir: str = None,
        preset: str = "medium",
    ) -> bool:
        """
        Generate video with animated text overlay.

        Args:
            input_video: Path to input video
            output_video: Path to output video
            ass_file: Path to save ASS file (if None, uses temporary file)
            font_dir: Directory containing fonts
            preset: FFmpeg encoding preset

        Returns:
            True if successful, False otherwise
        """
        if ass_file is None:
            ass_file = "generated_animation.ass"

        # Save ASS file
        self.animator.save_ass_file(ass_file)
        logger.info(f"Saved ASS file: {ass_file}")

        # Process video
        success = self.processor.overlay_subtitle(
            input_video,
            ass_file,
            output_video,
            font_dir=font_dir,
            preset=preset,
        )

        return success

    def generate_video_fast(
        self,
        input_video: str,
        output_video: str,
        ass_file: str = None,
        font_dir: str = None,
    ) -> bool:
        """Generate video with fast processing (copy codec)"""
        if ass_file is None:
            ass_file = "generated_animation.ass"

        self.animator.save_ass_file(ass_file)
        logger.info(f"Saved ASS file: {ass_file}")

        success = self.processor.overlay_subtitle_fast(
            input_video,
            ass_file,
            output_video,
            font_dir=font_dir,
        )

        return success

    def generate_video_hq(
        self,
        input_video: str,
        output_video: str,
        ass_file: str = None,
        font_dir: str = None,
    ) -> bool:
        """Generate video with high quality settings"""
        if ass_file is None:
            ass_file = "generated_animation.ass"

        self.animator.save_ass_file(ass_file)
        logger.info(f"Saved ASS file: {ass_file}")

        success = self.processor.overlay_subtitle_hq(
            input_video,
            ass_file,
            output_video,
            font_dir=font_dir,
        )

        return success


def create_example_animation(output_ass: str = "example.ass", output_video: str = "example_output.mp4"):
    """Create an example animation with typewriter, reveal, and fade-in effects"""
    logger.info("Creating example animation...")

    # Create animator
    animator = TextAnimator()

    # Define custom style
    title_style = TextStyle(
        font_name="Arial",
        font_size=72,
        bold=True,
        color="&H00FFFFFF",  # White
        outline_width=3,
        shadow_depth=2,
    )

    subtitle_style = TextStyle(
        font_name="Arial",
        font_size=36,
        color="&H0000FFFF",  # Yellow
        outline_width=2,
    )

    # Timeline
    current_time = 0.5

    # Add title with typewriter effect
    current_time = animator.add_typewriter_text(
        "AMAZING TITLE",
        current_time,
        typing_speed=100,
        style=title_style,
        position=(960, 300),
    )

    # Add pause
    current_time += 1.0

    # Add subtitle with reveal effect
    current_time = animator.add_reveal_text(
        "WITH REVEAL EFFECT",
        current_time,
        style=subtitle_style,
        position=(960, 400),
    )

    # Add pause
    current_time += 0.5

    # Add fade-in text
    current_time = animator.add_fade_in_text(
        "And this fades in smoothly",
        current_time,
        duration=2.0,
        style=TextStyle(font_size=24),
        position=(960, 500),
    )

    # Save ASS file
    animator.save_ass_file(output_ass)
    logger.info(f"Example ASS file saved to: {output_ass}")

    return animator


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        input_video = sys.argv[1]
        output_video = sys.argv[2] if len(sys.argv) > 2 else "output.mp4"

        generator = TextVideoGenerator()

        # Add some example text
        generator.add_typewriter_text("HELLO WORLD", 0.5, typing_speed=80)
        generator.add_typewriter_text("This is a test", 5.0, typing_speed=60)

        # Generate video
        success = generator.generate_video(input_video, output_video)
        if success:
            logger.info(f"Video generated successfully: {output_video}")
        else:
            logger.error("Failed to generate video")
            sys.exit(1)
    else:
        # Create example
        logger.info("No input video provided. Creating example ASS file...")
        create_example_animation()
