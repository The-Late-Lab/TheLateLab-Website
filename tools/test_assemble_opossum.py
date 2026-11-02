import hashlib
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('assembler', Path(__file__).with_name('assemble-opossum.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OpossumAssemblyTests(unittest.TestCase):
    def attempt(self, extra=None, bad_hash=False, html=None):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            site = root/'site';site.mkdir();(site/'index.html').write_text('Production')
            archive = root/'player.zip'
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('index.html',html if html is not None else '<meta name="robots" content="noindex, nofollow"><script>matchWebGLToCanvasSize: true</script>')
                z.writestr('Build/game.loader.js','loader')
                z.writestr('Build/game.wasm.unityweb',b'compressed wasm')
                if extra:z.writestr(extra,'invalid')
            manifest={'sha256':'bad' if bad_hash else hashlib.sha256(archive.read_bytes()).hexdigest(),'release':'test'}
            result=module.assemble(archive,site,manifest)
            self.assertEqual((site/'index.html').read_text(),'Production')
            self.assertTrue((site/'classes/opossum-atelier/index.html').is_file())
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

    def test_bounded_manual_canvas_preserves_existing_site(self):
        html = ('noindex, nofollow; matchWebGLToCanvasSize: false; function resizePlayer(); '
                '1920/Math.max(1,box.width); 1080/Math.max(1,box.height); '
                'new ResizeObserver(resizePlayer).observe(canvas); canvas.width=width;canvas.height=height;')
        self.assertEqual(self.attempt(html=html)['files'],3)

    def test_unbounded_manual_canvas_rejected(self):
        with self.assertRaisesRegex(ValueError,'canvas configuration'):
            self.attempt(html='noindex, nofollow; matchWebGLToCanvasSize: false')

    def test_indexable_player_rejected(self):
        with self.assertRaisesRegex(ValueError,'indexing policy'):
            self.attempt(html='matchWebGLToCanvasSize: true')


if __name__=='__main__':unittest.main()
