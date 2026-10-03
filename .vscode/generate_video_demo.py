#!/usr/bin/env python3
"""
Demo Video Generator

Generates example videos with different text animations.
No user input required - just run and it creates demo videos.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_animator import TextAnimator, TextStyle
from src.video_processor import VideoProcessor
import subprocess
import os


def create_test_video(duration=5, output_path="input_video.mp4"):
    """Create a simple test video"""
    if os.path.exists(output_path):
        return output_path

    print(f"[INFO] Creating test video ({duration}s)...")
    try:
        cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"color=c=0x1a1a1a:s=1920x1080:d={duration}",
            "-f", "lavfi",
            "-i", f"anullsrc=r=48000:cl=mono:d={duration}",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-y",
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        if result.returncode == 0:
            print(f"[OK] Test video created")
            return output_path
    except Exception as e:
        print(f"[ERROR] {e}")
    return None


def generate_demo_video(name: str, text: str, output_dir: Path):
    """Generate a single demo video"""
    print(f"\n[GENERATING] {name}...")

    input_video = output_dir / "input_video.mp4"
    ass_file = output_dir / f"{name}.ass"
    output_video = output_dir / f"{name}.mp4"

    # Create ASS file
    animator = TextAnimator()

    title_style = TextStyle(
        font_name="Arial",
        font_size=64,
        bold=True,
        color="&H0000FFFF",
        outline_width=2.5,
    )

    if name == "demo_typewriter":
        animator.add_typewriter_text(
            text,
            0.5,
            typing_speed=100,
            style=title_style,
            position=(960, 300),
        )
    elif name == "demo_reveal":
        animator.add_reveal_text(
            text.upper(),
            0.5,
            style=title_style,
            position=(960, 300),
        )
    elif name == "demo_fade":
        animator.add_fade_in_text(
            text,
            0.5,
            duration=2.0,
            style=TextStyle(font_size=56),
            position=(960, 300),
        )
    elif name == "demo_multiple":
        t = 0.5
        t = animator.add_typewriter_text(
            "ANIMATION",
            t,
            typing_speed=80,
            style=title_style,
            position=(960, 250),
        )
        t += 1.0
        t = animator.add_reveal_text(
            "EFFECTS",
            t,
            style=TextStyle(font_size=48),
            position=(960, 400),
        )
        t += 1.0
        animator.add_fade_in_text(
            "Combined",
            t,
            duration=1.5,
            style=TextStyle(font_size=36),
            position=(960, 550),
        )

    animator.save_ass_file(str(ass_file))

    # Overlay on video
    processor = VideoProcessor()
    success = processor.overlay_subtitle(
        str(input_video),
        str(ass_file),
        str(output_video),
        preset="fast",
    )

    if success:
        size_mb = output_video.stat().st_size / (1024*1024)
        print(f"[OK] {name}.mp4 ({size_mb:.2f} MB)")
        return True
    else:
        print(f"[ERROR] Failed to create {name}")
        return False


def main():
    """Generate demo videos"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("\n" + "="*60)
    print("DEMO VIDEO GENERATOR")
    print("="*60)
    print(f"[INFO] Output: {output_dir}\n")

    # Create test video
    input_video = output_dir / "input_video.mp4"
    if not input_video.exists():
        if not create_test_video(output_path=str(input_video)):
            print("[ERROR] Failed to create test video")
            return 1

    # Generate demo videos
    demos = [
        ("demo_typewriter", "TYPEWRITER EFFECT"),
        ("demo_reveal", "REVEAL ANIMATION"),
        ("demo_fade", "FADE IN EFFECT"),
        ("demo_multiple", "COMBINED EFFECTS"),
    ]

    success_count = 0
    for name, text in demos:
        if generate_demo_video(name, text, output_dir):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"[SUCCESS] Generated {success_count}/{len(demos)} demo videos")
    print(f"[INFO] All files in: {output_dir}")
    print(f"{'='*60}\n")

    return 0 if success_count == len(demos) else 1


if __name__ == "__main__":
    sys.exit(main())
