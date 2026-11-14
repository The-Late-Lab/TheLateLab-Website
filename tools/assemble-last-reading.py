"""Verify the pinned WebGL player and add it to the unlisted beta route."""
from importlib import import_module
import json
from pathlib import Path
import re
import sys

if __name__ == "__main__":
    manifest = json.loads(Path("betas/last-reading.release.json").read_text())
    release = manifest["release"]
    if not re.fullmatch(r"last-reading-beta-[0-9]{8}-[0-9]{6}", release):
        raise ValueError("Invalid The Last Reading beta release tag")

    route = "betas/thelastreading.com"
    site = Path(sys.argv[2])
    result = import_module("assemble-opossum").assemble(
        sys.argv[1], site, manifest, route=f"{route}/{release}",
        require_canvas_markers=False,
        extra_paths=re.compile(r"TemplateData/[a-zA-Z0-9_.-]+\.(?:css|ico|png|svg)|ThirdPartyNotices\.txt|CHANGELOG\.md|beta\.json"),
    )
    destination = site / route
    (destination / "index.html").write_text(
        '<!doctype html><meta name="robots" content="noindex, nofollow">'
        '<title>The Last Reading | Web beta</title>'
        f'<meta http-equiv="refresh" content="0; url=./{release}/">'
        f'<a href="./{release}/">Open the latest playtest</a>',
        encoding="utf-8",
    )
    print(json.dumps(result))
