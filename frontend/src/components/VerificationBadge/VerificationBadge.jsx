import "./VerificationBadge.css";

const LABELS = {
  patient_reported: "Patient reported",
  document_supported: "Document supported",
  physician_verified: "Physician verified",
};

const ICONS = {
  patient_reported: "●",
  document_supported: "●",
  physician_verified: "✓",
};

/**
 * The core trust-layer UI: every piece of clinical information carries
 * one of these three badges so the AI never presents an unverified
 * claim as settled fact.
 * status: "patient_reported" | "document_supported" | "physician_verified"
 */
export default function VerificationBadge({ status = "patient_reported" }) {
  return (
    <span className={`mb-verify mb-verify--${status}`}>
      <span aria-hidden="true">{ICONS[status]}</span>
      {LABELS[status] || status}
    </span>
  );
}
