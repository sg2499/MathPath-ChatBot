import { useEffect, useMemo, useRef, useState } from "react";
import { MessageCircle, Send, X, Minimize2, UserRoundPlus } from "lucide-react";
import { sendChatMessage, streamChatMessage } from "./api.js";
import ChatMessage from "./ChatMessage.jsx";
import SuggestedQuestions from "./SuggestedQuestions.jsx";
import LeadForm from "./LeadForm.jsx";

function createSessionId() {
  const existing = window.localStorage.getItem("mathpath_chat_session_id");
  if (existing) return existing;

  const sessionId = `mp_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
  window.localStorage.setItem("mathpath_chat_session_id", sessionId);
  return sessionId;
}

const welcomeMessage = {
  role: "assistant",
  content:
    "Hi! I’m MathPath AI. I can help you choose the right MathPath Abacus program, explain our hybrid learning model, Bridge Course, daily practice system, and help you book a free demo. What would you like to know?"
};

export default function ChatWidget() {
  const params = new URLSearchParams(window.location.search);
  const shouldAutoOpen = params.get("open") === "1" || params.get("open") === "true";
  const [isOpen, setIsOpen] = useState(shouldAutoOpen);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([welcomeMessage]);
  const [isLoading, setIsLoading] = useState(false);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef(null);

  const sessionId = useMemo(() => createSessionId(), []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, showLeadForm]);

  function shouldShowLeadButton(text) {
    const triggerWords = ["demo", "admission", "join", "enroll", "enrol", "fee", "fees", "callback", "contact", "book", "trial"];
    return triggerWords.some((word) => String(text || "").toLowerCase().includes(word));
  }

  async function handleSend(customText) {
    const text = (customText || input).trim();
    if (!text || isLoading) return;

    setInput("");
    setError("");
    setMessages((current) => [...current, { role: "user", content: text }]);
    setIsLoading(true);

    const assistantMessageId = `assistant_${Date.now()}`;
    setMessages((current) => [
      ...current,
      { id: assistantMessageId, role: "assistant", content: "", streaming: true }
    ]);

    try {
      const data = await streamChatMessage({
        message: text,
        sessionId,
        onToken: (_token, fullAnswer) => {
          setMessages((current) =>
            current.map((message) =>
              message.id === assistantMessageId
                ? { ...message, content: fullAnswer, streaming: true }
                : message
            )
          );
        }
      });

      const answer = data.answer || "I’m sorry, I could not generate an answer right now.";
      setMessages((current) =>
        current.map((message) =>
          message.id === assistantMessageId
            ? { ...message, content: answer, streaming: false }
            : message
        )
      );

      if (data.session_id) {
        window.localStorage.setItem("mathpath_chat_session_id", data.session_id);
      }

      if (shouldShowLeadButton(text) || shouldShowLeadButton(answer) || data.should_capture_lead) {
        setShowLeadForm(true);
      }
    } catch (_err) {
      try {
        const data = await sendChatMessage({ message: text, sessionId });
        const answer = data.answer || "I’m sorry, I could not generate an answer right now.";
        setMessages((current) =>
          current.map((message) =>
            message.id === assistantMessageId
              ? { ...message, content: answer, streaming: false }
              : message
          )
        );
        if (data.session_id) {
          window.localStorage.setItem("mathpath_chat_session_id", data.session_id);
        }
        if (shouldShowLeadButton(text) || shouldShowLeadButton(answer) || data.should_capture_lead) {
          setShowLeadForm(true);
        }
      } catch (_fallbackErr) {
        setError("I’m having trouble connecting to the MathPath AI server. Please make sure the backend is running.");
        setMessages((current) =>
          current.map((message) =>
            message.id === assistantMessageId
              ? {
                  ...message,
                  streaming: false,
                  content:
                    "I’m unable to connect to the chatbot backend right now. You can still contact MathPath directly at 7980918759 / 9831684229 or email info@mathpath.in."
                }
              : message
          )
        );
      }
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="mp-chatbot-root">
      {!isOpen && (
        <button className="mp-chat-launcher" type="button" onClick={() => setIsOpen(true)} aria-label="Open MathPath AI Chatbot">
          <img src="/MathPath-Logo.png" alt="MathPath" />
          <span>Ask MathPath AI</span>
          <MessageCircle size={18} aria-hidden="true" />
        </button>
      )}

      {isOpen && (
        <section className="mp-chat-window" aria-label="MathPath AI Chatbot">
          <header className="mp-chat-header">
            <div className="mp-chat-brand">
              <img src="/MathPath-Logo.png" alt="MathPath" />
              <div>
                <strong>MathPath AI</strong>
                <span>Ace with Abacus</span>
              </div>
            </div>
            <div className="mp-chat-actions">
              <button type="button" aria-label="Show lead form" onClick={() => setShowLeadForm((value) => !value)}>
                <UserRoundPlus size={18} />
              </button>
              <button type="button" aria-label="Minimize chatbot" onClick={() => setIsOpen(false)}>
                <Minimize2 size={18} />
              </button>
              <button
                type="button"
                aria-label="Reset chat"
                onClick={() => {
                  setMessages([welcomeMessage]);
                  setShowLeadForm(false);
                  setError("");
                }}
              >
                <X size={18} />
              </button>
            </div>
          </header>

          <div className="mp-chat-body">
            <SuggestedQuestions onSelect={handleSend} disabled={isLoading} />
            <div className="mp-message-list">
              {messages.map((message, index) => (
                <ChatMessage key={message.id || `${message.role}-${index}`} message={message} />
              ))}
              {showLeadForm && (
                <LeadForm
                  sessionId={sessionId}
                  onSubmitted={() =>
                    setMessages((current) => [
                      ...current,
                      {
                        role: "assistant",
                        content:
                          "Thank you for sharing the details. The MathPath team will contact you shortly for demo class and level guidance."
                      }
                    ])
                  }
                />
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {error && <div className="mp-chat-error">{error}</div>}

          <footer className="mp-chat-footer">
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about MathPath programs, Bridge Course, daily practice, demo class..."
              rows={1}
              disabled={isLoading}
            />
            <button type="button" onClick={() => handleSend()} disabled={isLoading || !input.trim()} aria-label="Send message">
              <Send size={18} />
            </button>
          </footer>
        </section>
      )}
    </div>
  );
}
