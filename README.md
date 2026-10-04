# Video Text Type Effect Generator

Generates a transparent overlay video (ProRes 4444 `.mov`, or VP9 `.webm`) with:

1. a background that fades from transparent to an RGBA colour,
2. text appearing with a `typewriter` or `reveal` effect (all lines animate in parallel, `\n` = new line),
3. the text holding for a while, then the background fading back to transparent.

Requires Python 3 and FFmpeg in the PATH. Fonts are looked up in `fonts/`.

## Example

```
python typewriter_cli.py "HELLO WORLD HELLO WORLD\nHELLO WORLD HELLO\nWORLD" -o output\hello4.mov --font Staatliches --font-size 160 --font-color "#FFFFFF" --letter-spacing 6 --width 1920 --height 1080 --background-rgba 0,0,0,200 --bg-fade-in 1 --hold 5 --bg-fade-out 1 --effect reveal
```

| Option | Meaning |
|---|---|
| `-o` | Output file (`.mov` recommended for video editors, or `.webm`) |
| `--font`, `--font-size`, `--font-color`, `--letter-spacing` | Text style |
| `--width`, `--height` | Size of the centred text area / background box |
| `--background-rgba` | `r,g,b,a` (0-255) or `#RRGGBBAA` |
| `--bg-fade-in` | Seconds, transparent to background colour, before the text |
| `--hold` | Seconds the text stays once fully displayed |
| `--bg-fade-out` | Seconds, background to transparent, after the text |
| `--effect` | `typewriter` (default) or `reveal` |
| `--typing-speed` | Milliseconds per step (optional) |
| `--preview` | Also write a checkerboard `.mp4` preview |
