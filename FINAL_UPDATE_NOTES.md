# Final Update Notes

This final folder includes the latest requested changes:

- Premium professional chatbot UI update.
- MathPath logo and favicon setup.
- Corrected frontend API URL handling for Vercel/Render deployment.
- Lead/demo form no longer appears after every answer.
- Updated MathPath knowledge base from the FAQ document.
- Crisp professional answer style for commercial use.
- Program overview answers show only the three enrolment entry programs: Young Learner, Preparatory Level 1, and Bridge Course.
- Placeholder contact text is blocked and sanitized.
- Default OpenAI model upgraded to `gpt-5.1-chat-latest`.
- Backend Python version pinned to `3.11.11` for Render reliability.

## Replace your current repository files

You can replace your project with this folder, or copy the updated files into your existing GitHub repo and push.

## Important production env values

Render backend:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.1-chat-latest
PYTHON_VERSION=3.11.11
ADMIN_API_KEY=your_secure_admin_key
ALLOWED_ORIGINS=http://localhost:5173,https://your-vercel-url.vercel.app,https://www.mathpath.in,https://mathpath.in
```

Vercel frontend:

```env
VITE_MATHPATH_API_URL=https://your-render-backend-url.onrender.com
```
