import ReactMarkdown from 'react-markdown';

export default function ChatMessage({ message }) {
  const isBot = message.role === "assistant";
  const content = message.content || "";

  return (
    <div className={`mp-message-row ${isBot ? "bot" : "user"}`}>
      {isBot && <img src="/MathPath-Logo.png" alt="MathPath" className="mp-message-avatar" />}
      <div className={`mp-message-bubble ${isBot ? "bot" : "user"}`}>
        {content ? (
          <ReactMarkdown>{content}</ReactMarkdown>
        ) : (
          <p> </p>
        )}
        {message.streaming && <span className="mp-streaming-cursor" aria-label="Streaming response" />}
      </div>
    </div>
  );
}
