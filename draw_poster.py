#!/usr/bin/env python3
"""Draw the Monday 23 November 2026 world-news poster.

Reads nothing from disk except the DejaVu fonts, needs no network and
uses no randomness, so every run paints the same pixels. The finished
1024x1024 picture is written to entry.png beside this file with a plain
open() call, then chmod 0644, so any other user on the machine can read
it afterwards.

Layout: masthead, one lead story, six story cards in two columns, a
sport strip, an "also today" strip and a markets strip.
"""

import hashlib
import io
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_NAME = "entry.png"
SIZE = (1024, 1024)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
PLAIN = os.path.join(FONT_DIR, "DejaVuSans.ttf")

NAVY_TOP = (8, 20, 38)
NAVY_BOTTOM = (12, 39, 78)
CARD = (17, 42, 82)
CARD_ALT = (15, 37, 71)
LEAD_CARD = (19, 44, 85)
EDGE = (42, 74, 122)
WHITE = (255, 255, 255)
SOFT = (201, 214, 236)
MUTED = (138, 160, 196)
GOLD = (201, 162, 39)
RED = (229, 72, 77)
AMBER = (245, 166, 35)
CYAN = (56, 189, 248)
GREEN = (52, 199, 123)
ORANGE = (249, 115, 22)
PURPLE = (176, 124, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_background(img):
    draw = ImageDraw.Draw(img)
    top = NAVY_TOP
    bottom = NAVY_BOTTOM
    height = img.height
    for y in range(height):
        t = y / max(height - 1, 1)
        colour = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (img.width, y)], fill=colour)
    return draw


def story_card(draw, x, y, w, h, accent, tag, headline, body, alt=False):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD_ALT if alt else CARD, outline=EDGE, width=1)
    draw.rectangle([x, y + 10, x + 6, y + h - 10], fill=accent)
    tag_font = font(BOLD, 19)
    head_font = font(BOLD, 27)
    body_font = font(PLAIN, 19)
    inner = x + 20
    text_w = w - 40
    draw.text((inner, y + 12), tag, font=tag_font, fill=accent)
    head_lines = wrap(draw, headline, head_font, text_w)[:2]
    line_y = y + 40
    for line in head_lines:
        draw.text((inner, line_y), line, font=head_font, fill=WHITE)
        line_y += 31
    body_lines = wrap(draw, body, body_font, text_w)[:2]
    line_y += 4
    for line in body_lines:
        draw.text((inner, line_y), line, font=body_font, fill=SOFT)
        line_y += 23


