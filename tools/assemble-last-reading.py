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
    (destination / "latest.json").write_text(json.dumps({"release": release}) + "\n", encoding="utf-8")
    (destination / "index.html").write_text(
        '<!doctype html><meta name="robots" content="noindex, nofollow">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>The Last Reading | Web beta</title>'
        f'<a id="launch" href="./{release}/">Open the latest playtest</a>'
        '<script>'
        'const launch = document.getElementById("launch");'
        'const manifest = new URL("latest.json", location.href);'
        'manifest.searchParams.set("v", Date.now());'
        'fetch(manifest, {cache:"no-store", signal:AbortSignal.timeout(5000)})'
        '.then(response => {if (!response.ok) throw new Error("Beta manifest unavailable"); return response.json();})'
        '.then(({release}) => {if (/^last-reading-beta-[0-9]{8}-[0-9]{6}$/.test(release)) launch.href = "./" + release + "/";})'
        '.catch(() => {}).finally(() => location.replace(launch.href));'
        '</script>',
        encoding="utf-8",
    )
    print(json.dumps(result))
