# MathPath AI Chatbot — Final Production-Ready Project

> Final premium version: includes professional UI, concise commercial response style, updated MathPath FAQ knowledge base, controlled demo lead capture, and OpenAI model default `gpt-5.1-chat-latest`.


This is the complete MathPath website chatbot package. It includes the knowledge base, Agentic RAG backend, React chatbot widget with ChatGPT-style streaming, lead capture, deployment files, website embed script, QA testing suite, and admin dashboard.

## What this bot is built to do

MathPath AI is designed as an admissions, counselling, and program-guidance assistant for MathPath. It can answer parent questions about:

- MathPath as an organisation
- Young Learner Program
- Preparatory Level
- Intermediate Level
- Master Module
- Bridge Course for late joiners
- Abacus + visualisation learning model
- School syllabus support
- Daily app-based practice
- DPS, mock tests, report cards, alerts, and parent feedback
- Age/class-based program recommendation
- Parent concerns such as weak basics, fear of maths, slow calculation, late joining, and lack of regular practice
- Contact details, location, demo guidance, and callback flow

The bot is grounded in the MathPath knowledge base and is instructed not to invent fees, batch timings, guarantees, or unsupported claims.

## Final folder structure

```text
mathpath-ai-chatbot-final-verified/
├── backend/                  # FastAPI backend + Agentic RAG + lead APIs + admin APIs
├── frontend/                 # React/Vite website chatbot widget
├── admin-dashboard/          # React/Vite admin dashboard for leads and exports
├── embed/                    # Website embed script and sample integration HTML
├── qa/                       # API/RAG/lead/deployment tests + Postman collection
├── docs/                     # Setup, deployment, integration, admin, and QA guides
├── assets/                   # MathPath logo assets
├── scripts/                  # Local helper scripts
├── render.yaml               # Render backend deployment helper
└── README.md                 # This final guide
```


## Streaming response support

The final build includes professional live answer streaming:

- Backend endpoint: `POST /chat/stream`
- Streaming protocol: Server-Sent Events
- Frontend behaviour: assistant messages appear progressively with a blinking cursor
- Safety fallback: if streaming fails, the widget automatically falls back to `POST /chat`
- No-key fallback: without an OpenAI key, the backend still streams safe RAG-based fallback answers word by word

See `docs/STREAMING_RESPONSE_GUIDE.md` for implementation and production notes.

## Fast local start

### 1. Start backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend health check:

```text
http://localhost:8000/health
```

API docs:

```text
http://localhost:8000/docs
```

### 2. Start chatbot frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open:

```text
http://localhost:5173
```

### 3. Start admin dashboard

```bash
cd admin-dashboard
npm install
cp .env.example .env
npm run dev
```

Use the same `ADMIN_API_KEY` value configured in backend `.env`.

## Required environment values

Backend `.env` important values:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.1-chat-latest
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,https://www.mathpath.in,https://mathpath.in
ADMIN_API_KEY=change_this_admin_key
LEADS_CSV_PATH=storage/leads.csv
CHAT_LOG_CSV_PATH=storage/chat_logs.csv
```

The backend can run without an OpenAI key in fallback mode, but production should use an OpenAI key for better natural-language answers.

## Website integration

After deployment, integrate the bot into the MathPath website using the embed script in `embed/mathpath-chatbot-embed.js`.

Example:

```html
<script>
  window.MATHPATH_CHATBOT_CONFIG = {
    widgetUrl: "https://your-chatbot-frontend-domain.vercel.app",
    position: "bottom-right"
  };
</script>
<script src="https://your-chatbot-frontend-domain.vercel.app/mathpath-chatbot-embed.js"></script>
```

See `docs/integration/MATHPATH_WEBSITE_INTEGRATION_GUIDE.md` for the complete instructions.

## Admin dashboard

The admin dashboard allows MathPath staff to:

- View leads
- Search/filter enquiries
- See hot/warm/new lead priority
- Export leads as CSV
- Export chat logs as CSV
- Track parent enquiry patterns

Backend admin endpoints are protected using `ADMIN_API_KEY`.

## QA and testing

The `qa/` folder contains:

- API smoke tests
- Lead capture tests
- RAG answer-quality tests
- Admin endpoint tests
- Parent-style test prompts
- Deployment smoke test script
- Postman collection
- Manual frontend checklist

Recommended test order:

```bash
cd qa
pip install -r requirements-test.txt
python scripts/run_all_tests.py
```

## Production deployment recommendation

Recommended deployment stack:

- Backend: Render
- Frontend widget: Vercel
- Admin dashboard: Vercel or private deployment
- Lead storage: Local CSV initially, Supabase for stronger production workflows
- Optional automation: Google Sheets / Make / Zapier webhook for lead forwarding

## Important safety rules already built into the bot

- Does not invent fees, timings, guarantees, or admission deadlines
- Uses MathPath knowledge base as grounding
- Guides users to MathPath team for batch/fee-specific information
- Uses parent-friendly counselling language
- Avoids medical or diagnostic claims
- Encourages demo/callback when the parent shows interest
- Captures consent before contact

## Final recommended launch checklist

1. Add production OpenAI API key to Render.
2. Change `ADMIN_API_KEY` from default value.
3. Add final frontend/admin domains to backend `ALLOWED_ORIGINS`.
4. Deploy backend and verify `/health`.
5. Deploy frontend and verify chat responses.
6. Deploy/admin-protect dashboard.
7. Run QA tests from `qa/`.
8. Add embed script to MathPath website.
9. Submit 3-5 test leads and verify CSV/admin dashboard.
10. Keep knowledge base updated whenever programs, fees, batches, or contact details change.

