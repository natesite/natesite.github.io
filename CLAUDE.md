# Nate's Page

Nate's personal website for sharing his writings, drawings and photos.
Live at https://natesite.github.io (GitHub Pages publishes the `main` branch as is).

This repository is public. Never put anything private in it, including this file.

## How the site works

- Plain HTML and CSS served by GitHub Pages. No frameworks, build tools or paid services.
  `.nojekyll` is there so GitHub serves files exactly as they are.
- Look: very basic early internet. Times New Roman, standard blue and purple links, a centered
  box with a ridged border, horizontal lines and an old-school visitor counter.
- Background: Nate's duck photo, full screen (`duck-full.jpg`). Nate chose this over tiled;
  `duck-tile.jpg` is the unused tiled version. The background sits on a fixed `#bg` layer so it
  stays still on iPhone too.
- The white content box is about 60% see-through: `rgba(255, 255, 255, 0.62)`.
- Nate is usually on his phone, so every page must look good on a small screen. Check pages at
  phone width before saying a change is done.
- View counts will come from GoatCounter. The visitor counter and like buttons on the home page
  are placeholders until those services are connected.
- Pages: `index.html` (home), `writings.html`, `drawings.html`, `photos.html`, `about.html`.
  The menu section is called "Writings", not "Essays". Each page repeats the home page styles
  and menu; the other pages also have a Home link and show the current page in bold.

## When Nate adds new work

- Photos and drawings: resize to about 1600 pixels wide, keep each file under 500 KB, and remove
  all hidden data (EXIF), especially GPS location, before committing.
- Add each new piece to the "What's New" list on the home page and update the "Last updated" date.
- Explain any GitHub steps simply, one step at a time.

## Handwriting font

- Writings will use a font made from Nate's handwriting.
- `font/make_template.py` builds the 2-page template (`font/handwriting-font-template.pdf`) and
  writes `font/template-layout.json` with every box position relative to the four corner marks.
  Page 2 has a small extra square right of the top-left mark.
- When Nate sends photos of the filled-in pages, run the script to get the layout, straighten each
  photo using the corner marks, cut out each box, and build the font from the letters.
  Guide lines (light blue) are at these fractions of box height from the top: cap 0.14,
  x-height 0.44, baseline 0.70.

## Still deciding

- Like buttons: which free service.
- Mailing list: Buttondown or Kit.
- Contact page: Web3Forms form or a simple email link.
- Whether writings get a "switch to plain text" link.
