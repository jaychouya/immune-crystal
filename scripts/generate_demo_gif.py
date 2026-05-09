"""Generate assets/demo/immune-crystal-demo.gif (workflow storyboard, ~60s)."""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "demo" / "immune-crystal-demo.gif"
W, H = 1200, 675
BG = "#07111f"
FG = "#e5eefb"
SUB = "#9fb3c8"
ACCENT = "#7dd3fc"
FRAME_MS = 7500


def _fonts(size_title: int, size_sub: int) -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    candidates = [
        os.environ.get("IMMUNE_CRYSTAL_FONT"),
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size_title), ImageFont.truetype(path, size_sub)
            except OSError:
                continue
    return ImageFont.load_default(), ImageFont.load_default()


def _draw_slide(title: str, lines: list[str]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    ft, fs = _fonts(42, 26)
    draw.text((W // 2, 160), title, fill=ACCENT, font=ft, anchor="mm")
    y = 280
    for i, line in enumerate(lines):
        draw.text((W // 2, y), line, fill=FG if i == 0 else SUB, font=fs, anchor="mm")
        y += 44
    draw.text((W // 2, H - 56), "immune-crystal · immune-memory symbiote", fill=SUB, font=fs, anchor="mm")
    return img


def main() -> None:
    slides: list[tuple[str, list[str]]] = [
        (
            "immune-crystal",
            [
                "Enterprise AI Immune-Memory Symbiote",
                "Domain isolation + memory self-repair + audit lineage",
            ],
        ),
        (
            "1 · Bootstrap domains",
            [
                "POST /bootstrap or POST /inject",
                "Register customer_support, engineering, hr …",
            ],
        ),
        (
            "2 · Query with domain",
            [
                "POST /chat with domain = customer_support",
                "Immune layer retrieves B-Cells + crystal weights",
            ],
        ),
        (
            "3 · Cross-domain block",
            [
                "T-Cell detects foreign-sensitive leakage",
                "blocked=true · reason shows cross-domain signal",
            ],
        ),
        (
            "4 · Safe answer path",
            [
                "blocked=false · answer + purity",
                "lineage lists contributing B-Cells",
            ],
        ),
        (
            "5 · Governance APIs",
            [
                "GET /domains · GET /crystal/state · GET /audit",
                "SQLite audit.db + domains.json + cells.json",
            ],
        ),
        (
            "6 · Dashboard (optional)",
            [
                "npm run dev under web/",
                "Oscillation curve + audit stream",
            ],
        ),
        (
            "Ship it",
            [
                "Docker: docker compose up --build",
                "PoC checklist: docs/enterprise-evaluation.md",
            ],
        ),
    ]
    frames = [_draw_slide(t, ls) for t, ls in slides]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {OUT} ({len(frames)} frames, ~{len(frames) * FRAME_MS // 1000}s)")


if __name__ == "__main__":
    main()
