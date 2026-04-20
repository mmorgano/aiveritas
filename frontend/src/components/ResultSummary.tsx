import type { ValidationSummary } from "../api";

interface ResultSummaryProps {
  summary: ValidationSummary | null;
}

function renderRowCount(rowCount: number | null): string {
  if (rowCount === null) {
    return "Unavailable";
  }

  return String(rowCount);
}

export default function ResultSummary({ summary }: ResultSummaryProps) {
  return (
    <section className="panel">
      <div className="section-heading">
        <h2>Latest Summary</h2>
        <p>Shows the latest report returned by the backend.</p>
      </div>
      {summary ? (
        <dl className="summary-grid">
          <div>
            <dt>Report ID</dt>
            <dd>{summary.reportId}</dd>
          </div>
          <div>
            <dt>Generated at</dt>
            <dd>{summary.createdAt || "Unavailable"}</dd>
          </div>
          <div>
            <dt>Run status</dt>
            <dd>{summary.runStatus}</dd>
          </div>
          <div>
            <dt>Validation status</dt>
            <dd>{summary.validationStatus}</dd>
          </div>
          <div>
            <dt>Rows</dt>
            <dd>{renderRowCount(summary.rowCount)}</dd>
          </div>
          <div>
            <dt>Total issues</dt>
            <dd>{summary.issueCount}</dd>
          </div>
        </dl>
      ) : (
        <p className="empty-state">
          No validation run yet. Submit CSV content to populate this summary.
        </p>
      )}
    </section>
  );
}
