#!/usr/bin/env python3
"""
VS Code Interactive Video Generator

Takes user input (text/word) and generates a video with text animation overlay.
Outputs video to local output folder.
"""

import sys
import os
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_animator import TextAnimator, TextStyle, AnimationMode
from src.video_processor import VideoProcessor


def create_output_dir():
    """Create output directory if it doesn't exist"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


def create_test_video(duration=5, width=1920, height=1080, output_path="input_video.mp4"):
    """
    Create a simple test video if one doesn't exist.
    Uses FFmpeg to generate a colored video with silence.
    """
    import subprocess

    if os.path.exists(output_path):
        print(f"[INFO] Test video already exists: {output_path}")
        return output_path

    print(f"[INFO] Creating test video...")
    try:
        cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"color=c=0x1a1a1a:s={width}x{height}:d={duration}",
            "-f", "lavfi",
            "-i", f"anullsrc=r=48000:cl=mono:d={duration}",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y",
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"[OK] Test video created: {output_path}")
            return output_path
        else:
            print(f"[ERROR] Failed to create test video")
            print(result.stderr)
            return None
    except Exception as e:
        print(f"[ERROR] Error creating test video: {e}")
        return None


def generate_video_from_text(text: str, output_dir: Path = None) -> bool:
    """
    Generate a video with text animation.

    Args:
        text: Text to animate
        output_dir: Directory to save output (default: ./output)

    Returns:
        True if successful, False otherwise
    """
    if output_dir is None:
        output_dir = create_output_dir()

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    print(f"\n{'='*60}")
    print(f"[VIDEO GENERATOR]")
    print(f"{'='*60}")
    print(f"[INFO] Input text: '{text}'")
    print(f"[INFO] Output directory: {output_dir}")

    # File paths
    ass_file = output_dir / "animation.ass"
    input_video = output_dir / "input_video.mp4"
    output_video = output_dir / f"output_{text[:20]}.mp4"

    # Step 1: Create test video if needed
    if not input_video.exists():
        print(f"\n[STEP 1] Creating test video...")
        create_test_video(duration=10, output_path=str(input_video))
        if not input_video.exists():
            print(f"[ERROR] Failed to create test video")
            return False
    else:
        print(f"\n[STEP 1] Using existing test video: {input_video}")

    # Step 2: Generate ASS file with animation
    print(f"\n[STEP 2] Generating ASS animation file...")
    try:
        animator = TextAnimator()

        # Create styled text
        title_style = TextStyle(
            font_name="Arial",
            font_size=72,
            bold=True,
            color="&H0000FFFF",  # Yellow (BGR)
            outline_width=3.0,
            shadow_depth=2.0,
        )

        # Add multiple animations
        current_time = 0.5

        # Typewriter effect
        current_time = animator.add_typewriter_text(
            text.upper(),
            current_time,
            typing_speed=80,
            style=title_style,
            position=(960, 300),
        )

        # Add some spacing
        current_time += 1.0

        # Reveal effect (optional)
        animator.add_reveal_text(
            f"Generated: {text}",
            current_time,
            style=TextStyle(font_size=36),
            position=(960, 450),
        )

        # Save ASS file
        animator.save_ass_file(str(ass_file))
        print(f"[OK] ASS file created: {ass_file}")

    except Exception as e:
        print(f"[ERROR] Failed to generate ASS file: {e}")
        return False

    # Step 3: Overlay on video
    print(f"\n[STEP 3] Overlaying animation on video...")
    try:
        processor = VideoProcessor()
        success = processor.overlay_subtitle(
            str(input_video),
            str(ass_file),
            str(output_video),
            preset="fast",  # Fast for quick preview
        )

        if success:
            print(f"[OK] Video generated: {output_video}")
            print(f"[INFO] File size: {output_video.stat().st_size / (1024*1024):.2f} MB")
        else:
            print(f"[ERROR] Failed to generate video")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to overlay subtitles: {e}")
        return False

    print(f"\n{'='*60}")
    print(f"[SUCCESS] Video output: {output_video}")
    print(f"{'='*60}\n")

    return True


def main():
    """Main entry point with user interaction"""
    print("\n" + "="*60)
    print("VIDEO TEXT EFFECT GENERATOR")
    print("="*60)

    output_dir = create_output_dir()
    print(f"[INFO] Output directory: {output_dir}\n")

    # Get user input
    print("Enter text/word to generate video (or press Enter for demo):")
    text = input(">>> ").strip()

    if not text:
        # Demo text
        text = "HELLO WORLD"
        print(f"[INFO] Using demo text: '{text}'")

    # Validate text
    if len(text) == 0:
        print("[ERROR] Text cannot be empty")
        return 1

    if len(text) > 50:
        print("[WARNING] Text is long, truncating to 50 characters")
        text = text[:50]

    # Generate video
    success = generate_video_from_text(text, output_dir)

    if success:
        print(f"[INFO] Output file ready in: {output_dir}")
        print(f"[INFO] Files:")
        for f in sorted(output_dir.glob("*.mp4")):
            size_mb = f.stat().st_size / (1024*1024)
            print(f"  - {f.name} ({size_mb:.2f} MB)")
        return 0
    else:
        print("[ERROR] Failed to generate video")
        return 1


if __name__ == "__main__":
    sys.exit(main())
