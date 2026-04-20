interface BackendRecentReport {
  input_name: string;
  report_id: string;
  run_status: string;
  timestamp: string;
}

interface BackendValidationReport {
  issues?: BackendIssue[];
  dataset?: {
    loaded?: boolean;
    row_count?: number | null;
  };
  run?: {
    generated_at?: string;
    status?: string;
  };
  summary?: {
    total_issues?: number;
  };
  validation?: {
    executed_checks?: string[];
    issue_count?: number;
    status?: string;
  };
}

interface BackendIssueScope {
  columns?: string[];
  entity_keys?: Record<string, unknown>;
  row_indices?: Array<number | string>;
}

interface BackendIssue {
  code?: string;
  issue_id?: string;
  message?: string;
  scope?: BackendIssueScope;
  severity?: string;
}

interface BackendRecentReportsResponse {
  entries?: BackendRecentReport[];
}

interface BackendValidationResponse {
  report?: BackendValidationReport;
  report_id?: string;
  report_location?: string;
}

interface BackendErrorResponse {
  detail?: string;
}

export interface ValidationSubmission {
  file: File;
  keyColumns: string;
  timeColumn: string;
  valueColumn: string;
}

export interface RecentReportItem {
  createdAt: string;
  filename: string;
  id: string;
  runStatus: string;
}

export interface ValidationSummary {
  createdAt: string;
  executedChecks: string[];
  issueCount: number;
  issues: ValidationIssue[];
  inputName: string;
  reportId: string;
  reportDownloadUrl: string;
  reportLocation: string;
  rowCount: number | null;
  runStatus: string;
  validationStatus: string;
}

export interface ValidationIssue {
  code: string;
  columns: string[];
  id: string;
  message: string;
  rowIndices: Array<number | string>;
  severity: string;
}

const DEFAULT_API_BASE = "http://localhost:8000/api";

function normalizeApiBase(apiBase: string): string {
  return apiBase.replace(/\/+$/, "");
}

const API_BASE = normalizeApiBase(
  import.meta.env.VITE_API_BASE_URL?.trim() || DEFAULT_API_BASE,
);

export function buildReportDownloadUrl(reportId: string): string {
  return `${API_BASE}/reports/${reportId}/download`;
}

function parseResponseBody(bodyText: string): unknown {
  if (!bodyText) {
    return null;
  }

  try {
    return JSON.parse(bodyText) as unknown;
  } catch {
    return bodyText;
  }
}

function toErrorDetail(response: Response, data: unknown): string {
  if (
    data &&
    typeof data === "object" &&
    typeof (data as BackendErrorResponse).detail === "string"
  ) {
    return (data as BackendErrorResponse).detail;
  }

  if (typeof data === "string" && data.trim()) {
    return data.trim();
  }

  return `Request failed with status ${response.status}.`;
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, init);
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error("Unable to reach the local API. Check that make api-dev is running.");
    }

    throw error;
  }

  const bodyText = await response.text();
  const data = parseResponseBody(bodyText);

  if (!response.ok) {
    throw new Error(toErrorDetail(response, data));
  }

  return data as T;
}

function mapRecentReport(entry: BackendRecentReport): RecentReportItem {
  return {
    createdAt: entry.timestamp,
    filename: entry.input_name,
    id: entry.report_id,
    runStatus: entry.run_status,
  };
}

function mapValidationSummary(
  response: BackendValidationResponse,
): ValidationSummary {
  const report = response.report ?? {};
  const issueCount =
    report.summary?.total_issues ?? report.validation?.issue_count ?? 0;

  return {
    createdAt: report.run?.generated_at ?? "",
    executedChecks: report.validation?.executed_checks ?? [],
    inputName: report.run?.input_path?.split("/").pop() ?? "",
    issueCount,
    issues: (report.issues ?? []).map((issue) => ({
      code: issue.code ?? "unknown_issue",
      columns: issue.scope?.columns ?? [],
      id: issue.issue_id ?? "",
      message: issue.message ?? "",
      rowIndices: issue.scope?.row_indices ?? [],
      severity: issue.severity ?? "unknown",
    })),
    reportId: response.report_id ?? "",
    reportDownloadUrl: buildReportDownloadUrl(response.report_id ?? ""),
    reportLocation: response.report_location ?? "",
    rowCount:
      typeof report.dataset?.row_count === "number" ? report.dataset.row_count : null,
    runStatus: report.run?.status ?? "unknown",
    validationStatus: report.validation?.status ?? "unknown",
  };
}

export async function fetchRecentReports(): Promise<RecentReportItem[]> {
  const response = await requestJson<BackendRecentReportsResponse>(
    "/reports/recent",
  );
  return (response.entries ?? []).map(mapRecentReport);
}

export async function reopenReport(reportId: string): Promise<ValidationSummary> {
  const response = await requestJson<BackendValidationResponse>(
    `/reports/${reportId}`,
  );
  return mapValidationSummary(response);
}

export async function submitValidation(
  submission: ValidationSubmission,
): Promise<ValidationSummary> {
  const formData = new FormData();
  formData.append("file", submission.file);
  formData.append("key_columns", submission.keyColumns);
  formData.append("value_column", submission.valueColumn);
  formData.append("time_column", submission.timeColumn);

  const response = await requestJson<BackendValidationResponse>("/validate", {
    body: formData,
    method: "POST",
  });

  return mapValidationSummary(response);
}
