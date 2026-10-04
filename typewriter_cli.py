#!/usr/bin/env python3
"""
Generate a transparent video (VP9 .webm with alpha, or ProRes 4444 .mov):

    background fades in -> text appears (typewriter or reveal) -> text holds -> background fades out

Example:
    python typewriter_cli.py "HELLO WORLD" -o hello.webm --font Staatliches \
        --font-size 90 --font-color "#FFFF00" --letter-spacing 4 \
        --width 1200 --height 400 --background-rgba 20,20,60,200 \
        --bg-fade-in 1 --hold 2 --bg-fade-out 1
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.text_animator import TextAnimator, TextStyle  # noqa: E402
from src.video_processor import VideoProcessor  # noqa: E402


def parse_rgb(value: str):
    """'#RRGGBB' or 'r,g,b' -> (r, g, b)"""
    value = value.strip()
    if value.startswith("#"):
        value = value[1:]
        if len(value) != 6:
            raise argparse.ArgumentTypeError("expected #RRGGBB")
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    parts = [int(p) for p in value.split(",")]
    if len(parts) != 3 or any(not 0 <= p <= 255 for p in parts):
        raise argparse.ArgumentTypeError("expected r,g,b (0-255) or #RRGGBB")
    return tuple(parts)


def parse_rgba(value: str):
    """'#RRGGBBAA' or 'r,g,b,a' (a: 0-255) -> (r, g, b, a)"""
    value = value.strip()
    if value.startswith("#"):
        h = value[1:]
        if len(h) == 6:
            h += "FF"
        if len(h) != 8:
            raise argparse.ArgumentTypeError("expected #RRGGBBAA")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4, 6))
    parts = [int(p) for p in value.split(",")]
    if len(parts) != 4 or any(not 0 <= p <= 255 for p in parts):
        raise argparse.ArgumentTypeError("expected r,g,b,a (0-255) or #RRGGBBAA")
    return tuple(parts)


def resolve_font(font: str):
    """Return (font family name, font directory or None). Accepts a family name or a font file path."""
    path = Path(font)
    if path.suffix.lower() in (".ttf", ".otf") and path.exists():
        try:
            from PIL import ImageFont

            family = ImageFont.truetype(str(path), 10).getname()[0]
        except Exception:
            family = path.stem
        return family, str(path.parent.resolve())
    for d in (ROOT / "fonts", ROOT / "legacy" / "fonts"):
        if d.is_dir():
            return font, str(d)
    return font, None


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("text", help="Text to type")
    p.add_argument("-o", "--output", default="output/typewriter.mov",
                   help="Output .mov (ProRes 4444 alpha: Premiere/DaVinci/etc.) or .webm (VP9 alpha: browsers/OBS)")
    p.add_argument("--font", default="Staatliches", help="Font family name, or path to a .ttf/.otf file")
    p.add_argument("--font-size", type=int, default=90)
    p.add_argument("--font-color", type=parse_rgb, default=(255, 255, 255), help="#RRGGBB or r,g,b")
    p.add_argument("--letter-spacing", type=float, default=0.0, help="Extra pixels between letters")
    p.add_argument("--width", type=int, default=1200, help="Text area width in px (centered on screen)")
    p.add_argument("--height", type=int, default=400, help="Text area height in px (centered on screen)")
    p.add_argument("--background-rgba", type=parse_rgba, default=(0, 0, 0, 180),
                   help="Text area background: r,g,b,a (a 0-255) or #RRGGBBAA")
    p.add_argument("--bg-fade-in", type=float, default=1.0, help="Seconds: background transparent -> rgba")
    p.add_argument("--hold", type=float, default=1.0, help="Seconds the text stays after being fully typed")
    p.add_argument("--bg-fade-out", type=float, default=1.0,
                   help="Seconds: background rgba -> transparent, after the text disappears")
    p.add_argument("--effect", choices=["typewriter", "reveal"], default="typewriter",
                   help="typewriter: letters appear one after the other; "
                        "reveal: letters resolve from the center outward (like legacy/)")
    p.add_argument("--typing-speed", type=float, default=None,
                   help="typewriter: ms per letter (default 80); reveal: ms per frame (default 110)")
    p.add_argument("--screen-width", type=int, default=1920)
    p.add_argument("--screen-height", type=int, default=1080)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--preview", action="store_true",
                   help="Also write <output>_preview.mp4: the result over a checkerboard, "
                        "viewable in any player (VLC/WMP ignore the alpha of the real output)")
    p.add_argument("--keep-ass", action="store_true", help="Keep the intermediate .ass file next to the output")
    return p


def render_preview(video: Path, preview: Path, width: int, height: int, fps: int, duration: float) -> bool:
    """Composite the transparent video over a checkerboard into a regular opaque mp4."""
    decoder = ["-c:v", "libvpx-vp9"] if video.suffix.lower() == ".webm" else []
    chk = "if(lt(mod(floor(X/40)+floor(Y/40),2),1),136,187)"
    graph = (
        f"color=c=black:s={width}x{height}:r={fps}:d={duration:.3f},format=gbrp,"
        f"geq=r='{chk}':g='{chk}':b='{chk}',format=rgba[bg];"
        "[0:v]format=rgba[fg];"
        "[bg][fg]overlay=shortest=1,format=yuv420p[out]"
    )
    cmd = ["ffmpeg", "-y", "-loglevel", "error", *decoder, "-i", str(video),
           "-filter_complex", graph, "-map", "[out]", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(preview)]
    return subprocess.run(cmd).returncode == 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.width > args.screen_width or args.height > args.screen_height:
        print("error: text area is larger than the screen", file=sys.stderr)
        return 2

    family, font_dir = resolve_font(args.font)
    r, g, b = args.font_color
    style = TextStyle(
        font_name=family,
        font_size=args.font_size,
        color=f"&H00{b:02X}{g:02X}{r:02X}",
        spacing=args.letter_spacing,
        outline_width=0,
        shadow_depth=0,
    )

    raw = args.text.replace("\\n", "\n").replace("\r\n", "\n")
    text = "\n".join(" ".join(l.split()) for l in raw.split("\n"))
    text = text.replace("{", "(").replace("}", ")")

    animator = TextAnimator(args.screen_width, args.screen_height)
    if args.effect == "reveal":
        text_end = animator.add_reveal_text(
            text,
            args.bg_fade_in,
            frame_delay=args.typing_speed or 110,
            style=style,
            hold=args.hold,
            area=(args.width, args.height),
        )
    else:
        text_end = animator.add_typewriter_text(
            text,
            args.bg_fade_in,
            typing_speed=args.typing_speed or 80,
            wait_after=args.hold * 1000,
            style=style,
            area=(args.width, args.height),
        )
    animator.add_background(
        0.0,
        text_end + args.bg_fade_out,
        color=args.background_rgba,
        fade_in=args.bg_fade_in,
        fade_out=args.bg_fade_out,
        rect=(args.width, args.height),
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    ass_file = output.with_suffix(".ass")
    animator.save_ass_file(str(ass_file), embed_fades=False)

    ok = VideoProcessor().render_transparent(
        str(ass_file),
        str(output),
        animator.total_duration(),
        width=args.screen_width,
        height=args.screen_height,
        fps=args.fps,
        font_dir=font_dir,
        fade_in=args.bg_fade_in,
        fade_out=args.bg_fade_out,
    )
    if not args.keep_ass:
        ass_file.unlink(missing_ok=True)
    if not ok:
        print("error: rendering failed", file=sys.stderr)
        return 1
    print(f"Created {output} ({animator.total_duration():.2f}s)")
    if args.preview:
        preview = output.with_name(output.stem + "_preview.mp4")
        if render_preview(output, preview, args.screen_width, args.screen_height, args.fps,
                          animator.total_duration()):
            print(f"Created {preview} (checkerboard preview)")
        else:
            print("warning: preview rendering failed", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
