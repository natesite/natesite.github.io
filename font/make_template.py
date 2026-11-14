"""Build a printable handwriting-font template (US Letter, 2 pages) and a layout JSON
describing every box relative to the four corner marks, for later extraction."""
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Sans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("SansB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

W, H = letter  # 612 x 792 pt
BLUE = (0.55, 0.74, 0.95)       # light "dropout" blue for guides
LABEL = (0.25, 0.45, 0.80)      # darker blue for labels (outside the writing area)
INK = (0, 0, 0)

# Corner mark centers (pt, origin bottom-left) and grid area inside them
MARK = 16
MX0, MX1, MY0, MY1 = 30, 582, 30, 650
GX0, GX1, GY0, GY1 = 46, 566, 46, 634
COLS, ROWS = 8, 7
CW = (GX1 - GX0) / COLS          # 65
CH = (GY1 - GY0) / ROWS          # 84
PAD = 4
LABEL_H = 14
# guide lines as fraction of box height measured from the TOP of the box
ASC, XH, BASE = 0.14, 0.44, 0.70

NAMES = {
    ".": "period", ",": "comma", "?": "question", "!": "exclaim", "'": "apostrophe",
    '"': "quote", "-": "hyphen", ":": "colon", ";": "semicolon", "(": "open paren", ")": "close paren",
    "&": "and", "/": "slash", "@": "at", "$": "dollar", "%": "percent", "#": "number",
    "*": "star", "+": "plus", "=": "equals", "[": "open bracket", "]": "close bracket",
    "l": "lower L", "I": "capital i", "1": "one", "0": "zero", "O": "capital o", "o": "lower o",
}

PAGES = [
    {
        "title": "Page 1 of 2: Letters",
        "chars": list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        "sample": False,
    },
    {
        "title": "Page 2 of 2: Numbers and punctuation",
        "chars": list("0123456789") + list(".,?!'\"-:;()&/@$%#*+=[]"),
        "sample": True,
    },
]

INSTRUCTIONS = [
    "1.  Print at 100% (\"Actual size\"), not \"Fit to page.\"",
    "2.  Use a black felt-tip pen, like a Sharpie Pen or Flair. Ballpoint is too faint.",
    "3.  Write one character per box, sitting on the solid line. Small letters reach the dashed",
    "     line. Capitals and tall letters reach the dotted line. Tails (g, j, p, q, y) hang below.",
    "4.  Stay inside the boxes and don't mark the black corner squares.",
    "5.  Photograph each page straight on in good light with all 4 corner squares showing.",
]
OPTIONAL = ("Optional: print page 1 twice and fill in both. I'll use both versions so your "
            "letters alternate and look more natural.")


def mark(c, cx, cy, size=MARK):
    c.setFillColorRGB(*INK)
    c.rect(cx - size / 2, cy - size / 2, size, size, stroke=0, fill=1)


def header(c, page):
    c.setFillColorRGB(*INK)
    c.setFont("SansB", 15)
    c.drawString(40, 762, "Handwriting Font Template")
    c.setFont("Sans", 10.5)
    c.drawRightString(572, 763, page["title"])
    c.setFont("Sans", 8.6)
    y = 744
    for line in INSTRUCTIONS:
        c.drawString(40, y, line)
        y -= 11.5
    if page is PAGES[0]:
        c.setFont("Sans", 8.6)
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.drawString(40, y - 2, OPTIONAL)


def cell_box(i):
    r, col = divmod(i, COLS)
    x0 = GX0 + col * CW
    ytop = GY1 - r * CH
    bx0, bx1 = x0 + PAD, x0 + CW - PAD
    by1 = ytop - LABEL_H            # top of writing box
    by0 = ytop - CH + PAD           # bottom of writing box
    return x0, ytop, bx0, by0, bx1, by1


def guides(c, bx0, by0, bx1, by1, dashed_xh=True):
    h = by1 - by0
    c.setStrokeColorRGB(*BLUE)
    c.setLineWidth(0.8)
    c.setDash()
    c.rect(bx0, by0, bx1 - bx0, h, stroke=1, fill=0)
    yb = by1 - BASE * h
    c.setLineWidth(1.0)
    c.line(bx0, yb, bx1, yb)                      # baseline (solid)
    c.setLineWidth(0.6)
    c.setDash(3, 2)
    c.line(bx0, by1 - XH * h, bx1, by1 - XH * h)  # x-height (dashed)
    c.setDash(1, 2.5)
    c.line(bx0, by1 - ASC * h, bx1, by1 - ASC * h)  # cap height (dotted)
    c.setDash()


def label(c, x0, ytop, ch):
    c.setFillColorRGB(*LABEL)
    c.setFont("Mono", 10.5)
    c.drawString(x0 + PAD + 1, ytop - LABEL_H + 3, ch)
    name = NAMES.get(ch)
    if name:
        c.setFont("Sans", 5.8)
        c.drawRightString(x0 + CW - PAD - 1, ytop - LABEL_H + 3.6, name)


def writing_sample(c, first_row):
    """Lined area for a normal handwriting sample, filling rows first_row..ROWS-1."""
    top = GY1 - first_row * CH - 6
    bottom = GY0 + PAD
    c.setFillColorRGB(*LABEL)
    c.setFont("Sans", 8.6)
    c.drawString(GX0 + PAD, top - 10,
                 "Writing sample: copy this in your normal handwriting, on the lines below.")
    c.setFont("Sans", 11)
    c.setFillColorRGB(0.15, 0.15, 0.15)
    c.drawString(GX0 + PAD, top - 26, "The quick brown fox jumps over the lazy dog. Then it took a nap by the pond.")
    c.setStrokeColorRGB(*BLUE)
    c.setLineWidth(0.8)
    c.rect(GX0 + PAD, bottom, (GX1 - GX0) - 2 * PAD, (top - 36) - bottom, stroke=1, fill=0)
    y = top - 36 - 46
    lines = []
    while y > bottom + 8:
        c.setLineWidth(1.0)
        c.line(GX0 + PAD + 6, y, GX1 - PAD - 6, y)
        lines.append(y)
        y -= 50
    return {"x0": GX0 + PAD, "y0": bottom, "x1": GX1 - PAD, "y1": top - 36, "baselines": lines}


def build(path_pdf, path_json):
    c = canvas.Canvas(path_pdf, pagesize=letter)
    c.setTitle("Handwriting Font Template")
    layout = {"page_size_pt": [W, H], "marks_pt": {"tl": [MX0, MY1], "tr": [MX1, MY1],
              "bl": [MX0, MY0], "br": [MX1, MY0]}, "guides": {"asc": ASC, "xh": XH, "base": BASE},
              "pages": []}
    for p_i, page in enumerate(PAGES):
        header(c, page)
        for cx, cy in [(MX0, MY0), (MX1, MY0), (MX0, MY1), (MX1, MY1)]:
            mark(c, cx, cy)
        # page id: page 2 gets a small extra square right of the top-left mark
        if p_i == 1:
            mark(c, MX0 + 26, MY1, size=8)
        boxes = []
        for i, ch in enumerate(page["chars"]):
            x0, ytop, bx0, by0, bx1, by1 = cell_box(i)
            guides(c, bx0, by0, bx1, by1)
            label(c, x0, ytop, ch)
            boxes.append({"char": ch, "box_pt": [bx0, by0, bx1, by1]})
        entry = {"title": page["title"], "boxes": boxes}
        if page["sample"]:
            used_rows = -(-len(page["chars"]) // COLS)
            entry["sample"] = writing_sample(c, used_rows)
        layout["pages"].append(entry)
        # footer
        c.setFillColorRGB(0.4, 0.4, 0.4)
        c.setFont("Sans", 7)
        c.drawCentredString(W / 2, 14, "Keep the four black squares visible in your photo.")
        c.showPage()
    c.save()
    with open(path_json, "w") as f:
        json.dump(layout, f, indent=1)


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    build(os.path.join(here, "handwriting-font-template.pdf"), os.path.join(here, "template-layout.json"))
    print("done")
