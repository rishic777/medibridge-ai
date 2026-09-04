import "./Button.css";

/**
 * variant: "primary" | "secondary" | "ghost" | "danger"
 */
export default function Button({ children, variant = "primary", onClick, type = "button", disabled = false, fullWidth = false }) {
  return (
    <button
      type={type}
      className={`mb-btn mb-btn--${variant}${fullWidth ? " mb-btn--full" : ""}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
