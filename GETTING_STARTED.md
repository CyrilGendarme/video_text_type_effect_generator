# Getting Started Guide

## Installation

### Step 1: Install FFmpeg

FFmpeg must be installed on your system to use this tool.

**Windows:**
```bash
# Using Chocolatey (recommended)
choco install ffmpeg

# Or download from ffmpeg.org
# Add to PATH: C:\ffmpeg\bin (or wherever you installed it)
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
ffprobe -version
```

### Step 2: Clone and Setup

```bash
git clone https://github.com/yourusername/video_text_type_effect_generator.git
cd video_text_type_effect_generator

# Install Python package (optional, for CLI access)
pip install -e .
```

### Step 3: Test Your Installation

```bash
# Run examples to generate ASS files
python examples/basic_examples.py
python examples/advanced_examples.py

# This should create several .ass files in the current directory
```

## Quick Start Examples

### Example 1: Basic Typewriter Effect

Create a simple typewriter animation:

```python
from src.text_animator import TextAnimator

animator = TextAnimator()
animator.add_typewriter_text("Hello World", start_time=0.5, typing_speed=80)
animator.save_ass_file("output.ass")
```

Then overlay it on a video:

```python
from src.video_processor import VideoProcessor

processor = VideoProcessor()
processor.overlay_subtitle("input.mp4", "output.ass", "result.mp4")
```

### Example 2: Using the High-Level API

```python
from src.main import TextVideoGenerator
from src.text_animator import TextStyle

generator = TextVideoGenerator()

# Add text with custom style
style = TextStyle(
    font_name="Arial",
    font_size=48,
    bold=True,
    color="&H00FFFFFF"  # White
)

generator.add_typewriter_text("My Title", 0.5, style=style, position=(960, 300))
generator.add_reveal_text("My Subtitle", 3.0, style=style, position=(960, 400))

# Generate the video
generator.generate_video("input.mp4", "output.mp4")
```

### Example 3: Using the CLI

```bash
# Create an ASS file
python cli.py create-ass animation.ass --type typewriter --text "Hello"

# Overlay on video
python cli.py overlay input.mp4 animation.ass output.mp4 --quality high

# Or generate in one step
python cli.py generate-video input.mp4 animation.ass output.mp4
```

## Common Tasks

### Task 1: Add Multiple Texts with Different Effects

```python
from src.text_animator import TextAnimator, TextStyle

animator = TextAnimator()

# Title - typewriter
current_time = animator.add_typewriter_text("TITLE", 0.5, typing_speed=100)

# Add 1 second pause
current_time += 1.0

# Subtitle - reveal
current_time = animator.add_reveal_text("SUBTITLE", current_time)

# Another pause
current_time += 1.0

# Description - fade in
animator.add_fade_in_text("Description text", current_time, duration=2.0)

animator.save_ass_file("output.ass")
```

### Task 2: Use Custom Fonts

Place your font files (TTF/OTF) in a directory, then:

```python
from src.video_processor import VideoProcessor

processor = VideoProcessor()
processor.overlay_subtitle(
    "input.mp4",
    "animation.ass",
    "output.mp4",
    font_dir="./my_fonts"  # Directory with TTF files
)
```

### Task 3: Generate High-Quality Output

```python
generator = TextVideoGenerator()
generator.add_typewriter_text("Text", 0.5)
generator.generate_video_hq("input.mp4", "output.mp4")
```

### Task 4: Fast Processing

For quick preview or re-encoding:

```python
generator = TextVideoGenerator()
generator.add_typewriter_text("Text", 0.5)
generator.generate_video_fast("input.mp4", "output.mp4")
```

## Understanding Color Format (BGR Hex)

ASS uses BGR (not RGB) hexadecimal format:

