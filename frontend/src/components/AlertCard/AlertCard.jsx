import "./AlertCard.css";

/**
 * priority: "urgent" | "routine"
 * Never conveys urgency with color alone -- always paired with an icon + label.
 */
export default function AlertCard({ priority = "routine", message, onAcknowledge }) {
  const isUrgent = priority === "urgent";
  return (
    <div className={`mb-alert ${isUrgent ? "mb-alert--urgent" : "mb-alert--routine"}`} role="alert">
      <div className="mb-alert__header">
        <span aria-hidden="true">{isUrgent ? "🚨" : "ℹ️"}</span>
        <strong>{isUrgent ? "URGENT" : "Notice"}</strong>
      </div>
      <p className="mb-alert__message">{message}</p>
      {onAcknowledge && (
        <button type="button" className="mb-alert__ack" onClick={onAcknowledge}>
          Acknowledge
        </button>
      )}
    </div>
  );
}
