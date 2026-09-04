import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Button from "../components/Button";
import Card from "../components/Card";
import { processReport, uploadReport } from "../services/api";

export default function UploadReport() {
  const { patientId } = useParams();
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | uploading | processing | done | error
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    setError(null);
    try {
      const report = await uploadReport(patientId, file);
      setStatus("processing");
      await processReport(report.id);
      setStatus("done");
    } catch (err) {
      setError(err.message);
      setStatus("error");
    }
  };

  return (
    <div className="mb-page mb-upload">
      <Card title="Step 4 of 5 — Upload any reports you have">
        <p>Blood tests, prescriptions, or discharge summaries all help your doctor build a fuller picture. This step is optional.</p>

        <input type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />

        {error && <p className="mb-form__error">{error}</p>}

        <div className="mb-upload__actions">
          <Button variant="ghost" onClick={() => navigate(`/history/${patientId}`)}>
            Skip
          </Button>
          <Button onClick={handleUpload} disabled={!file || status === "uploading" || status === "processing"}>
            {status === "uploading" && "Uploading…"}
            {status === "processing" && "Reading document…"}
            {(status === "idle" || status === "error") && "Upload"}
            {status === "done" && "Uploaded ✓"}
          </Button>
        </div>

        {status === "done" && (
          <Button fullWidth onClick={() => navigate(`/history/${patientId}`)}>
            Continue →
          </Button>
        )}
      </Card>
    </div>
  );
}
