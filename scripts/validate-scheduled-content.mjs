import { readdir, readFile, access } from 'node:fs/promises';
import { join } from 'node:path';

const root = new URL('..', import.meta.url).pathname.replace(/^\/(.:)/, '$1');
const contentDir = join(root, 'src', 'content', 'insights');
const files = (await readdir(contentDir)).filter(name => /^ay-sea-2026-.*\.md$/.test(name));
const seenIds = new Set();
const seenSlugs = new Set();
const errors = [];
const field = (frontmatter, name) => frontmatter.match(new RegExp(`^${name}:\\s*["']?(.*?)["']?\\s*$`, 'm'))?.[1] || '';

for (const name of files) {
  const text = await readFile(join(contentDir, name), 'utf8');
  const frontmatter = text.match(/^---\s*\n([\s\S]*?)\n---/)?.[1] || '';
  const record = Object.fromEntries(['content_id','status','slug','publish_at','featured_image','image_status','fact_check_status','alan_approval'].map(key => [key, field(frontmatter, key)]));
  for (const key of ['content_id','slug','publish_at','featured_image']) if (!record[key]) errors.push(`${name}: missing ${key}`);
  if (!['scheduled','published'].includes(record.status)) errors.push(`${name}: invalid status`);
  if (record.image_status !== 'ready') errors.push(`${name}: image not ready`);
  if (record.fact_check_status !== 'verified') errors.push(`${name}: fact check not verified`);
  if (record.alan_approval !== 'approved') errors.push(`${name}: Alan approval missing`);
  if (Number.isNaN(Date.parse(record.publish_at))) errors.push(`${name}: invalid publish_at`);
  if (seenIds.has(record.content_id)) errors.push(`${name}: duplicate content_id`); else seenIds.add(record.content_id);
  if (seenSlugs.has(record.slug)) errors.push(`${name}: duplicate slug`); else seenSlugs.add(record.slug);
  if (record.featured_image) try { await access(join(root, 'public', record.featured_image.replace(/^\//, ''))); } catch { errors.push(`${name}: image not found`); }
}

if (files.length !== 16) errors.push(`Expected 16 scheduled articles, found ${files.length}`);
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
console.log(`Validated ${files.length} scheduled articles with unique IDs, dates, approvals and images.`);