def build():
    img = Image.new("RGB", SIZE)
    draw = paint_background(img)

    # Masthead.
    title_font = font(BOLD, 62)
    date_font = font(BOLD, 25)
    title = "WORLD NEWS TODAY"
    title_w = draw.textlength(title, font=title_font)
    draw.text(((SIZE[0] - title_w) / 2, 22), title, font=title_font, fill=WHITE)
    dateline = "MONDAY, 23 NOVEMBER 2026  ·  THE DAY IN EIGHT STORIES"
    date_w = draw.textlength(dateline, font=date_font)
    draw.text(((SIZE[0] - date_w) / 2, 96), dateline, font=date_font, fill=GOLD)
    draw.line([(32, 132), (992, 132)], fill=GOLD, width=3)

    # Lead story: COP31.
    draw.rounded_rectangle([32, 148, 992, 276], radius=10, fill=LEAD_CARD,
                           outline=EDGE, width=1)
    draw.rectangle([32, 158, 40, 266], fill=AMBER)
    draw.text((56, 160), "CLIMATE  ·  ANTALYA, TURKEY", font=font(BOLD, 21), fill=AMBER)
    draw.text((56, 186), "COP31 COLLAPSES WITHOUT A DEAL",
              font=font(BOLD, 40), fill=WHITE)
    sub = ("EU and about 130 nations reject the final text with no "
           "fossil-fuel phase-out, after two days of overtime talks.")
    sub_lines = wrap(draw, sub, font(PLAIN, 22), 920)[:2]
    sub_y = 232
    for line in sub_lines:
        draw.text((56, sub_y), line, font=font(PLAIN, 22), fill=SOFT)
        sub_y += 26

    # Six story cards.
    cards = [
        (RED, "WAR  ·  KYIV REGION",
         "Russian strikes kill at least 11 in Kyiv region",
         "Teenager among the dead in Dymer; a 7-year-old pulled alive from rubble."),
        (CYAN, "POLITICS  ·  WASHINGTON",
         "Democrats clinch the House with 258 seats",
         "Largest House majority since 1992, AP projects."),
        (ORANGE, "CONFLICT  ·  THE GULF",
         "Trump 'inclined' to resume war with Iran",
         "Warns of new conflict if no deal by New Year; Tehran says it downed a US drone."),
        (PURPLE, "WAR  ·  LIBYA & THE BALTIC",
         "Ukraine sea drone sinks Russian warship",
         "Corvette hit off Benghazi; Russian cargo ship left ablaze in the Baltic."),
        (AMBER, "DISASTER  ·  INDONESIA",
         "Factory fire kills at least 24 in Banten",
         "Candy-plant blaze leaves about 30 people unaccounted for."),
        (GREEN, "TRAVEL  ·  ATLANTA",
         "Delta delays 1,000+ flights at its hub",
         "Technical failure hits Atlanta as Thanksgiving travel begins."),
    ]
    for i, (accent, tag, headline, body) in enumerate(cards):
        col, row = i % 2, i // 2
        x = 32 + col * 504
        y = 292 + row * 160
        story_card(draw, x, y, 472, 148, accent, tag, headline, body,
                   alt=(row % 2 == 1))

    # Sport strip.
    draw.rounded_rectangle([32, 774, 992, 840], radius=10, fill=CARD,
                           outline=EDGE, width=1)
    draw.rectangle([32, 784, 38, 830], fill=GREEN)
    sport_tag = "SPORT  ·  ANFIELD"
    draw.text((56, 784), sport_tag, font=font(BOLD, 19), fill=GREEN)
    sport_head_x = 56 + int(draw.textlength(sport_tag, font=font(BOLD, 19))) + 18
    draw.text((sport_head_x, 782), "Liverpool 4–0 Manchester United",
              font=font(BOLD, 28), fill=WHITE)
    draw.text((56, 812),
              "Pochettino's first match as United boss ends in a rout; 10-man United collapse.",
              font=font(PLAIN, 19), fill=SOFT)

    # Also today.
    draw.text((32, 854), "ALSO TODAY", font=font(BOLD, 20), fill=GOLD)
    also = ("Houthis claim Saudi refinery strike  ·  Five children killed by "
            "drone strikes in Khartoum  ·  24 civilians killed in South Sudan  ·  "
            "Trump signs law ending the penny")
    also_lines = wrap(draw, also, font(PLAIN, 19), 960)[:2]
    also_y = 880
    for line in also_lines:
        draw.text((32, also_y), line, font=font(PLAIN, 19), fill=SOFT)
        also_y += 24

    # Markets strip: two lines, so the five items never collide.
    draw.rounded_rectangle([32, 930, 992, 1000], radius=10, fill=CARD,
                           outline=EDGE, width=1)
    draw.text((48, 942), "MARKETS", font=font(BOLD, 22), fill=GOLD)
    row1 = [("S&P 500  6,910", "▼3.7%"), ("Nasdaq  22,618", "▼5.3%"),
            ("Dow  48,147", "▼1.9%")]
    cursor = 48 + int(draw.textlength("MARKETS", font=font(BOLD, 22))) + 28
    for name, change in row1:
        draw.text((cursor, 942), name, font=font(BOLD, 20), fill=WHITE)
        cursor += int(draw.textlength(name, font=font(BOLD, 20))) + 8
        draw.text((cursor, 942), change, font=font(BOLD, 20), fill=RED)
        cursor += int(draw.textlength(change, font=font(BOLD, 20))) + 36
    row2 = [("Nikkei", "▼5.1%"), ("Gold  $3,514", "")]
    cursor = 48
    for name, change in row2:
        draw.text((cursor, 970), name, font=font(BOLD, 20), fill=WHITE)
        cursor += int(draw.textlength(name, font=font(BOLD, 20)))
        if change:
            cursor += 8
            draw.text((cursor, 970), change, font=font(BOLD, 20), fill=RED)
            cursor += int(draw.textlength(change, font=font(BOLD, 20)))
        cursor += 36
    note2 = "US closes Fri 20 Nov  ·  Nikkei Mon 23 Nov"
    draw.text((992 - int(draw.textlength(note2, font=font(PLAIN, 18))) - 16, 971),
              note2, font=font(PLAIN, 18), fill=MUTED)

    # Footnote.
    note = "Sources: AP, Reuters, Xinhua, France 24"
    note_font = font(PLAIN, 15)
    note_w = draw.textlength(note, font=note_font)
    draw.text(((SIZE[0] - note_w) / 2, 1006), note, font=note_font, fill=MUTED)

    # Write the bytes with open() and make the file world-readable.
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    payload = buffer.getvalue()
    target = os.path.join(HERE, OUT_NAME)
    with open(target, "wb") as handle:
        handle.write(payload)
    os.chmod(target, 0o644)
    digest = hashlib.sha256(payload).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (target, len(payload), digest))
    return target


if __name__ == "__main__":
    build()
