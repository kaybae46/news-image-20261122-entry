#!/usr/bin/env python3
"""Compose the news-image entry: a newspaper front page for 22 November 2026.

Reads assets/hero.png (a generated editorial illustration of the COP31
summit hall in Antalya) and draws the masthead, date, headlines and
captions for the day's verified top stories with PIL, then writes
entry.png (1024x1024, under 1 MiB). Deterministic: same inputs give
the same bytes on every run.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

PAPER = (247, 242, 231)      # warm newsprint
INK = (20, 20, 20)
RED = (166, 30, 34)
NAVY = (15, 34, 43)          # dark band
AMBER = (232, 178, 90)
MUTED = (74, 72, 66)
DIVIDER = (201, 194, 180)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_row(draw, top, tag, tag_color, headline, caption):
    # Tag chip.
    chip_w, chip_h = 150, 36
    draw.rounded_rectangle([36, top + 24, 36 + chip_w, top + 24 + chip_h],
                           radius=4, fill=tag_color)
    tag_font = font(SANS_B, 19)
    tw = draw.textlength(tag, font=tag_font)
    draw.text((36 + (chip_w - tw) / 2, top + 24 + 8), tag,
              font=tag_font, fill=(255, 255, 255))
    # Headline.
    draw.text((204, top + 12), headline, font=font(SERIF_B, 32), fill=INK)
    # Caption, up to two lines.
    cap_font = font(SANS, 22)
    lines = wrap(draw, caption, cap_font, 1024 - 204 - 36)[:2]
    for i, line in enumerate(lines):
        draw.text((204, top + 52 + i * 25), line, font=cap_font, fill=MUTED)


def main():
    page = Image.new("RGB", (1024, 1024), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead.
    draw.text((36, 18), "THE WORLD IN ONE DAY",
              font=font(SERIF_B, 50), fill=INK)
    draw.text((36, 76), "SUNDAY, 22 NOVEMBER 2026",
              font=font(SANS_B, 27), fill=RED)
    draw.line([(36, 112), (988, 112)], fill=INK, width=3)
    draw.line([(36, 118), (988, 118)], fill=INK, width=1)

    # Hero image, full-bleed, cropped to 1024x400.
    hero = Image.open(os.path.join(
        ASSETS,
        "media-generation-hero-0-0602df9a-1a89-4949-98fc-e27c99b7bd44.png"
    )).convert("RGB")
    hero = hero.resize((1024, 512), Image.LANCZOS)
    hero = hero.crop((0, 56, 1024, 456))
    page.paste(hero, (0, 128))
    draw = ImageDraw.Draw(page)

    # Caption band over the hero's foot.
    draw.rectangle([0, 468, 1024, 528], fill=NAVY)
    draw.text((36, 474), "CLIMATE SUMMIT IN OVERTIME",
              font=font(SANS_B, 27), fill=(255, 255, 255))
    draw.text((36, 504),
              "COP31 talks in Antalya stall over fossil fuels; summit runs into a second extra day",
              font=font(SANS, 21), fill=(220, 220, 220))

    # Four story rows.
    rows = [
        ("CONFLICT", (140, 29, 24), "IRAN STRIKES BAHRAIN",
         "Missile hits an industrial site; Bahrain says civilian property was damaged."),
        ("JUSTICE", (31, 78, 121), "MEXICO CAPTURES \u2018EL CHAPO ISIDRO\u2019",
         "Cartel boss Fausto Isidro Meza Flores, on the FBI\u2019s most-wanted list, arrested in Sinaloa; 11 killed."),
        ("DIPLOMACY", (91, 45, 142), "TRUMP, XI AND PUTIN MEET",
         "Leaders agree in Shenzhen to begin talks on reducing nuclear risks."),
        ("MARKETS", (138, 109, 0), "AI SELL-OFF HITS STOCKS",
         "S&P 500 falls 3.7% and Japan\u2019s Nikkei 5.1% as technology shares slide into correction."),
    ]
    for i, (tag, color, headline, caption) in enumerate(rows):
        top = 528 + i * 100
        if i:
            draw.line([(36, top), (988, top)], fill=DIVIDER, width=1)
        draw_row(draw, top, tag, color, headline, caption)

    # "Also today" band.
    draw.rectangle([0, 928, 1024, 1016], fill=NAVY)
    draw.text((36, 938), "ALSO TODAY", font=font(SANS_B, 20), fill=AMBER)
    draw.text((36, 962),
              "EU\u2013Indonesia sign a trade deal after a decade of talks  \u2022  6.8 quake in the Banda Sea",
              font=font(SANS, 19), fill=(255, 255, 255))
    draw.text((36, 987),
              "Russia strikes Kryvyi Rih; 2 killed  \u2022  Denmark expels a Russian attach\u00e9",
              font=font(SANS, 19), fill=(255, 255, 255))

    # Thin frame.
    draw.rectangle([8, 8, 1016, 1016], outline=INK, width=3)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
