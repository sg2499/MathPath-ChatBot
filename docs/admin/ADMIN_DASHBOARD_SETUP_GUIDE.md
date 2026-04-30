# MathPath Admin Dashboard Setup Guide

## 1. Prerequisites

You need:

- Node.js 18 or newer
- The MathPath chatbot backend running
- Backend `.env` containing `ADMIN_API_KEY`

## 2. Run locally

```bash
cd admin-dashboard
npm install
npm run dev
```

Open the URL shown by Vite.

## 3. Connect to backend

Enter:

```text
Backend URL: http://localhost:8000
Admin API Key: your backend ADMIN_API_KEY
```

The dashboard checks `/health`, then loads `/admin/leads`.

## 4. Required backend endpoints

Minimum required:

```text
GET /health
GET /admin/leads?limit=500
GET /admin/leads/export
GET /admin/chat-logs/export
```

These are already present in the Step 4 backend package.

## 5. Production deployment

Recommended deployment options:

- Vercel: easiest for React dashboard
- Render Static Site
- Netlify
- Private internal route on the main admin website

For Vercel:

```bash
cd admin-dashboard
npm run build
```

Set environment variable:

```text
VITE_DEFAULT_BACKEND_URL=https://your-render-backend-url.onrender.com
```

## 6. Security checklist

Before production:

- Use a strong `ADMIN_API_KEY`.
- Do not commit `.env` files.
- Restrict backend CORS to trusted frontend domains.
- Do not share the dashboard link publicly.
- Rotate the admin key if it is accidentally exposed.
- Prefer a private/admin-only page for the dashboard.

## 7. Common errors

### 401 or 403 error

The admin key is missing or incorrect. Check that the value entered in the dashboard matches `ADMIN_API_KEY` in backend `.env`.

### CORS error

Add the dashboard domain to backend `ALLOWED_ORIGINS`.

### Leads not visible

Check whether leads have been captured by the chatbot. You can create a test lead using the frontend chatbot or Postman.

### CSV export downloads empty file

This means the CSV exists but has no records yet. Create a test lead first.
