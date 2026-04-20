# AIVeritas GUI First Iteration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first local browser-based GUI to AIVeritas using FastAPI and React/Vite while preserving the existing CLI and validation core.

**Architecture:** The implementation adds a thin FastAPI layer on top of the current Python core plus a separate React/Vite frontend. Shared orchestration logic should keep GUI behavior aligned with CLI behavior, while a small JSON-based recent-report index provides minimal local history without introducing a database.

**Tech Stack:** Python, FastAPI, pytest, React, Vite, TypeScript, JSON file persistence

---

## File Map

- Modify: `requirements.txt`
- Modify: `requirements-dev.txt`
- Modify: `src/main.py`
- Create: `src/services/__init__.py`
- Create: `src/services/validation_service.py`
- Create: `src/services/history_service.py`
- Create: `src/api/__init__.py`
- Create: `src/api/schemas.py`
- Create: `src/api/app.py`
- Create: `src/api/routes.py`
- Create: `tests/test_validation_service.py`
- Create: `tests/test_history_service.py`
- Create: `tests/test_api.py`
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/index.html`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/styles.css`
- Create: `frontend/src/types.ts`
- Create: `frontend/src/api.ts`
- Create: `frontend/src/components/ValidationForm.tsx`
- Create: `frontend/src/components/ResultSummary.tsx`
- Create: `frontend/src/components/RecentReports.tsx`
- Create: `frontend/src/components/StatusMessage.tsx`
- Create: `frontend/src/components/Layout.tsx`
- Create: `frontend/src/__tests__/App.test.tsx`
- Modify: `Makefile`
- Modify: `.gitignore`
- Modify later: `README.md`, `docs/ROADMAP.md`, `docs/SPRINTS.md`, `docs/FEATURES.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, `docs/TEST_MATRIX.md`, `CHANGELOG.md`

### Task 1: Extract Shared Validation Orchestration

**Files:**
- Create: `src/services/__init__.py`
- Create: `src/services/validation_service.py`
- Modify: `src/main.py`
- Test: `tests/test_validation_service.py`

- [ ] **Step 1: Write the failing service test for successful validation orchestration**

```python
from pathlib import Path

from src.services.validation_service import run_validation


def test_run_validation_builds_report_for_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "input.csv"
    csv_path.write_text("ID,DATE,VALUE\n1,2026-01-01,10\n2,2026-01-02,999\n", encoding="utf-8")

    report_path = tmp_path / "report.json"

    report = run_validation(
        input_path=csv_path,
        output_path=report_path,
        key_columns=["ID"],
        value_column="VALUE",
        time_column="DATE",
    )

    assert report["run"]["status"] == "success"
    assert report_path.exists()
    assert "issues" in report
```

- [ ] **Step 2: Run the new test to verify it fails**

Run: `python3 -m pytest tests/test_validation_service.py::test_run_validation_builds_report_for_csv -v`
Expected: FAIL because `src.services.validation_service` does not exist yet

- [ ] **Step 3: Write the minimal shared orchestration service**

```python
from pathlib import Path
from typing import Any

from src.ai_module import explain_issue
from src.loader import load_csv
from src.report import build_validation_report, save_report_as_json
from src.validator import run_all_validations


def run_validation(
    input_path: Path,
    output_path: Path,
    key_columns: list[str],
    value_column: str | None,
    time_column: str | None,
) -> dict[str, Any]:
    dataframe = load_csv(input_path)
    issues = run_all_validations(
        dataframe=dataframe,
        key_columns=key_columns,
        value_column=value_column,
        time_column=time_column,
    )
    enriched_issues = [
        {
            **issue,
            "ai_explanation": explain_issue(issue),
        }
        for issue in issues
    ]
    report = build_validation_report(
        input_path=input_path,
        dataframe=dataframe,
        issues=enriched_issues,
        key_columns=key_columns,
        value_column=value_column,
        time_column=time_column,
    )
    save_report_as_json(report, output_path)
    return report
```

- [ ] **Step 4: Update the CLI to use the shared service**

```python
from pathlib import Path

from src.services.validation_service import run_validation

