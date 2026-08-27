import { remarkMdxMermaid } from 'fumadocs-core/mdx-plugins';
import { defineConfig } from 'fumadocs-mdx/config';

export default defineConfig({
  mdxOptions: {
    // Turns ```mermaid code fences into <Mermaid chart="..." /> elements,
    // which are rendered by the component registered in components/mdx.tsx.
    remarkPlugins: [remarkMdxMermaid],
  },
});
