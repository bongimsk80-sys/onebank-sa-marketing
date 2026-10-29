# OneView — marketing website

Static site served by Netlify. Pages are generated from `tools/build.py` so the header, footer and metadata stay identical everywhere.

## Edit and build

```bash
python3 tools/build.py          # writes index.html, product/, security/, pricing/, about/, faq/, demo/, legal/, 404, sitemap, robots
python3 -m http.server 8080     # preview at http://localhost:8080
```

Commit the generated files. Pushing to `main` runs `.github/workflows/deploy.yml`, which uploads every site file to Netlify.

## Settings to check before going live

| Setting | Where | Now |
| --- | --- | --- |
| Site URL (canonical links, sitemap, social image) | `SITE_URL` in `tools/build.py` | `https://onebank-sa.netlify.app` |
| App URL (sign-in links, demo form endpoint) | `APP_URL` in `tools/build.py` and `connect-src` in `netlify.toml` | `https://onebank-sa-iota.vercel.app` |
| Contact, security and privacy mailboxes | `CONTACT`, `SECURITY`, `PRIVACY` in `tools/build.py` | `@oneview.co.za` addresses; the domain must be registered and the mailboxes working |
| Allowed form origin | `MARKETING_ORIGINS` in the app's environment | must include the site URL |

## Demo form

The form posts JSON to the app's `POST /api/enquiries`, which validates the fields, requires privacy consent, ignores bots that fill the hidden field, throttles repeat submissions and stores the enquiry in the app database. The page shows the real result, including errors.

## Content rules

- Label every feature Live in beta, In integration, In development or Planned. Do not call anything live that customers cannot use.
- Never present simulated payments as transaction volume or GMV.
- Do not use the word "bank" in the company or product name (Banks Act s22(5)).
