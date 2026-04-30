# MathPath Website Integration Guide

This guide explains how to add the chatbot to the live MathPath website.

## Recommended method: one script tag

After deploying the frontend on Vercel, add this script before the closing `</body>` tag of the MathPath website page/template.

```html
<script
  src="https://your-vercel-chatbot-url.vercel.app/mathpath-chatbot-embed.js"
  data-chatbot-url="https://your-vercel-chatbot-url.vercel.app/?embed=1&open=1"
  data-logo-url="https://your-vercel-chatbot-url.vercel.app/MathPath-Logo.png"
  data-position="right"
></script>
```

Replace `your-vercel-chatbot-url` with the actual deployed Vercel URL.

## Where to add it

Add it to the website layout/footer so it loads across all pages where you want the chatbot to appear.

## Backend CORS setting

The backend `ALLOWED_ORIGINS` must include:

```env
https://www.mathpath.in,https://mathpath.in,https://your-vercel-chatbot-url.vercel.app
```

## Testing checklist

1. Open the MathPath website.
2. Confirm the **Ask MathPath AI** button appears at the bottom right.
3. Click it.
4. Ask: `Which program is suitable for my Class 4 child?`
5. Ask: `Can I book a demo?`
6. Submit the lead form.
7. Check backend CSV export or Supabase/webhook destination.

## If the widget does not appear

Check:

- Script URL is correct.
- Vercel deployment is live.
- Browser console has no blocked script/CSP error.
- The script tag is placed before `</body>`.

## If the bot appears but cannot answer

Check:

- Backend Render URL is correct in Vercel environment variable.
- Backend `/health` endpoint is working.
- Backend `ALLOWED_ORIGINS` includes the frontend URL and MathPath domain.
- OpenAI API key is valid if LLM-based responses are required.
