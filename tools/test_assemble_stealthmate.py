"""Fresh Unity templates and already-versioned players must resolve moved assets."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


class StealthmateAssemblyTests(unittest.TestCase):
    def test_loader_and_streaming_urls_follow_immutable_directories(self):
        script = Path(__file__).with_name('assemble-stealthmate.py').resolve()
        release = 'stealthmate-beta-regression'
        for preversioned in (False, True):
            with self.subTest(preversioned=preversioned), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / 'betas').mkdir()
                (root / 'site').mkdir()
                (root / 'site/index.html').write_text('site')
                prefix = release + '/' if preversioned else ''
                html = ('<meta name="robots" content="noindex, nofollow">'
                        f'<script>var buildUrl = "{prefix}Build";'
                        f'var config = {{streamingAssetsUrl: "{prefix}StreamingAssets"}};</script>')
                archive = root / 'player.zip'
                with zipfile.ZipFile(archive, 'w') as output:
                    output.writestr('index.html', html)
                    output.writestr('Build/player.loader.js', 'loader')
                    output.writestr('StreamingAssets/catalog.json', '{}')
                manifest = dict(release=release, asset=archive.name,
                                sha256=hashlib.sha256(archive.read_bytes()).hexdigest())
                (root / 'betas/stealthmate_paper.release.json').write_text(json.dumps(manifest))
                subprocess.run([sys.executable, str(script), str(archive), 'site', '--paper'],
                               cwd=root, check=True, capture_output=True)
                page = root / 'site/betas/stealthmate_paper'
                result = (page / 'index.html').read_text()
                self.assertIn(f'"{release}/Build"', result)
                self.assertIn(f'"{release}/StreamingAssets"', result)
                self.assertTrue((page / release / 'Build/player.loader.js').is_file())
                self.assertTrue((page / release / 'StreamingAssets/catalog.json').is_file())


if __name__ == '__main__':
    unittest.main()
