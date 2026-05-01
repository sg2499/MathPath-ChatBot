# Production Environment Checklist

## Backend

Required:

```env
APP_ENV=production
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-5.1-chat-latest
ALLOWED_ORIGINS=https://your-vercel-chatbot-url.vercel.app,https://www.mathpath.in,https://mathpath.in
ADMIN_API_KEY=long_random_secret
```

Optional:

```env
LEAD_WEBHOOK_URL=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_LEADS_TABLE=mathpath_leads
```

## Frontend

Required:

```env
VITE_MATHPATH_API_URL=https://your-render-backend-url.onrender.com
```

## Website integration

Required:

```html
<script
  src="https://your-vercel-chatbot-url.vercel.app/mathpath-chatbot-embed.js"
  data-chatbot-url="https://your-vercel-chatbot-url.vercel.app/?embed=1&open=1"
  data-logo-url="https://your-vercel-chatbot-url.vercel.app/MathPath-Logo.png"
></script>
```

## Security

- Never expose `OPENAI_API_KEY` in frontend code.
- Keep `SUPABASE_SERVICE_ROLE_KEY` only in backend environment variables.
- Change `ADMIN_API_KEY` before production.
- Do not commit `.env` files.
- Restrict CORS to actual domains only in production.
