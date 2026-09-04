import VerificationBadge from "../VerificationBadge";
import "./PatientTimeline.css";

/**
 * items: [{ id, name, detail, source }]
 */
export default function PatientTimeline({ items = [] }) {
  if (items.length === 0) {
    return <p className="mb-timeline__empty">No history recorded yet.</p>;
  }

  return (
    <ul className="mb-timeline">
      {items.map((item) => (
        <li key={item.id} className="mb-timeline__item">
          <div className="mb-timeline__dot" />
          <div className="mb-timeline__content">
            <div className="mb-timeline__row">
              <span className="mb-timeline__name">{item.name}</span>
              <VerificationBadge status={item.source} />
            </div>
            {item.detail && <div className="mb-timeline__detail">{item.detail}</div>}
          </div>
        </li>
      ))}
    </ul>
  );
}
