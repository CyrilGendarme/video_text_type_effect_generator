"""
Video Text Type Effect Generator

A Python-based tool to generate dynamic text animations for video overlays
using FFmpeg and ASS subtitle format.

Architecture:
Python → Generate timed ASS/text → FFmpeg ass/overlay → MP4
"""

from src.text_animator import (
    TextAnimator,
    TextStyle,
    TextEvent,
    AnimationMode,
)
from src.video_processor import VideoProcessor
from src.main import TextVideoGenerator, create_example_animation

__version__ = "0.1.0"
__author__ = "Video Text Effect Generator"

__all__ = [
    "TextAnimator",
    "TextStyle",
    "TextEvent",
    "AnimationMode",
    "VideoProcessor",
    "TextVideoGenerator",
    "create_example_animation",
]
