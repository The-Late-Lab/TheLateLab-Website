# Website deployment

The public repository contains the marketing site and deployment tooling. The game
source remains in the private `The-Late-Lab/Stealthmate-Tiny` repository. Production
JavaScript, fonts, sprites and audio are downloadable by players, as required for a
browser game; authored TypeScript, tests, source maps and Git history are not deployed.

The homepage embeds the demo after the visitor presses **Launch demo**. Its standalone,
shareable URL is `https://thelatelab.com/play/stealthmate/`. Both use the same browser-local
progress. Fullscreen has a standalone-page fallback.

## Publish

GitHub Pages uses **GitHub Actions**, not a published branch. On website pushes to `main`
or a manual dispatch, `.github/workflows/deploy.yml`:

1. Checks out the website and the private game's `main` using a read-only SSH deploy key.
2. Builds the game for `/play/stealthmate/`, without source maps.
3. Runs `tools/assemble-site.mjs` to allowlist the production game files and assemble `_site/`.
4. Uploads only `_site/` as the Pages artifact and deploys it to the existing domain.

No compiled game files are committed to this public repository. The checkout credentials
are not persisted. The workflow does not run on pull requests. Its deploy environment is
`github-pages`; the secret `STEALTHMATE_DEPLOY_KEY` grants read-only access to the game repo.

Website updates deploy automatically. To publish a newer private game release without
changing the website:

```sh
gh workflow run deploy.yml --repo The-Late-Lab/TheLateLab-Website --ref main
```

Revoke the deploy key in the private repo's Settings → Deploy keys and remove the website
secret if this integration is retired. Never add a GitHub token or private key to site files.

## Local verification

## Unlisted micro-demo beta

`https://thelatelab.com/play/stealthmatebeta/` contains the reviewed beta commit pinned in
the deployment workflow. Production still builds the private game's `main` separately.
The beta is not linked in navigation or the sitemap and has `noindex, nofollow` metadata.
This is an unlisted public URL, not authentication: anyone with the URL can play it.
Promoting a beta requires an explicit production release; deploying the website does not
replace the normal micro-demo with beta code.

## Local verification

Build the private game with `VITE_PUBLIC_BASE=/play/stealthmate/`, then from this repo:

```sh
node tools/assemble-site.mjs /absolute/path/to/Stealthmate-Tiny/dist _site
python -m http.server 4160 --directory _site
```

Open `http://localhost:4160/` and `/play/stealthmate/`. Use a fresh output directory for each
assembly. `_site/` and `private-game/` are ignored by Git.
