import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Card from "../components/Card";
import PatientTimeline from "../components/PatientTimeline";
import AlertCard from "../components/AlertCard";
import { getHistory } from "../services/api";

export default function PatientHistory() {
  const { patientId } = useParams();
  const [history, setHistory] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getHistory(patientId)
      .then(setHistory)
      .catch((err) => setError(err.message));
  }, [patientId]);

  if (error) return <p className="mb-form__error">{error}</p>;
  if (!history) return <p>Loading your history…</p>;

  const timelineItems = history.symptoms.map((s) => ({
    id: s.id,
    name: s.name,
    detail: [s.duration, s.severity].filter(Boolean).join(" · "),
    source: s.source,
  }));

  return (
    <div className="mb-page mb-history">
      <Card title="Step 5 of 5 — Review your history">
        {history.red_flags.length > 0 && (
          <div className="mb-history__alerts">
            {history.red_flags.map((message, i) => (
              <AlertCard key={i} priority="urgent" message={message} />
            ))}
          </div>
        )}
        <PatientTimeline items={timelineItems} />
        <p className="mb-history__note">
          This is a summary of what you've told us. Your doctor will review and confirm each item before it becomes
          part of your official record.
        </p>
      </Card>
    </div>
  );
}
