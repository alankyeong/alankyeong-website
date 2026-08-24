# Hostinger deployment and migration runbook

## Before cutover

1. Export a full WordPress backup, including files and database.
2. Record current DNS, SSL, redirects, analytics, Search Console, Stripe destinations and form recipients.
3. Export current WordPress URLs and create redirects for any URL that changes.
4. Verify the approved LinkedIn URL, Stripe link, GA4 ID, enquiry recipient and any biographical claims.
5. Keep `ai.alankyeong.com` unchanged. Do not alter its DNS, files, forms, analytics or routing.

## Build and stage

1. Install dependencies with `npm install`.
2. Create `.env` from `.env.example` and add approved public configuration.
3. Run `npm run build`.
4. Upload the contents of `dist/` to a staging subdomain or temporary Hostinger directory.
5. Verify all routes, mobile layouts, metadata, sitemap, robots file, outbound links, Stripe flow and the form's email delivery and redirect.

## Production cutover

1. Put the current WordPress site into a short maintenance window.
2. Preserve the backup outside `public_html`.
3. Replace the main-domain files with the contents of `dist/`.
4. Confirm SSL, the canonical host and HTTP-to-HTTPS redirects.
5. Test the production root route, at least two articles, contact form, thank-you page, Stripe destination and external AI link.
6. Submit `https://alankyeong.com/sitemap-index.xml` in Search Console.

## Acceptance checks

- No WordPress admin or database is required for the public site.
- Page titles, descriptions, canonical URLs, Open Graph fields and Article schema are present.
- Article files marked `draft: true` are excluded.
- Enquiry emails arrive and contain no data in analytics.
- The Stripe link reaches the approved purchase flow.
- Images are WebP/AVIF where used, correctly sized, and have meaningful alt text.
- Keyboard navigation, focus states, headings and contrast are reviewed.
- `ai.alankyeong.com` remains unchanged and separately measured.

## Rollback

If a material production issue occurs, restore the saved WordPress files and database, then re-test the main domain. Do not change the AI subdomain during rollback.
