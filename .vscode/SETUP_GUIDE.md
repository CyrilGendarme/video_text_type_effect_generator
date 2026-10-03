# VS Code Launch Configuration - Setup Guide

## Overview

This guide explains how to use the VS Code launch configurations to generate videos from text input locally.

## Prerequisites

### 1. FFmpeg Installation (Required)

**Windows:**
```bash
choco install ffmpeg
# Or download from https://ffmpeg.org/download.html
# Then add to PATH
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
ffprobe -version
```

### 2. VS Code Extensions (Recommended)

VS Code will suggest installing recommended extensions when you open the project. Recommended:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Python Debugger (ms-python.debugpy)

## Configuration Files

### launch.json
Defines three run configurations:
1. **Generate Video from Text** - Interactive, prompts for user input
2. **Generate Video Demo** - Generates 4 example videos
3. **Quick Video Generator** - Fast, minimal UI

### tasks.json
Defines build and utility tasks:
- Generate Video from Input (Ctrl+Shift+B)
- Generate Demo Video
- Open Output Folder
- Clean Output Folder

### settings.json
Workspace-level settings:
- Python formatting and linting
- Editor configuration
- Excluded folders for search/watch

### extensions.json
Lists recommended VS Code extensions

## How to Use

### Method 1: Launch with Text Input (F5)

**Steps:**
1. Open the project in VS Code
2. Press `F5` to open Run and Debug
3. Select "Generate Video from Text"
4. Type your text in the integrated terminal (e.g., "HELLO WORLD")
5. Watch the generation progress
6. Check the `output/` folder for your video

**What happens:**
- Creates a test video if it doesn't exist
- Generates an ASS animation file
- Overlays the animation on the video
- Outputs `output_YOUR_TEXT.mp4`

### Method 2: Generate Demo Videos (F5)

**Steps:**
1. Press `F5` to open Run and Debug
2. Select "Generate Video Demo (Fixed Text)"
3. Watch 4 example videos generate automatically
4. Check `output/` folder for:
   - `demo_typewriter.mp4`
   - `demo_reveal.mp4`
   - `demo_fade.mp4`
   - `demo_multiple.mp4`

### Method 3: Quick Generator (F5)

**Steps:**
1. Press `F5` to open Run and Debug
2. Select "Quick Video Generator"
3. Type your text
4. Instant video generation with minimal output

## Output Location

All generated files go to:
```
video_text_type_effect_generator/
└── output/
    ├── input_video.mp4         # Test video (created once)
    ├── animation.ass           # ASS subtitle file
    ├── output_YOURTEXT.mp4     # Final video
    └── demo_*.mp4              # Demo videos
```

## Folder Structure

```
.vscode/
├── launch.json                 # Run configurations
├── tasks.json                  # Build tasks
├── settings.json              # Workspace settings
├── extensions.json            # Recommended extensions
├── README.md                  # This folder's README
├── generate_video_input.py    # Interactive generator
├── generate_video_demo.py     # Demo video generator
└── quick_generator.py         # Quick generator
```

## Example Workflows

### Workflow 1: Generate Single Video from Text

```
1. Press F5
   ↓
2. Select "Generate Video from Text"
   ↓
3. Type: "AMAZING"
   ↓
4. Wait for generation
   ↓
5. Video: output/output_AMAZING.mp4
```

### Workflow 2: Test All Animation Types

```
1. Press F5
   ↓
2. Select "Generate Video Demo (Fixed Text)"
   ↓
3. Wait for 4 videos to generate
   ↓
4. Videos: demo_typewriter.mp4, demo_reveal.mp4, etc.
```

### Workflow 3: Batch Video Generation

```
1. Press F5 → "Generate Video from Text" → "HELLO"
   ↓
2. Press F5 → "Generate Video from Text" → "WORLD"
   ↓
3. Press F5 → "Generate Video from Text" → "CODING"
   ↓
4. Videos: output_HELLO.mp4, output_WORLD.mp4, output_CODING.mp4
```

## Troubleshooting

### Issue: "FFmpeg not found"

**Solution:**
1. Install FFmpeg:
   - Windows: `choco install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
2. Restart VS Code
3. Try again

**Verify:**
```bash
ffmpeg -version
ffprobe -version
```

### Issue: Video generation fails silently

**Solution:**
1. Check the integrated terminal for error messages
2. Verify FFmpeg is installed and in PATH
3. Check disk space is available
4. Try the "Generate Demo Video" to test setup

### Issue: Output folder not visible

**Solution:**
1. Run Ctrl+Shift+B to generate
2. Click on "output" folder in Explorer
3. Or run "Open Output Folder" task
4. Explorer → File → Refresh (F5)

### Issue: Videos are very large files

**Solution:**
- Use "Quick Video Generator" (faster, smaller)
- This is normal for first run (creates 10-second test video)
- Subsequent generations are faster
- Delete `output/input_video.mp4` to recreate smaller version

## Advanced Usage

### Custom Text Input Script

Edit `generate_video_input.py` to modify:
- Default text
- Animation speeds
- Colors
- Positions
- Text styles

### Add New Launch Configuration

1. Open `.vscode/launch.json`
2. Add new configuration:
```json
{
  "name": "My Config",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/.vscode/my_script.py",
  "console": "integratedTerminal"
}
```

### Add New Task

1. Open `.vscode/tasks.json`
2. Add new task:
```json
{
  "label": "My Task",
  "type": "shell",
  "command": "python",
  "args": ["my_script.py"]
}
```

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Run Debug (F5 menu) | F5 |
| Build Task (Generate) | Ctrl+Shift+B |
| Stop Debug | Shift+F5 |
| Toggle Terminal | Ctrl+` |
| Open File | Ctrl+P |
| Search | Ctrl+Shift+F |

## Performance Tips

1. **First Run**: Takes longer (creates test video)
2. **Reuse Test Video**: Subsequent runs reuse test video
3. **Fast Mode**: Use "Quick Video Generator" preset
4. **Batch Mode**: Run multiple times for multiple videos
5. **Cleanup**: Run "Clean Output Folder" task to remove all files

## File Size Expectations

| File | Size |
|------|------|
| Test Video (10s) | ~18 KB (ultra-fast) |
| ASS Subtitle | ~1 KB |
| Output Video (10s) | 2-5 MB (depends on encoding) |

## Next Steps

1. ✅ Set up FFmpeg
2. ✅ Press F5 and try "Generate Video from Text"
3. ✅ Enter your first text
4. ✅ Check output folder for video
5. ✅ Open video in media player
6. ✅ Experiment with different texts

## Getting Help

- **Configuration Help**: See `.vscode/README.md`
- **API Documentation**: See `README.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`
- **Getting Started**: See `GETTING_STARTED.md`

## Architecture

```
VS Code Launch Config
       ↓
  Python Script
       ↓
  TextAnimator (generates ASS)
       ↓
  VideoProcessor (calls FFmpeg)
       ↓
  FFmpeg + libass (renders video)
       ↓
  Output Video (MP4)
```

---

**Ready to generate your first video? Press F5!**
