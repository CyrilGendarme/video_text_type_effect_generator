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
    spacing: float = 0.0  # letter spacing in pixels


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
    area: Optional[Tuple[int, int]] = None  # (width, height) of a screen-centered text box
    frames: Optional[List[Tuple[float, str, float]]] = None  # (time_ms, text, alpha)
    fade_ms: int = 0  # fade-in duration for FADE_IN


@dataclass
class BackgroundEvent:
    """Full-screen colored rectangle with fade in/out"""
    start_time: float
    end_time: float
    color: Tuple[int, int, int, int]  # r, g, b, a (a: 255 = opaque)
    fade_in: float = 1.0
    fade_out: float = 1.0
    rect: Optional[Tuple[int, int]] = None  # (width, height), centered; None = full screen


class TextAnimator:
    """Generates animated text sequences for ASS subtitles"""

    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        self.events: List[TextEvent] = []
        self.backgrounds: List[BackgroundEvent] = []

    def add_background(
        self,
        start_time: float,
        end_time: float,
        color: Tuple[int, int, int, int] = (0, 0, 0, 180),
        fade_in: float = 1.0,
        fade_out: float = 1.0,
        rect: Optional[Tuple[int, int]] = None,
    ) -> None:
        """Add an RGBA background fading in from / out to transparent.
        color is (r, g, b, a) with a in 0-255 (255 = opaque).
        rect is (width, height) of a screen-centered box; None fills the screen."""
        self.backgrounds.append(
            BackgroundEvent(start_time, end_time, color, fade_in, fade_out, rect)
        )

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
        area: Optional[Tuple[int, int]] = None,
    ) -> float:
        """
        Add typewriter effect text.
        area: (width, height) of a screen-centered box in which the text is wrapped.
        Returns the end time of the animation.
        """
        if style is None:
            style = TextStyle()

        # Calculate duration based on text length and typing speed
        num_chars = max(len(l) for l in text.split("\n")) if text else 0
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
            area=area,
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
        hold: float = 0.0,
        area: Optional[Tuple[int, int]] = None,
    ) -> float:
        """
        Add radial reveal effect (like legacy reveal animation).
        hold: seconds the full text stays visible once revealed.
        area: (width, height) of a screen-centered box in which the text is wrapped.
        Returns the end time of the animation.
        """
        if style is None:
            style = TextStyle()

        event = TextEvent(
            start_time=start_time,
            end_time=start_time,
            text=text,
            style=style,
            position=position,
            alignment=alignment,
            animation_mode=AnimationMode.REVEAL,
            typing_speed=frame_delay,
            area=area,
        )
        event.frames = self._generate_reveal_frames(event)
        last_ms = event.frames[-1][0] if event.frames else 0
        end_time = start_time + last_ms / 1000.0 + hold
        event.end_time = end_time
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
        hold: float = 0.0,
    ) -> float:
        """Add fade-in effect text; it stays fully visible for `hold` seconds after the fade."""
        if style is None:
            style = TextStyle()

        end_time = start_time + duration + hold

        event = TextEvent(
            start_time=start_time,
            end_time=end_time,
            text=text,
            style=style,
            position=position,
            alignment=alignment,
            animation_mode=AnimationMode.FADE_IN,
            fade_ms=int(duration * 1000),
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

    def _style_to_ass(self, style_name: str, style: TextStyle) -> str:
        """Convert TextStyle to ASS style definition"""
        # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,
        # BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,
        # BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
        bold = -1 if style.bold else 0
        italic = -1 if style.italic else 0
        underline = -1 if style.underline else 0

        return (
            f"{style_name},{style.font_name},{style.font_size},{style.color},"
            f"&H0000FF00,{style.outline_color},&H00000000,"
            f"{bold},{italic},{underline},0,100,100,{style.spacing},0,1,"
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
        lines = event.text.upper().split("\n")
        per_line = [self._reveal_line_frames(l, event.typing_speed) for l in lines]
        times = sorted({ms for fr in per_line for ms, _, _ in fr})
        frames = []
        for t in times:
            parts = []
            for l, fr in zip(lines, per_line):
                cur = [f for f in fr if f[0] <= t]
                parts.append(cur[-1][1] if cur else " " * len(l))
            frames.append((t, "\n".join(parts), 0))
        return frames

    def _reveal_line_frames(self, text: str, frame_delay: float) -> List[Tuple[float, str, float]]:
        frames = []
        num_chars = len(text)

        if num_chars == 0:
            return frames

        # Calculate center position
        center = (num_chars - 1) / 2.0
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

    def to_ass_string(self, embed_fades: bool = True) -> str:
        """Generate complete ASS file content"""
        # ASS file structure - Video resolution for proper positioning
        ass_lines = [
            "[Script Info]",
            "Title: Generated Text Animation",
            f"PlayResX: {self.width}",
            f"PlayResY: {self.height}",
            ""
        ]

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
                event.style.spacing,
                event.style.outline_width,
                event.style.shadow_depth,
            )
            if style_key not in styles:
                style_name = f"Style{len(styles)}"
                styles[style_key] = event.style
                style_names[i] = style_name
            else:
                style_names[i] = next(
                    f"Style{idx}" for idx, k in enumerate(styles) if k == style_key
                )

        # Add styles section
        ass_lines.append("[V4+ Styles]")
        ass_lines.append(
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,"
            " BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
            " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"
        )

        for style_idx, (style_key, style) in enumerate(styles.items()):
            style_name = f"Style{style_idx}"
            ass_lines.append(f"Style: {self._style_to_ass(style_name, style)}")

        ass_lines.append("")

        # Add events section
        ass_lines.append("[Events]")
        ass_lines.append(
            "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
        )

        for bg in self.backgrounds:
            r, g, b, a = bg.color
            bw, bh = bg.rect or (self.width, self.height)
            x0, y0 = (self.width - bw) // 2, (self.height - bh) // 2
            ass_lines.append(
                f"Dialogue: 0,{self._time_to_ass_format(bg.start_time)},"
                f"{self._time_to_ass_format(bg.end_time)},Style0,,0,0,0,,"
                f"{{\\an7\\pos({x0},{y0})\\bord0\\shad0\\1c&H{b:02X}{g:02X}{r:02X}&"
                f"\\1a&H{255 - a:02X}&"
                + (f"\\fad({int(bg.fade_in * 1000)},{int(bg.fade_out * 1000)})" if embed_fades else "")
                + 
                f"\\p1}}m 0 0 l {bw} 0 {bw} {bh} 0 {bh}{{\\p0}}"
            )

        for event_idx, event in enumerate(self.events):
            style_name = style_names.get(event_idx, "Style0")  # Use the style name from our mapping

            if event.animation_mode == AnimationMode.TYPEWRITER and event.text:
                # One dialogue per typed character; the untyped remainder is invisible
                # so the layout (centering) stays stable.
                pos = ""
                margins = "0,0,0"
                if event.area:
                    aw, ah = event.area
                    mh = max((self.width - aw) // 2, 0)
                    margins = f"{mh},{mh},{max((self.height - ah) // 2, 0)}"
                elif event.position != (0, 0):
                    pos = f"\\pos({event.position[0]},{event.position[1]})"
                t0 = event.start_time + event.wait_before / 1000.0
                step = event.typing_speed / 1000.0
                lines = event.text.split("\n")
                n = max(len(l) for l in lines)
                for i in range(1, n + 1):
                    s = t0 + (i - 1) * step
                    e = event.end_time if i == n else t0 + i * step
                    # All lines type in parallel; each keeps its untyped remainder hidden.
                    body = "\\N".join(
                        l[:i] + (f"{{\\alpha&HFF&}}{l[i:]}{{\\alpha&H00&}}" if l[i:] else "")
                        for l in lines
                    )
                    ass_lines.append(
                        f"Dialogue: 1,{self._time_to_ass_format(s)},"
                        f"{self._time_to_ass_format(e)},{style_name},,{margins},,"
                        f"{{\\an{event.alignment}{pos}}}{body}"
                    )
                continue

            if event.animation_mode == AnimationMode.REVEAL and event.frames:
                pos = ""
                margins = "0,0,0"
                if event.area:
                    aw, ah = event.area
                    mh = max((self.width - aw) // 2, 0)
                    margins = f"{mh},{mh},{max((self.height - ah) // 2, 0)}"
                elif event.position != (0, 0):
                    pos = f"\\pos({event.position[0]},{event.position[1]})"
                full = event.text.upper()
                for k, (ms, frame_text, _) in enumerate(event.frames):
                    s = event.start_time + ms / 1000.0
                    e = (
                        event.end_time
                        if k == len(event.frames) - 1
                        else event.start_time + event.frames[k + 1][0] / 1000.0
                    )
                    # Unrevealed letters stay in the layout but are invisible,
                    # so wrapping and centering don't change between frames.
                    body = ""
                    hidden = False
                    for ch_full, ch in zip(full, frame_text):
                        if ch_full == "\n":
                            body += "\\N"
                            continue
                        is_hidden = ch == " " and ch_full != " "
                        if is_hidden != hidden:
                            body += "{\\alpha&HFF&}" if is_hidden else "{\\alpha&H00&}"
                            hidden = is_hidden
                        body += ch_full if is_hidden else ch
                    ass_lines.append(
                        f"Dialogue: 1,{self._time_to_ass_format(s)},"
                        f"{self._time_to_ass_format(e)},{style_name},,{margins},,"
                        f"{{\\an{event.alignment}{pos}}}{body}"
                    )
                continue

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

            if event.animation_mode == AnimationMode.FADE_IN:
                text = f"{{\\fad({event.fade_ms},0)}}{text}"

            # Format text with position if specified
            if event.position != (0, 0):
                pos_x, pos_y = event.position
                text = f"{{\\pos({pos_x},{pos_y})}}{text}"

            # Add alignment
            text = f"{{\\an{event.alignment}}}{text}"

            ass_lines.append(
                f"Dialogue: 0,{start},{end},{style_name},,0,0,0,,{text}"
            )

        return "\n".join(ass_lines)

    def total_duration(self) -> float:
        """End time of the last event or background"""
        ends = [e.end_time for e in self.events] + [b.end_time for b in self.backgrounds]
        return max(ends, default=0.0)

    def save_ass_file(self, filepath: str, embed_fades: bool = True):
        """Save generated ASS content to file.
        embed_fades=False leaves the background at constant opacity (the fades are
        then applied to the alpha channel by VideoProcessor.render_transparent)."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.to_ass_string(embed_fades))
