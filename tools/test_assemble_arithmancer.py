import hashlib
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('assembler', Path(__file__).with_name('assemble-arithmancer.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ArithmancerAssemblyTests(unittest.TestCase):
    def attempt(self, extra=None, bad_hash=False):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            site = root/'site';site.mkdir();(site/'index.html').write_text('Production')
            archive = root/'player.zip'
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('index.html','<meta name="robots" content="noindex, nofollow"><script>matchWebGLToCanvasSize: true</script>')
                z.writestr('Build/game.loader.js','loader')
                z.writestr('Build/game.wasm.unityweb',b'compressed wasm')
                if extra:z.writestr(extra,'invalid')
            manifest={'sha256':'bad' if bad_hash else hashlib.sha256(archive.read_bytes()).hexdigest(),'release':'test'}
            result=module.assemble(archive,site,manifest)
            self.assertEqual((site/'index.html').read_text(),'Production')
            self.assertTrue((site/'betas/arithmancer/index.html').is_file())
            return result

    def test_valid_player_preserves_existing_site(self):
        self.assertEqual(self.attempt()['files'],3)

    def test_checksum_rejected(self):
        with self.assertRaisesRegex(ValueError,'checksum'):self.attempt(bad_hash=True)

    def test_path_traversal_rejected(self):
        with self.assertRaisesRegex(ValueError,'Unsafe'):self.attempt('../index.html')

    def test_private_source_rejected(self):
        with self.assertRaisesRegex(ValueError,'Unexpected'):self.attempt('Build/source.cs')

    def test_debug_symbols_rejected(self):
        with self.assertRaisesRegex(ValueError,'Unexpected'):self.attempt('Build/game.symbols.json')


if __name__=='__main__':unittest.main()
