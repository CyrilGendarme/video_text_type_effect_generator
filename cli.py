#!/usr/bin/env python3
"""
Command-line interface for Video Text Effect Generator

Usage:
    python cli.py generate-video <input> <output> <ass-file> [--font-dir FONTS] [--quality QUALITY]
    python cli.py create-ass <output> [--type TYPE] [--text TEXT]
    python cli.py overlay <video> <ass> <output> [--font-dir FONTS] [--quality QUALITY]
    python cli.py info <video>
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_animator import TextAnimator, TextStyle
from src.video_processor import VideoProcessor
from src.main import TextVideoGenerator


def cmd_generate_video(args):
    """Generate video with text overlay"""
    print(f"📹 Generating video with text overlay...")
    print(f"  Input:  {args.input}")
    print(f"  ASS:    {args.ass}")
    print(f"  Output: {args.output}")

    generator = TextVideoGenerator()

    success = generator.generate_video(
        args.input,
        args.output,
        ass_file=args.ass,
        font_dir=args.font_dir,
        preset=args.quality,
    )

    if success:
        print(f"✓ Video generated successfully!")
        print(f"  Saved to: {args.output}")
    else:
        print(f"✗ Failed to generate video")
        return 1

    return 0


def cmd_create_ass(args):
    """Create ASS subtitle file"""
    print(f"📝 Creating ASS subtitle file: {args.output}")

    animator = TextAnimator()

    if args.type == "typewriter":
        text = args.text or "Sample Text"
        animator.add_typewriter_text(text, 0.5)
        print(f"  Type: Typewriter effect")
        print(f"  Text: {text}")

    elif args.type == "reveal":
        text = args.text or "REVEAL TEXT"
        animator.add_reveal_text(text, 0.5)
        print(f"  Type: Reveal effect")
        print(f"  Text: {text}")

    elif args.type == "fade":
        text = args.text or "Fade In Text"
        animator.add_fade_in_text(text, 0.5, duration=2.0)
        print(f"  Type: Fade-in effect")
        print(f"  Text: {text}")

    else:
        print(f"  Type: Multiple effects")
        animator.add_typewriter_text("Title", 0.5, typing_speed=80)
        animator.add_reveal_text("Subtitle", 3.0)
        animator.add_fade_in_text("Extra Text", 5.0, duration=2.0)

    animator.save_ass_file(args.output)
    print(f"✓ ASS file created: {args.output}")

    return 0


def cmd_overlay(args):
    """Overlay ASS subtitles on video"""
    print(f"🎬 Overlaying subtitles on video...")
    print(f"  Video:  {args.video}")
    print(f"  ASS:    {args.ass}")
    print(f"  Output: {args.output}")

    processor = VideoProcessor()
    quality_preset = "medium" if args.quality == "medium" else args.quality

    success = processor.overlay_subtitle(
        args.video,
        args.ass,
        args.output,
        font_dir=args.font_dir,
        preset=quality_preset,
        crf=23 if args.quality == "medium" else (18 if args.quality == "high" else 28),
    )

    if success:
        print(f"✓ Video created successfully!")
        print(f"  Saved to: {args.output}")
    else:
        print(f"✗ Failed to overlay subtitles")
        return 1

    return 0


def cmd_info(args):
    """Display video information"""
    print(f"📊 Video Information: {args.video}")

    processor = VideoProcessor()
    info = processor.get_video_info(args.video)

    if info:
        print(f"  Resolution: {info['width']}x{info['height']}")
        print(f"  Framerate:  {info['framerate']:.2f} fps")
        print(f"  Duration:   {info['duration']:.2f}s ({int(info['duration']//60)}m {int(info['duration']%60)}s)")
    else:
        print(f"✗ Failed to get video info")
        return 1

    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Video Text Effect Generator - CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create ASS file with typewriter effect
  python cli.py create-ass output.ass --type typewriter --text "Hello World"

  # Overlay ASS on video
  python cli.py overlay input.mp4 output.ass result.mp4 --quality high

  # Generate complete video with text
  python cli.py generate-video input.mp4 output.ass result.mp4

  # Get video info
  python cli.py info input.mp4
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Generate video command
    gen_parser = subparsers.add_parser("generate-video", help="Generate video with text overlay")
    gen_parser.add_argument("input", help="Input video file")
    gen_parser.add_argument("ass", help="ASS subtitle file")
    gen_parser.add_argument("output", help="Output video file")
    gen_parser.add_argument("--font-dir", help="Directory containing fonts")
    gen_parser.add_argument("--quality", choices=["fast", "medium", "high"], default="medium")
    gen_parser.set_defaults(func=cmd_generate_video)

    # Create ASS command
    ass_parser = subparsers.add_parser("create-ass", help="Create ASS subtitle file")
    ass_parser.add_argument("output", help="Output ASS file")
    ass_parser.add_argument("--type", choices=["typewriter", "reveal", "fade", "multi"], default="typewriter")
    ass_parser.add_argument("--text", help="Text to animate")
    ass_parser.set_defaults(func=cmd_create_ass)

    # Overlay command
    overlay_parser = subparsers.add_parser("overlay", help="Overlay ASS on video")
    overlay_parser.add_argument("video", help="Input video file")
    overlay_parser.add_argument("ass", help="ASS subtitle file")
    overlay_parser.add_argument("output", help="Output video file")
    overlay_parser.add_argument("--font-dir", help="Directory containing fonts")
    overlay_parser.add_argument("--quality", choices=["fast", "medium", "high"], default="medium")
    overlay_parser.set_defaults(func=cmd_overlay)

    # Info command
    info_parser = subparsers.add_parser("info", help="Display video information")
    info_parser.add_argument("video", help="Video file")
    info_parser.set_defaults(func=cmd_info)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        return args.func(args)
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
