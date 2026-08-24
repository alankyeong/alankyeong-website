import { defineConfig } from 'astro/config';
import { join } from 'node:path';
import sitemap from '@astrojs/sitemap';
export default defineConfig({site:'https://alankyeong.com',output:'static',devToolbar:{enabled:false},integrations:[sitemap()],build:{assets:'assets'},vite:{cacheDir:join(process.env.TEMP||'work','alankyeong-vite-cache'),build:{cssMinify:true}}});
