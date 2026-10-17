# Homepage source

Edit `home-template.html`, then run `node _site-src/build-home.mjs` from the repository root.
The builder uses only Node.js built-ins and produces the French homepage plus `/en/` and `/es/` with their own canonical URLs, language links, metadata, and visible translated copy. It also updates the language links and authorship data in the three service pages.

The `_site-src` directory is excluded by GitHub Pages' default Jekyll processing. These source files are for maintenance; they are not additional pages in the sitemap.

Legacy `?lang=en`, `?lang=es`, and language-specific section links still lead to the corresponding language page. Contact categories, Formspree, email, telephone, and WhatsApp remain supported.
