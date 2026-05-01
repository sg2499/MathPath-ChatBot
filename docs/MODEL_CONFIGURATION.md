# Model Configuration

This project is configured to use a current premium OpenAI chat model by default.

## Default model

```env
OPENAI_MODEL=gpt-5.1-chat-latest
```

## Why this model

`gpt-5.1-chat-latest` is selected for the public MathPath chatbot because it is optimized for a polished ChatGPT-style conversation experience and points to the GPT-5.1 model currently used in ChatGPT.

## Required deployment setting

In Render, set:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.1-chat-latest
```

If you need to optimize cost later, you can change `OPENAI_MODEL` in the Render environment variables without editing code.

## Fallback behavior

If no OpenAI key is provided, the backend still runs in deterministic fallback mode using the MathPath knowledge base. For production, always configure `OPENAI_API_KEY`.
