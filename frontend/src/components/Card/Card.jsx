import "./Card.css";

export default function Card({ title, children, footer }) {
  return (
    <div className="mb-card">
      {title && <div className="mb-card__title">{title}</div>}
      <div className="mb-card__body">{children}</div>
      {footer && <div className="mb-card__footer">{footer}</div>}
    </div>
  );
}
