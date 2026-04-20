import { useEffect, useState } from "react";

import {
  fetchRecentReports,
  reopenReport,
  submitValidation,
  type RecentReportItem,
  type ValidationSubmission,
  type ValidationSummary,
} from "./api";
import Layout from "./components/Layout";
import RecentReports from "./components/RecentReports";
import ResultSummary from "./components/ResultSummary";
import StatusMessage from "./components/StatusMessage";
import ValidationForm from "./components/ValidationForm";
import type { StatusState } from "./types";

const INITIAL_STATUS: StatusState = {
  message: "Ready to validate a CSV sample.",
  tone: "idle",
};

function toErrorMessage(error: unknown, fallbackMessage: string): string {
  if (error instanceof Error && error.message) {
    return error.message;
  }

  return fallbackMessage;
}

export default function App() {
  const [status, setStatus] = useState<StatusState>({
    message: "Loading recent reports.",
    tone: "info",
  });
  const [summary, setSummary] = useState<ValidationSummary | null>(null);
  const [recentReports, setRecentReports] = useState<RecentReportItem[]>([]);
  const [isLoadingReports, setIsLoadingReports] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activeReportId, setActiveReportId] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadInitialReports() {
      try {
        const reports = await fetchRecentReports();
        if (!isMounted) {
          return;
        }

        setRecentReports(reports);
        setStatus(INITIAL_STATUS);
      } catch (error) {
        if (!isMounted) {
          return;
        }

        setStatus({
          message: toErrorMessage(error, "Unable to load recent reports."),
          tone: "error",
        });
      } finally {
        if (isMounted) {
          setIsLoadingReports(false);
        }
      }
    }

    void loadInitialReports();

    return () => {
      isMounted = false;
    };
  }, []);

  async function refreshRecentReports(): Promise<void> {
    setIsLoadingReports(true);

    try {
      const reports = await fetchRecentReports();
      setRecentReports(reports);
    } finally {
      setIsLoadingReports(false);
    }
  }

  async function handleValidation(submission: ValidationSubmission) {
    try {
      setIsSubmitting(true);
      setSummary(null);
      setStatus({
        message: "Validation in progress.",
        tone: "info",
      });

      const nextSummary = await submitValidation(submission);
      setSummary(nextSummary);

      try {
        await refreshRecentReports();
        setStatus({
          message: `Validation complete. ${nextSummary.issueCount} issues found.`,
          tone: "success",
        });
      } catch (error) {
        setStatus({
          message: toErrorMessage(
            error,
            "Validation finished, but recent reports could not be refreshed.",
          ),
          tone: "error",
        });
      }
    } catch (error) {
      setSummary(null);
      setStatus({
        message: toErrorMessage(error, "Validation failed."),
        tone: "error",
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleReopen(reportId: string) {
    try {
      setActiveReportId(reportId);
      setStatus({
        message: `Reopening report ${reportId}.`,
        tone: "info",
      });

      const reopenedSummary = await reopenReport(reportId);
      setSummary(reopenedSummary);
      setStatus({
        message: `Reopened report ${reportId}.`,
        tone: "success",
      });
    } catch (error) {
      setStatus({
        message: toErrorMessage(error, "Unable to reopen report."),
        tone: "error",
      });
    } finally {
      setActiveReportId(null);
    }
  }

  return (
    <Layout>
      <ValidationForm isSubmitting={isSubmitting} onSubmit={handleValidation} />
      <div className="stack">
        <StatusMessage status={status} />
        <ResultSummary summary={summary} />
        <RecentReports
          activeReportId={activeReportId}
          isLoading={isLoadingReports}
          onReopen={handleReopen}
          reports={recentReports}
        />
      </div>
    </Layout>
  );
}
