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

function renderIssueScope(summary: ValidationSummary, issueIndex: number): string {
  const issue = summary.issues[issueIndex];
  const scopeParts: string[] = [];

  if (issue.columns.length > 0) {
    scopeParts.push(`columns: ${issue.columns.join(", ")}`);
  }

  if (issue.rowIndices.length > 0) {
    scopeParts.push(`rows: ${issue.rowIndices.join(", ")}`);
  }

  return scopeParts.join(" | ");
}

export default function ResultSummary({ summary }: ResultSummaryProps) {
  return (
    <section className="panel">
      <div className="section-heading">
        <h2>Latest Summary</h2>
        <p>Shows the latest report returned by the backend.</p>
      </div>
      {summary ? (
        <>
          <dl className="summary-list">
            <div className="summary-row">
              <dt>Report ID</dt>
              <dd>{summary.reportId}</dd>
            </div>
            <div className="summary-row">
              <dt>Input file</dt>
              <dd>{summary.inputName || "Unavailable"}</dd>
            </div>
            <div className="summary-row">
              <dt>Generated at</dt>
              <dd>{summary.createdAt || "Unavailable"}</dd>
            </div>
            <div className="summary-row">
              <dt>Run status</dt>
              <dd>{summary.runStatus}</dd>
            </div>
            <div className="summary-row">
              <dt>Validation status</dt>
              <dd>{summary.validationStatus}</dd>
            </div>
            <div className="summary-row">
              <dt>Rows</dt>
              <dd>{renderRowCount(summary.rowCount)}</dd>
            </div>
            <div className="summary-row">
              <dt>Total issues</dt>
              <dd>{summary.issueCount}</dd>
            </div>
            <div className="summary-row">
              <dt>Saved report</dt>
              <dd>
                {summary.reportDownloadUrl ? (
                  <a
                    className="report-link"
                    href={summary.reportDownloadUrl}
                    target="_blank"
                    rel="noreferrer"
                    title={summary.reportLocation || "Download JSON report"}
                  >
                    Download JSON report
                  </a>
                ) : (
                  "Unavailable"
                )}
              </dd>
            </div>
          </dl>
          <div className="details-grid">
            <div className="detail-card">
              <h3>Executed checks</h3>
              {summary.executedChecks.length > 0 ? (
                <ul className="chip-list">
                  {summary.executedChecks.map((check) => (
                    <li key={check}>{check}</li>
                  ))}
                </ul>
              ) : (
                <p className="empty-state">No checks were reported by the backend.</p>
              )}
            </div>
            <div className="detail-card">
              <h3>Issues found</h3>
              {summary.issues.length > 0 ? (
                <ul className="issue-list">
                  {summary.issues.map((issue, index) => (
                    <li key={issue.id || `${issue.code}-${index}`}>
                      <strong>{issue.id || issue.code}</strong>
                      <span>{issue.message}</span>
                      <span>{`${issue.severity} | ${issue.code}`}</span>
                      {renderIssueScope(summary, index) ? (
                        <span>{renderIssueScope(summary, index)}</span>
                      ) : null}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="empty-state">No issues were reported for this run.</p>
              )}
            </div>
          </div>
        </>
      ) : (
        <p className="empty-state">
          No validation run yet. Submit a CSV file to populate this summary.
        </p>
      )}
    </section>
  );
}
