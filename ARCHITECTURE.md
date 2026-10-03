# Architecture and Design

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Video Text Effect Generator                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Python Application Layer                    │   │
│  │                                                          │   │
│  │  ┌─────────────────┐      ┌─────────────────────────┐   │   │
│  │  │   TextAnimator  │      │  TextVideoGenerator    │   │   │
│  │  │                 │      │  (High-level API)      │   │   │
│  │  │ - add_typewriter│─────►│  - add_typewriter_text │   │   │
│  │  │ - add_reveal    │      │  - add_reveal_text     │   │   │
│  │  │ - add_fade_in   │      │  - generate_video*     │   │   │
│  │  │ - to_ass_string │      │                        │   │   │
│  │  │ - save_ass_file │      └─────────────────────────┘   │   │
│  │  └─────────────────┘                                      │   │
│  │           │                                               │   │
│  │           ▼                                               │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │      ASS Subtitle File (.ass)                      │ │   │
│  │  │      [Script Info]                                 │ │   │
│  │  │      [V4+ Styles]                                  │ │   │
│  │  │      [Events]                                      │ │   │
│  │  │      Dialogue: 0,0:00:00.50,0:00:03.80,Default,,.. │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           FFmpeg Integration Layer                      │   │
│  │                                                          │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │   VideoProcessor                                   │ │   │
│  │  │   - overlay_subtitle()                             │ │   │
│  │  │   - overlay_subtitle_fast()                        │ │   │
│  │  │   - overlay_subtitle_hq()                          │ │   │
│  │  │   - get_video_info()                               │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  │           │                                               │   │
│  │           ▼                                               │   │
│  │   FFmpeg Command Line:                                  │   │
│  │   ffmpeg -i input.mp4 \                                │   │
│  │       -vf ass=animation.ass:fontsdir=./fonts \         │   │
│  │       -c:v libx264 -preset medium -crf 23 \           │   │
│  │       output.mp4                                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │      External Dependencies                              │   │
│  │      - FFmpeg (video encoding/rendering)               │   │
│  │      - libass (ASS subtitle renderer)                  │   │
│  │      - FFprobe (video information)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│                   ┌──────────────────┐                          │
│                   │   Output Video   │                          │
│                   │  (MP4 with text  │                          │
│                   │   overlays)      │                          │
│                   └──────────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

## Module Structure

### `text_animator.py`
**Responsible for:** Generating timed ASS subtitle files

**Key Classes:**
- `AnimationMode` (Enum): Animation types
- `TextStyle` (Dataclass): Text styling configuration
- `TextEvent` (Dataclass): Single animation event
- `TextAnimator` (Main): Generates ASS files

**Public Methods:**
- `add_typewriter_text()` - Add typewriter animation
- `add_reveal_text()` - Add radial reveal animation
- `add_fade_in_text()` - Add fade-in animation
- `to_ass_string()` - Generate ASS format string
- `save_ass_file()` - Save to file

**Workflow:**
1. User creates `TextAnimator` instance
2. User calls `add_*_text()` methods to add animations
3. `TextAnimator` maintains list of `TextEvent` objects
4. On `to_ass_string()`, generates ASS format with proper timing
5. On `save_ass_file()`, writes to disk

### `video_processor.py`
**Responsible for:** Video processing with FFmpeg

**Key Class:**
- `VideoProcessor` (Main): Handles FFmpeg operations

**Public Methods:**
- `overlay_subtitle()` - Overlay ASS on video
- `overlay_subtitle_fast()` - Fast processing variant
- `overlay_subtitle_hq()` - High-quality variant
- `get_video_info()` - Retrieve video metadata

**Workflow:**
1. User provides video, ASS file, and output path
2. `VideoProcessor` constructs FFmpeg command
3. Applies ASS filter with optional font directory
4. Executes FFmpeg process
5. Returns success/failure status

### `main.py`
**Responsible for:** High-level API and CLI entry point

**Key Class:**
- `TextVideoGenerator` (Wrapper): Convenience interface

**Purpose:**
- Combines `TextAnimator` and `VideoProcessor`
- Provides simple methods for common tasks
- Handles file management

## Data Flow

### Flow 1: Generate ASS File
```
User Code
   │
   ├─ TextAnimator()
   │
   ├─ add_typewriter_text(...)
   │  └─ Creates TextEvent object
   │     └─ Appends to events list
   │
   ├─ add_reveal_text(...)
   │  └─ Creates TextEvent object
   │     └─ Appends to events list
   │
   ├─ add_fade_in_text(...)
   │  └─ Creates TextEvent object
   │     └─ Appends to events list
   │
   └─ save_ass_file("output.ass")
      ├─ to_ass_string()
      │  ├─ Collect unique styles
      │  ├─ Generate [Script Info]
      │  ├─ Generate [V4+ Styles]
      │  ├─ Generate [Events] with timings
      │  └─ Return ASS format string
      └─ Write to file
```

### Flow 2: Process Video
```
User Code
   │
   ├─ VideoProcessor(ffmpeg_path)
   │  └─ Verify FFmpeg is available
   │
   └─ overlay_subtitle(input.mp4, animation.ass, output.mp4)
      ├─ Validate input files exist
      ├─ Construct FFmpeg command:
      │  ├─ Input: input.mp4
      │  ├─ Filter: -vf ass=animation.ass:fontsdir=...
      │  ├─ Codec: -c:v libx264 -preset X -crf Y
      │  └─ Output: output.mp4
      ├─ Execute subprocess
      └─ Return success status
```

