"""
Text animator module for generating typewriter and reveal effects
"""
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple


class AnimationMode(Enum):
    """Different text animation modes"""
    TYPEWRITER = "typewriter"  # Sequential character reveal
    REVEAL = "reveal"  # Radial reveal from center (like the legacy effect)
    FADE_IN = "fade_in"  # Fade in effect
    MARQUEE = "marquee"  # Scrolling text


@dataclass
class TextStyle:
    """Style configuration for text"""
    font_name: str = "Arial"
    font_size: int = 48
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str = "&H00FFFFFF"  # BGR format (white)
    outline_color: str = "&H00000000"  # BGR format (black)
    outline_width: float = 2.0
    shadow_depth: float = 2.0
    shadow_angle: float = 45.0
    alpha: float = 0.0  # 0 = opaque, 1 = transparent


@dataclass
class TextEvent:
    """A single text animation event"""
    start_time: float  # seconds
    end_time: float  # seconds
    text: str
    style: TextStyle
    position: Tuple[int, int] = (0, 0)  # (x, y) screen coordinates
    alignment: int = 5  # 5 = center (numpad position)
    animation_mode: AnimationMode = AnimationMode.TYPEWRITER
    typing_speed: float = 80  # ms per character
    wait_before: float = 0  # ms before animation starts
    wait_after: float = 0  # ms after animation completes


