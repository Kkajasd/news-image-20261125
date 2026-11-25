#!/usr/bin/env python3
"""Draw "The World Today" — Wednesday, 25 November 2026.

Renders a one-page newspaper front page (1024x1024 PNG) summing up the
day's world news. Every story is baked into the script below; the output is
fully deterministic — same bytes on every run — and uses only Pillow plus
the DejaVu fonts shipped with the system. No network, no timestamps, no
randomness.

Run:  python3 tools/draw_frontpage.py
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30
INK = (18, 18, 22)
PAPER = (253, 252, 246)
NAVY = (16, 42, 84)
RED = (178, 34, 34)
GREY = (110, 108, 100)
RULE = (150, 146, 134)
FAINT = (232, 230, 220)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

LEADS = [
    (
        "TARIFFS",
        "US weighs new tariffs on China, EU and 14 partners",
        "Washington prepares fresh import duties after a probe into excess "
        "industrial capacity.",
    ),
    (
        "BALTIC SEA",
        "Zelenskyy confirms Ukraine hit Russian ship",
        "Kyiv says its drones struck a Russian cargo ship in the Gulf of "
        "Finland.",
    ),
    (
        "SPACE",
        "Shenzhou-24 lifts off — with Pakistan's first astronaut",
        "China launches its Tiangong crew, carrying Wing Cmdr. Muhammad "
        "Zeeshan Ali.",
    ),
]

COLUMNS = [
    (
        "WORLD",
        [
            (
                "Russia calls ship strikes \u201cterrorism\u201d",
                "Moscow warns of severe consequences after drone hits in the "
                "Baltic and off Libya.",
            ),
            (
                "NATO to send early-warning jets to Poland",
                "Alliance moves surveillance aircraft after missiles landed "
                "in Poland during a strike on Ukraine.",
            ),
            (
                "Three tankers hit by mines in Hormuz strait",
                "Iran's Revolutionary Guard navy blames naval mines; shipping "
                "fears rise in the Gulf.",
            ),
            (
                "Houthis hit Riyadh's tallest tower; 11 hurt",
                "Saudi civil defence says a strike struck the capital's "
                "tallest tower.",
            ),
            (
                "700,000 Russian soldiers killed, analysis finds",
                "A new estimate puts Moscow's dead in the Ukraine war above "
                "700,000.",
            ),
            (
                "Gaza death toll reaches 74,746",
                "The WAFA count rises as Israeli attacks continue, Gaza "
                "officials say.",
            ),
            (
                "266 million face acute hunger, WFP warns",
                "The UN food agency says acute food insecurity now grips "
                "266m people.",
            ),
            (
                "Landmine toll hits five-year high",
                "At least 6,929 killed or hurt in 2025, mostly civilians — "
                "half of them children.",
            ),
        ],
    ),
    (
        "MARKETS & AMERICAS",
        [
            (
                "Wall Street splits: Nasdaq \u22122%, Dow +0.9%",
                "Tech sell-off a day after the Nvidia-led surge; most S&P "
                "stocks still rose.",
            ),
            (
                "Nvidia gives back 6% as Huang says sorry",
                "The reinstated chief apologises to staff at an all-hands "
                "meeting.",
            ),
            (
                "Anthropic slips below its IPO price",
                "Shares fall under $83 as doubts grow over unreleased AI "
                "models.",
            ),
            (
                "Bitcoin falls to $59,700",
                "Crypto slides 2.6% as tech stocks drag markets lower.",
            ),
            (
                "Sensex sinks 1,484 points",
                "Indian stocks reverse after a four-week rally; metals and "
                "banks lead the fall.",
            ),
            (
                "Trump pardons turkeys Freedom and Feathers",
                "The Thanksgiving pardoning spares two birds ahead of the "
                "holiday.",
            ),
            (
                "Giuliani awarded Medal of Freedom",
                "Trump honours the former New York mayor with the top "
                "civilian award.",
            ),
            (
                "BJP and Akali Dal reunite for Punjab 2027",
                "The two parties announce an alliance six years after "
                "splitting.",
            ),
        ],
    ),
    (
        "SPORT, TECH & LIFE",
        [
            (
                "England level T20 series in Australia",
                "England chase 185 to beat Australia by eight wickets in "
                "the second T20.",
            ),
            (
                "Arsenal held 1\u20131 by Dortmund",
                "Champions League group game ends level in Germany.",
            ),
            (
                "Priyansh Arya smashes 181 in T20",
                "The second-highest score in T20 history.",
            ),
            (
                "Gukesh faces Sindarov for chess crown",
                "India's champion opens a 14-game classical title match.",
            ),
            (
                "Walmart brings Black Friday to Meta's Muse",
                "Holiday deals arrive inside the AI agent ahead of Black "
                "Friday.",
            ),
            (
                "Threads comes to iPad with cashtags",
                "Meta's app adds iPad support and stock-ticker tags.",
            ),
            (
                "WHO chief visits Cuba as hospitals run short",
                "Tedros visits as Cuban hospitals struggle for supplies.",
            ),
        ],
    ),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns a list of lines."""
    lines = []
    for raw in text.split("\n"):
        line = ""
        for word in raw.split(" "):
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_globe(draw, cx, cy, s):
    """Small line-art globe: circle, meridians, latitude lines."""
    r = 15 * s
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=NAVY, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=NAVY, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=NAVY, width=2)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 180, 360, fill=NAVY, width=2)


