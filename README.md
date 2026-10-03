# Video Text Type Effect Generator

A Python-based tool to generate dynamic text animations (typewriter, reveal, fade-in effects) for video overlays using FFmpeg and ASS subtitle format.

## Architecture

```
Python → Generate timed ASS/text → FFmpeg ass/overlay → MP4
```

The system uses:
- **Python**: Core animation logic and orchestration
- **ASS (Advanced SubStation Alpha)**: Subtitle format for timed text with styling
- **libass**: LibreOffice ASS renderer (integrated with FFmpeg)
- **FFmpeg**: Video processing and rendering

## Features

### Animation Modes

1. **Typewriter Effect**
   - Sequential character reveal
   - Configurable typing speed
   - Optional wait before/after animation

2. **Reveal Effect**
   - Radial reveal from center (like the legacy webview effect)
   - Probabilistic character appearance with underscores
   - Expandable radius animation

3. **Fade-In Effect**
   - Smooth opacity transition
   - Configurable duration

4. **Marquee Effect**
   - Scrolling text (coming soon)

### Styling Options

- Font name and size
- Bold, italic, underline
- Text color (BGR format)
- Outline and shadow
- Position and alignment

## Installation

### Requirements

- Python 3.8+
- FFmpeg with libass support
- FFprobe (bundled with FFmpeg)

### Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### Verify Installation

```bash
ffmpeg -version
ffprobe -version
```

## Quick Start

### Basic Usage

```python
from src.main import TextVideoGenerator
from src.text_animator import TextStyle

# Create generator
generator = TextVideoGenerator()

# Add typewriter effect
generator.add_typewriter_text("Hello World", start_time=0.5, typing_speed=80)

# Add reveal effect
generator.add_reveal_text("Animated Text", start_time=3.0)

# Generate output video
generator.generate_video(
    input_video="input.mp4",
    output_video="output.mp4",
    font_dir="./legacy/fonts"
)
```

### Advanced Example

```python
from src.text_animator import TextAnimator, TextStyle, AnimationMode

# Create animator
animator = TextAnimator()

# Define custom styles
title_style = TextStyle(
    font_name="Arial",
    font_size=72,
    bold=True,
    color="&H00FFFFFF",  # White (BGR format)
    outline_width=3,
    shadow_depth=2,
)

# Add animations with timing
current_time = 0.5
current_time = animator.add_typewriter_text(
    "TITLE",
    current_time,
    typing_speed=100,
    style=title_style,
    position=(960, 300),
)

# Add pause
current_time += 1.0

# Add another animation
current_time = animator.add_reveal_text(
    "SUBTITLE",
    current_time,
    style=TextStyle(font_size=36),
    position=(960, 400),
)

# Save ASS file
animator.save_ass_file("animation.ass")

# Process video with FFmpeg
from src.video_processor import VideoProcessor
processor = VideoProcessor()
processor.overlay_subtitle(
    "input.mp4",
    "animation.ass",
    "output.mp4",
    font_dir="./legacy/fonts"
)
```

## API Reference

### TextAnimator

Main class for creating text animations.

#### Methods

- `add_typewriter_text(text, start_time, typing_speed=80, wait_before=0, wait_after=0, style=None, position=(0,0), alignment=5) -> float`
  - Adds typewriter effect
  - Returns end time

- `add_reveal_text(text, start_time, frame_delay=110, style=None, position=(0,0), alignment=5) -> float`
  - Adds radial reveal effect
  - Returns end time

- `add_fade_in_text(text, start_time, duration=1.0, style=None, position=(0,0), alignment=5) -> float`
  - Adds fade-in effect
  - Returns end time

- `to_ass_string() -> str`
  - Returns ASS format string

- `save_ass_file(filepath: str)`
  - Saves ASS file

### TextStyle

Configuration for text styling.

#### Attributes

- `font_name: str` - Font family (default: "Arial")
- `font_size: int` - Font size in pixels (default: 48)
- `bold: bool` - Bold text (default: False)
- `italic: bool` - Italic text (default: False)
- `underline: bool` - Underlined text (default: False)
- `color: str` - Text color in BGR hex format (default: "&H00FFFFFF" = white)
- `outline_color: str` - Outline color in BGR hex format
- `outline_width: float` - Outline width in pixels (default: 2.0)
- `shadow_depth: float` - Shadow depth (default: 2.0)
- `shadow_angle: float` - Shadow angle in degrees (default: 45.0)
- `alpha: float` - Transparency (0 = opaque, 1 = transparent, default: 0)

### VideoProcessor

Handles video processing with FFmpeg.

#### Methods

- `overlay_subtitle(input_video, ass_subtitle_file, output_video, font_dir=None, copy_codec=False, preset="medium", crf=23) -> bool`
  - Overlays ASS subtitles on video
  - `preset`: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
  - `crf`: Quality (0-51, lower is better)

- `overlay_subtitle_fast(input_video, ass_subtitle_file, output_video, font_dir=None) -> bool`
  - Fast processing using codec copy

- `overlay_subtitle_hq(input_video, ass_subtitle_file, output_video, font_dir=None, preset="slow") -> bool`
  - High quality with better settings

