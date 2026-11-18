"""Assemble the pinned, unlisted Stealthmate Unity player."""
from importlib import import_module
import json
from pathlib import Path
import sys
import re


if __name__ == "__main__":
    paper = len(sys.argv) > 3 and sys.argv[3] == "--paper"
    route = "betas/stealthmate_paper" if paper else "betas/stealthmate"
    manifest_path = Path(route + ".release.json")
    manifest = json.loads(manifest_path.read_text())
    release = manifest["release"]
    if not re.fullmatch(r"stealthmate-beta-[a-z0-9-]+", release):
        raise ValueError("Invalid Stealthmate release tag")
    assemble = import_module("assemble-opossum").assemble
    site = Path(sys.argv[2])
    result = assemble(sys.argv[1], site, manifest, route=route,
                      require_canvas_markers=False)
    destination = site / route
    versioned = destination / release
    versioned.mkdir()
    for directory in ("Build", "StreamingAssets"):
        (destination / directory).rename(versioned / directory)
    entry = destination / 'index.html'
    html = entry.read_text(encoding='utf-8')
    if paper:
        footer_css = '''<style>
        a[href^="https://store.steampowered.com/app/5141490/"],
        a[href="https://thelatelab.com/stealthmate/beta/"] {
            display: flex; align-items: center; justify-content: center;
            height: 44px !important; background: #f7f1df !important;
            color: #344321 !important; border-color: #8c996e !important;
        }
        a[href^="https://store.steampowered.com/app/5141490/"]:focus-visible,
        a[href="https://thelatelab.com/stealthmate/beta/"]:focus-visible {
            outline: 2px solid #344321; outline-offset: -4px;
        }
        </style>'''
        html = html.replace('viewport.height - 34', 'viewport.height - 44')
        html = html.replace('</head>', footer_css + '\n</head>', 1)
    for directory in ("Build", "StreamingAssets"):
        # Unity's fresh template uses relative directory literals. Older reviewed
        # archives may already contain this release's immutable prefix.
        html = html.replace('"' + directory + '"', '"' + release + '/' + directory + '"')
        if release + '/' + directory not in html:
            raise ValueError('Missing versioned Unity asset URL: ' + directory)
    entry.write_text(html, encoding='utf-8')
    print(json.dumps(result))
