import { useState, type ChangeEvent, type FormEvent } from "react";

import type { ValidationSubmission } from "../api";

interface ValidationFormProps {
  isSubmitting: boolean;
  onSubmit: (submission: ValidationSubmission) => Promise<void>;
}

export default function ValidationForm({
  isSubmitting,
  onSubmit,
}: ValidationFormProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [keyColumns, setKeyColumns] = useState("");
  const [valueColumn, setValueColumn] = useState("");
  const [timeColumn, setTimeColumn] = useState("");

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    setSelectedFile(event.target.files?.[0] ?? null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedFile) {
      return;
    }

    await onSubmit({
      file: selectedFile,
      keyColumns,
      timeColumn,
      valueColumn,
    });
  }

  return (
    <section className="panel">
      <div className="section-heading">
        <h2>Validate CSV</h2>
        <p>Choose a CSV file and submit it to the local FastAPI backend.</p>
      </div>
      <form className="stack" onSubmit={handleSubmit}>
        <label className="stack" htmlFor="csv-file-input">
          <span className="field-label">CSV file</span>
          <input
            accept=".csv,text/csv"
            aria-label="CSV file"
            id="csv-file-input"
            name="csv-file"
            onChange={handleFileChange}
            type="file"
          />
          <span className="field-hint">
            {selectedFile ? `Selected: ${selectedFile.name}` : "Choose one CSV file to validate."}
          </span>
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
        <button
          className="primary-action"
          disabled={isSubmitting || !selectedFile}
          type="submit"
        >
          {isSubmitting ? "Validating..." : "Run validation"}
        </button>
      </form>
    </section>
  );
}
