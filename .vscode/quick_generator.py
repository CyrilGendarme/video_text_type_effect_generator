#!/usr/bin/env python3
"""
Quick Video Generator

Fastest way to generate a video from text input.
Single step, minimal output, immediate feedback.
"""

import sys
from pathlib import Path
import subprocess

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_animator import TextAnimator, TextStyle
from src.video_processor import VideoProcessor


def main():
    """Quick generate"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("\n" + "="*50)
    print("QUICK VIDEO GENERATOR")
    print("="*50)

    # Get input
    text = input("\nEnter text (default: QUICK DEMO): ").strip() or "QUICK DEMO"
    text = text[:40]  # Limit length

    print(f"\nGenerating video for: '{text}'")

    # Prepare files
    input_video = output_dir / "input_video.mp4"
    ass_file = output_dir / "quick.ass"
    output_video = output_dir / f"output_{text[:15]}.mp4"

    # Create test video if needed
    if not input_video.exists():
        print("Creating test video...", end=" ", flush=True)
        try:
            subprocess.run([
                "ffmpeg",
                "-f", "lavfi",
                "-i", "color=c=0x1a1a1a:s=1920x1080:d=8",
                "-f", "lavfi",
                "-i", "anullsrc=r=48000:cl=mono:d=8",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-c:a", "aac",
                "-y",
                str(input_video)
            ], capture_output=True, timeout=30)
            print("OK")
        except:
            print("FAILED")
            return 1

    # Generate animation
    print("Generating animation...", end=" ", flush=True)
    try:
        animator = TextAnimator()
        style = TextStyle(
            font_size=72,
            bold=True,
            color="&H0000FFFF",
            outline_width=2.0,
        )
        animator.add_typewriter_text(text, 0.5, typing_speed=70, style=style, position=(960, 300))
        animator.add_fade_in_text("Generated", 2.5, duration=1.5, position=(960, 450))
        animator.save_ass_file(str(ass_file))
        print("OK")
    except Exception as e:
        print(f"FAILED: {e}")
        return 1

    # Process video
    print("Processing video...", end=" ", flush=True)
    try:
        processor = VideoProcessor()
        processor.overlay_subtitle(str(input_video), str(ass_file), str(output_video), preset="fast")
        print("OK")
    except Exception as e:
        print(f"FAILED: {e}")
        return 1

    # Summary
    size_mb = output_video.stat().st_size / (1024*1024) if output_video.exists() else 0
    print(f"\n[OK] Output: {output_video.name} ({size_mb:.1f}MB)")
    print(f"[OK] Location: {output_dir}")
    print("="*50 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
