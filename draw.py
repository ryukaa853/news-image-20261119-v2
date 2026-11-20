#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page, v2 (1024x1024 PNG).

A hero-led broadsheet, drawn with PIL only. No network, no randomness:
the same script always writes the same bytes.

Layout: navy masthead + one-line standfirst, then a full-width hero for
the Shenzhen summit (the day's lead story), a two-story middle row, and
a three-story bottom row. Every story is numbered 01-06 and carries its
own drawn illustration. All six stories are real 19-Nov-2026 news.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)      # warm newsprint
INK = (20, 33, 61)           # deep navy
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GOLD = (184, 134, 11)
GOLD_LT = (255, 200, 60)
TEAL = (15, 118, 110)
GREEN = (22, 101, 52)
PURPLE = (88, 28, 135)
GREY = (90, 90, 90)
PANEL = (255, 255, 255)
BORDER = (20, 33, 61)
SKY_NIGHT = (16, 28, 54)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SERIF = F + "DejaVuSerif.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using real pixel widths."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block_height(draw, lines, fnt, leading):
    return len(lines) * (fnt.size + leading)


def star5(d, cx, cy, r, fill):
    """Five-pointed star centred on (cx, cy), outer radius r."""
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.382
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def curve_points(p0, p1, p2, n=12):
    """Quadratic Bezier sample points."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


# ---------------------------------------------------------------- flags

def flag_us(d, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                        fill=(178, 34, 34))
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=(20, 33, 61))
    for r in range(5):
        for c in range(6):
            sx = x + cw * (c + 0.5) / 6
            sy = y + ch * (r + 0.5) / 5
            star5(d, sx, sy, max(2.0, cw / 34), (255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star5(d, x + w * 0.16, y + h * 0.22, h * 0.16, (255, 222, 0))
    for sx, sy in [(0.34, 0.10), (0.42, 0.24), (0.40, 0.42), (0.30, 0.50)]:
        star5(d, x + w * sx, y + h * sy, h * 0.055, (255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(120, 120, 120), width=1)


# ------------------------------------------------------- hero illustration

def illo_summit(d, x, y, w, h):
    """Three flags on poles above a round table, Shenzhen skyline behind."""
    # skyline removed: flags + table + caption read cleaner at this size
    # flagpoles + flags
    fw = (w - 48) // 3
    fh = min(78, h - 110)
    fy = y + 6
    for i, fl in enumerate((flag_us, flag_cn, flag_ru)):
        fx = x + 8 + i * (fw + 16)
        fl(d, fx + 4, fy, fw, fh)
        d.line([fx, fy, fx, y + h - 62], fill=INK, width=3)
        d.ellipse([fx - 4, fy - 5, fx + 4, fy + 3], fill=GOLD)
    # round table: top ellipse + three chairs
    ty = y + h - 62
    for cx in (x + w * 0.22, x + w * 0.5, x + w * 0.78):
        d.rectangle([cx - 14, ty - 30, cx + 14, ty - 4], fill=(120, 90, 60))
    d.ellipse([x + 18, ty - 16, x + w - 18, ty + 12], fill=(90, 60, 30))
    d.ellipse([x + 18, ty - 16, x + w - 18, ty + 2], fill=(150, 105, 55))
    d.text((x + w // 2, y + h - 24), "KYLIN VILLA · SHENZHEN",
           font=font(SANS_B, 13), fill=TEAL, anchor="ma")


def illo_scales(d, x, y, w, h):
    """Balanced scales of justice, level beam, two hanging pans."""
    cx = x + w // 2
    top, bot = y + 4, y + h - 8
    mid = top + int((bot - top) * 0.28)
    pan_y = top + int((bot - top) * 0.74)
    d.ellipse([cx - 6, top - 4, cx + 6, top + 6], fill=GOLD)
    d.line([cx, top + 6, cx, bot], fill=INK, width=5)
    d.line([cx - 78, mid, cx + 78, mid], fill=INK, width=5)
    for px in (cx - 78, cx + 78):
        d.line([px, mid, px - 24, pan_y], fill=INK, width=3)
        d.line([px, mid, px + 24, pan_y], fill=INK, width=3)
        d.arc([px - 24, pan_y - 8, px + 24, pan_y + 18], start=0, end=180,
              fill=INK, width=3)


def illo_gta(d, x, y, w, h):
    """Vice City sunset: gradient sky, skyline, palm, big VI."""
    top, mid, bot = (255, 154, 61), (232, 74, 122), (107, 63, 160)
    for i in range(h):
        t = i / max(h - 1, 1)
        if t < 0.5:
            c = tuple(int(top[j] + (mid[j] - top[j]) * t * 2) for j in range(3))
        else:
            c = tuple(int(mid[j] + (bot[j] - mid[j]) * (t - 0.5) * 2)
                        for j in range(3))
        d.line([x, y + i, x + w, y + i], fill=c)
    # skyline
    base = y + h
    for bx, bw_, bh in [(0, 34, int(h * 0.30)), (40, 28, int(h * 0.46)),
                        (74, 34, int(h * 0.34)), (114, 28, int(h * 0.52)),
                        (148, 30, int(h * 0.38))]:
        d.rectangle([x + bx, base - bh, x + bx + bw_, base],
                    fill=(40, 20, 60))
    # palm: leaning trunk + fronds that arc up, then droop (right side)
    px, py = x + w - 70, y + 10
    trunk = curve_points((px - 6, base), (px + 14, base - h // 2),
                         (px + 12, py), n=10)
    d.line(trunk, fill=(40, 20, 60), width=6, joint="curve")
    crown = (px + 12, py)
    for ex, ey in [(-50, 28), (-34, 38), (-14, 34), (14, 34),
                   (34, 38), (50, 26)]:
        tip = (crown[0] + ex, crown[1] + ey)
        midp = (crown[0] + ex * 0.55, crown[1] - 16)
        d.line(curve_points(crown, midp, tip, n=8), fill=(40, 20, 60),
               width=3, joint="curve")
    # big VI, bottom left
    vf = font(SANS_B, max(30, int(h * 0.78)))
    d.text((x + 10, base - int(h * 0.82)), "VI", font=vf,
           fill=(255, 255, 255), stroke_width=2, stroke_fill=(40, 20, 60))


def illo_ipo(d, x, y, w, h):
    """Rising bars, steep red arrow, $81BN label and ANT +17% tag."""
    label_h = min(30, h // 3)
    d.text((x + 4, y), "$81BN", font=font(SANS_B, label_h), fill=INK)
    tw = d.textlength("ANT +17%", font=font(SANS_B, 15)) + 16
    d.rounded_rectangle([x + w - tw, y, x + w, y + 24], radius=4, fill=GREEN)
    d.text((x + w - tw + 8, y + 3), "ANT +17%", font=font(SANS_B, 15),
           fill=(255, 255, 255))
    bars = [0.40, 0.52, 0.48, 0.64, 0.78, 1.0]
    bw = (w - 36) // len(bars)
    base = y + h
    for i, frac in enumerate(bars):
        bh = int((h - label_h - 8) * frac)
        bx = x + 4 + i * bw
        d.rectangle([bx, base - bh, bx + bw - 7, base],
                    fill=(22, 101, 52) if i < 5 else TEAL)
    # steep rising arrow across the bars
    ax0, ay0 = x + 6, base - int((h - label_h) * 0.44)
    ax1, ay1 = x + w - 8, y + label_h + 4
    d.line([ax0, ay0, ax1, ay1], fill=RED, width=4)
    d.polygon([(ax1, ay1), (ax1 - 18, ay1 + 2), (ax1 - 4, ay1 + 16)],
              fill=RED)


def illo_riyadh(d, x, y, w, h):
    """Night over Riyadh: skyline, twisted PIF Tower, missile streak."""
    d.rectangle([x, y, x + w, y + h], fill=SKY_NIGHT)
    base = y + h
    for bx, bw_, bh in [(0, 42, int(h * 0.50)), (50, 36, int(h * 0.66)),
                        (94, 44, int(h * 0.44))]:
        d.rectangle([x + bx, base - bh, x + bx + bw_, base],
                    fill=(60, 80, 120))
    # twisted PIF tower (tall, tapered, leaning top)
    tx = x + w - 86
    d.polygon([(tx, base), (tx + 12, y + 4), (tx + 46, y + 4), (tx + 58, base)],
              fill=(150, 180, 220))
    for i in range(5):
        yy = y + 12 + i * max(9, (h - 22) // 5)
        d.line([tx + 10 + i, yy, tx + 48 - i, yy], fill=SKY_NIGHT, width=2)
    # missile streak from upper left, glowing head
    d.line([x + 8, y + 8, x + w - 96, y + h // 2], fill=(255, 200, 60),
           width=4)
    d.ellipse([x + w - 104, y + h // 2 - 8, x + w - 88, y + h // 2 + 8],
              fill=(255, 120, 40))
    d.text((x + 8, base - 22), "PIF TOWER · RIYADH",
           font=font(SANS_B, 13), fill=(255, 255, 255))


def illo_wars(d, x, y, w, h):
    """Two stacked mini-scenes: Gaza yellow line + Crimean Bridge."""
    half = h // 2
    # --- Gaza: yellow dashed line, tank crossing it
    d.text((x + 4, y + 2), "GAZA", font=font(SANS_B, 12), fill=RED)
    gy = y + half - 6
    for lx in range(x, x + w, 18):
        d.line([lx, gy, lx + 11, gy], fill=(230, 190, 0), width=5)
    tx, ty = x + w // 2 - 34, gy - 19
    d.rectangle([tx, ty, tx + 68, ty + 12], fill=INK)
    d.rectangle([tx + 16, ty - 7, tx + 42, ty], fill=INK)
    d.line([tx + 42, ty - 4, tx + 64, ty - 4], fill=INK, width=4)
    for wx in range(tx + 4, tx + 64, 12):
        d.ellipse([wx, ty + 12, wx + 9, ty + 19], fill=INK)
    # --- Crimea: bridge deck with a gap, explosion starburst
    d.text((x + w - 78, y + half + 1), "CRIMEA", font=font(SANS_B, 12),
           fill=NAVY)
    deck_y = y + h - 18
    d.rectangle([x, deck_y + 8, x + w, y + h], fill=(30, 90, 140))
    d.line([x, deck_y, x + w // 2 - 22, deck_y], fill=INK, width=6)
    d.line([x + w // 2 + 22, deck_y, x + w, deck_y], fill=INK, width=6)
    for bx in range(x + 8, x + w, 24):
        if abs(bx + 10 - (x + w // 2)) > 30:
            d.line([bx, deck_y, bx, deck_y + 8], fill=INK, width=3)
    cx, cy = x + w // 2, deck_y - 6
    for dx, dy in [(-15, 0), (15, 0), (0, -15), (0, 13),
                   (-11, -11), (11, -11), (-11, 11), (11, 11)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 140, 0), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 200, 60))


# ------------------------------------------------------------------ panels

def draw_panel(d, x, y, w, h, kicker, kicker_color, headline, body,
               hl_size=30, body_size=19, illo=None, illo_h=80,
               kicker_size=17):
    """One news panel: white card, kicker chip, headline, body, and a
    fixed-height illustration strip at the bottom. Raises if the text
    does not fit above the illustration strip."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=PANEL, outline=BORDER,
                width=2)
    pad = 18
    cx = x + pad
    text_w = w - 2 * pad
    cy = y + 14
    kf = font(SANS_B, kicker_size)
    kw = d.textlength(kicker, font=kf) + 20
    d.rounded_rectangle([cx, cy, cx + kw, cy + 26], radius=4,
                        fill=kicker_color)
    d.text((cx + 10, cy + 4), kicker, font=kf, fill=(255, 255, 255))
    cy += 26 + 8
    hf = font(SANS_B, hl_size)
    hl_lines = wrap(d, headline, hf, text_w)
    for line in hl_lines:
        d.text((cx, cy), line, font=hf, fill=INK)
        cy += hl_size + 6
    cy += 4
    bf = font(SANS, body_size)
    body_lines = wrap(d, body, bf, text_w)
    for line in body_lines:
        d.text((cx, cy), line, font=bf, fill=(40, 40, 40))
        cy += body_size + 5
    illo_top = y + h - illo_h - 8
    if cy > illo_top - 4:
        raise SystemExit(
            f"text overflow in panel {kicker!r}: text ends at {cy}, "
            f"illustration starts at {illo_top}")
    if illo is not None:
        illo(d, x + pad, illo_top, text_w, illo_h)


