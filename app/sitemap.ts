import type { MetadataRoute } from 'next';
import { absoluteUrl } from '@/lib/metadata';
import { source } from '@/lib/source';

export default function sitemap(): MetadataRoute.Sitemap {
  const docs = source.getPages().map((page) => ({
    url: absoluteUrl(page.url),
    changeFrequency: 'weekly' as const,
    // The docs landing page outranks section indexes, which outrank leaves.
    priority: page.url === '/docs' ? 0.9 : page.slugs.length > 1 ? 0.7 : 0.8,
  }));

  return [
    {
      url: absoluteUrl('/'),
      changeFrequency: 'monthly' as const,
      priority: 1,
    },
    ...docs,
  ];
}
