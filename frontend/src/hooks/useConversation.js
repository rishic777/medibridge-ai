import { useCallback, useState } from "react";
import { postMessage, startConversation } from "../services/api";

/**
 * Drives the adaptive-question interview flow: sends a patient message,
 * receives the AI's reply plus the next question, and keeps local chat
 * state for the Interview page.
 */
export function useConversation(patientId) {
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [nextQuestion, setNextQuestion] = useState(null);
  const [redFlags, setRedFlags] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const ensureConversation = useCallback(async () => {
    if (conversationId) return conversationId;
    const conversation = await startConversation(patientId);
    setConversationId(conversation.id);
    return conversation.id;
  }, [conversationId, patientId]);

  const sendMessage = useCallback(
    async (text) => {
      setIsLoading(true);
      setError(null);
      try {
        const id = await ensureConversation();
        setMessages((prev) => [...prev, { role: "patient", content: text }]);
        const reply = await postMessage(id, text);
        setMessages((prev) => [...prev, { role: "ai", content: reply.content }]);
        setNextQuestion(reply.next_question || null);
        setRedFlags(reply.red_flags || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    },
    [ensureConversation]
  );

  return { conversationId, messages, nextQuestion, redFlags, isLoading, error, sendMessage };
}
