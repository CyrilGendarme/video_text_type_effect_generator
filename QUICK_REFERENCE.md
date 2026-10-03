# Quick Reference Guide

## Installation

```bash
# Install FFmpeg
choco install ffmpeg           # Windows
brew install ffmpeg            # macOS
sudo apt-get install ffmpeg    # Linux

# Verify
ffmpeg -version
ffprobe -version
```

## Core Modules

| Module | Purpose | Main Class |
|--------|---------|------------|
| `src/text_animator.py` | Generate ASS subtitle files | `TextAnimator` |
| `src/video_processor.py` | Process video with FFmpeg | `VideoProcessor` |
| `src/main.py` | High-level API | `TextVideoGenerator` |
| `cli.py` | Command-line interface | `main()` |

## Basic Usage Pattern

```python
from src.text_animator import TextAnimator

# Create animator
animator = TextAnimator()

# Add animations
animator.add_typewriter_text("Text", 0.5, typing_speed=80)
animator.add_reveal_text("Text", 3.0)
animator.add_fade_in_text("Text", 5.0, duration=2.0)

# Save ASS file
animator.save_ass_file("output.ass")
```

## Processing Video

```python
from src.video_processor import VideoProcessor

processor = VideoProcessor()
success = processor.overlay_subtitle(
    "input.mp4",
    "output.ass",
    "result.mp4",
    font_dir="./fonts"
)
```

## CLI Commands

```bash
# Create ASS file
python cli.py create-ass output.ass --type typewriter --text "Hello"

# Overlay on video
python cli.py overlay input.mp4 output.ass result.mp4

# Get video info
python cli.py info input.mp4

# One-step generation
python cli.py generate-video input.mp4 output.ass result.mp4 --quality high
```

## TextStyle Properties

```python
TextStyle(
    font_name="Arial",
    font_size=48,
    bold=True,
    italic=False,
    underline=False,
    color="&H00FFFFFF",        # BGR format (white)
    outline_color="&H00000000", # Black
    outline_width=2.0,
    shadow_depth=2.0,
    shadow_angle=45.0,
    alpha=0.0                   # 0=opaque, 1=transparent
)
```

## Animation Methods

### Typewriter
```python
end_time = animator.add_typewriter_text(
    "Text",
    start_time=0.5,
    typing_speed=80,            # ms per character
    wait_before=0,              # ms before animation
    wait_after=0,               # ms after animation
    style=TextStyle(),
    position=(960, 300),        # (x, y) coordinates
    alignment=5                 # 1-9 numpad
)
```

### Reveal (Radial from center)
```python
end_time = animator.add_reveal_text(
    "Text",
    start_time=0.5,
    frame_delay=110,            # ms between frames
    style=TextStyle(),
    position=(960, 300),
    alignment=5
)
```

### Fade-In
```python
end_time = animator.add_fade_in_text(
    "Text",
    start_time=0.5,
    duration=1.0,               # seconds
    style=TextStyle(),
    position=(960, 300),
    alignment=5
)
```

## Color Reference (BGR Format)

| Color | BGR Format | RGB Equivalent |
|-------|-----------|-----------------|
| White | &H00FFFFFF | #FFFFFF |
| Black | &H00000000 | #000000 |
| Red | &H0000FF | #FF0000 |
| Green | &H0000FF00 | #00FF00 |
| Blue | &H00FF00FF | #0000FF |
| Yellow | &H0000FFFF | #FFFF00 |
| Cyan | &H00FFFF00 | #00FFFF |
| Magenta | &H00FF00FF | #FF00FF |

## Position and Alignment

```
Numpad Alignment:
7 (TopLeft)    8 (TopCenter)    9 (TopRight)
4 (MidLeft)    5 (MidCenter)    6 (MidRight)
1 (BotLeft)    2 (BotCenter)    3 (BotRight)

Position: (x, y) pixels from top-left corner
1920x1080 video:
  - Center: (960, 540)
  - Top-left: (0, 0)
  - Bottom-right: (1920, 1080)
```

## FFmpeg Quality Options

```python
# Fast (preview)
processor.overlay_subtitle_fast(...)

# Balanced (default)
processor.overlay_subtitle(
    ...,
    preset="medium",
    crf=23
)

# High quality
processor.overlay_subtitle_hq(
    ...,
    preset="slow"
)

# Custom quality
processor.overlay_subtitle(
    ...,
    preset="veryslow",  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    crf=18              # 0-51, lower = better (0=best, 51=worst)
)
```

## Timeline Control

```python
animator = TextAnimator()
t = 0.5  # Start at 0.5 seconds

# Add animation and get end time
t = animator.add_typewriter_text("First", t, typing_speed=100)  # ~1 sec

# Add pause
t += 1.0

# Add next animation
t = animator.add_reveal_text("Second", t)  # ~2 sec

# Another pause
t += 0.5

# Final animation
t = animator.add_fade_in_text("Third", t, duration=2.0)

print(f"Total animation duration: {t} seconds")
```

## Common Patterns

### Sequential Animations
```python
t = 0.5
t = animator.add_typewriter_text("Title", t, typing_speed=80)
t += 1.0  # Pause
t = animator.add_typewriter_text("Subtitle", t, typing_speed=60)
```

### Multiple Layers
```python
# Different positions on same screen
animator.add_typewriter_text("Top", 0.5, position=(960, 200))
animator.add_typewriter_text("Middle", 2.0, position=(960, 540))
animator.add_typewriter_text("Bottom", 4.0, position=(960, 880))
```

### Custom Colors
```python
red_style = TextStyle(color="&H0000FF")
green_style = TextStyle(color="&H0000FF00")
blue_style = TextStyle(color="&H00FF00FF")

animator.add_typewriter_text("Red", 0.5, style=red_style)
animator.add_typewriter_text("Green", 2.0, style=green_style)
animator.add_typewriter_text("Blue", 4.0, style=blue_style)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| FFmpeg not found | Install FFmpeg, add to PATH |
| Font not found | Provide `font_dir` parameter |
| Text not appearing | Check video duration > animation duration |
| Poor quality | Use `generate_video_hq()` |
| Slow encoding | Use `generate_video_fast()` |

## File Structure

```
video_text_type_effect_generator/
├── src/
│   ├── __init__.py
│   ├── text_animator.py          # ASS file generation
│   ├── video_processor.py         # FFmpeg video processing
│   └── main.py                    # High-level API
├── examples/
│   ├── basic_examples.py          # Simple examples
│   └── advanced_examples.py       # Complex examples
├── cli.py                         # Command-line interface
├── README.md                      # Full documentation
├── GETTING_STARTED.md             # Installation & quick start
├── ARCHITECTURE.md                # System design
├── QUICK_REFERENCE.md             # This file
└── requirements.txt               # Dependencies
```

## Performance Tips

1. **Use `copy_codec=True`** for quick previews
2. **Lower CRF** for better quality (slower)
3. **Faster preset** for quicker encoding (worse quality)
4. **Place text centrally** to avoid edge artifacts
5. **Test with short videos** first

## Examples

```bash
# Generate basic ASS file
python examples/basic_examples.py

# Generate advanced animations
python examples/advanced_examples.py

# View generated files
cat example_typewriter.ass
cat example_reveal.ass
cat example_multiple.ass
```