- `get_video_info(video_path) -> Optional[dict]`
  - Returns video width, height, framerate, duration

### TextVideoGenerator

High-level convenience wrapper.

#### Methods

- `add_typewriter_text(text, start_time, typing_speed=80, style=None, position=(0,0)) -> float`
- `add_reveal_text(text, start_time, style=None, position=(0,0)) -> float`
- `add_fade_in_text(text, start_time, duration=1.0, style=None, position=(0,0)) -> float`
- `generate_video(input_video, output_video, ass_file=None, font_dir=None, preset="medium") -> bool`
- `generate_video_fast(input_video, output_video, ass_file=None, font_dir=None) -> bool`
- `generate_video_hq(input_video, output_video, ass_file=None, font_dir=None) -> bool`

## Color Format (BGR Hex)

ASS format uses BGR (Blue-Green-Red) hexadecimal format, not RGB:

```
Red:   &H0000FF
Green: &H00FF00
Blue:  &H00FF00
White: &H00FFFFFF
Black: &H00000000
Yellow: &H0000FFFF
Cyan:  &H00FFFF00
```

Convert RGB to BGR:
- RGB #FF0000 (Red) → BGR &H0000FF
- RGB #00FF00 (Green) → BGR &H00FF00
- RGB #0000FF (Blue) → BGR &H00FF00

## Timeline Example

```python
animator = TextAnimator()

# Start at 0.5 seconds
t = 0.5

# Typewriter effect: 3 seconds
t = animator.add_typewriter_text("Hello", t, typing_speed=100)  # t = 0.8s

# Pause: 1 second
t += 1.0  # t = 1.8s

# Reveal effect: 2 seconds
t = animator.add_reveal_text("World", t)  # t = ~3.8s

# Fade-in: 2 seconds
t = animator.add_fade_in_text("End", t, duration=2.0)  # t = ~5.8s
```

## ASS File Format

The system generates valid ASS (v4+) subtitle files:

```
[Script Info]
Title: Generated Text Animation

[V4+ Styles]
Format: Name, Fontname, Fontsize, ...
Style: Default,Arial,48,...

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:00:03.80,Default,,0,0,0,,{\a5}Hello World
```

### Position and Alignment

- Position: `{\pos(x,y)}` - Absolute position on screen
- Alignment: `{\a5}` - Numpad alignment (1-9)
  - 1=BotLeft, 2=BotCenter, 3=BotRight
  - 4=MidLeft, 5=MidCenter, 6=MidRight
  - 7=TopLeft, 8=TopCenter, 9=TopRight

## Advanced Features

### Custom Fonts

Place font files (TTF, OTF) in a directory and pass `font_dir`:

```python
processor.overlay_subtitle(
    "input.mp4",
    "animation.ass",
    "output.mp4",
    font_dir="./legacy/fonts"  # Points to DMSans.ttf, Staatliches-Regular.ttf
)
```

### Performance Options

**Fast Processing** (copy codec, minimal re-encoding):
```python
generator.generate_video_fast("input.mp4", "output.mp4")
```

**High Quality** (best quality, slower):
```python
generator.generate_video_hq("input.mp4", "output.mp4")
```

**Balanced** (default):
```python
generator.generate_video("input.mp4", "output.mp4")
```

## Troubleshooting

### FFmpeg Not Found
```
RuntimeError: FFmpeg not found at 'ffmpeg'
```

Solution: Install FFmpeg or provide the correct path:
```python
generator = TextVideoGenerator(ffmpeg_path="/path/to/ffmpeg")
```

### Font Not Found in ASS
- Ensure fonts are in the `font_dir` directory
- Verify font filenames match exactly (case-sensitive on Linux/Mac)
- Use `fc-list` (Linux) or Font Book (macOS) to verify font names

### Subtitle Not Appearing
- Check ASS file format with text editor
- Verify video duration is longer than subtitle end time
- Ensure FFmpeg was compiled with libass support: `ffmpeg -filters | grep subtitles`

### Windows: Video Generation Fails with "Unable to parse option value"
This error occurs when FFmpeg's ass filter cannot parse paths with backslashes.

**Solution**: The library automatically handles this by:
1. Converting backslashes to forward slashes in the filter parameter
2. Using relative paths when possible
3. This is handled transparently in `VideoProcessor.overlay_subtitle()`

If you still encounter this issue:
- Ensure FFmpeg is version 4.0 or later: `ffmpeg -version`
- Check that the ASS file path is correct and the file exists
- Try with absolute paths instead of relative paths

### Poor Quality
- Increase CRF (lower value): use `generate_video_hq()`
- Increase preset quality: pass `preset="slower"` or `preset="veryslow"`
- Check input video resolution and bitrate

## Examples

See `src/main.py` for example usage:

```bash
# Create example ASS file
python src/main.py

# Generate video with text overlays
python src/main.py input.mp4 output.mp4
```

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! Please submit issues and pull requests.

## References

- [ASS Format Specification](https://en.wikipedia.org/wiki/Advanced_SubStation_Alpha)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [libass GitHub](https://github.com/libass/libass)