| Color | RGB | BGR (ASS) |
|-------|-----|-----------|
| Red | #FF0000 | &H0000FF |
| Green | #00FF00 | &H00FF00 |
| Blue | #0000FF | &H00FF00 |
| White | #FFFFFF | &H00FFFFFF |
| Black | #000000 | &H00000000 |
| Yellow | #FFFF00 | &H0000FFFF |
| Cyan | #00FFFF | &H00FFFF00 |
| Magenta | #FF00FF | &H00FF00FF |

**Conversion:** Swap the first and last 2 digits of RGB hex.

```python
from src.text_animator import TextStyle

# Use BGR format
style = TextStyle(
    color="&H0000FFFF"  # Yellow (BGR) = #FFFF00 (RGB)
)
```

## Understanding Positions and Alignment

Text position in video (assuming 1920x1080):

```python
# Alignment uses numpad positions:
# 7 (TopLeft)    8 (TopCenter)    9 (TopRight)
# 4 (MidLeft)    5 (MidCenter)    6 (MidRight)
# 1 (BotLeft)    2 (BotCenter)    3 (BotRight)

animator.add_typewriter_text(
    "Text",
    0.5,
    position=(960, 300),  # (x, y) coordinates
    alignment=5  # Center alignment
)
```

## Troubleshooting

### Problem: "FFmpeg not found"

```
RuntimeError: FFmpeg not found at 'ffmpeg'
```

**Solution:** Ensure FFmpeg is installed and in your PATH:
- Windows: Add C:\ffmpeg\bin to PATH
- macOS/Linux: Run `which ffmpeg` to verify location

### Problem: Windows - "Unable to parse option value" or Filter Error

```
[Parsed_ass_0] Unable to parse option value as image size
Error applying option 'original_size' to filter 'ass': Invalid argument
```

**Solution:** This is a Windows-specific issue with path handling in FFmpeg's ass filter.

The library automatically handles this by:
1. Converting Windows backslashes to forward slashes in filter parameters
2. Using relative paths when possible
3. This ensures compatibility with FFmpeg's filter syntax

**If you still encounter this:**
- Update FFmpeg to version 4.0 or later: `ffmpeg -version`
- Verify the ASS file exists: `dir output\animation.ass`
- Try with shorter file paths (avoid very long directory names)
- Check that no special characters are in the path

### Problem: Font not found in output

The font name in ASS might not match the system font name.

**Solutions:**
1. Use standard fonts: Arial, Times New Roman, Courier New
2. Provide fonts in a directory: `font_dir="./fonts"`
3. On Linux/Mac: use `fc-list` to find installed fonts
4. Verify font filename matches font name in ASS

### Problem: Text appears but animation is static

Make sure you're using the correct timing. Verify:
1. ASS file was generated correctly (check with text editor)
2. Video duration is longer than animation end time
3. Text has actual content and isn't just whitespace

### Problem: Poor output quality

Try high-quality settings:

```python
generator.generate_video_hq(
    "input.mp4",
    "output.mp4",
    preset="slower"
)
```

Or manually adjust:

```python
processor.overlay_subtitle(
    "input.mp4",
    "animation.ass",
    "output.mp4",
    preset="veryslow",  # Better quality
    crf=18  # Lower CRF = better quality (but larger file)
)
```

## Next Steps

1. **Try the examples:**
   ```bash
   python examples/basic_examples.py
   python examples/advanced_examples.py
   ```

2. **Read the API documentation:** See README.md

3. **Explore advanced features:**
   - Multiple animation layers
   - Custom timing sequences
   - Different animation modes

4. **Create your own project:**
   - Start with `cli.py` for quick commands
   - Use `main.py` for more control
   - Use `text_animator.py` for maximum flexibility

## Resources

- [ASS Format Specification](https://en.wikipedia.org/wiki/Advanced_SubStation_Alpha)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FFmpeg ASS Filter](https://ffmpeg.org/ffmpeg-filters.html#ass-1)
- [libass GitHub](https://github.com/libass/libass)

## Getting Help

1. Check existing examples in `examples/`
2. Read the API documentation in README.md
3. Review generated ASS files (plain text format)
4. Enable logging for debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
