# amethis.io

Public landing page of Amethis — the Executable Operating Model. Static HTML, no cookies, no third-party requests.

```
src/template.html   page layout (one template for every language)
src/build.py        EN and PL content, company imprint; renders dist/index.html and dist/pl/index.html
dist/               everything that is served: assets, fonts (SIL OFL), robots.txt, sitemap.xml, 404.html
```

Build and preview locally:

```bash
python3 src/build.py
cd dist && python3 -m http.server 8000   # http://localhost:8000
```

Every push to `main` renders the pages and publishes `dist/` to GitHub Pages
(`.github/workflows/pages.yml`). The custom domain `amethis.io` is configured in the repository's Pages settings.
`dist/.htaccess` is only used if the site is ever served by Apache.
