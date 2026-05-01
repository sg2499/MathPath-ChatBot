import { useEffect, useMemo, useRef, useState } from "react";
import { sendChatMessage, streamChatMessage, submitLead } from "./api";
import "../styles/chatbot.css";

const LOGO_SRC = "/MathPath-Logo.png";

const QUICK_PROMPTS = [
  "Which program is right for my child?",
  "My child is weak in maths. Can MathPath help?",
  "What is the Bridge Course?",
  "What is the class duration?",
  "How does daily practice work?",
  "How can I book a free demo?",
];

const INITIAL_MESSAGES = [
  {
    id: "welcome",
    role: "bot",
    text:
      "Hi! I’m MathPath AI. I can help you choose the right MathPath Abacus program, explain our learning model, Bridge Course, class structure, assessments, and demo process. What would you like to know?",
  },
];

function makeId(prefix = "msg") {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function formatMessage(text) {
  if (!text) return null;

  const lines = text.split("\n").filter((line) => line.trim() !== "");

  return lines.map((line, index) => {
    const trimmed = line.trim();

    if (trimmed.startsWith("- ") || trimmed.startsWith("• ")) {
      return (
        <div className="mp-bullet-line" key={`${trimmed}-${index}`}>
          <span>•</span>
          <p>{trimmed.replace(/^[-•]\s*/, "")}</p>
        </div>
      );
    }

    return <p key={`${trimmed}-${index}`}>{trimmed}</p>;
  });
}

function shouldOpenLeadFormFromUser(text) {
  const value = text.toLowerCase();
  const directLeadPhrases = [
    "book demo",
    "free demo",
    "schedule demo",
    "trial class",
    "book a class",
    "call me",
    "callback",
    "contact me",
    "i want admission",
    "admission",
    "enroll",
    "enrol",
    "register",
    "how to join",
    "want to join",
  ];

  return directLeadPhrases.some((phrase) => value.includes(phrase));
}

function isConversationClosing(text) {
  const value = text.trim().toLowerCase();
  return [
    "thanks",
    "thank you",
    "ok thanks",
    "okay thanks",
    "that's all",
    "thats all",
    "no thanks",
    "done",
    "got it",
  ].some((phrase) => value === phrase || value.includes(phrase));
}

function LeadForm({ onCancel, onSuccess }) {
  const [form, setForm] = useState({
    parent_name: "",
    child_name: "",
    child_age: "",
    child_class: "",
    phone: "",
    email: "",
    preferred_mode: "Not sure",
    main_concern: "",
    preferred_callback_time: "",
    consent: true,
  });
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const updateField = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!form.parent_name.trim() || !form.phone.trim()) {
      setError("Please enter parent name and phone number.");
      return;
    }

    if (!form.consent) {
      setError("Please confirm consent so the MathPath team can contact you.");
      return;
    }

    try {
      setStatus("submitting");
      const result = await submitLead({
        parent_name: form.parent_name,
        child_name: form.child_name,
        child_age: form.child_age,
        child_class: form.child_class,
        phone: form.phone,
        email: form.email,
        preferred_mode: form.preferred_mode,
        main_concern: form.main_concern,
        preferred_callback_time: form.preferred_callback_time,
        consent: form.consent,
        source: "MathPath AI Chatbot",
      });
      setStatus("success");
      onSuccess(result?.lead_id || result?.reference_id || "submitted");
    } catch {
      setStatus("idle");
      setError("Unable to submit right now. Please call 7980918759 / 9831684229.");
    }
  };

  return (
    <form className="mp-lead-card" onSubmit={handleSubmit}>
      <div className="mp-lead-card-header">
        <div>
          <span className="mp-eyebrow">Free guidance</span>
          <h4>Book a Demo / Callback</h4>
        </div>
        <button type="button" className="mp-icon-button muted" onClick={onCancel} aria-label="Close form">
          ×
        </button>
      </div>

      <div className="mp-form-row">
        <input
          value={form.parent_name}
          onChange={(e) => updateField("parent_name", e.target.value)}
          placeholder="Parent name *"
        />
        <input
          value={form.child_name}
          onChange={(e) => updateField("child_name", e.target.value)}
          placeholder="Child name"
        />
      </div>

      <div className="mp-form-row two">
        <input
          value={form.child_age}
          onChange={(e) => updateField("child_age", e.target.value)}
          placeholder="Age"
        />
        <input
          value={form.child_class}
          onChange={(e) => updateField("child_class", e.target.value)}
          placeholder="Class"
        />
      </div>

      <input
        value={form.phone}
        onChange={(e) => updateField("phone", e.target.value)}
        placeholder="Phone number *"
      />
      <input
        value={form.email}
        onChange={(e) => updateField("email", e.target.value)}
        placeholder="Email"
      />

      <select value={form.preferred_mode} onChange={(e) => updateField("preferred_mode", e.target.value)}>
        <option>Not sure</option>
        <option>Offline</option>
        <option>Online</option>
        <option>Hybrid</option>
      </select>

      <input
        value={form.main_concern}
        onChange={(e) => updateField("main_concern", e.target.value)}
        placeholder="Main concern: basics, speed, school maths"
      />
      <input
        value={form.preferred_callback_time}
        onChange={(e) => updateField("preferred_callback_time", e.target.value)}
        placeholder="Preferred callback time"
      />

      <label className="mp-consent-row">
        <input
          type="checkbox"
          checked={form.consent}
          onChange={(e) => updateField("consent", e.target.checked)}
        />
        <span>I agree to be contacted by MathPath for demo class and admission guidance.</span>
      </label>

      {error ? <p className="mp-form-error">{error}</p> : null}

      <button type="submit" className="mp-primary-button" disabled={status === "submitting"}>
        {status === "submitting" ? "Submitting..." : "Submit Details"}
      </button>
    </form>
  );
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [leadSuccessId, setLeadSuccessId] = useState("");
  const [showClosingCta, setShowClosingCta] = useState(false);
  const [error, setError] = useState("");
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const hasConversation = messages.length > 1;

  const statusLabel = useMemo(() => {
    if (isStreaming) return "Answering live";
    return "Online now";
  }, [isStreaming]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, isStreaming, showLeadForm, leadSuccessId, showClosingCta]);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isOpen]);

  const sendMessage = async (messageText = input) => {
    const trimmed = messageText.trim();
    if (!trimmed || isStreaming) return;

    setInput("");
    setError("");
    setShowClosingCta(false);
    setLeadSuccessId("");

    const userMessage = { id: makeId("user"), role: "user", text: trimmed };
    const botMessageId = makeId("bot");
    const botMessage = { id: botMessageId, role: "bot", text: "" };

    setMessages((prev) => [...prev, userMessage, botMessage]);
    setIsStreaming(true);

    if (shouldOpenLeadFormFromUser(trimmed)) {
      setShowLeadForm(true);
    }

    if (isConversationClosing(trimmed)) {
      setShowClosingCta(true);
    }

    try {
      let finalText = "";
      await streamChatMessage(trimmed, (_chunk, fullText) => {
        finalText = fullText;
        setMessages((prev) =>
          prev.map((msg) => (msg.id === botMessageId ? { ...msg, text: fullText } : msg))
        );
      });

      if (!finalText.trim()) {
        const fallback = await sendChatMessage(trimmed);
        finalText = fallback?.answer || fallback?.response || "I’m sorry, I could not generate an answer right now.";
        setMessages((prev) =>
          prev.map((msg) => (msg.id === botMessageId ? { ...msg, text: finalText } : msg))
        );
      }
    } catch {
      setError("I’m having trouble connecting to the MathPath AI server. Please make sure the backend is running.");
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === botMessageId
            ? {
                ...msg,
                text:
                  "I’m unable to connect to the chatbot backend right now. You can still contact MathPath directly at 7980918759 / 9831684229 or email info@mathpath.in.",
              }
            : msg
        )
      );
    } finally {
      setIsStreaming(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  if (!isOpen) {
    return (
      <div className="mp-chatbot-root">
        <button className="mp-premium-launcher" onClick={() => setIsOpen(true)} aria-label="Open MathPath AI chatbot">
          <span className="mp-launcher-orb">
            <img src={LOGO_SRC} alt="MathPath" />
          </span>
          <span className="mp-launcher-copy">
            <strong>Ask MathPath AI</strong>
            <small>Program guidance • Demo help</small>
          </span>
          <span className="mp-launcher-pulse" />
        </button>
      </div>
    );
  }

  return (
    <div className={`mp-chatbot-root ${isExpanded ? "expanded" : ""}`}>
      <section className="mp-chat-window premium" aria-label="MathPath AI chatbot">
        <header className="mp-chat-header premium">
          <div className="mp-chat-brand premium">
            <div className="mp-logo-shell">
              <img src={LOGO_SRC} alt="MathPath" />
            </div>
            <div>
              <div className="mp-title-row">
                <strong>MathPath AI</strong>
                <span className="mp-status-dot" />
              </div>
              <span className="mp-subtitle">{statusLabel}</span>
            </div>
          </div>

          <div className="mp-chat-actions premium">
            <button className="mp-icon-button" onClick={() => setShowLeadForm((prev) => !prev)} aria-label="Book demo">
              ♡
            </button>
            <button className="mp-icon-button" onClick={() => setIsExpanded((prev) => !prev)} aria-label="Expand chat">
              {isExpanded ? "↙" : "↗"}
            </button>
            <button className="mp-icon-button" onClick={() => setIsOpen(false)} aria-label="Close chat">
              ×
            </button>
          </div>
        </header>

        <div className="mp-chat-body premium">
          <div className="mp-suggestions premium">
            {QUICK_PROMPTS.map((prompt) => (
              <button
                type="button"
                className="mp-suggestion-chip premium"
                key={prompt}
                disabled={isStreaming}
                onClick={() => sendMessage(prompt)}
              >
                {prompt}
              </button>
            ))}
          </div>

          <div className="mp-message-list premium">
            {!hasConversation ? (
              <div className="mp-start-panel">
                <span className="mp-eyebrow">MathPath guidance assistant</span>
                <h3>Find the right learning path in seconds.</h3>
                <p>
                  Ask about programs, age groups, Bridge Course, class duration, daily practice, assessments, or demo booking.
                </p>
              </div>
            ) : null}

            {messages.map((message, index) => {
              const isLast = index === messages.length - 1;
              const showCursor = isStreaming && message.role === "bot" && isLast;

              return (
                <div className={`mp-message-row ${message.role}`} key={message.id}>
                  {message.role === "bot" ? (
                    <img className="mp-message-avatar premium" src={LOGO_SRC} alt="MathPath" />
                  ) : null}

                  <div className={`mp-message-bubble premium ${message.role}`}>
                    {message.text ? formatMessage(message.text) : <span className="mp-thinking-text">Thinking...</span>}
                    {showCursor ? <span className="mp-streaming-cursor" /> : null}
                  </div>
                </div>
              );
            })}

            {isStreaming ? (
              <div className="mp-typing premium" aria-label="MathPath AI is typing">
                <span />
                <span />
                <span />
              </div>
            ) : null}

            {showClosingCta && !showLeadForm ? (
              <div className="mp-conversation-cta premium">
                <p>Would you like to ask anything else, or should I help you book a free MathPath demo?</p>
                <div className="mp-conversation-cta-actions">
                  <button type="button" onClick={() => setShowLeadForm(true)}>
                    Book free demo
                  </button>
                  <button type="button" className="secondary" onClick={() => setShowClosingCta(false)}>
                    Ask another question
                  </button>
                </div>
              </div>
            ) : null}

            {showLeadForm ? (
              <LeadForm
                onCancel={() => setShowLeadForm(false)}
                onSuccess={(id) => {
                  setShowLeadForm(false);
                  setLeadSuccessId(id);
                }}
              />
            ) : null}

            {leadSuccessId ? (
              <div className="mp-lead-success premium">
                <strong>Thank you. Your request has been captured.</strong>
                <span>The MathPath team will contact you shortly.</span>
                <small>Reference: {leadSuccessId}</small>
              </div>
            ) : null}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {error ? <div className="mp-chat-error premium">{error}</div> : null}

        <footer className="mp-chat-footer premium">
          <textarea
            ref={inputRef}
            value={input}
            rows={1}
            placeholder="Ask about MathPath programs, Bridge Course, daily practice, demo class..."
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button type="button" onClick={() => sendMessage()} disabled={isStreaming || !input.trim()} aria-label="Send message">
            ➤
          </button>
        </footer>
      </section>
    </div>
  );
}
