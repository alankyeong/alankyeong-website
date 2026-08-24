# alankyeong.com

Deployment-ready static website for Hostinger. Astro builds every page from reusable layouts and structured Markdown content. WordPress is not required.

## Publish an article

1. Run `npm run new:article -- "Your article title"`.
2. Edit the new file in `src/content/insights/`.
3. Complete its title, description, category, tags and article body.
4. Change `draft: true` to `draft: false` after approval.
5. Commit and push. The deployment workflow can build and upload the resulting `dist/` folder.

Existing articles are safe to use as templates. No page code is required for routine publishing.

## Import a scheduled article package

The website also accepts the structured publishing-package format used by the September–October 2026 content cycle. Copy approved Markdown files into `src/content/insights/` and their WebP assets into `public/assets/images/insights/`.

The content schema supports both the original article-template fields and the automation fields including `slug`, `excerpt`, `publish_at`, `featured_image`, `featured_image_alt`, `meta_title`, `meta_description`, `fact_check_status`, `alan_approval` and `image_status`.

Staging builds created with `PUBLIC_SITE_ENV=staging` include draft articles with a visible Preview Draft badge and site-wide `noindex`. Production builds exclude records where `status: draft` or `draft: true` remains set. Change publication and approval statuses only after editorial review.

For Hostinger staging when Astro compilation is unavailable locally, run `scripts/import_articles_to_preview.py`. It regenerates `preview_dist/`, imports the scheduled drafts and images, and retains staging `noindex` protection.

## Local preview and production build

```text
npm install
npm run dev
npm run build
```

The production website is generated in `dist/`. Upload the contents of `dist/` to Hostinger's `public_html` folder, preserving the `api/` folder.

## Production configuration

Copy `.env.example` to `.env` for local builds and replace placeholders with approved values. Configure the same values in the build service:

- `PUBLIC_GA4_ID`: dedicated alankyeong.com GA4 measurement ID.
- `PUBLIC_LINKEDIN_URL`: approved public LinkedIn profile.
- `PUBLIC_STRIPE_URL`: existing Stripe Payment Link or Checkout URL.
- `PUBLIC_AI_SITE_URL`: defaults to the separate `https://ai.alankyeong.com/` property.

On Hostinger, confirm PHP mail delivery for `public/api/contact.php` and set `CONTACT_TO` where supported. If the hosting plan does not expose environment variables, replace the fallback recipient in that file before deployment. Add server-side spam protection or a transactional email provider before public launch if form abuse becomes material.

## Git-based deployment

Recommended flow: GitHub repository → GitHub Actions build → Hostinger deployment. Store Hostinger credentials only as encrypted repository secrets. Never commit them.

The launch sequence is documented in `docs/DEPLOYMENT.md`.

Scheduled article activation and required GitHub/Hostinger secrets are documented in `docs/SCHEDULED_PUBLISHING.md`.
