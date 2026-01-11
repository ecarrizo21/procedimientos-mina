import os
import urllib.parse

PAGES = [
    # page_file, pdf_folder, start_tag, end_tag, link_prefix
    ("dr/index.html",  "pdf/DR",  "<!-- AUTO:START:DR -->",  "<!-- AUTO:END:DR -->",  "../"),
    ("dpi/index.html", "pdf/DPi", "<!-- AUTO:START:DPI -->", "<!-- AUTO:END:DPI -->", "../"),
]

def sorted_pdfs(folder: str):
    if not os.path.isdir(folder):
        return []
    files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    return sorted(files, key=lambda s: s.lower())

def build_ul(pdf_folder: str, link_prefix: str):
    pdfs = sorted_pdfs(pdf_folder)
    if not pdfs:
        return "<ul>\n  <li><em>Sin documentos cargados aún.</em></li>\n</ul>"

    lines = ["<ul>"]
    for fname in pdfs:
        url = link_prefix + pdf_folder + "/" + urllib.parse.quote(fname)
        label = fname.replace(".pdf", "").replace("_", " ")
        lines.append(
            f'  <li>'
            f'<a href="{url}" target="_blank" rel="noopener">{label} (Abrir)</a> — '
            f'<a href="{url}" download>Descargar</a>'
            f'</li>'
        )
    lines.append("</ul>")
    return "\n".join(lines)

for page_file, pdf_folder, start_tag, end_tag, link_prefix in PAGES:
    with open(page_file, "r", encoding="utf-8") as f:
        html = f.read()

    if start_tag not in html or end_tag not in html:
        raise RuntimeError(f"No encuentro marcadores en {page_file}: {start_tag} / {end_tag}")

    start = html.index(start_tag) + len(start_tag)
    end = html.index(end_tag)

    new_ul = "\n" + build_ul(pdf_folder, link_prefix) + "\n"
    html = html[:start] + new_ul + html[end:]

    with open(page_file, "w", encoding="utf-8") as f:
        f.write(html)
