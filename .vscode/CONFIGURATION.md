# VS Code Launch Configuration - Complete Reference

## Quick Start (60 seconds)

1. **Ensure FFmpeg is installed:**
   ```bash
   ffmpeg -version
   ```

2. **Press `F5`** in VS Code

3. **Select** "Generate Video from Text"

4. **Type** your text (e.g., "HELLO")

5. **Press Enter** and wait

6. **Check** `output/` folder for your video

Done! 🎉

## Three Launch Configurations

### 1. Generate Video from Text (Interactive)
- **Status**: ✅ Primary configuration
- **Usage**: Press F5 → Select option
- **Input**: User types text in terminal
- **Output**: `output/output_YOUR_TEXT.mp4`
- **Speed**: ~30-60 seconds per video
- **Best for**: Creating custom text videos

**Workflow:**
```
F5 → Select Config → Type Text → Enter → Generated
```

### 2. Generate Video Demo
- **Status**: ✅ Demo/testing
- **Usage**: Press F5 → Select option
- **Input**: None (uses predefined text)
- **Output**: 4 demo videos
  - `demo_typewriter.mp4`
  - `demo_reveal.mp4`
  - `demo_fade.mp4`
  - `demo_multiple.mp4`
- **Best for**: Testing setup, viewing examples

**Workflow:**
```
F5 → Select Config → Auto-generates 4 videos
```

### 3. Quick Video Generator
- **Status**: ✅ Fast mode
- **Usage**: Press F5 → Select option
- **Input**: User types text
- **Output**: `output_YOUR_TEXT.mp4`
- **Speed**: Fastest option
- **Best for**: Quick single-video generation

**Workflow:**
```
F5 → Select Config → Type Text → Enter → Generated
```

## File Structure

### Configuration Files (Edit as needed)
```
.vscode/
├── launch.json              ← Debug configurations (F5)
├── tasks.json               ← Build tasks (Ctrl+Shift+B)
├── settings.json            ← Workspace settings
└── extensions.json          ← Recommended extensions
```

### Python Scripts (Run via F5)
```
.vscode/
├── generate_video_input.py  ← Interactive generator (main)
├── generate_video_demo.py   ← Demo videos generator
└── quick_generator.py       ← Quick single-video
```

### Documentation (Read first!)
```
.vscode/
├── README.md                ← How to use this folder
├── SETUP_GUIDE.md           ← Detailed setup & troubleshooting
└── CONFIGURATION.md         ← This file
```

## Output Locations

### Output Folder
```
output/
├── input_video.mp4          ← Test video (created once)
├── animation.ass            ← ASS animation file
├── output_YOURTEXT.mp4      ← Your generated video
└── demo_*.mp4               ← Demo videos
```

