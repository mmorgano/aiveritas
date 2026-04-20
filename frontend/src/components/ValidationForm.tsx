import { useState, type FormEvent } from "react";

import type { ValidationSubmission } from "../api";

interface ValidationFormProps {
  isSubmitting: boolean;
  onSubmit: (submission: ValidationSubmission) => Promise<void>;
}

const SAMPLE_CSV = "email,name\nada@example.com,Ada Lovelace";

export default function ValidationForm({
  isSubmitting,
  onSubmit,
}: ValidationFormProps) {
  const [filename, setFilename] = useState("input.csv");
  const [csvText, setCsvText] = useState(SAMPLE_CSV);
  const [keyColumns, setKeyColumns] = useState("");
  const [valueColumn, setValueColumn] = useState("");
  const [timeColumn, setTimeColumn] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await onSubmit({
      csvText,
      filename,
      keyColumns,
      timeColumn,
      valueColumn,
    });
  }

  return (
    <section className="panel">
      <div className="section-heading">
        <h2>Validate CSV</h2>
        <p>Submit CSV content to the local FastAPI backend.</p>
      </div>
      <form className="stack" onSubmit={handleSubmit}>
        <label className="stack" htmlFor="filename-input">
          <span className="field-label">Filename</span>
          <input
            id="filename-input"
            name="filename"
            onChange={(event) => setFilename(event.target.value)}
            type="text"
            value={filename}
          />
        </label>
        <label className="stack" htmlFor="key-columns-input">
          <span className="field-label">Key columns</span>
          <input
            id="key-columns-input"
            name="key-columns"
            onChange={(event) => setKeyColumns(event.target.value)}
            type="text"
            value={keyColumns}
          />
        </label>
        <label className="stack" htmlFor="value-column-input">
          <span className="field-label">Value column</span>
          <input
            id="value-column-input"
            name="value-column"
            onChange={(event) => setValueColumn(event.target.value)}
            type="text"
            value={valueColumn}
          />
        </label>
        <label className="stack" htmlFor="time-column-input">
          <span className="field-label">Time column</span>
          <input
            id="time-column-input"
            name="time-column"
            onChange={(event) => setTimeColumn(event.target.value)}
            type="text"
            value={timeColumn}
          />
        </label>
        <label className="stack" htmlFor="csv-input">
          <span className="field-label">CSV content</span>
          <textarea
            id="csv-input"
            name="csv-input"
            onChange={(event) => setCsvText(event.target.value)}
            rows={8}
            value={csvText}
          />
        </label>
        <button className="primary-action" disabled={isSubmitting} type="submit">
          {isSubmitting ? "Validating..." : "Run validation"}
        </button>
      </form>
    </section>
  );
}