def kicker_chip(d, x, y, text, color, size=18):
    kf = font(SANS_B, size)
    kw = d.textlength(text, font=kf) + 22
    d.rounded_rectangle([x, y, x + kw, y + 28], radius=4, fill=color)
    d.text((x + 11, y + 5), text, font=kf, fill=(255, 255, 255))
    return kw


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((W // 2, 10), "THE WORLD IN ONE DAY", font=font(SERIF_B, 54),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 70), "THURSDAY  ·  19 NOVEMBER 2026",
           font=font(SANS_B, 28), fill=GOLD_LT, anchor="ma")
    d.rectangle([0, 104, W, 108], fill=RED)
    # ---- standfirst ----
    d.text((W // 2, 116),
           "Three nuclear powers at one table, a genocide verdict, and the "
           "biggest launch in entertainment history.",
           font=font(SERIF, 17), fill=INK, anchor="ma")

    # ---- HERO: Shenzhen summit (full width) ----
    hx, hy, hw, hh = 24, 148, 976, 260
    d.rectangle([hx, hy, hx + hw - 1, hy + hh - 1], fill=PANEL,
                outline=BORDER, width=2)
    kicker_chip(d, hx + 24, hy + 14, "01 · SHENZHEN SUMMIT", RED, size=18)
    hf = font(SANS_B, 36)
    cy = hy + 52
    for line in wrap(d, "TRUMP, XI AND PUTIN MEET FOR THE FIRST TIME", hf,
                     552):
        d.text((hx + 24, cy), line, font=hf, fill=INK)
        cy += 42
    cy += 6
    bf = font(SANS, 19)
    deck = ("The three leaders sat for 90 minutes at a round table in "
            "Shenzhen and issued a joint statement: a nuclear war "
            "\u201ccannot be won and must never be fought\u201d.")
    for line in wrap(d, deck, bf, 552):
        d.text((hx + 24, cy), line, font=bf, fill=(40, 40, 40))
        cy += 24
    cy += 10
    d.text((hx + 24, cy),
           "\u201cWe are really making history.\u201d \u2014 President Trump",
           font=font(SERIF, 18), fill=TEAL)
    illo_summit(d, hx + 620, hy + 14, 332, hh - 28)

    # ---- row 2: ICJ + GTA VI ----
    draw_panel(d, 24, 420, 480, 268, "02 · THE HAGUE", NAVY,
               "MYANMAR GUILTY OF GENOCIDE",
               "The world court ruled 9\u20136: Myanmar committed "
               "genocide against the Rohingya.",
               hl_size=30, body_size=17, illo=illo_scales, illo_h=78)
    draw_panel(d, 520, 420, 480, 268, "03 · ENTERTAINMENT", PURPLE,
               "GTA VI SMASHES EVERY RECORD",
               "Launched at midnight: an estimated $2.36bn on day one "
               "\u2014 the biggest entertainment launch ever.",
               hl_size=30, body_size=17, illo=illo_gta, illo_h=78)

    # ---- row 3: IPO + Riyadh + Gaza/Crimea ----
    draw_panel(d, 24, 700, 314, 262, "04 · WALL STREET", GREEN,
               "THE BIGGEST IPO EVER",
               "Anthropic raised a record $81bn at $83 a share; "
               "\u201cANT\u201d closed up 17% at $97.17.",
               hl_size=24, body_size=17, illo=illo_ipo, illo_h=70,
               kicker_size=15)
    draw_panel(d, 355, 700, 314, 262, "05 · MIDDLE EAST", RED,
               "MISSILE HITS RIYADH TOWER",
               "A Houthi missile struck the PIF Tower, blowing out "
               "windows on 7\u20138 floors. No injuries.",
               hl_size=24, body_size=17, illo=illo_riyadh, illo_h=70,
               kicker_size=15)
    draw_panel(d, 686, 700, 314, 262, "06 · WAR UPDATES", NAVY,
               "TANKS CROSS THE YELLOW LINE",
               "Israeli armour entered central Gaza; Ukraine hit the "
               "Crimean Bridge again.",
               hl_size=24, body_size=17, illo=illo_wars, illo_h=70,
               kicker_size=15)

    # ---- footer: sources ----
    d.text((W // 2, 978),
           "Sources: WSJ  •  Reuters  •  CNN  •  Le Monde  •  HRW  •  "
           "Sensor Tower  —  19 November 2026",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
