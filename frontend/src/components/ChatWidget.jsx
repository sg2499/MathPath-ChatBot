import { useEffect, useMemo, useRef, useState } from "react";
import { sendChatMessage, streamChatMessage, submitLead } from "./api";
import { motion, AnimatePresence } from "framer-motion";
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
    text: "Hi! I’m MathPath AI. I can help you choose the right MathPath Abacus program, explain our learning model, Bridge Course, class structure, assessments, and demo process. What would you like to know?",
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
    "book demo", "book a demo", "free demo", "schedule demo", "demo class",
    "arrange demo", "want a demo", "need a demo", "trial class", "book a trial",
    "callback", "call me", "please call",
  ];
  return directLeadPhrases.some((phrase) => value.includes(phrase));
}

function LeadForm({ onCancel, onSuccess }) {
  const [form, setForm] = useState({
    parent_name: "", child_name: "", child_age: "", child_class: "", phone: "",
    email: "", preferred_mode: "Not sure", main_concern: "", preferred_callback_time: "", consent: true,
  });
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");

  const updateField = (field, value) => setForm((prev) => ({ ...prev, [field]: value }));

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
      const result = await submitLead({ ...form, source: "MathPath AI Chatbot" });
      setStatus("success");
      onSuccess(result?.lead_id || result?.reference_id || "submitted");
    } catch {
      setStatus("idle");
      setError("Unable to submit right now. Please call 7980918759.");
    }
  };

  return (
    <motion.form 
      className="mp-lead-card" 
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 10, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
    >
      <div className="mp-lead-card-header">
        <div>
          <h4>Book a Demo / Callback</h4>
        </div>
        <button type="button" className="mp-icon-button muted" onClick={onCancel}>×</button>
      </div>
      <div className="mp-form-row">
        <input value={form.parent_name} onChange={(e) => updateField("parent_name", e.target.value)} placeholder="Parent name *" />
        <input value={form.child_name} onChange={(e) => updateField("child_name", e.target.value)} placeholder="Child name" />
      </div>
      <div className="mp-form-row two">
        <input value={form.child_age} onChange={(e) => updateField("child_age", e.target.value)} placeholder="Age" />
        <input value={form.child_class} onChange={(e) => updateField("child_class", e.target.value)} placeholder="Class" />
      </div>
      <input value={form.phone} onChange={(e) => updateField("phone", e.target.value)} placeholder="Phone number *" />
      <input value={form.email} onChange={(e) => updateField("email", e.target.value)} placeholder="Email" />
      <select value={form.preferred_mode} onChange={(e) => updateField("preferred_mode", e.target.value)}>
        <option>Not sure</option><option>Offline</option><option>Online</option><option>Hybrid</option>
      </select>
      <input value={form.main_concern} onChange={(e) => updateField("main_concern", e.target.value)} placeholder="Main concern: basics, speed, school maths" />
      <label className="mp-consent-row">
        <input type="checkbox" checked={form.consent} onChange={(e) => updateField("consent", e.target.checked)} />
        <span>I agree to be contacted by MathPath for demo class and admission guidance.</span>
      </label>
      {error && <p className="mp-form-error">{error}</p>}
      <button type="submit" className="mp-primary-button" disabled={status === "submitting"}>
        {status === "submitting" ? "Submitting..." : "Submit Details"}
      </button>
    </motion.form>
  );
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const [leadSuccessId, setLeadSuccessId] = useState("");
  const [error, setError] = useState("");
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);

  const statusLabel = useMemo(() => isStreaming ? "Answering live" : "Online now", [isStreaming]);

  const scrollSuggestions = (direction) => {
    if (suggestionsRef.current) {
      const scrollAmount = 200;
      suggestionsRef.current.scrollBy({ left: direction === 'left' ? -scrollAmount : scrollAmount, behavior: 'smooth' });
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, isStreaming, showLeadForm, leadSuccessId]);

  useEffect(() => {
    if (isOpen) setTimeout(() => inputRef.current?.focus(), 200);
  }, [isOpen]);

  const sendMessage = async (messageText = input) => {
    const trimmed = messageText.trim();
    if (!trimmed || isStreaming) return;

    setInput("");
    setError("");
    setLeadSuccessId("");

    const userMessage = { id: makeId("user"), role: "user", text: trimmed };
    const botMessageId = makeId("bot");
    const botMessage = { id: botMessageId, role: "bot", text: "" };

    setMessages((prev) => [...prev, userMessage, botMessage]);
    setIsStreaming(true);

    if (shouldOpenLeadFormFromUser(trimmed)) {
      setShowLeadForm(true);
    }

    try {
      let finalText = "";
      await streamChatMessage(trimmed, (_chunk, fullText) => {
        finalText = fullText;
        setMessages((prev) => prev.map((msg) => (msg.id === botMessageId ? { ...msg, text: fullText } : msg)));
      });

      if (!finalText.trim()) {
        const fallback = await sendChatMessage(trimmed);
        finalText = fallback?.answer || fallback?.response || "I’m sorry, I could not generate an answer right now.";
        setMessages((prev) => prev.map((msg) => (msg.id === botMessageId ? { ...msg, text: finalText } : msg)));
      }
    } catch {
      setError("I’m having trouble connecting to the MathPath AI server. Please make sure the backend is running.");
      setMessages((prev) => prev.map((msg) => msg.id === botMessageId ? { ...msg, text: "I’m unable to connect to the chatbot backend right now. You can still contact MathPath directly at 7980918759." } : msg));
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

  return (
    <div className="mp-chatbot-root">
      <AnimatePresence>
        {!isOpen && (
          <motion.button 
            className="mp-premium-launcher" 
            onClick={() => setIsOpen(true)}
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="mp-launcher-orb"><img src={LOGO_SRC} alt="MathPath" /></span>
            <span className="mp-launcher-copy">
              <strong>Ask MathPath AI</strong>
              <small>Program guidance &bull; Demo help</small>
            </span>
          </motion.button>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {isOpen && (
          <motion.section 
            className="mp-chat-window premium"
            initial={{ opacity: 0, y: 40, scale: 0.95, filter: "blur(10px)" }}
            animate={{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)" }}
            exit={{ opacity: 0, y: 40, scale: 0.95, filter: "blur(10px)" }}
            transition={{ type: "spring", stiffness: 260, damping: 25 }}
          >
            <header className="mp-chat-header premium">
              <div className="mp-chat-brand premium">
                <div className="mp-logo-shell"><img src={LOGO_SRC} alt="MathPath" /></div>
                <div>
                  <div className="mp-title-row">
                    <strong>MathPath AI</strong>
                    <span className="mp-status-dot" />
                  </div>
                  <span className="mp-subtitle">{statusLabel}</span>
                </div>
              </div>
              <div className="mp-chat-actions premium">
                <button className="mp-icon-button" onClick={() => setMessages(INITIAL_MESSAGES)}>↻</button>
                <button className="mp-icon-button" onClick={() => setShowLeadForm(!showLeadForm)}>♡</button>
                <button className="mp-icon-button" onClick={() => setIsOpen(false)}>×</button>
              </div>
            </header>

            <div className="mp-chat-body premium">
              <div className="mp-suggestions-container">
                <button className="mp-scroll-btn left" onClick={() => scrollSuggestions('left')}>❮</button>
                <div className="mp-suggestions premium" ref={suggestionsRef}>
                  {QUICK_PROMPTS.map((prompt) => (
                    <button key={prompt} className="mp-suggestion-chip premium" disabled={isStreaming} onClick={() => sendMessage(prompt)}>
                      {prompt}
                    </button>
                  ))}
                </div>
                <button className="mp-scroll-btn right" onClick={() => scrollSuggestions('right')}>❯</button>
              </div>

              <div className="mp-message-list premium">
                {messages.length === 1 && (
                  <motion.div className="mp-start-panel" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                    <span className="mp-eyebrow">MathPath guidance assistant</span>
                    <h3>Find the right learning path in seconds.</h3>
                    <p>Ask about programs, age groups, Bridge Course, class duration, daily practice, assessments, or demo booking.</p>
                  </motion.div>
                )}

                <AnimatePresence initial={false}>
                  {messages.map((message, index) => {
                    const isLast = index === messages.length - 1;
                    const showCursor = isStreaming && message.role === "bot" && isLast;
                    return (
                      <motion.div 
                        className={`mp-message-row ${message.role}`} 
                        key={message.id}
                        initial={{ opacity: 0, y: 10, scale: 0.95 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        transition={{ type: "spring", stiffness: 300, damping: 25 }}
                      >
                        {message.role === "bot" && <img className="mp-message-avatar premium" src={LOGO_SRC} alt="MathPath" />}
                        <div className={`mp-message-bubble premium ${message.role}`}>
                          {message.text ? formatMessage(message.text) : <span className="mp-thinking-text">Thinking...</span>}
                          {showCursor && <span className="mp-streaming-cursor" />}
                        </div>
                      </motion.div>
                    );
                  })}
                </AnimatePresence>

                {isStreaming && (
                  <motion.div className="mp-typing premium" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <span /><span /><span />
                  </motion.div>
                )}

                <AnimatePresence>
                  {showLeadForm && (
                    <LeadForm onCancel={() => setShowLeadForm(false)} onSuccess={(id) => { setShowLeadForm(false); setLeadSuccessId(id); }} />
                  )}
                </AnimatePresence>

                <div ref={messagesEndRef} />
              </div>
            </div>

            <footer className="mp-chat-footer premium">
              <textarea
                ref={inputRef}
                value={input}
                rows={1}
                placeholder="Message MathPath AI..."
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
              />
              <button type="button" onClick={() => sendMessage()} disabled={isStreaming || !input.trim()}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="m22 2-7 20-4-9-9-4Z" /><path d="M22 2 11 13" />
                </svg>
              </button>
            </footer>
          </motion.section>
        )}
      </AnimatePresence>
    </div>
  );
}
