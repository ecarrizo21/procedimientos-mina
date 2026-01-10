import os
import urllib.parse

PDF_DIR = "pdf"
INDEX_FILE = "index.html"

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html = f.read()

start = html.index("<!-- AUTO:START -->")
end = html.index("<!-- AUTO:END -->")

items = []
for fname in sorted(os.listdir(PDF_DIR)):
    if fname.lower().endswith(".pdf"):
        url = "pdf/" + urllib.parse.quote(fname)
        label = fname.replace(".pdf", "").replace("_", " ")
        items.append(f"""  <li>
    <a href="{url}" target="_blank" rel="noopener">{label} (Abrir)</a> —
    <a href="{url}" download>Descargar</a>
  </li>""")

new_block = "<!-- AUTO:START -->\n<ul>\n" + "\n".join(items) + "\n</ul>\n<!-- AUTO:END -->"

html = html[:start] + new_block + html[end + len("<!-- AUTO:END -->"):]

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)
