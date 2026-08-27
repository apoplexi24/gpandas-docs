import type { MetadataRoute } from 'next';
import { absoluteUrl, baseUrl } from '@/lib/metadata';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        // The search endpoint returns JSON and has no crawl value.
        disallow: ['/api/'],
      },
    ],
    sitemap: absoluteUrl('/sitemap.xml'),
    host: baseUrl.origin,
  };
}
