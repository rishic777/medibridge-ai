import { useState } from "react";
import { useParams } from "react-router-dom";
import Button from "../components/Button";
import ChatMessage from "../components/ChatMessage";
import AlertCard from "../components/AlertCard";
import VoiceInput from "../components/VoiceInput";
import { useConversation } from "../hooks/useConversation";

/**
 * The core conversation interface. Deliberately avoids anything that
 * feels like a medical form -- one question at a time, plain language,
 * voice or text.
 */
export default function Interview() {
  const { patientId } = useParams();
  const { messages, nextQuestion, redFlags, isLoading, error, sendMessage } = useConversation(patientId);
  const [draft, setDraft] = useState("");

  const handleSend = async (text) => {
    const value = (text ?? draft).trim();
    if (!value) return;
    setDraft("");
    await sendMessage(value);
  };

  return (
    <div className="mb-page mb-interview">
      <div className="mb-interview__header">
        <span className="mb-interview__step">AI Health Assistant</span>
      </div>

      <div className="mb-interview__thread">
        {messages.length === 0 && (
          <ChatMessage role="ai">Tell us what you're experiencing, in your own words.</ChatMessage>
        )}
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role}>
            {m.content}
          </ChatMessage>
        ))}
        {nextQuestion && <ChatMessage role="ai">{nextQuestion.text}</ChatMessage>}
      </div>

      {redFlags.length > 0 && (
        <div className="mb-interview__alerts">
          {redFlags.map((message, i) => (
            <AlertCard key={i} priority="urgent" message={message} />
          ))}
        </div>
      )}

      <div className="mb-interview__input">
        <VoiceInput onTranscript={(text) => handleSend(text)} />

        <p className="mb-interview__or">Or type your response</p>
        <textarea
          rows={3}
          value={draft}
          placeholder="I have been having fever..."
          onChange={(e) => setDraft(e.target.value)}
        />
        {error && <p className="mb-form__error">{error}</p>}
        <Button onClick={() => handleSend()} disabled={isLoading} fullWidth>
          {isLoading ? "Sending…" : "Continue →"}
        </Button>
      </div>
    </div>
  );
}
