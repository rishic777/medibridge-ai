import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Card from "../components/Card";
import Button from "../components/Button";
import AlertCard from "../components/AlertCard";
import PatientTimeline from "../components/PatientTimeline";
import { getHistory, getPatient, listAlerts, verifyHistoryItem } from "../services/api";

export default function DoctorDashboard() {
  const { patientId } = useParams();
  const [patient, setPatient] = useState(null);
  const [history, setHistory] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [summaryDraft, setSummaryDraft] = useState("");

  const load = async () => {
    if (!patientId) return;
    const [p, h] = await Promise.all([getPatient(patientId), getHistory(patientId)]);
    setPatient(p);
    setHistory(h);
  };

  useEffect(() => {
    load();
    listAlerts().then(setAlerts).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [patientId]);

  const handleVerify = async (symptomId) => {
    await verifyHistoryItem(patientId, {
      information_id: symptomId,
      information_type: "symptom",
      status: "physician_verified",
    });
    load();
  };

  return (
    <div className="mb-page mb-dashboard">
      <aside className="mb-dashboard__sidebar">
        <div className="mb-dashboard__logo">MediBridge AI</div>
        <nav>
          <a href="#dashboard">Dashboard</a>
          <a href="#patients">Patients</a>
          <a href="#reports">Reports</a>
          <a href="#alerts">Alerts</a>
          <a href="#settings">Settings</a>
        </nav>
      </aside>

      <main className="mb-dashboard__main">
        {!patientId && (
          <Card title="Alerts">
            {alerts.length === 0 && <p>No open alerts.</p>}
            {alerts.map((a) => (
              <AlertCard key={a.id} priority={a.priority} message={a.message} />
            ))}
          </Card>
        )}

        {patient && history && (
          <>
            <Card title="Patient Overview">
              <h2>
                {patient.name}, {patient.age ?? "—"}
              </h2>
              <p>Patient ID: {patient.id}</p>

              <div className="mb-dashboard__stats">
                <Card title="Chief Complaint">{history.chief_complaint || "Not yet reported"}</Card>
                <Card title="Symptoms reported">{history.symptoms.length}</Card>
              </div>

              <h3>🚨 Red Flags</h3>
              {history.red_flags.length === 0 && <p>None detected</p>}
              {history.red_flags.map((message, i) => (
                <AlertCard key={i} priority="urgent" message={message} />
              ))}

              <h3>Patient History</h3>
              <PatientTimeline
                items={history.symptoms.map((s) => ({
                  id: s.id,
                  name: s.name,
                  detail: [s.duration, s.severity].filter(Boolean).join(" · "),
                  source: s.source,
                }))}
              />

              <h3>AI Summary</h3>
              <textarea
                rows={4}
                value={summaryDraft}
                onChange={(e) => setSummaryDraft(e.target.value)}
                placeholder="Editable AI-generated summary appears here…"
              />

              <div className="mb-dashboard__actions">
                {history.symptoms.map((s) => (
                  <Button key={s.id} variant="secondary" onClick={() => handleVerify(s.id)}>
                    Verify "{s.name}"
                  </Button>
                ))}
              </div>
            </Card>
          </>
        )}

        {!patient && patientId && <p>Loading patient…</p>}
      </main>
    </div>
  );
}
