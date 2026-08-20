# Stealthmate Website

Static GitHub Pages website for **Stealthmate — A Chess Puzzle**.

The site intentionally has no build step or JavaScript framework. It is plain HTML/CSS, uses the supplied Stealthmate logo, and embeds the current itch.io browser build.

## Repository contents

```text
.
├── index.html
├── styles.css
├── CNAME
├── .nojekyll
├── robots.txt
├── sitemap.xml
└── assets/
    ├── stealthmate-logo.png
    ├── favicon.png
    └── social-preview.jpg
```

## Run locally

Any static server works. For example:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

## GitHub Pages

Recommended repository name:

`The-Late-Lab/Stealthmate-Website`

Make the repository **public** unless the organization has a GitHub plan that supports Pages from private repositories.

In GitHub:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select the default branch (normally `main`) and `/ (root)`.
4. Save.
5. Set **Custom domain** to `thelatelab.com`.
6. When DNS has propagated and GitHub makes the option available, enable **Enforce HTTPS**.

`CNAME` is already included with `thelatelab.com`.

## Hostinger DNS for `thelatelab.com`

Before changing DNS, remove or replace any conflicting `A`, `AAAA`, `ALIAS`, or `ANAME` records for the root (`@`) that point somewhere else.

Add these four `A` records:

| Type | Name | Points to |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

For `www`, add:

| Type | Name | Target |
|---|---|---|
| CNAME | www | the-late-lab.github.io |

Use Hostinger's default TTL unless you have a reason to change it.

GitHub also supports AAAA records for IPv6, but they are optional for this setup.

DNS changes can take time to propagate.

## itch.io embed

The page currently embeds:

```html
<iframe
  src="https://itch.io/embed-upload/18809896?color=333333"
  title="Play Stealthmate"
  allowfullscreen
></iframe>
```

Direct fallback:

`https://thelatelab.itch.io/stealthmate`

## Updating the public copy

The current page copy is based on the game's existing design documentation:

- compact turn-based stealth puzzle
- familiar chess movement
- predictable enemy patrols / threats
- extraction through green exits
- campaign and Daily Challenges

Keep the marketing copy player-facing; implementation details belong in the game repository.
