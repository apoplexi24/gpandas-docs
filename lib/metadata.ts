/**
 * Canonical origin for the docs site.
 *
 * Set `NEXT_PUBLIC_SITE_URL` in the production environment (see `.env.example`).
 * Without it, absolute URLs in `sitemap.xml`, `robots.txt` and the Open Graph
 * tags fall back to the Vercel deployment URL, then to localhost.
 */
export const baseUrl = new URL(
  process.env.NEXT_PUBLIC_SITE_URL ??
    (process.env.VERCEL_PROJECT_PRODUCTION_URL
      ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
      : 'http://localhost:3000'),
);

export function absoluteUrl(path: string): string {
  return new URL(path, baseUrl).href;
}