# inside main flow
report = run_validation(
    input_path=Path(args.input),
    output_path=Path(args.output),
    key_columns=args.key_columns,
    value_column=args.value_column,
    time_column=args.time_column,
)
```

- [ ] **Step 5: Run the service test to verify it passes**

Run: `python3 -m pytest tests/test_validation_service.py::test_run_validation_builds_report_for_csv -v`
Expected: PASS

- [ ] **Step 6: Add a failure-path service test**

```python
from pathlib import Path

import pytest

from src.services.validation_service import run_validation


def test_run_validation_raises_for_missing_input(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        run_validation(
            input_path=tmp_path / "missing.csv",
            output_path=tmp_path / "report.json",
            key_columns=["ID"],
            value_column="VALUE",
            time_column="DATE",
        )
```

- [ ] **Step 7: Run the focused test file**

Run: `python3 -m pytest tests/test_validation_service.py -v`
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add src/services/__init__.py src/services/validation_service.py src/main.py tests/test_validation_service.py
git commit -m "refactor: extract shared validation service"
```

### Task 2: Add Recent Report History Service

**Files:**
- Create: `src/services/history_service.py`
- Test: `tests/test_history_service.py`

- [ ] **Step 1: Write the failing test for storing recent reports**

```python
from pathlib import Path

from src.services.history_service import RecentReportStore


def test_recent_report_store_appends_entry(tmp_path: Path) -> None:
    store = RecentReportStore(tmp_path / "recent_reports.json")

    store.add_entry(
        report_id="r1",
        report_path=tmp_path / "report.json",
        input_name="input.csv",
        run_status="success",
    )

    entries = store.list_entries()
    assert len(entries) == 1
    assert entries[0]["report_id"] == "r1"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tests/test_history_service.py::test_recent_report_store_appends_entry -v`
Expected: FAIL because `RecentReportStore` does not exist

- [ ] **Step 3: Write the minimal JSON-backed history store**

```python
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, UTC
from pathlib import Path
import json


@dataclass
class RecentReportEntry:
    report_id: str
    timestamp: str
    input_name: str
    report_path: str
    run_status: str


class RecentReportStore:
    def __init__(self, index_path: Path, limit: int = 10) -> None:
        self._index_path = index_path
        self._limit = limit

    def add_entry(self, report_id: str, report_path: Path, input_name: str, run_status: str) -> None:
        entries = self.list_entries()
        entries.insert(
            0,
            asdict(
                RecentReportEntry(
                    report_id=report_id,
                    timestamp=datetime.now(UTC).isoformat(),
                    input_name=input_name,
                    report_path=str(report_path),
                    run_status=run_status,
                )
            ),
        )
        self._write(entries[: self._limit])

    def list_entries(self) -> list[dict[str, str]]:
        if not self._index_path.exists():
            return []
        return json.loads(self._index_path.read_text(encoding="utf-8"))

    def _write(self, entries: list[dict[str, str]]) -> None:
        self._index_path.parent.mkdir(parents=True, exist_ok=True)
        self._index_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
```

- [ ] **Step 4: Add a trimming test for the history limit**

```python
from pathlib import Path

from src.services.history_service import RecentReportStore


def test_recent_report_store_keeps_newest_entries_only(tmp_path: Path) -> None:
    store = RecentReportStore(tmp_path / "recent_reports.json", limit=2)

    for index in range(3):
        store.add_entry(
            report_id=f"r{index}",
            report_path=tmp_path / f"report-{index}.json",
            input_name=f"input-{index}.csv",
            run_status="success",
        )

    entries = store.list_entries()
    assert [entry["report_id"] for entry in entries] == ["r2", "r1"]
```

- [ ] **Step 5: Run the history test file**

Run: `python3 -m pytest tests/test_history_service.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/services/history_service.py tests/test_history_service.py
git commit -m "feat: add recent report history service"
```

### Task 3: Add FastAPI Backend

**Files:**
- Modify: `requirements.txt`
- Create: `src/api/__init__.py`
- Create: `src/api/schemas.py`
- Create: `src/api/routes.py`
- Create: `src/api/app.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: Add backend dependencies**

```text
requirements.txt
fastapi>=0.115,<1.0
uvicorn>=0.30,<1.0
python-multipart>=0.0.9,<1.0
```

- [ ] **Step 2: Write the failing API health test**

```python
from fastapi.testclient import TestClient

from src.api.app import create_app


def test_health_endpoint_returns_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 3: Run the health test to verify it fails**

Run: `python3 -m pytest tests/test_api.py::test_health_endpoint_returns_ok -v`
Expected: FAIL because the API application does not exist yet

- [ ] **Step 4: Create the minimal FastAPI app and health route**

```python
from fastapi import APIRouter, FastAPI


def create_router() -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return router


def create_app() -> FastAPI:
    app = FastAPI(title="AIVeritas API")
    app.include_router(create_router())
    return app
```

- [ ] **Step 5: Add the failing validate endpoint test**

```python
from pathlib import Path

from fastapi.testclient import TestClient

from src.api.app import create_app


def test_validate_endpoint_returns_report(tmp_path: Path) -> None:
    csv_path = tmp_path / "input.csv"
    csv_path.write_text("ID,DATE,VALUE\n1,2026-01-01,10\n", encoding="utf-8")

    client = TestClient(create_app())
    with csv_path.open("rb") as input_file:
        response = client.post(
            "/api/validate",
            files={"file": ("input.csv", input_file, "text/csv")},
            data={
                "key_columns": "ID",
                "value_column": "VALUE",
                "time_column": "DATE",
            },
        )

    assert response.status_code == 200
    assert response.json()["report"]["run"]["status"] == "success"
```

- [ ] **Step 6: Implement the validate route using the shared services**

```python
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4

from fastapi import APIRouter, File, Form, UploadFile

from src.services.history_service import RecentReportStore
from src.services.validation_service import run_validation


def create_router() -> APIRouter:
    router = APIRouter(prefix="/api")
    history = RecentReportStore(Path("data/app_state/recent_reports.json"))

    @router.post("/validate")
    async def validate(
        file: UploadFile = File(...),
        key_columns: str = Form(""),
        value_column: str = Form(""),
        time_column: str = Form(""),
    ) -> dict[str, object]:
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / file.filename
            input_path.write_bytes(await file.read())

            report_id = str(uuid4())
            report_path = Path("reports") / f"{report_id}.json"
            report = run_validation(
                input_path=input_path,
                output_path=report_path,
                key_columns=[column for column in key_columns.split(",") if column],
                value_column=value_column or None,
                time_column=time_column or None,
            )
            history.add_entry(
                report_id=report_id,
                report_path=report_path,
                input_name=file.filename,
                run_status=report["run"]["status"],
            )
            return {"report_id": report_id, "report": report}
```

- [ ] **Step 7: Add the recent-reports endpoint test**

```python
from fastapi.testclient import TestClient

from src.api.app import create_app


def test_recent_reports_endpoint_returns_entries() -> None:
    client = TestClient(create_app())

    response = client.get("/api/reports/recent")

    assert response.status_code == 200
    assert "entries" in response.json()
```

- [ ] **Step 8: Implement recent and reopen routes**

```python
@router.get("/reports/recent")
def recent_reports() -> dict[str, object]:
    return {"entries": history.list_entries()}

@router.get("/reports/{report_id}")
def get_report(report_id: str) -> dict[str, object]:
    entries = history.list_entries()
    entry = next(item for item in entries if item["report_id"] == report_id)
    report = json.loads(Path(entry["report_path"]).read_text(encoding="utf-8"))
    return {"report_id": report_id, "report": report}
```

- [ ] **Step 9: Run the API test file**

Run: `python3 -m pytest tests/test_api.py -v`
Expected: PASS

- [ ] **Step 10: Commit**

```bash
git add requirements.txt src/api/__init__.py src/api/schemas.py src/api/routes.py src/api/app.py tests/test_api.py
git commit -m "feat: add FastAPI GUI backend"
```

### Task 4: Scaffold React + Vite Frontend

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/index.html`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/styles.css`
- Create: `frontend/src/types.ts`
- Create: `frontend/src/api.ts`
- Create: `frontend/src/components/Layout.tsx`
- Create: `frontend/src/components/ValidationForm.tsx`
- Create: `frontend/src/components/ResultSummary.tsx`
- Create: `frontend/src/components/RecentReports.tsx`
- Create: `frontend/src/components/StatusMessage.tsx`
- Test: `frontend/src/__tests__/App.test.tsx`

- [ ] **Step 1: Create the frontend package manifest**

```json
{
  "name": "aiveritas-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest run"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.4.8",
    "@testing-library/react": "^16.0.0",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "typescript": "^5.5.4",
    "vite": "^5.4.0",
    "vitest": "^2.0.5"
  }
}
```

- [ ] **Step 2: Write the failing app render test**

```tsx
import { render, screen } from "@testing-library/react";

import App from "../App";


test("renders validator heading", () => {
  render(<App />);
  expect(screen.getByText("AIVeritas GUI")).toBeInTheDocument();
});
```

- [ ] **Step 3: Run the frontend test to verify it fails**

Run: `cd frontend && npm test`
Expected: FAIL because the React app is not scaffolded yet

- [ ] **Step 4: Create the minimal React app shell**

```tsx
export default function App() {
  return (
    <main>
      <h1>AIVeritas GUI</h1>
      <p>Local validation for one CSV at a time.</p>
    </main>
  );
}
```

- [ ] **Step 5: Add typed API helpers and UI components**

```tsx
// src/types.ts
export type RecentReportEntry = {
  report_id: string;
  timestamp: string;
  input_name: string;
  report_path: string;
  run_status: string;
};

export type ValidationResponse = {
  report_id: string;
  report: {
    run: { status: string };
    validation: { status: string };
    summary: Record<string, unknown>;
    issues: Array<Record<string, unknown>>;
  };
};
```

- [ ] **Step 6: Build the single-page layout**

```tsx
return (
  <Layout>
    <ValidationForm />
    <ResultSummary />
    <RecentReports />
  </Layout>
);
```

- [ ] **Step 7: Run the frontend test to verify it passes**

Run: `cd frontend && npm test`
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add frontend/package.json frontend/tsconfig.json frontend/vite.config.ts frontend/index.html frontend/src/main.tsx frontend/src/App.tsx frontend/src/styles.css frontend/src/types.ts frontend/src/api.ts frontend/src/components/Layout.tsx frontend/src/components/ValidationForm.tsx frontend/src/components/ResultSummary.tsx frontend/src/components/RecentReports.tsx frontend/src/components/StatusMessage.tsx frontend/src/__tests__/App.test.tsx
git commit -m "feat: scaffold React GUI frontend"
```

### Task 5: Connect Frontend to Backend

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/api.ts`
- Modify: `frontend/src/components/ValidationForm.tsx`
- Modify: `frontend/src/components/ResultSummary.tsx`
- Modify: `frontend/src/components/RecentReports.tsx`
- Modify: `frontend/src/components/StatusMessage.tsx`
- Test: `frontend/src/__tests__/App.test.tsx`

- [ ] **Step 1: Write the failing test for loading recent reports**

```tsx
import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import App from "../App";

vi.mock("../api", () => ({
  fetchRecentReports: vi.fn().mockResolvedValue({
    entries: [
      {
        report_id: "r1",
        timestamp: "2026-04-19T10:00:00Z",
        input_name: "sample.csv",
        report_path: "reports/r1.json",
        run_status: "success",
      },
    ],
  }),
}));

test("renders recent reports returned by backend", async () => {
  render(<App />);
  await waitFor(() => expect(screen.getByText("sample.csv")).toBeInTheDocument());
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd frontend && npm test`
Expected: FAIL because App does not fetch and render backend data yet

- [ ] **Step 3: Implement recent-report loading in App**

```tsx
const [recentReports, setRecentReports] = useState<RecentReportEntry[]>([]);

useEffect(() => {
  fetchRecentReports().then((response) => setRecentReports(response.entries));
}, []);
```

- [ ] **Step 4: Add validation submission flow**

```tsx
async function handleValidate(form: ValidationFormData): Promise<void> {
  setStatus({ type: "loading", message: "Running validation..." });
  const response = await submitValidation(form);
  setCurrentReport(response.report);
  setStatus({ type: "success", message: "Validation completed." });
  const recent = await fetchRecentReports();
  setRecentReports(recent.entries);
}
```

- [ ] **Step 5: Add reopen-report flow**

```tsx
async function handleOpenReport(reportId: string): Promise<void> {
  setStatus({ type: "loading", message: "Loading report..." });
  const response = await fetchReport(reportId);
  setCurrentReport(response.report);
  setStatus({ type: "success", message: "Report loaded." });
}
```

- [ ] **Step 6: Run the frontend tests again**

Run: `cd frontend && npm test`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add frontend/src/App.tsx frontend/src/api.ts frontend/src/components/ValidationForm.tsx frontend/src/components/ResultSummary.tsx frontend/src/components/RecentReports.tsx frontend/src/components/StatusMessage.tsx frontend/src/__tests__/App.test.tsx
git commit -m "feat: connect GUI frontend to backend"
```

### Task 6: Add Developer Workflow and Integration Verification

**Files:**
- Modify: `Makefile`
- Modify: `.gitignore`

- [ ] **Step 1: Add frontend and API commands to the Makefile**

```makefile
frontend-install:
	cd frontend && npm install

frontend-test:
	cd frontend && npm test

api-dev:
	.venv/bin/python -m uvicorn src.api.app:create_app --factory --reload

gui-dev:
	cd frontend && npm run dev
```

- [ ] **Step 2: Ignore frontend build and app-state artifacts**

```gitignore
frontend/node_modules/
frontend/dist/
data/app_state/
```

- [ ] **Step 3: Run backend tests**

Run: `python3 -m pytest tests/test_validation_service.py tests/test_history_service.py tests/test_api.py -v`
Expected: PASS

- [ ] **Step 4: Run existing core tests**

Run: `python3 -m pytest -v`
Expected: PASS

- [ ] **Step 5: Run lint**

Run: `make lint`
Expected: PASS

- [ ] **Step 6: Build the frontend**

Run: `cd frontend && npm run build`
Expected: PASS and create `frontend/dist`

- [ ] **Step 7: Commit**

```bash
git add Makefile .gitignore
git commit -m "chore: add GUI developer workflow commands"
```

### Task 7: Update Project Documentation and Traceability

**Files:**
- Modify: `README.md`
- Modify: `docs/ROADMAP.md`
- Modify: `docs/SPRINTS.md`
- Modify: `docs/FEATURES.md`
- Modify: `docs/ARCHITECTURE.md`
- Modify: `docs/DECISIONS.md`
- Modify: `docs/TEST_MATRIX.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update README for GUI usage**

```md
Add:
- FastAPI backend and React frontend overview
- local GUI development commands
- minimal GUI usage description
```

- [ ] **Step 2: Update roadmap and sprint tracking**

```md
Add the GUI initiative as planned or in-progress work with realistic scope.
```

- [ ] **Step 3: Update feature inventory and test matrix**

```md
Add feature entries for:
- GUI backend interface
- GUI frontend
- recent report history
- corresponding test coverage references
```

- [ ] **Step 4: Update architecture and decisions**

```md
Document:
- FastAPI as secondary interface layer
- React/Vite frontend separation
- minimal JSON-backed recent report history
```

- [ ] **Step 5: Update changelog**

```md
Record the GUI first-iteration introduction and related developer workflow additions.
```

- [ ] **Step 6: Run documentation sanity checks**

Run: `rg -n "GUI|FastAPI|frontend|recent report|history" README.md docs CHANGELOG.md`
Expected: the GUI-related documentation appears in the intended files

- [ ] **Step 7: Commit**

```bash
git add README.md docs/ROADMAP.md docs/SPRINTS.md docs/FEATURES.md docs/ARCHITECTURE.md docs/DECISIONS.md docs/TEST_MATRIX.md CHANGELOG.md
git commit -m "docs: document first GUI iteration"
```

## Self-Review

- Spec coverage: the plan covers the FastAPI backend, React/Vite frontend, single-file flow, minimal result summary, recent report history, shared orchestration, and documentation traceability.
- Placeholder scan: each task names concrete files, commands, and expected behavior.
- Type consistency: backend, history, and frontend naming consistently use `report_id`, `run_validation`, recent reports, and a single-file GUI flow.
