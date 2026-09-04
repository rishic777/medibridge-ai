import "./ChatMessage.css";

/**
 * role: "patient" | "ai"
 */
export default function ChatMessage({ role, children }) {
  return (
    <div className={`mb-msg mb-msg--${role}`}>
      <div className="mb-msg__label">{role === "patient" ? "You" : "AI Health Assistant"}</div>
      <div className="mb-msg__bubble">{children}</div>
    </div>
  );
}
