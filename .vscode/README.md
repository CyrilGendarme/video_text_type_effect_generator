# VS Code Launch Configuration

This folder contains VS Code configuration for the Video Text Effect Generator project.

## Quick Start

### Option 1: Interactive Text Input (Recommended)
Press `F5` and select "Generate Video from Text"
- Prompts you to enter text/word
- Generates ASS animation file
- Creates MP4 video with animation overlay
- Outputs to `./output/` folder

### Option 2: Demo Videos
Press `F5` and select "Generate Video Demo (Fixed Text)"
- Generates 4 example videos automatically
- No input required
- Shows different animation types
- Outputs to `./output/` folder

### Option 3: Quick Generator
Press `F5` and select "Quick Video Generator"
- Fastest way to generate a video
- Minimal UI, instant feedback
- Outputs to `./output/` folder

## Files

### Launch Configurations (launch.json)

**Generate Video from Text**
- Takes user text input
- Creates animation ASS file
- Overlays on video
- Outputs MP4 with embedded animation

**Generate Video Demo (Fixed Text)**
- Uses predefined text
- No user interaction
- Perfect for testing

**Quick Video Generator**
- Single-step generation
- Fast feedback
- Minimal output messages

### Tasks (tasks.json)

**Generate Video from Input**
- Primary build task (Ctrl+Shift+B)
- Runs the interactive generator

**Generate Demo Video**
- Generates example videos
- Useful for testing functionality

**Open Output Folder**
- Opens the output directory
- Platform-specific (Windows/macOS/Linux)

**Clean Output Folder**
- Removes all generated files
- Useful before starting fresh

## Workflow

### Generate Your First Video

1. **Press F5** to open Run and Debug menu
2. **Select "Generate Video from Text"**
3. **Type your text** in the terminal (e.g., "HELLO WORLD")
4. **Wait** for video generation to complete
5. **Check output** in `./output/` folder

### Output Files

Generated files are saved to:
```
video_text_type_effect_generator/
└── output/
    ├── input_video.mp4         (Test video)
    ├── animation.ass           (ASS subtitle file)
    └── output_YOUR_TEXT.mp4    (Final video with animation)
```

### Check Your Video

Once generated, your video appears in VS Code Explorer:
- Navigate to `output/` in Explorer
- Right-click video file
- Select "Open with External Program"
- Or use "Open Output Folder" task

## Configuration

### settings.json
Contains VS Code workspace settings:
- Python linting with flake8
- Black code formatting
- Excluded folders (pycache, output)
- Editor configuration

### launch.json
Three launch configurations available:
- All configurations use Python interpreter
- Integrated terminal for output
- Console feedback enabled

### tasks.json
Build and utility tasks:
- Shell-based execution
- Platform-specific commands
- Custom presentation options

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Start Debug | F5 |
| Build (Generate) | Ctrl+Shift+B |
| Stop Debug | Shift+F5 |
| Terminal | Ctrl+` |
| Search | Ctrl+Shift+F |

## Troubleshooting

### "FFmpeg not found"
- Install FFmpeg: `choco install ffmpeg` (Windows)
- Verify: `ffmpeg -version` in terminal
- Restart VS Code after installation

### Video generation is slow
- First run creates test video (5-10 seconds)
- Use "Quick Video Generator" for faster results
- Use "Generate Video Demo" for testing

### Output folder not created
- The output folder is created automatically
- Check the terminal for error messages
- Verify disk space is available

### Cannot find generated video
- Check `output/` folder in Explorer
- Videos are prefixed with `output_` or `demo_`
- File search: Ctrl+P, type ".mp4"

## Development

### Adding New Launch Configuration

Edit `launch.json`:
```json
{
  "name": "My Custom Config",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/.vscode/my_script.py",
  "console": "integratedTerminal"
}
```

### Adding New Task

Edit `tasks.json`:
```json
{
  "label": "My Custom Task",
  "type": "shell",
  "command": "python",
  "args": ["my_script.py"]
}
```

## Python Scripts

### generate_video_input.py
- Interactive user input
- Creates test video if needed
- Generates ASS file
- Processes video with FFmpeg
- Outputs MP4 with animation

### generate_video_demo.py
- Generates 4 demo videos
- Typewriter effect
- Reveal effect
- Fade-in effect
- Combined effects

### quick_generator.py
- Single-step generation
- Minimal output
- Fastest workflow
- Best for quick testing

## Examples

### Generate "CODING" Video
1. Press F5 → "Generate Video from Text"
2. Type: `CODING`
3. Watch generation progress
4. Video saved to: `output/output_CODING.mp4`

### Generate Demo Videos
1. Press F5 → "Generate Video Demo (Fixed Text)"
2. Watch all 4 demos generate
3. Check `output/` folder for:
   - `demo_typewriter.mp4`
   - `demo_reveal.mp4`
   - `demo_fade.mp4`
   - `demo_multiple.mp4`

### Quick Test
1. Press F5 → "Quick Video Generator"
2. Type: `TEST`
3. Instant video generation
4. Minimal console output

## Tips & Tricks

1. **Batch Generation**: Generate multiple videos by running the script multiple times
2. **Custom Text**: Try short words (1-5 chars) for best visual effect
3. **Long Text**: Limited to 50 characters (configurable in script)
4. **Test Video**: Created once, reused for all subsequent videos
5. **Clean Start**: Run "Clean Output Folder" task before major tests
6. **Debug Mode**: Add breakpoints in Python scripts for debugging

## Performance Tips

- First run takes longer (creates test video)
- Subsequent runs are faster (reuse test video)
- Use "Quick Video Generator" for fastest results
- "Demo Video" shows all animation types

## Next Steps

1. ✓ Run your first video generation
2. ✓ Check the output folder
3. ✓ Experiment with different text inputs
4. ✓ Try different animation types
5. ✓ Customize colors and fonts (see main project documentation)

---

For more information, see:
- [README.md](../README.md) - Full API documentation
- [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Quick lookup guide
- [GETTING_STARTED.md](../GETTING_STARTED.md) - Installation & tutorials
