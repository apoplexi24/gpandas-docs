import { HomeLayout } from 'fumadocs-ui/layouts/home';
import type { ReactNode } from 'react';
import { baseOptions } from '@/lib/layout.shared';

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <HomeLayout {...baseOptions()}>
      {children}
      <footer className="border-t border-fd-border py-8 text-center text-sm text-fd-muted-foreground">
        A product by the House of Apoplexi
      </footer>
    </HomeLayout>
  );
}
