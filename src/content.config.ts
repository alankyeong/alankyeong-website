import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const insights = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/insights' }),
  schema: z.object({
    content_id: z.string().optional(),
    status: z.enum(['draft', 'scheduled', 'published', 'archived']).optional(),
    title: z.string(),
    slug: z.string().optional(),
    description: z.string().optional(),
    excerpt: z.string().optional(),
    publishDate: z.coerce.date().optional(),
    publish_at: z.string().optional(),
    updatedDate: z.coerce.date().optional(),
    category: z.string(),
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    draft: z.boolean().default(false),
    image: z.string().optional(),
    featured_image: z.string().optional(),
    imageAlt: z.string().optional(),
    featured_image_alt: z.string().optional(),
    canonical: z.string().url().optional(),
    canonical_url: z.string().url().optional(),
    meta_title: z.string().optional(),
    meta_description: z.string().optional(),
    author: z.string().default('Alan Yeong'),
    fact_check_status: z.enum(['pending-verification', 'verified']).optional(),
    alan_approval: z.enum(['pending', 'approved', 'rejected']).optional(),
    image_status: z.enum(['pending', 'ready']).optional(),
  }).refine(data => Boolean(data.description || data.excerpt), {
    message: 'An insight requires description or excerpt.',
  }).refine(data => Boolean(data.publishDate || data.publish_at), {
    message: 'An insight requires publishDate or publish_at.',
  }),
});

export const collections = { insights };
