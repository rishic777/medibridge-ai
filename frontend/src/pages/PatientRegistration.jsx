import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/Button";
import Card from "../components/Card";
import { createPatient } from "../services/api";

export default function PatientRegistration() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", age: "", gender: "", preferred_language: "en" });
  const [consent, setConsent] = useState(false);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const update = (field) => (e) => setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!consent) {
      setError("Please confirm consent to continue.");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const patient = await createPatient({ ...form, age: form.age ? Number(form.age) : null });
      navigate(`/interview/${patient.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mb-page mb-registration">
      <Card title="Step 1 of 5 — Tell us a bit about you">
        <form onSubmit={handleSubmit} className="mb-form">
          <label>
            Full name
            <input value={form.name} onChange={update("name")} required />
          </label>
          <label>
            Age
            <input type="number" min="0" value={form.age} onChange={update("age")} />
          </label>
          <label>
            Gender
            <select value={form.gender} onChange={update("gender")}>
              <option value="">Prefer not to say</option>
              <option value="female">Female</option>
              <option value="male">Male</option>
              <option value="other">Other</option>
            </select>
          </label>
          <label>
            Preferred language
            <select value={form.preferred_language} onChange={update("preferred_language")}>
              <option value="en">English</option>
              <option value="hi">हिन्दी</option>
            </select>
          </label>

          <label className="mb-checkbox">
            <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
            I consent to my information being used to prepare my medical history for a clinician to review.
          </label>

          {error && <p className="mb-form__error">{error}</p>}

          <Button type="submit" fullWidth disabled={submitting}>
            {submitting ? "Please wait…" : "Continue →"}
          </Button>
        </form>
      </Card>
    </div>
  );
}
