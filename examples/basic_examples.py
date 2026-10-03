#!/usr/bin/env python3
"""
Example: Basic Typewriter Effect

Demonstrates how to create a simple typewriter animation overlay.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_animator import TextAnimator, TextStyle
from src.video_processor import VideoProcessor


def example_basic_typewriter():
    """Create a basic typewriter effect"""
    print("Creating basic typewriter effect...")

    animator = TextAnimator()

    # Simple typewriter text
    current_time = 0.5
    current_time = animator.add_typewriter_text(
        "Hello, World!",
        current_time,
        typing_speed=80,
    )

    # Save ASS file
    ass_file = "example_typewriter.ass"
    animator.save_ass_file(ass_file)
    print(f"[OK] Saved ASS file: {ass_file}")

    return ass_file


def example_styled_typewriter():
    """Typewriter effect with custom styling"""
    print("Creating styled typewriter effect...")

    animator = TextAnimator()

    # Define custom style
    title_style = TextStyle(
        font_name="Arial",
        font_size=72,
        bold=True,
        color="&H00FFFFFF",  # White
        outline_color="&H00000000",  # Black outline
        outline_width=3.0,
        shadow_depth=2.0,
    )

    # Add styled text
    current_time = 0.5
    current_time = animator.add_typewriter_text(
        "AMAZING TITLE",
        current_time,
        typing_speed=100,
        style=title_style,
        position=(960, 300),  # Center horizontally, upper-middle vertically
    )

    ass_file = "example_styled_typewriter.ass"
    animator.save_ass_file(ass_file)
    print(f"[OK] Saved ASS file: {ass_file}")

    return ass_file


def example_multiple_animations():
    """Multiple animations with different effects"""
    print("Creating multiple animations...")

    animator = TextAnimator()

    # Title style
    title_style = TextStyle(
        font_name="Arial",
        font_size=64,
        bold=True,
        color="&H00FFFFFF",  # White
        outline_width=2.0,
    )

    # Subtitle style
    subtitle_style = TextStyle(
        font_name="Arial",
        font_size=36,
        color="&H0000FFFF",  # Yellow (BGR)
        outline_width=1.5,
    )

    # Timeline
    current_time = 0.5

    # Typewriter effect
    current_time = animator.add_typewriter_text(
        "WELCOME",
        current_time,
        typing_speed=100,
        style=title_style,
        position=(960, 300),
    )

    # Pause between animations
    current_time += 1.0

    # Reveal effect
    current_time = animator.add_reveal_text(
        "TO THE SHOW",
        current_time,
        style=subtitle_style,
        position=(960, 400),
    )

    # Pause
    current_time += 1.0

    # Fade-in effect
    current_time = animator.add_fade_in_text(
        "Enjoy the content!",
        current_time,
        duration=2.0,
        style=TextStyle(font_size=28),
        position=(960, 500),
    )

    ass_file = "example_multiple.ass"
    animator.save_ass_file(ass_file)
    print(f"[OK] Saved ASS file: {ass_file}")

    return ass_file


def print_ass_content(ass_file):
    """Display the generated ASS file content"""
    try:
        with open(ass_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n{'='*60}")
        print(f"ASS File Content: {ass_file}")
        print(f"{'='*60}")
        print(content)
        print(f"{'='*60}\n")
    except FileNotFoundError:
        print(f"File not found: {ass_file}")


if __name__ == "__main__":
    print("Video Text Type Effect - Examples\n")

    # Run examples
    ass_file1 = example_basic_typewriter()
    print_ass_content(ass_file1)

    ass_file2 = example_styled_typewriter()
    print_ass_content(ass_file2)

    ass_file3 = example_multiple_animations()
    print_ass_content(ass_file3)

    print("\nAll examples completed!")
    print("Next steps:")
    print("1. Create a sample video or use an existing one")
    print("2. Use video_processor.py to overlay the ASS files")
    print("   Example: processor.overlay_subtitle('input.mp4', 'example_typewriter.ass', 'output.mp4')")

