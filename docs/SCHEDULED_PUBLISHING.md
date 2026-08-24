# Scheduled publishing activation

## What the workflow does

GitHub Actions runs every day at 01:05 UTC, shortly after 09:00 in Malaysia. It validates all scheduled content, builds the static production website and uploads updated public files to Hostinger. A scheduled article is included only when all of these are true:

- `status` is `scheduled` or `published`;
- `alan_approval` is `approved`;
- `fact_check_status` is `verified`;
- `image_status` is `ready`;
- `publish_at` has arrived.

Future articles do not have public production routes before their dates. The Insights library and sitemap are rebuilt when an article becomes eligible.

## GitHub setup

1. Create a private GitHub repository and upload this source code.
2. Open **Settings → Secrets and variables → Actions**.
3. Add these repository secrets:
   - `HOSTINGER_SFTP_HOST`
   - `HOSTINGER_SFTP_PORT`
   - `HOSTINGER_SFTP_USERNAME`
   - `HOSTINGER_SFTP_PASSWORD`
   - `HOSTINGER_SFTP_PATH` with the value `/public_html`
4. Keep analytics disabled for now. Do not add a GA4 secret until cookie consent has been implemented.
5. Open **Actions → Publish scheduled articles → Run workflow** for the first controlled test.

## Hostinger setup

Enable Hostinger SFTP/SSH remote access and use its dedicated connection details. Do not use or expose the hPanel login password. The deployment uploads and updates generated website files but deliberately does not delete remote-only folders, so `.private`, `ai` and `preview` remain untouched.

## Operating rules

- To hold an article, change `status` to `draft` or `alan_approval` to `pending`.
- To reschedule, edit `publish_at` with the `+08:00` timezone offset.
- Commit and push the content change before its scheduled date.
- A failed validation stops deployment and leaves the live website unchanged.
- After a successful run, verify the article URL, Insights page and sitemap.

## Rollback

Revert the relevant Git commit and run the workflow manually. Because the safe deployment does not delete remote-only files, removal of an already-published article requires a deliberate Hostinger cleanup after the rollback build is deployed.
