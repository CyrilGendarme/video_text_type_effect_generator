"""
FFmpeg video processor for overlaying animated text on videos
"""
import subprocess
import os
from pathlib import Path
from typing import Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoProcessor:
    """Handles video processing with FFmpeg"""

    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        """
        Initialize video processor.

        Args:
            ffmpeg_path: Path to FFmpeg executable
        """
        self.ffmpeg_path = ffmpeg_path
        self._check_ffmpeg()

    def _check_ffmpeg(self):
        """Verify FFmpeg is available"""
        try:
            subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                check=True,
                timeout=5,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            raise RuntimeError(
                f"FFmpeg not found at '{self.ffmpeg_path}'. "
                "Please install FFmpeg or provide the correct path."
            )

    def overlay_subtitle(
        self,
        input_video: str,
        ass_subtitle_file: str,
        output_video: str,
        font_dir: Optional[str] = None,
        copy_codec: bool = False,
        preset: str = "medium",
        crf: int = 23,
    ) -> bool:
        """
        Overlay ASS subtitles on video using FFmpeg.

        Args:
            input_video: Path to input video file
            ass_subtitle_file: Path to ASS subtitle file
            output_video: Path to output video file
            font_dir: Optional directory containing fonts
            copy_codec: If True, copy video codec (faster, no re-encoding)
            preset: FFmpeg encoding preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
            crf: Quality level (0-51, lower is better)

        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(input_video):
            logger.error(f"Input video not found: {input_video}")
            return False

        if not os.path.exists(ass_subtitle_file):
            logger.error(f"Subtitle file not found: {ass_subtitle_file}")
            return False

        # Get absolute paths for existence check, but try to use relative paths for FFmpeg
        abs_input = os.path.abspath(input_video)
        abs_ass = os.path.abspath(ass_subtitle_file)
        abs_output = os.path.abspath(output_video)

        # Try to compute relative paths from common directory (output dir or project root)
        try:
            cwd = os.getcwd()
            rel_input = os.path.relpath(abs_input, cwd)
            rel_ass = os.path.relpath(abs_ass, cwd)
            rel_output = os.path.relpath(abs_output, cwd)
            
            # Use relative paths if they don't go too far up (to avoid complexity)
            use_input = rel_input if ".." not in rel_input or rel_input.count("..") < 2 else abs_input
            use_ass = rel_ass if ".." not in rel_ass or rel_ass.count("..") < 2 else abs_ass
            use_output = rel_output if ".." not in rel_output or rel_output.count("..") < 2 else abs_output
        except ValueError:
            # On Windows, relpath can fail across drives; use absolute
            use_input = abs_input
            use_ass = abs_ass
            use_output = abs_output

        # Build FFmpeg filter for subtitle overlay
        # IMPORTANT: Convert backslashes to forward slashes in the filter parameter
        # FFmpeg filter syntax requires forward slashes even on Windows
        ass_for_filter = use_ass.replace("\\", "/")
        if font_dir and os.path.exists(font_dir):
            try:
                abs_font = os.path.abspath(font_dir)
                rel_font = os.path.relpath(abs_font, os.getcwd())
                use_font = rel_font if ".." not in rel_font or rel_font.count("..") < 2 else abs_font
            except ValueError:
                use_font = os.path.abspath(font_dir)
            font_for_filter = use_font.replace("\\", "/")
            subtitle_filter = f"ass={ass_for_filter}:fontsdir={font_for_filter}"
        else:
            subtitle_filter = f"ass={ass_for_filter}"

        # Build FFmpeg command
        cmd = [
            self.ffmpeg_path,
            "-i", use_input,
            "-vf", subtitle_filter,
        ]

        # Add codec options
        if copy_codec:
            cmd.extend(["-c:v", "copy", "-c:a", "aac"])
        else:
            cmd.extend([
                "-c:v", "libx264",
                "-preset", preset,
                "-crf", str(crf),
                "-c:a", "aac",
            ])

        cmd.extend([
            "-y",  # Overwrite output file
            use_output,
        ])

        logger.info(f"Overlaying subtitles on video...")
        logger.info(f"Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
            )

            if result.returncode != 0:
                logger.error(f"FFmpeg error:\n{result.stderr}")
                return False

            logger.info(f"Successfully created: {output_video}")
            return True

        except subprocess.TimeoutExpired:
            logger.error("FFmpeg process timed out")
            return False
        except Exception as e:
            logger.error(f"Error during video processing: {e}")
            return False

    def overlay_subtitle_hq(
        self,
        input_video: str,
        ass_subtitle_file: str,
        output_video: str,
        font_dir: Optional[str] = None,
        preset: str = "slow",
    ) -> bool:
        """
        Overlay subtitles with high quality settings.

        Args:
            input_video: Path to input video file
            ass_subtitle_file: Path to ASS subtitle file
            output_video: Path to output video file
            font_dir: Optional directory containing fonts
            preset: FFmpeg encoding preset

        Returns:
            True if successful, False otherwise
        """
        return self.overlay_subtitle(
            input_video,
            ass_subtitle_file,
            output_video,
            font_dir=font_dir,
            copy_codec=False,
            preset=preset,
            crf=18,  # Higher quality
        )

    def overlay_subtitle_fast(
        self,
        input_video: str,
        ass_subtitle_file: str,
        output_video: str,
        font_dir: Optional[str] = None,
    ) -> bool:
        """
        Overlay subtitles with fast processing (copy codec if possible).

        Args:
            input_video: Path to input video file
            ass_subtitle_file: Path to ASS subtitle file
            output_video: Path to output video file
            font_dir: Optional directory containing fonts

        Returns:
            True if successful, False otherwise
        """
        return self.overlay_subtitle(
            input_video,
            ass_subtitle_file,
            output_video,
            font_dir=font_dir,
            copy_codec=True,
        )

    def get_video_info(self, video_path: str) -> Optional[dict]:
        """
        Get video information using FFprobe.

        Args:
            video_path: Path to video file

        Returns:
            Dictionary with video info or None if error
        """
        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v", "error",
                    "-select_streams", "v:0",
                    "-show_entries", "stream=width,height,r_frame_rate,duration",
                    "-of", "default=noprint_wrappers=1:nokey=1:noprint_wrappers=1",
                    video_path,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 4:
                    return {
                        "width": int(float(lines[0])),
                        "height": int(float(lines[1])),
                        "framerate": eval(lines[2]),  # e.g., "30/1" -> 30
                        "duration": float(lines[3]) if lines[3] else 0,
                    }
        except Exception as e:
            logger.error(f"Error getting video info: {e}")

        return None
