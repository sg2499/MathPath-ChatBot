const API_BASE_URL =
  import.meta.env.VITE_MATHPATH_API_URL ||
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000";

export async function sendChatMessage(message) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed with status ${response.status}`);
  }

  return response.json();
}

export async function streamChatMessage(message, onChunk) {
  const response = await fetch(`${API_BASE_URL}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!response.ok || !response.body) {
    throw new Error(`Streaming request failed with status ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";
  let fullText = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() || "";

    for (const event of events) {
      const line = event
        .split("\n")
        .find((item) => item.startsWith("data:"));

      if (!line) continue;

      const data = line.replace(/^data:\s?/, "");
      if (data === "[DONE]") continue;

      try {
        const parsed = JSON.parse(data);
        const chunk = parsed.token || parsed.content || parsed.text || "";
        if (chunk) {
          fullText += chunk;
          onChunk(chunk, fullText);
        }
      } catch {
        if (data) {
          fullText += data;
          onChunk(data, fullText);
        }
      }
    }
  }

  return fullText;
}

export async function submitLead(leadPayload) {
  const response = await fetch(`${API_BASE_URL}/lead`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(leadPayload),
  });

  if (!response.ok) {
    throw new Error(`Lead submission failed with status ${response.status}`);
  }

  return response.json();
}