### View Output
1. **In Explorer**: Click `output` folder
2. **Open Folder Task**: Run "Open Output Folder"
3. **Terminal**: `explorer .\output` (Windows)

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| F5 | Open Run & Debug menu |
| Ctrl+Shift+B | Run build task (Generate) |
| Shift+F5 | Stop debug |
| Ctrl+` | Toggle integrated terminal |
| Ctrl+P | Open file |

## Python Scripts Reference

### generate_video_input.py
**Interactive text input generator**

Features:
- Prompts for text input
- Creates test video automatically
- Generates ASS animation file
- Overlays on video with FFmpeg
- Outputs MP4 file

Usage:
```bash
python .vscode/generate_video_input.py
```

Example:
```
Enter text/word: CODING
[INFO] Input text: 'CODING'
[STEP 1] Creating test video...
[STEP 2] Generating ASS animation file...
[STEP 3] Overlaying animation on video...
[SUCCESS] Video output: output_CODING.mp4
```

### generate_video_demo.py
**Generates 4 example videos**

Features:
- No input required
- Generates typewriter example
- Generates reveal example
- Generates fade-in example
- Generates combined effects example

Usage:
```bash
python .vscode/generate_video_demo.py
```

### quick_generator.py
**Fastest single-video generation**

Features:
- Minimal console output
- Quick processing
- Direct feedback
- Optimized for speed

Usage:
```bash
python .vscode/quick_generator.py
```

## Step-by-Step Tutorials

### Tutorial 1: Generate Your First Video

**Goal**: Create a video with text "HELLO WORLD"

**Steps**:
1. Open VS Code
2. Open this project folder
3. Press `F5`
4. Select "Generate Video from Text"
5. Type: `HELLO WORLD`
6. Press Enter
7. Watch the terminal output
8. When done, go to `output/` folder
9. Open `output_HELLO WORLD.mp4`

**Expected Output**:
```
[VIDEO GENERATOR]
[INFO] Input text: 'HELLO WORLD'
[STEP 1] Using existing test video
[STEP 2] Generating ASS animation file
[OK] ASS file created
[STEP 3] Overlaying animation on video
[OK] Video generated
[SUCCESS] Video output: output_HELLO WORLD.mp4
```

### Tutorial 2: Generate Demo Videos

**Goal**: Create all 4 example videos

**Steps**:
1. Press `F5`
2. Select "Generate Video Demo (Fixed Text)"
3. Wait for all videos to generate
4. Check `output/` folder for 4 MP4 files

**Expected Output**:
- `demo_typewriter.mp4` - Characters typing sequentially
- `demo_reveal.mp4` - Characters appearing from center outward
- `demo_fade.mp4` - Text fading in smoothly
- `demo_multiple.mp4` - All effects combined

### Tutorial 3: Batch Generate Multiple Videos

**Goal**: Create 3 videos with different texts

**Steps**:
1. Press `F5` → "Generate Video from Text" → Type "APPLE" → Enter
2. Press `F5` → "Generate Video from Text" → Type "BANANA" → Enter
3. Press `F5` → "Generate Video from Text" → Type "CHERRY" → Enter
4. Check `output/` folder for 3 videos

**Result**:
- `output_APPLE.mp4`
- `output_BANANA.mp4`
- `output_CHERRY.mp4`

## Configuration Details

### launch.json Configurations

```json
{
  "name": "Generate Video from Text",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/.vscode/generate_video_input.py",
  "console": "integratedTerminal"
}
```

**What it does:**
- Runs Python script
- Uses integrated terminal for I/O
- Prompts for text input
- Generates and processes video

### tasks.json Tasks

```json
{
  "label": "Generate Video from Input",
  "type": "shell",
  "command": "python",
  "args": ["${workspaceFolder}/.vscode/generate_video_input.py"],
  "group": { "kind": "build", "isDefault": true }
}
```

**Keyboard Shortcut**: Ctrl+Shift+B
**What it does**: Run build task (alternative to F5)

## System Requirements

### Required
- Python 3.8+
- FFmpeg (system installation)
- VS Code

### Optional
- Python extensions (recommended by project)
- 100MB disk space (for test videos)
- Fast internet (not required, but helpful for initial setup)

## Troubleshooting

### Problem: "No such file or directory: 'ffmpeg'"

**Cause**: FFmpeg not installed or not in PATH

**Solution**:
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Verify
ffmpeg -version
```

### Problem: Text input doesn't work

**Cause**: Terminal not active or Python environment issue

