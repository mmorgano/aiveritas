import type { PropsWithChildren } from "react";

export default function Layout({ children }: PropsWithChildren) {
  return (
    <div className="app-shell">
      <header className="hero">
        <p className="eyebrow">GUI Preview</p>
        <h1>AIVeritas GUI</h1>
        <p className="hero-copy">
          Lightweight frontend shell for CSV validation, report summaries, and
          recent activity.
        </p>
      </header>
      <main className="content-grid">{children}</main>
    </div>
  );
}
