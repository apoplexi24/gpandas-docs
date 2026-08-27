import './global.css';
import { RootProvider } from 'fumadocs-ui/provider/next';
import { Inter } from 'next/font/google';
import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { baseUrl } from '@/lib/metadata';

const inter = Inter({
  subsets: ['latin'],
});

const description =
  "A high-performance data manipulation and analysis library for Go, inspired by Python's pandas";

export const metadata: Metadata = {
  metadataBase: baseUrl,
  title: {
    default: 'GPandas',
    template: '%s | GPandas',
  },
  description,
  applicationName: 'GPandas Documentation',
  keywords: [
    'gpandas',
    'go',
    'golang',
    'dataframe',
    'pandas',
    'data analysis',
    'data manipulation',
  ],
  openGraph: {
    type: 'website',
    siteName: 'GPandas',
    title: 'GPandas',
    description,
    url: baseUrl,
    images: '/images/gpandas.png',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'GPandas',
    description,
    images: '/images/gpandas.png',
  },
};

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={inter.className} suppressHydrationWarning>
      <body className="flex flex-col min-h-screen">
        <RootProvider>{children}</RootProvider>
      </body>
    </html>
  );
}