class TextAnimator:
    """Generates animated text sequences for ASS subtitles"""

    def __init__(self):
        self.events: List[TextEvent] = []

    def add_typewriter_text(
        self,
        text: str,
        start_time: float,
        typing_speed: float = 80,
        wait_before: float = 0,
        wait_after: float = 0,
        style: Optional[TextStyle] = None,
        position: Tuple[int, int] = (0, 0),
        alignment: int = 5,
    ) -> float:
        """
        Add typewriter effect text.
        Returns the end time of the animation.
        """
        if style is None:
            style = TextStyle()

        # Calculate duration based on text length and typing speed
        num_chars = len(text)
        animation_duration = (num_chars * typing_speed) / 1000.0
        end_time = start_time + wait_before / 1000.0 + animation_duration + wait_after / 1000.0

        event = TextEvent(
            start_time=start_time,
            end_time=end_time,
            text=text,
            style=style,
            position=position,
            alignment=alignment,
            animation_mode=AnimationMode.TYPEWRITER,
            typing_speed=typing_speed,
            wait_before=wait_before,
            wait_after=wait_after,
        )
        self.events.append(event)
        return end_time

    def add_reveal_text(
        self,
        text: str,
        start_time: float,
        frame_delay: float = 110,
        style: Optional[TextStyle] = None,
        position: Tuple[int, int] = (0, 0),
        alignment: int = 5,
    ) -> float:
        """
        Add radial reveal effect (like legacy reveal animation).
        Returns the end time of the animation.
        """
        if style is None:
            style = TextStyle()

        num_chars = len(text)
        # Calculate based on frame delay and number of characters
        # Adjust to account for the expanding radius
        animation_duration = (num_chars * frame_delay) / 1000.0 * 1.2
        end_time = start_time + animation_duration

        event = TextEvent(
            start_time=start_time,
            end_time=end_time,
            text=text,
            style=style,
            position=position,
            alignment=alignment,
            animation_mode=AnimationMode.REVEAL,
            typing_speed=frame_delay,
        )
        self.events.append(event)
        return end_time

    def add_fade_in_text(
        self,
        text: str,
        start_time: float,
        duration: float = 1.0,
        style: Optional[TextStyle] = None,
        position: Tuple[int, int] = (0, 0),
        alignment: int = 5,
    ) -> float:
        """Add fade-in effect text."""
        if style is None:
            style = TextStyle()

        end_time = start_time + duration

        event = TextEvent(
            start_time=start_time,
            end_time=end_time,
            text=text,
            style=style,
            position=position,
            alignment=alignment,
            animation_mode=AnimationMode.FADE_IN,
        )
        self.events.append(event)
        return end_time

    def _time_to_ass_format(self, seconds: float) -> str:
        """Convert time in seconds to ASS timestamp format (H:MM:SS.CC)"""
        hours = int(seconds // 3600)
        remaining = seconds % 3600
        minutes = int(remaining // 60)
        secs = remaining % 60
        centiseconds = int((secs % 1) * 100)
        return f"{hours}:{minutes:02d}:{int(secs):02d}.{centiseconds:02d}"

    def _style_to_ass(self, style: TextStyle) -> str:
        """Convert TextStyle to ASS style definition"""
        # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,
        # BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,
        # BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        bold = -1 if style.bold else 0
        italic = -1 if style.italic else 0
        underline = -1 if style.underline else 0

        return (
            f"Default,{style.font_name},{style.font_size},{style.color},"
            f"&H0000FF00,{style.outline_color},&H00000000,"
            f"{bold},{italic},{underline},0,100,100,0,0,1,"
            f"{style.outline_width},{style.shadow_depth},2,10,10,10,1"
        )

    def _generate_typewriter_frames(
        self, event: TextEvent
    ) -> List[Tuple[float, str, float]]:
        """Generate keyframes for typewriter effect.
        Returns list of (time_ms, visible_text, alpha)
        """
        frames = []
        text = event.text
        num_chars = len(text)

        if num_chars == 0:
            return frames

        # Wait before animation
        if event.wait_before > 0:
            frames.append((0, "", 0))
            frames.append((event.wait_before, "", 0))

        # Type each character
        start_delay = event.wait_before
        for i in range(num_chars + 1):
            time_ms = start_delay + (i * event.typing_speed)
            visible_text = text[:i]
            frames.append((time_ms, visible_text, 0))

        # Wait after animation
        if event.wait_after > 0:
            frames.append((start_delay + (num_chars * event.typing_speed), text, 0))
            frames.append(
                (start_delay + (num_chars * event.typing_speed) + event.wait_after, text, 0)
            )

        return frames

    def _generate_reveal_frames(self, event: TextEvent) -> List[Tuple[float, str, float]]:
        """Generate keyframes for radial reveal effect.
        Mimics the legacy reveal animation with expanding radius.
        """
        frames = []
        text = event.text.upper()
        num_chars = len(text)

        if num_chars == 0:
            return frames

        # Calculate center position
        center = (num_chars - 1) / 2.0
        frame_delay = event.typing_speed
        radius_increment = 0.45

        # Generate frames showing progressive reveal
        time_ms = 0
        radius = 0
        solved = [False] * num_chars
        random_underscore_chance = 0.45

        max_iterations = int((num_chars / 2) / radius_increment) + 10

        for _ in range(max_iterations):
            if all(solved):
                frames.append((time_ms, text, 0))
                break

            # Build current frame text
            frame_text = ""
            for i in range(num_chars):
                dist = abs(i - center)
                if dist > radius:
                    frame_text += " "
                elif solved[i]:
                    frame_text += text[i]
                else:
                    # Probabilistically reveal character
                    import random

                    if random.random() < random_underscore_chance:
                        solved[i] = True
                        frame_text += text[i]
                    else:
                        frame_text += "_"

            frames.append((time_ms, frame_text, 0))

            # Calculate next delay
            delay = max(
                min((frame_delay / num_chars) * 12, frame_delay), frame_delay / 2
            )
            time_ms += delay
            radius += radius_increment

        return frames

    def _generate_fade_in_frames(self, event: TextEvent) -> List[Tuple[float, str, float]]:
        """Generate keyframes for fade-in effect"""
        frames = []
        duration_ms = (event.end_time - event.start_time) * 1000
        num_frames = max(10, int(duration_ms / 50))  # ~50ms per frame

        for i in range(num_frames + 1):
            time_ms = (i / num_frames) * duration_ms
            # Alpha goes from 1 (transparent) to 0 (opaque)
            alpha = 1.0 - (i / num_frames)
            frames.append((time_ms, event.text, alpha))

        return frames

    def to_ass_string(self) -> str:
        """Generate complete ASS file content"""
        # ASS file structure
        ass_lines = ["[Script Info]", "Title: Generated Text Animation", ""]

        # Collect all unique styles
        styles = {}
        style_names = {}
        for i, event in enumerate(self.events):
            style_key = (
                event.style.font_name,
                event.style.font_size,
                event.style.bold,
                event.style.italic,
                event.style.color,
            )
            if style_key not in styles:
                style_name = f"Style{len(styles)}"
                styles[style_key] = event.style
                style_names[i] = style_name
            else:
                style_names[i] = style_name

        # Add styles section
        ass_lines.append("[V4+ Styles]")
        ass_lines.append(
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
            " BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
            " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"
        )

        for idx, (style_key, style) in enumerate(styles.items()):
            ass_lines.append(f"Style: {self._style_to_ass(style)}")

        ass_lines.append("")

        # Add events section
        ass_lines.append("[Events]")
        ass_lines.append(
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        )

        for event_idx, event in enumerate(self.events):
            style_name = f"Default"

            start = self._time_to_ass_format(event.start_time)
            end = self._time_to_ass_format(event.end_time)

            # Generate appropriate frames based on animation mode
            if event.animation_mode == AnimationMode.TYPEWRITER:
                # For typewriter, we'll use the text as-is and let FFmpeg handle timing
                text = event.text
            elif event.animation_mode == AnimationMode.REVEAL:
                text = event.text
            elif event.animation_mode == AnimationMode.FADE_IN:
                text = event.text
            else:
                text = event.text

            # Format text with position if specified
            if event.position != (0, 0):
                pos_x, pos_y = event.position
                text = f"{{\\pos({pos_x},{pos_y})}}{text}"

            # Add alignment
            text = f"{{\\a{event.alignment}}}{text}"

            ass_lines.append(
                f"Dialogue: 0,{start},{end},{style_name},,0,0,0,,{text}"
            )

        return "\n".join(ass_lines)

    def save_ass_file(self, filepath: str):
        """Save generated ASS content to file"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_ass_string())
