import Link from 'next/link';
import Image from 'next/image';
import type { Metadata } from 'next';
import {
  BadgeCheck,
  Code,
  Database,
  Download,
  Gauge,
  Grid3x3,
  Brain,
  Rocket,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

export const metadata: Metadata = {
  title: 'GPandas - Data Manipulation for Go',
  description:
    'A high-performance data manipulation and analysis library for Go',
};

const features: {
  title: string;
  description: string;
  icon: LucideIcon;
}[] = [
  {
    title: 'High Performance',
    icon: Gauge,
    description:
      "Leverages Go's concurrency model with worker pools for parallel CSV parsing and efficient columnar storage architecture.",
  },
  {
    title: 'Familiar API',
    icon: Brain,
    description:
      'Pandas-inspired API with DataFrame, Series, and intuitive methods like Read_csv(), Merge(), Select(), Loc(), and iLoc().',
  },
  {
    title: 'Type Safe',
    icon: BadgeCheck,
    description:
      'Strong type support through Series-level dtype enforcement ensuring data integrity across all operations.',
  },
  {
    title: 'SQL Integration',
    icon: Database,
    description:
      'Built-in support for SQL databases and Google BigQuery with Read_sql() and From_gbq() functions.',
  },
  {
    title: 'Flexible Indexing',
    icon: Grid3x3,
    description:
      'Label-based (Loc) and position-based (iLoc) indexing for intuitive data access, just like pandas.',
  },
  {
    title: 'Easy Export',
    icon: Download,
    description:
      'Export DataFrames to CSV format with customizable separators. Write to files or get string output directly.',
  },
];

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col">
      <section className="mx-auto flex w-full max-w-5xl flex-col items-center gap-10 px-4 py-20 md:flex-row md:items-center md:justify-between">
        <div className="flex flex-col items-center gap-6 text-center md:items-start md:text-left">
          <span className="rounded-full bg-fd-primary/10 px-3 py-1 text-xs font-medium text-fd-primary">
            v1.0
          </span>
          <h1 className="text-5xl font-bold tracking-tight sm:text-6xl">
            GPandas
          </h1>
          <p className="max-w-3xl text-lg text-fd-muted-foreground">
            A high-performance data manipulation and analysis library for Go,
            inspired by Python&apos;s pandas. Work with DataFrames, read CSV
            files, query databases, and perform complex data operations with
            ease.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3 md:justify-start">
            <Link
              href="/docs"
              className="inline-flex items-center gap-2 rounded-lg bg-fd-primary px-5 py-2.5 text-sm font-medium text-fd-primary-foreground transition-opacity hover:opacity-90"
            >
              <Rocket className="size-4" aria-hidden="true" />
              Get Started
            </Link>
            <a
              href="https://github.com/apoplexi24/gpandas"
              className="inline-flex items-center gap-2 rounded-lg border border-fd-border px-5 py-2.5 text-sm font-medium transition-colors hover:bg-fd-accent"
            >
              <Code className="size-4" aria-hidden="true" />
              View on GitHub
            </a>
          </div>
          <p className="text-sm text-fd-muted-foreground">
            <strong className="font-semibold text-fd-foreground">
              Open Source
            </strong>{' '}
            Apache 2.0 Licensed | Built with Go
          </p>
        </div>
        <Image
          src="/images/gpandas.png"
          alt="GPandas DataFrame"
          width={1200}
          height={630}
          priority
          sizes="(min-width: 768px) 20vw, 45vw"
          className="h-auto w-full max-w-[45%] shrink-0 rounded-xl border border-fd-border shadow-lg md:max-w-[20%]"
        />
      </section>

      <section className="mx-auto w-full max-w-5xl px-4 pb-24">
        <div className="mb-10 text-center">
          <h2 className="text-3xl font-bold tracking-tight">Why GPandas?</h2>
          <p className="mx-auto mt-3 max-w-2xl text-fd-muted-foreground">
            GPandas brings the power of pandas-style data manipulation to Go
            with blazing performance and type safety.
          </p>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {features.map(({ title, description, icon: Icon }) => (
            <div
              key={title}
              className="rounded-xl border border-fd-border bg-fd-card p-5"
            >
              <Icon
                className="size-5 text-fd-primary"
                aria-hidden="true"
              />
              <h3 className="mt-3 font-semibold">{title}</h3>
              <p className="mt-1.5 text-sm text-fd-muted-foreground">
                {description}
              </p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