def draw_rocket(draw, cx, cy, s):
    """Small rocket glyph, pointing up-right."""
    body = [(cx - 6 * s, cy + 14 * s), (cx - 6 * s, cy - 2 * s),
            (cx, cy - 16 * s), (cx + 6 * s, cy - 2 * s),
            (cx + 6 * s, cy + 14 * s)]
    draw.polygon(body, fill=RED)
    draw.polygon([(cx - 6 * s, cy + 8 * s), (cx - 13 * s, cy + 18 * s),
                  (cx - 6 * s, cy + 14 * s)], fill=NAVY)
    draw.polygon([(cx + 6 * s, cy + 8 * s), (cx + 13 * s, cy + 18 * s),
                  (cx + 6 * s, cy + 14 * s)], fill=NAVY)
    draw.ellipse([cx - 3 * s, cy - 6 * s, cx + 3 * s, cy], fill=PAPER)
    draw.polygon([(cx - 4 * s, cy + 14 * s), (cx + 4 * s, cy + 14 * s),
                  (cx, cy + 22 * s)], fill=(232, 140, 40))


def draw_ship(draw, cx, cy, s):
    """Small cargo-ship glyph."""
    draw.polygon([(cx - 18 * s, cy + 2 * s), (cx + 18 * s, cy + 2 * s),
                  (cx + 12 * s, cy + 12 * s), (cx - 12 * s, cy + 12 * s)],
                 fill=NAVY)
    draw.rectangle([cx - 10 * s, cy - 8 * s, cx - 2 * s, cy + 2 * s], fill=RED)
    draw.rectangle([cx + 2 * s, cy - 8 * s, cx + 10 * s, cy + 2 * s], fill=RED)
    draw.line([cx - 22 * s, cy + 16 * s, cx + 22 * s, cy + 16 * s],
              fill=NAVY, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    title_f = font(SERIF, 66)
    d.text((MARGIN, 18), "THE WORLD TODAY", font=title_f, fill=INK)
    draw_globe(d, W - MARGIN - 34, 58, 2)

    d.line([MARGIN, 102, W - MARGIN, 102], fill=INK, width=3)
    d.line([MARGIN, 107, W - MARGIN, 107], fill=INK, width=1)
    date_f = font(SANS_B, 21)
    d.text((MARGIN, 116), "WEDNESDAY, 25 NOVEMBER 2026", font=date_f, fill=RED)
    tag_f = font(SANS, 15)
    tag = "ONE DAY  ·  ONE IMAGE  ·  THE WORLD IN A PAGE"
    d.text((W - MARGIN - d.textlength(tag, font=tag_f), 119), tag,
           font=tag_f, fill=GREY)

    # ---- Lead stories ---------------------------------------------------
    lead_top = 152
    lead_h = 162
    col_w = (W - 2 * MARGIN - 2 * 16) // 3
    icons = [draw_ship, draw_globe, draw_rocket]
    for i, (kicker, head, summ) in enumerate(LEADS):
        x = MARGIN + i * (col_w + 16)
        d.rectangle([x, lead_top, x + col_w, lead_top + lead_h],
                    outline=RULE, width=1)
        d.rectangle([x, lead_top, x + col_w, lead_top + 26], fill=NAVY)
        d.text((x + 10, lead_top + 4), kicker, font=font(SANS_B, 14),
               fill=(255, 255, 255))
        icons[i](d, x + col_w - 30, lead_top + 52, 1)
        head_lines = wrap(d, head, font(SANS_B, 18), col_w - 68)
        y = lead_top + 34
        for line in head_lines[:3]:
            d.text((x + 10, y), line, font=font(SANS_B, 18), fill=INK)
            y += 22
        summ_lines = wrap(d, summ, font(SANS, 13), col_w - 20)
        for line in summ_lines[:3]:
            d.text((x + 10, y + 2), line, font=font(SANS, 13), fill=(60, 58, 52))
            y += 17

    # ---- Three columns --------------------------------------------------
    col_top = lead_top + lead_h + 14
    col_bot = H - 44
    for i, (section, items) in enumerate(COLUMNS):
        x = MARGIN + i * (col_w + 16)
        d.rectangle([x, col_top, x + col_w, col_top + 30], fill=INK)
        d.text((x + 10, col_top + 5), section, font=font(SANS_B, 15),
               fill=(255, 255, 255))
        y = col_top + 42
        for head, summ in items:
            head_lines = wrap(d, head, font(SANS_B, 14), col_w - 4)
            for line in head_lines:
                d.text((x + 2, y), line, font=font(SANS_B, 14), fill=INK)
                y += 18
            summ_lines = wrap(d, summ, font(SANS, 11), col_w - 4)
            for line in summ_lines:
                d.text((x + 2, y), line, font=font(SANS, 11), fill=(60, 58, 52))
                y += 14
            y += 6
            if y < col_bot - 20:
                d.line([x, y - 4, x + col_w, y - 4], fill=FAINT, width=1)

    # ---- Footer ---------------------------------------------------------
    d.line([MARGIN, H - 36, W - MARGIN, H - 36], fill=INK, width=1)
    foot_f = font(SANS, 11)
    foot = ("Sources: Reuters · RFE/RL · The Hindu BusinessLine · Rivkin · Jagran Josh · "
            "BD Global Times · Mildgrim · Matrix24 — full list in SOURCES.md")
    d.text((MARGIN, H - 28), foot, font=foot_f, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print(f"Wrote entry.png {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
