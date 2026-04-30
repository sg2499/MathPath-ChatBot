const API_BASE_URL = import.meta.env.VITE_MATHPATH_API_URL || "http://localhost:8000";

export async function sendChatMessage({ message, sessionId, childAge, childClass }) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      child_age: childAge,
      child_class: childClass
    })
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Chat request failed");
  }

  return response.json();
}

export async function submitLead(lead) {
  const response = await fetch(`${API_BASE_URL}/lead`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(lead)
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Lead submission failed");
  }

  return response.json();
}

export async function streamChatMessage({ message, sessionId, childAge, childClass, onMetadata, onToken }) {
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "text/event-stream"
    },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      child_age: childAge,
      child_class: childClass
    })
  });

  if (!response.ok || !response.body) {
    const text = await response.text();
    throw new Error(text || "Streaming chat request failed");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";
  let metadata = null;
  let fullAnswer = "";

  function handleEvent(rawEvent) {
    const dataLines = rawEvent
      .split("\n")
      .filter((line) => line.startsWith("data:"))
      .map((line) => line.replace(/^data:\s*/, ""));

    if (!dataLines.length) return;
    const payload = JSON.parse(dataLines.join("\n"));

    if (payload.type === "metadata") {
      metadata = payload;
      onMetadata?.(payload);
      return;
    }

    if (payload.type === "delta") {
      fullAnswer += payload.content || "";
      onToken?.(payload.content || "", fullAnswer);
    }
  }

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() || "";
    events.forEach((event) => {
      if (event.trim()) handleEvent(event);
    });
  }

  if (buffer.trim()) handleEvent(buffer);
  return { answer: fullAnswer, ...(metadata || {}) };
}
