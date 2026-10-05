import fs from 'node:fs';
import path from 'node:path';
const build = path.resolve(process.argv[2] ?? 'private-game/dist');
const output = path.resolve(process.argv[3] ?? '_site');
if (fs.existsSync(output)) throw Error('Output directory must be fresh');
const allowed = /^(index\.html|favicon\.svg|assets\/[\w-]+\.(js|css)|art\/(?:[\w-]+\/)*[\w.-]+\.(png|ttf|txt)|audio\/[\w-]+\.mp3)$/;
function audit(directory, prefix = '') {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const relative = prefix + entry.name;
    if (entry.isSymbolicLink()) throw Error('Symlink rejected: ' + relative);
    if (entry.isDirectory()) audit(path.join(directory, entry.name), relative + '/');
    else {
      if (!entry.isFile() || !allowed.test(relative)) throw Error('Unexpected build file: ' + relative);
      if (/\.(js|css)$/.test(relative) && /sourceMappingURL/.test(fs.readFileSync(path.join(directory, entry.name), 'utf8'))) throw Error('Source map reference rejected: ' + relative);
    }
  }
}
audit(build);
if (!fs.existsSync(path.join(build, 'index.html'))) throw Error('Game entry point missing');
fs.mkdirSync(output, { recursive: true });
// Explicit website allowlist: never publish the checkout or private source tree.
for (const file of ['index.html', 'styles.css', 'demo.js', 'robots.txt', 'sitemap.xml', 'CNAME', '.nojekyll']) fs.copyFileSync(file, path.join(output, file));
fs.cpSync('assets', path.join(output, 'assets'), { recursive: true });
// Only the reviewed policy assets, not arbitrary files below the website checkout.
fs.mkdirSync(path.join(output, 'stealthmate/policy'), { recursive: true });
for (const file of ['index.html', 'policy.css']) fs.copyFileSync(path.join('stealthmate/policy', file), path.join(output, 'stealthmate/policy', file));
fs.cpSync(build, path.join(output, 'play/stealthmate'), { recursive: true });
console.log('Public artifact assembled: website files and production game only.');
