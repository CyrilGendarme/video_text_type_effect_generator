#!/usr/bin/env python3
"""
Advanced Example: Complex Animation Sequences

Demonstrates advanced features like:
- Color gradients in text
- Multiple animation layers
- Precise timing control
- Custom positions and alignments
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_animator import TextAnimator, TextStyle, AnimationMode


def example_music_video_credits():
    """Create a music video with artist and track information"""
    print("Creating music video credits...")

    animator = TextAnimator()

    # Album artwork title - large and bold
    album_style = TextStyle(
        font_name="Staatliches-Regular",
        font_size=96,
        bold=True,
        color="&H0000FFFF",  # Yellow
        outline_width=4.0,
        shadow_depth=3.0,
    )

    # Artist name - medium
    artist_style = TextStyle(
        font_name="DMSans",
        font_size=48,
        color="&H00FFFFFF",  # White
        outline_width=2.0,
    )

    # Track name - medium
    track_style = TextStyle(
        font_name="DMSans",
        font_size=42,
        italic=True,
        color="&H00FF00FF",  # Magenta (BGR)
        outline_width=2.0,
    )

    current_time = 1.0

    # Main title reveal
    current_time = animator.add_reveal_text(
        "NEON NIGHTS",
        current_time,
        style=album_style,
        position=(960, 200),
    )

    # Pause for effect
    current_time += 1.5

    # Artist name typewriter
    current_time = animator.add_typewriter_text(
        "Synthwave Rising",
        current_time,
        typing_speed=60,
        style=artist_style,
        position=(960, 350),
    )

    # Pause
    current_time += 1.0

    # Track name
    current_time = animator.add_typewriter_text(
        "Electronic Dreams",
        current_time,
        typing_speed=70,
        style=track_style,
        position=(960, 450),
    )

    # Credits fade in
    current_time += 1.0
    current_time = animator.add_fade_in_text(
        "Produced by Future Sound",
        current_time,
        duration=2.0,
        style=TextStyle(
            font_size=24,
            color="&H00CCCCCC",  # Light gray
        ),
        position=(960, 550),
    )

    # Save
    ass_file = "example_music_video.ass"
    animator.save_ass_file(ass_file)
    print(f"[OK] Saved: {ass_file}")
    return ass_file


def example_speech_subtitles():
    """Create subtitles for a speech with multiple speakers"""
    print("Creating speech subtitles...")

    animator = TextAnimator()

    # Speaker 1 style - blue
    speaker1_style = TextStyle(
        font_name="Arial",
        font_size=32,
        color="&H00FF0000",  # Blue
        outline_width=1.5,
    )

    # Speaker 2 style - green
    speaker2_style = TextStyle(
        font_name="Arial",
        font_size=32,
        color="&H0000FF00",  # Green
        outline_width=1.5,
    )

    current_time = 0.5

    # Speaker 1
    current_time = animator.add_typewriter_text(
        "Hello everyone, welcome to the presentation.",
        current_time,
        typing_speed=50,
        style=speaker1_style,
        position=(960, 540),
    )

    current_time += 0.5

    # Speaker 2
    current_time = animator.add_typewriter_text(
        "Thank you! Let's begin with the first topic.",
        current_time,
        typing_speed=50,
        style=speaker2_style,
        position=(960, 540),
    )

    current_time += 0.5

    # Speaker 1 again
    current_time = animator.add_typewriter_text(
        "Today we'll cover three main areas...",
        current_time,
        typing_speed=50,
        style=speaker1_style,
        position=(960, 540),
    )

    ass_file = "example_speech_subtitles.ass"
    animator.save_ass_file(ass_file)
    print(f"[OK] Saved: {ass_file}")
    return ass_file


def example_layered_animations():
    """Create layered animations with different positions"""
    print("Creating layered animations...")

    animator = TextAnimator()

    # Background text - static, barely visible
    bg_style = TextStyle(
        font_size=28,
        color="&H00666666",  # Dark gray
        alpha=0.5,
    )

    # Main text - bright
    main_style = TextStyle(
        font_size=48,
        bold=True,
        color="&H0000FFFF",  # Yellow
        outline_width=2.0,
    )

    current_time = 0.5

    # Reveal effect on center
    current_time = animator.add_reveal_text(
        "MAIN MESSAGE",
        current_time,
        style=main_style,
        position=(960, 300),
    )

    # Typewriter on top-left (starts at same time as reveal continues)
    animator.add_typewriter_text(
        "Side Info",
        current_time - 0.5,
        typing_speed=100,
        style=TextStyle(font_size=24),
        position=(200, 100),
    )

    # Typewriter on bottom-right (with delay)
    animator.add_typewriter_text(
        "Additional Details",
        current_time + 1.0,
        typing_speed=80,
        style=TextStyle(font_size=24),
        position=(1720, 900),  # Assuming 1920x1080 resolution
    )

    ass_file = "example_layered.ass"
    animator.save_ass_file(ass_file)
    print(f"[OK] Saved: {ass_file}")
    return ass_file


def example_color_palette():
    """Demonstrate different color combinations"""
    print("Creating color palette example...")

    animator = TextAnimator()

    colors = [
        ("&H00FFFFFF", "White"),          # White
        ("&H0000FFFF", "Yellow"),         # Yellow (BGR)
        ("&H00FF0000", "Blue"),           # Blue (BGR)
        ("&H0000FF00", "Green"),          # Green (BGR)
        ("&H00FF00FF", "Magenta"),        # Magenta (BGR)
        ("&H00FFFF00", "Cyan"),           # Cyan (BGR)
        ("&H000000FF", "Red"),            # Red (BGR)
        ("&H00FF6600", "Orange"),         # Orange (BGR)
    ]

    y_pos = 200
    current_time = 0.5

    for color, name in colors:
        style = TextStyle(
            font_size=36,
            bold=True,
            color=color,
            outline_width=2.0,
        )

        animator.add_typewriter_text(
            f"{name}",
            current_time,
            typing_speed=40,
            style=style,
            position=(960, y_pos),
        )

        y_pos += 80
        current_time += 0.8

    ass_file = "example_color_palette.ass"
    animator.save_ass_file(ass_file)
    print(f"[OK] Saved: {ass_file}")
    return ass_file


if __name__ == "__main__":
    print("Advanced Examples\n")

    examples = [
        example_music_video_credits,
        example_speech_subtitles,
        example_layered_animations,
        example_color_palette,
    ]

    for example_func in examples:
        try:
            ass_file = example_func()
            print(f"[OK] {example_func.__doc__}\n")
        except Exception as e:
            print(f"[ERROR] Error in {example_func.__name__}: {e}\n")

    print("All advanced examples completed!")
    print("\nGenerated files:")
    print("  - example_music_video.ass")
    print("  - example_speech_subtitles.ass")
    print("  - example_layered.ass")
    print("  - example_color_palette.ass")
