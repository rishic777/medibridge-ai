import { useCallback, useEffect, useRef, useState } from "react";

/**
 * Thin wrapper around the browser's Web Speech API (SpeechRecognition).
 * Speech-to-text runs entirely client-side in this prototype, so only
 * the final transcript is ever sent to the backend -- see
 * backend/app/services/speech_service.py for the server-side swap point.
 */
export function useVoice({ language = "en-US", onResult } = {}) {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);

  const SpeechRecognitionImpl =
    typeof window !== "undefined" ? window.SpeechRecognition || window.webkitSpeechRecognition : null;
  const isSupported = Boolean(SpeechRecognitionImpl);

  useEffect(() => {
    if (!isSupported) return undefined;

    const recognition = new SpeechRecognitionImpl();
    recognition.lang = language;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onResult?.(transcript);
    };
    recognition.onend = () => setIsListening(false);
    recognition.onerror = () => setIsListening(false);

    recognitionRef.current = recognition;
    return () => recognition.stop();
  }, [SpeechRecognitionImpl, isSupported, language, onResult]);

  const start = useCallback(() => {
    if (!recognitionRef.current) return;
    setIsListening(true);
    recognitionRef.current.start();
  }, []);

  const stop = useCallback(() => {
    recognitionRef.current?.stop();
    setIsListening(false);
  }, []);

  return { isListening, isSupported, start, stop };
}