**Solution**:
1. Click in the terminal window
2. Make sure integrated terminal is open (Ctrl+`)
3. Try running script directly: `python .vscode/generate_video_input.py`

### Problem: Video generation takes very long

**Cause**: First-time video creation, or encoding settings

**Solution**:
1. First run creates test video (normal delay)
2. Use "Quick Video Generator" (faster)
3. Use smaller text (fewer characters = faster)

### Problem: Generated video file not found

**Cause**: File saved to wrong location

**Solution**:
1. Check `output/` folder (should be in project root)
2. Search for `*.mp4` in Explorer (Ctrl+P, type ".mp4")
3. Check integrated terminal for error messages

### Problem: Out of disk space

**Cause**: Multiple video generations create large files

**Solution**:
1. Delete `output/input_video.mp4` (test video)
2. Delete old generated videos
3. Run "Clean Output Folder" task

## Advanced Configuration

### Modify Text Style

Edit `generate_video_input.py`:
```python
title_style = TextStyle(
    font_name="Arial",  # Change font
    font_size=72,       # Change size (72 = big)
    bold=True,          # Bold text
    color="&H0000FFFF", # Yellow (BGR format)
    outline_width=3.0,  # Outline thickness
    shadow_depth=2.0,   # Shadow depth
)
```

### Change Animation Speed

Edit `generate_video_input.py`:
```python
animator.add_typewriter_text(
    text.upper(),
    current_time,
    typing_speed=100,   # Change this (ms per char)
    # Lower = faster typing
    # Higher = slower typing
)
```

### Modify Output Quality

Edit `generate_video_input.py`:
```python
processor.overlay_subtitle(
    str(input_video),
    str(ass_file),
    str(output_video),
    preset="fast",  # Options: ultrafast, fast, medium, slow, veryslow
    # Faster = lower quality
    # Slower = higher quality
)
```

## Performance Metrics

| Metric | Value |
|--------|-------|
| First Run | ~15-20 seconds |
| Subsequent Runs | ~5-10 seconds |
| Text Input Lag | < 1 second |
| FFmpeg Encoding | ~5-15 seconds |
| Total Generation | 5-20 seconds |

## Tips & Tricks

1. **Short Text = Faster**: Use 1-5 character text for demos
2. **Reuse Test Video**: First run creates test video, subsequent runs reuse it
3. **Batch Mode**: Run script 3+ times with different text inputs
4. **Check Terminal**: Error messages appear in integrated terminal
5. **Clean Start**: Run "Clean Output Folder" to reset

## File Descriptions

### launch.json (1034 bytes)
VS Code debug configurations. Defines what happens when you press F5.

### tasks.json (2181 bytes)
Build and utility tasks. Defines Ctrl+Shift+B and other commands.

### settings.json (750 bytes)
Workspace settings. Python formatting, editor config, etc.

### extensions.json (230 bytes)
Recommended VS Code extensions to install.

### generate_video_input.py (6.5 KB)
Main interactive generator script. Prompts for text input.

### generate_video_demo.py (4.8 KB)
Demo generator. Creates 4 example videos automatically.

### quick_generator.py (2.9 KB)
Quick single-video generator. Minimal UI, fast output.

### README.md (6.4 KB)
Documentation for this folder. How to use launch configs.

### SETUP_GUIDE.md (7.1 KB)
Detailed setup guide and troubleshooting.

## Next Steps

1. ✅ **Read**: `.vscode/README.md` (overview)
2. ✅ **Setup**: Install FFmpeg (`ffmpeg -version`)
3. ✅ **Test**: Press F5 → "Generate Video from Text" → Type text
4. ✅ **Check**: Open `output/output_YOURTEXT.mp4`
5. ✅ **Experiment**: Try different texts, animation types
6. ✅ **Customize**: Edit colors, speeds, fonts (in Python scripts)

## Quick Reference

### Generate Video
- **Press**: F5
- **Select**: "Generate Video from Text"
- **Type**: Your text
- **Output**: `output/output_YOUR_TEXT.mp4`

### Generate Demos
- **Press**: F5
- **Select**: "Generate Video Demo"
- **Output**: 4 demo MP4 files in `output/`

### Build Task
- **Press**: Ctrl+Shift+B
- **Action**: Same as F5 → Generate Video from Text

### Open Output
- **Run**: "Open Output Folder" task
- **Or**: Click `output/` in Explorer
- **Or**: Terminal: `explorer .\output`

## Support & Documentation

### In This Project
- [README.md](../README.md) - Complete API docs
- [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Cheat sheet
- [GETTING_STARTED.md](../GETTING_STARTED.md) - Installation
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System design

### In .vscode Folder
- [README.md](./README.md) - How to use configs
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Setup & troubleshooting

---

## Summary

This VS Code setup provides **three easy ways** to generate videos from text:

1. **Interactive**: Type text, get video
2. **Demo**: View examples automatically
3. **Quick**: Fastest single-video generation

**All videos are saved locally to `output/` folder.**

**Ready? Press F5! 🚀**
