# MathPath AI Chatbot — Render Backend Deployment

This guide deploys the FastAPI backend that powers Agentic RAG, program recommendation, lead capture, and admin exports.

## 1. Create a GitHub repository

Upload the complete project folder to GitHub. Keep the folder structure unchanged.

## 2. Create a Render Web Service

1. Go to Render.
2. Click **New +** → **Web Service**.
3. Connect the GitHub repository.
4. Select the backend folder as the root directory:

```text
backend
```

5. Use these commands:

```bash
Build Command: pip install -r requirements.txt
Start Command: bash start.sh
```

Render can also detect the included `render.yaml` if you create the service using Blueprint mode.

## 3. Add environment variables

Add these in Render → Environment:

```env
APP_ENV=production
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
ALLOWED_ORIGINS=https://your-vercel-chatbot-url.vercel.app,https://www.mathpath.in,https://mathpath.in
ADMIN_API_KEY=use_a_long_random_secret
TOP_K=5
MIN_RETRIEVAL_SCORE=0.08
```

Optional lead integrations:

```env
LEAD_WEBHOOK_URL=
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_LEADS_TABLE=mathpath_leads
```

## 4. Verify backend

After deployment, open:

```text
https://your-render-backend-url.onrender.com/health
```

Expected response:

```json
{"status":"healthy","knowledge_base":"loaded"}
```

## 5. Test chat endpoint

Use Postman, Thunder Client, or curl:

```bash
curl -X POST https://your-render-backend-url.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Which MathPath program is suitable for a Class 5 child?"}'
```

## Important production note

Render free services can sleep when inactive. The first request after sleep may take longer. For production admissions usage, use a paid instance or another always-on platform.
