import type { RecentReportItem } from "../api";

interface RecentReportsProps {
  activeReportId: string | null;
  isLoading: boolean;
  onReopen: (reportId: string) => Promise<void>;
  reports: RecentReportItem[];
}

export default function RecentReports({
  activeReportId,
  isLoading,
  onReopen,
  reports,
}: RecentReportsProps) {
  return (
    <section className="panel">
      <div className="section-heading">
        <h2>Recent Reports</h2>
        <p>Stored runs exposed by the backend history endpoint.</p>
      </div>
      {isLoading ? (
        <p className="empty-state">Loading recent reports...</p>
      ) : null}
      {!isLoading && reports.length > 0 ? (
        <ul className="report-list">
          {reports.map((report) => {
            const isActive = activeReportId === report.id;

            return (
              <li key={report.id}>
                <strong>{report.filename}</strong>
                <span>{report.createdAt}</span>
                <span>{report.runStatus}</span>
                <button
                  disabled={isActive}
                  onClick={() => {
                    void onReopen(report.id);
                  }}
                  type="button"
                >
                  {isActive ? "Opening..." : `Reopen ${report.filename}`}
                </button>
              </li>
            );
          })}
        </ul>
      ) : null}
      {!isLoading && reports.length === 0 ? (
        <p className="empty-state">No recent reports available.</p>
      ) : null}
    </section>
  );
}
