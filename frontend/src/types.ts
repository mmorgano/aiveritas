export type StatusTone = "idle" | "info" | "success" | "error";

export interface StatusState {
  message: string;
  tone: StatusTone;
}

export interface ValidationSubmission {
  csvText: string;
}

export interface ValidationSummary {
  reportId: string;
  totalRows: number;
  validRows: number;
  issueCount: number;
  createdAt: string;
}

export interface RecentReport {
  id: string;
  filename: string;
  createdAt: string;
  issueCount: number;
}
