import type { StatusState } from "../types";

interface StatusMessageProps {
  status: StatusState;
}

export default function StatusMessage({ status }: StatusMessageProps) {
  return (
    <section
      aria-live="polite"
      className={`status-banner status-${status.tone}`}
      role="status"
    >
      {status.message}
    </section>
  );
}
