import { useVoice } from "../../hooks/useVoice";
import "./VoiceInput.css";

/**
 * Tap-to-speak control. Uses the browser's Web Speech API (see
 * hooks/useVoice.js) so no audio ever needs to reach the backend in
 * the prototype -- only the resulting transcript does.
 */
export default function VoiceInput({ onTranscript, language = "en-US" }) {
  const { isListening, isSupported, start, stop } = useVoice({ language, onResult: onTranscript });

  if (!isSupported) {
    return (
      <div className="mb-voice mb-voice--unsupported">
        Voice input isn't supported in this browser. Please type your response instead.
      </div>
    );
  }

  return (
    <button
      type="button"
      className={`mb-voice ${isListening ? "mb-voice--listening" : ""}`}
      onClick={isListening ? stop : start}
      aria-pressed={isListening}
      aria-label={isListening ? "Stop recording" : "Tap to speak"}
    >
      <span className="mb-voice__icon">🎤</span>
      <span className="mb-voice__label">{isListening ? "Listening…" : "Tap to speak"}</span>
    </button>
  );
}
