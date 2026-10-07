import fs from 'node:fs';
import path from 'node:path';
const build = path.resolve(process.argv[2] ?? 'private-game/dist');
const output = path.resolve(process.argv[3] ?? '_site');
const betaOnly = process.argv[4] === '--beta-only';
if (!betaOnly && fs.existsSync(output)) throw Error('Output directory must be fresh');
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
if (betaOnly) {
  if (!fs.existsSync(path.join(output, 'play/stealthmate/index.html'))) throw Error('Assemble production first');
  const destination = path.join(output, 'play/stealthmatebeta');
  if (fs.existsSync(destination)) throw Error('Beta destination must be fresh');
  fs.cpSync(build, destination, { recursive: true });
  const entry = path.join(destination, 'index.html');
  fs.writeFileSync(entry, fs.readFileSync(entry, 'utf8').replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow">'));
  console.log('Unlisted beta added; production runtime unchanged.');
  process.exit(0);
}
fs.mkdirSync(output, { recursive: true });
// Explicit website allowlist: never publish the checkout or private source tree.
for (const file of ['index.html', 'styles.css', 'demo.js', 'robots.txt', 'sitemap.xml', 'CNAME', '.nojekyll']) fs.copyFileSync(file, path.join(output, file));
fs.cpSync('assets', path.join(output, 'assets'), { recursive: true });
fs.mkdirSync(path.join(output, 'stealthmate'), { recursive: true });
fs.copyFileSync('stealthmate/index.html', path.join(output, 'stealthmate/index.html'));
// Only the reviewed policy assets, not arbitrary files below the website checkout.
fs.mkdirSync(path.join(output, 'stealthmate/policy'), { recursive: true });
for (const file of ['index.html', 'policy.css']) fs.copyFileSync(path.join('stealthmate/policy', file), path.join(output, 'stealthmate/policy', file));
fs.cpSync(build, path.join(output, 'play/stealthmate'), { recursive: true });
// Publish only reviewed press files, not working notes or the older draft ZIP.
fs.mkdirSync(path.join(output, 'stealthmate/press'), { recursive: true });
for (const file of ['index.html', 'press.css', 'next-fest-2026-en.png', 'stealthmate-press-kit.zip']) fs.copyFileSync(path.join('stealthmate/press', file), path.join(output, 'stealthmate/press', file));
console.log('Public artifact assembled: website files and production game only.');
