import "@testing-library/jest-dom/vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, vi } from "vitest";

import App from "../App";

interface MockResponseOptions {
  ok?: boolean;
  status?: number;
}

function createJsonResponse(
  body: unknown,
  options: MockResponseOptions = {},
): Response {
  return new Response(JSON.stringify(body), {
    status: options.status ?? (options.ok === false ? 500 : 200),
    headers: {
      "Content-Type": "application/json",
    },
  });
}

const fetchMock = vi.fn<typeof fetch>();

beforeEach(() => {
  fetchMock.mockReset();
  vi.stubGlobal("fetch", fetchMock);
});

afterEach(() => {
  vi.unstubAllGlobals();
});

function selectCsvFile(name = "input.csv", contents = "ID,VALUE\n1,10\n"): File {
  return new File([contents], name, { type: "text/csv" });
}

test("loads recent reports from the backend and reopens a stored report", async () => {
  fetchMock
    .mockResolvedValueOnce(
      createJsonResponse({
        entries: [
          {
            report_id: "r1",
            timestamp: "2026-04-19T08:15:00+00:00",
            input_name: "customers.csv",
            run_status: "succeeded",
          },
        ],
      }),
    )
    .mockResolvedValueOnce(
      createJsonResponse({
        report_id: "r1",
        report_location: "reports/r1.json",
        report: {
          run: {
            generated_at: "2026-04-19T08:15:00+00:00",
            status: "succeeded",
          },
          dataset: {
            loaded: true,
            row_count: 2,
          },
          validation: {
            status: "passed",
            issue_count: 0,
            executed_checks: ["missing_values", "duplicate_rows"],
          },
          summary: {
            total_issues: 0,
          },
          issues: [],
        },
      }),
    );

  render(<App />);

  expect(await screen.findByText("customers.csv")).toBeInTheDocument();

  fireEvent.click(
    screen.getByRole("button", { name: "Reopen customers.csv" }),
  );

  expect(await screen.findByText("r1")).toBeInTheDocument();
  expect(screen.getByText("passed")).toBeInTheDocument();
  expect(screen.getByText("missing_values")).toBeInTheDocument();
  expect(
    screen.getByRole("link", { name: "Download JSON report" }),
  ).toHaveAttribute("href", "http://localhost:8000/api/reports/r1/download");
  expect(screen.getByText("Reopened report r1.")).toBeInTheDocument();
});

test("submits validation to the backend and refreshes recent reports", async () => {
  fetchMock
    .mockResolvedValueOnce(createJsonResponse({ entries: [] }))
    .mockResolvedValueOnce(
      createJsonResponse({
        report_id: "r2",
        report_location: "reports/r2.json",
        report: {
          run: {
            generated_at: "2026-04-19T09:45:00+00:00",
            status: "succeeded",
          },
          dataset: {
            loaded: true,
            row_count: 3,
          },
          validation: {
            status: "failed",
            issue_count: 1,
            executed_checks: [
              "missing_values",
              "duplicate_rows",
              "numeric_outlier",
            ],
          },
          summary: {
            total_issues: 1,
          },
          issues: [
            {
              issue_id: "ISSUE-0001",
              code: "missing_values",
              message: "Missing values found in VALUE.",
              severity: "warning",
              scope: {
                columns: ["VALUE"],
                row_indices: [1],
                entity_keys: {},
              },
            },
          ],
        },
      }),
    )
    .mockResolvedValueOnce(
      createJsonResponse({
        entries: [
          {
            report_id: "r2",
            timestamp: "2026-04-19T09:45:00+00:00",
            input_name: "orders.csv",
            run_status: "succeeded",
          },
        ],
      }),
    );

  render(<App />);

  await screen.findByText("No recent reports available.");

  const fileInput = screen.getByLabelText("CSV file");
  const csvFile = selectCsvFile("orders.csv", "ID,VALUE\n1,10\n2,\n3,15");

  fireEvent.change(fileInput, {
    target: { files: [csvFile] },
  });
  fireEvent.change(screen.getByLabelText("Key columns"), {
    target: { value: "ID" },
  });

  fireEvent.click(screen.getByRole("button", { name: "Run validation" }));

  expect(await screen.findByText("Validation complete. 1 issues found.")).toBeInTheDocument();
  expect(screen.getByText("r2")).toBeInTheDocument();
  expect(await screen.findByText("orders.csv")).toBeInTheDocument();
  expect(screen.getByText("numeric_outlier")).toBeInTheDocument();
  expect(screen.getByText("Missing values found in VALUE.")).toBeInTheDocument();
  expect(
    screen.getByRole("link", { name: "Download JSON report" }),
  ).toHaveAttribute("href", "http://localhost:8000/api/reports/r2/download");

  await waitFor(() => {
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });

  const request = fetchMock.mock.calls[1];
  expect(request[0]).toBe("http://localhost:8000/api/validate");
  expect(request[1]?.method).toBe("POST");
  expect(request[1]?.body).toBeInstanceOf(FormData);

  const formData = request[1]?.body as FormData;
  expect(formData.get("key_columns")).toBe("ID");
  expect(formData.get("value_column")).toBe("");
  expect(formData.get("time_column")).toBe("");

  const uploadedFile = formData.get("file");
  expect(uploadedFile).toBeInstanceOf(File);
  expect((uploadedFile as File).name).toBe("orders.csv");
});