### Flow 3: Complete Pipeline
```
TextVideoGenerator
   │
   ├─ add_typewriter_text("Text", 0.5)
   │  └─ Delegates to animator.add_typewriter_text()
   │
   ├─ generate_video("input.mp4", "output.mp4")
   │  ├─ animator.save_ass_file("animation.ass")
   │  │  └─ Generates ASS file
   │  └─ processor.overlay_subtitle(...)
   │     └─ Processes video with FFmpeg
   │
   └─ Returns success status
```

## ASS File Format

The system generates valid ASS (v4+) files:

```
[Script Info]
Title: Generated Text Animation

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, ...
Style: Default,Arial,48,&H00FFFFFF,&H0000FF00,&H00000000,...

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.50,0:00:03.80,Default,,0,0,0,,{\pos(960,300)}{\a5}Hello World
Dialogue: 0,0:00:03.80,0:00:06.50,Default,,0,0,0,,{\pos(960,400)}{\a5}Subtitle
```

### Timing Format
- Format: `H:MM:SS.CC` (Hours:Minutes:Seconds.Centiseconds)
- Example: `0:00:05.50` = 5 seconds and 50 centiseconds

### Color Format (BGR Hex)
- ASS uses BGR (not RGB)
- Format: `&HBBGGRR`
- Example: `&H0000FF` = Red (not Blue)

### Position and Alignment
- `{\pos(x,y)}` - Absolute screen position
- `{\a5}` - Alignment (numpad 1-9)

## Animation Algorithms

### Typewriter Effect
```
For each character:
  show_time = start_time + (char_index * typing_speed)
  Append character to visible text
  Schedule next character
```

### Reveal Effect (from legacy)
```
center = (text_length - 1) / 2
For each frame:
  radius += 0.45
  For each character:
    distance = abs(char_index - center)
    If distance <= radius:
      Random chance to reveal character
    Else:
      Show space
```

### Fade-in Effect
```
For each frame from 0 to num_frames:
  alpha = 1.0 - (frame / num_frames)  // 1.0 = transparent, 0 = opaque
  Adjust text opacity
```

## Configuration Parameters

### TextStyle
```python
font_name: str              # Font family
font_size: int              # Pixels
bold, italic, underline     # Boolean flags
color: str                  # BGR hex format
outline_color: str          # Border color
outline_width: float        # Border thickness
shadow_depth: float         # Shadow distance
alpha: float                # 0=opaque, 1=transparent
```

### Animation Timing
```python
start_time: float           # When animation begins (seconds)
end_time: float             # When animation ends (seconds)
typing_speed: float         # Milliseconds per character
wait_before: float          # Milliseconds before animation
wait_after: float           # Milliseconds after animation
```

### FFmpeg Options
```python
preset: str                 # ultrafast, superfast, ..., veryslow
crf: int                    # 0-51, lower = better quality
copy_codec: bool            # True = fast (no re-encoding)
font_dir: str               # Directory with TTF/OTF fonts
```

## Performance Considerations

### Fast Processing
- Use `copy_codec=True` to skip video re-encoding
- Fast but subtitle rendering still takes time
- Best for previews

### Balanced Processing
- Standard preset with reasonable CRF
- Moderate re-encoding quality/speed trade-off

### High Quality Processing
- Slower preset, lower CRF value
- Maximum quality but takes longer
- Best for final output

## Error Handling

### FFmpeg Availability
```python
VideoProcessor._check_ffmpeg()
# Raises RuntimeError if FFmpeg not found
```

### File Validation
```python
overlay_subtitle()
# Checks input video exists
# Checks ASS file exists
```

### Process Execution
```python
try:
    subprocess.run(...)
except subprocess.TimeoutExpired:
    # 1 hour timeout
except subprocess.CalledProcessError:
    # Non-zero exit code
```

## Future Enhancements

1. **Animation Interpolation**
   - Smooth transitions between keyframes
   - Motion paths for moving text

2. **Advanced Text Effects**
   - Particle effects
   - Distortion filters
   - Wave effects

3. **Batch Processing**
   - Process multiple videos with same animation
   - Template system for common sequences

4. **Real-time Preview**
   - FFmpeg preview without full encoding
   - Quick feedback on timing

5. **Audio Integration**
   - Synchronize text with audio cues
   - Audio analysis for automatic timing

6. **Video Composition**
   - Multiple video layers
   - Picture-in-picture
   - Video transitions

## Testing Strategy

1. **Unit Tests** (text_animator.py)
   - Test ASS format generation
   - Test timing calculations
   - Test color format handling

2. **Integration Tests** (video_processor.py)
   - Test FFmpeg command construction
   - Test video processing (requires test video)
   - Test metadata extraction

3. **End-to-End Tests**
   - Generate full pipeline
   - Verify output video
   - Check for runtime errors

## Security Considerations

1. **File Path Injection**
   - All paths converted to absolute paths
   - Subprocess called with list (not shell string)

2. **FFmpeg Command Injection**
   - No user input in shell commands
   - All parameters passed as separate arguments

3. **Font Security**
   - Font directory must exist
   - Validated before passing to FFmpeg
