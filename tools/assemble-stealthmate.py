"""Assemble the pinned, unlisted Stealthmate Unity player."""
from importlib import import_module
import json
from pathlib import Path
import sys
import re


if __name__ == "__main__":
    manifest = json.loads(Path("betas/stealthmate.release.json").read_text())
    release = manifest["release"]
    if not re.fullmatch(r"stealthmate-beta-[a-z0-9-]+", release):
        raise ValueError("Invalid Stealthmate release tag")
    assemble = import_module("assemble-opossum").assemble
    site = Path(sys.argv[2])
    result = assemble(sys.argv[1], site, manifest, route="betas/stealthmate",
                      require_canvas_markers=False)
    destination = site / "betas/stealthmate"
    versioned = destination / release
    versioned.mkdir()
    for directory in ("Build", "StreamingAssets"):
        (destination / directory).rename(versioned / directory)
    print(json.dumps(result))
