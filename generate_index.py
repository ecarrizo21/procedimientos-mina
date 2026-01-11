import os
import urllib.parse

INDEX_FILE = "index.html"

SECTIONS = [
    ("DR", "pdf/DR", "<!-- AUTO:START:DR -->", "<!-- AUTO:END:DR -->"),
    ("DPI", "pdf/DPi", "<!-- AUTO:START:DPI -->", "<!-- AUTO:END:DPI -->"),
]

def sorted_pdfs(folder: str):
    if not os.path.isdir(folder):
        return []
    files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    return sorted(files, key=lambda s: s.lower())

def build_ul(folder: str):
    pdfs = sorted_pdfs(folder)
    if not pdfs:
        return "<ul>\n  <li><em>Sin documentos cargados aún.</em></li>\n</ul>"

    lines = ["<ul>"]
    for fname in pdfs:
        url = folder + "/" + urllib.parse.quote(fname)
        label = fname.replace(".pdf", "").replace("_", " ")
        lines.append(
            f'  <li>'
            f'<a href="{url}" target="_blank" rel="noopener">{label} (Abrir)</a> — '
            f'<a href="{url}" download>Descargar</a>'
            f'</li>'
        )
    lines.append("</ul>")
    return "\n".join(lines)

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    html = f.read()

for _, folder, start_tag, end_tag in SECTIONS:
    if start_tag not in html or end_tag not in html:
        raise RuntimeError(f"No encuentro los marcadores {start_tag} / {end_tag} en index.html")

    start = html.index(start_tag) + len(start_tag)
    end = html.index(end_tag)

    new_ul = "\n" + build_ul(folder) + "\n"
    html = html[:start] + new_ul + html[end:]

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(html)

