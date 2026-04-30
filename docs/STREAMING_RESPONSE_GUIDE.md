# Streaming Response Guide

The production chatbot supports ChatGPT-style streaming responses through the backend endpoint:

```http
POST /chat/stream
Accept: text/event-stream
Content-Type: application/json
```

## Request Body

```json
{
  "message": "Which MathPath program is right for Class 5?",
  "session_id": "optional-session-id"
}
```

## Server-Sent Event Types

The backend sends three main event payloads:

```json
{"type":"metadata","intent":"program_recommendation","session_id":"..."}
{"type":"delta","content":"MathPath "}
{"type":"done","session_id":"..."}
```

## Frontend Behaviour

The React widget reads the stream with `ReadableStream.getReader()` and updates the current assistant bubble progressively. A blinking cursor is shown while the answer is streaming.

## Fallback Behaviour

If an OpenAI API key is not configured, the backend streams the safe retrieval-based fallback answer word by word. If streaming fails in the browser, the widget automatically falls back to the normal `/chat` endpoint.

## Production Notes

- Keep `ALLOWED_ORIGINS` restricted to the MathPath website and approved deployment domains.
- Use HTTPS for both frontend and backend.
- Some reverse proxies buffer streaming responses. For Nginx, disable buffering for this route.
- The backend sets `X-Accel-Buffering: no` and `Cache-Control: no-cache, no-transform`.