test("keeps validation disabled until a CSV file is selected", async () => {
  fetchMock.mockResolvedValueOnce(createJsonResponse({ entries: [] }));

  render(<App />);

  await screen.findByText("No recent reports available.");

  expect(screen.getByRole("button", { name: "Run validation" })).toBeDisabled();
});

test("shows an error when validation submission fails", async () => {
  fetchMock
    .mockResolvedValueOnce(createJsonResponse({ entries: [] }))
    .mockResolvedValueOnce(
      createJsonResponse(
        {
          detail: "Backend unavailable.",
        },
        {
          ok: false,
          status: 503,
        },
      ),
    );

  render(<App />);

  await screen.findByText("No recent reports available.");

  fireEvent.change(screen.getByLabelText("CSV file"), {
    target: { files: [selectCsvFile()] },
  });
  fireEvent.click(screen.getByRole("button", { name: "Run validation" }));

  expect(await screen.findByText("Backend unavailable.")).toBeInTheDocument();
  expect(
    screen.getByText("No validation run yet. Submit a CSV file to populate this summary."),
  ).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Run validation" })).toBeEnabled();
});

test("uses the default FastAPI API base during local frontend development", async () => {
  fetchMock.mockResolvedValueOnce(createJsonResponse({ entries: [] }));

  render(<App />);

  await screen.findByText("No recent reports available.");

  expect(fetchMock).toHaveBeenCalledWith(
    "http://localhost:8000/api/reports/recent",
    undefined,
  );
});

test("shows a readable error when the backend returns a non-json failure body", async () => {
  fetchMock
    .mockResolvedValueOnce(createJsonResponse({ entries: [] }))
    .mockResolvedValueOnce(
      new Response("Service temporarily unavailable.", {
        status: 503,
        headers: {
          "Content-Type": "text/plain",
        },
      }),
    );

  render(<App />);

  await screen.findByText("No recent reports available.");

  fireEvent.change(screen.getByLabelText("CSV file"), {
    target: { files: [selectCsvFile()] },
  });
  fireEvent.click(screen.getByRole("button", { name: "Run validation" }));

  expect(
    await screen.findByText("Service temporarily unavailable."),
  ).toBeInTheDocument();
});

test("shows a helpful error when the local API cannot be reached", async () => {
  fetchMock
    .mockResolvedValueOnce(createJsonResponse({ entries: [] }))
    .mockRejectedValueOnce(new TypeError("Failed to fetch"));

  render(<App />);

  await screen.findByText("No recent reports available.");

  fireEvent.change(screen.getByLabelText("CSV file"), {
    target: { files: [selectCsvFile()] },
  });
  fireEvent.click(screen.getByRole("button", { name: "Run validation" }));

  expect(
    await screen.findByText("Unable to reach the local API. Check that make api-dev is running."),
  ).toBeInTheDocument();
});
